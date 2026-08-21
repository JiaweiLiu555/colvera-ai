"""Faithful PyTorch inference reconstruction of the released Keras 2.1.6 models.

The reconstruction is for *released-weight inference*, not retraining.  The
Keras HDF5 config records a 16-channel, channels-first input.  We preserve the
five parallel max-pooling/centre-cropping blocks and import all saved weights.
"""

from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


class ReleasedDCPCNN(nn.Module):
    """The one-input architecture encoded in the official HDF5 weights."""

    def __init__(self) -> None:
        super().__init__()
        self.convs = nn.ModuleList(
            [
                nn.Conv2d(16, 16, 3, padding=1),
                nn.Conv2d(32, 16, 3, padding=1),
                nn.Conv2d(48, 16, 3, padding=1),
                nn.Conv2d(64, 16, 3, padding=1),
                nn.Conv2d(80, 16, 3, padding=1),
                nn.Conv2d(96, 16, 4),
            ]
        )
        self.bns = nn.ModuleList([nn.BatchNorm2d(16, eps=1e-3, momentum=0.99) for _ in range(6)])
        self.dense1 = nn.Linear(16, 32)
        self.dense2 = nn.Linear(32, 8)
        self.dense3 = nn.Linear(8, 2)

    def forward(self, image: torch.Tensor) -> torch.Tensor:
        if image.ndim != 4 or tuple(image.shape[1:]) != (16, 128, 128):
            raise ValueError(f"Expected (N, 16, 128, 128), got {tuple(image.shape)}")
        x = image
        for block, (conv, bn) in enumerate(zip(self.convs[:5], self.bns[:5])):
            pooled = F.max_pool2d(bn(F.relu(conv(x))), kernel_size=2, stride=2)
            margin = 32 // (2**block)
            cropped = x[:, :, margin:-margin, margin:-margin]
            x = torch.cat([pooled, cropped], dim=1)
        x = self.bns[5](F.relu(self.convs[5](x)))
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.dense1(x))
        x = F.relu(self.dense2(x))  # dropout is inactive at inference, as in Keras predict.
        return self.dense3(x)


def _as_tensor(value: np.ndarray) -> torch.Tensor:
    return torch.from_numpy(np.asarray(value, dtype=np.float32))


def load_released_weights(weights_path: Path, device: str = "cpu") -> ReleasedDCPCNN:
    """Load Keras 2 HDF5 tensors into the exact evaluation graph."""
    model = ReleasedDCPCNN()
    with h5py.File(weights_path, "r") as h5:
        weights = h5["model_weights"]
        for idx, (conv, bn) in enumerate(zip(model.convs, model.bns), start=1):
            source_idx = idx
            # T2 was built later in the Keras session, hence layer indexes 19..24.
            if "conv2d_1" not in weights and "conv2d_19" in weights:
                source_idx = idx + 18
            conv_group = weights[f"conv2d_{source_idx}"][f"conv2d_{source_idx}"]
            keras_kernel = np.asarray(conv_group["kernel:0"])
            conv.weight.data.copy_(_as_tensor(keras_kernel.transpose(3, 2, 0, 1)))
            conv.bias.data.copy_(_as_tensor(np.asarray(conv_group["bias:0"])))
            bn_group = weights[f"batch_normalization_{source_idx}"][f"batch_normalization_{source_idx}"]
            bn.weight.data.copy_(_as_tensor(np.asarray(bn_group["gamma:0"])))
            bn.bias.data.copy_(_as_tensor(np.asarray(bn_group["beta:0"])))
            bn.running_mean.data.copy_(_as_tensor(np.asarray(bn_group["moving_mean:0"])))
            bn.running_var.data.copy_(_as_tensor(np.asarray(bn_group["moving_variance:0"])))
        for layer, torch_layer in (("dense_1", model.dense1), ("dense_2", model.dense2), ("dense_3", model.dense3)):
            group = weights[layer][layer]
            torch_layer.weight.data.copy_(_as_tensor(np.asarray(group["kernel:0"]).T))
            torch_layer.bias.data.copy_(_as_tensor(np.asarray(group["bias:0"])))
    model.eval()
    return model.to(device)


@torch.inference_mode()
def released_probabilities(model: ReleasedDCPCNN, volumes: np.ndarray, batch_size: int = 16) -> np.ndarray:
    """Return two-class softmax output for one predeclared release channel."""
    if volumes.ndim != 4:
        raise ValueError(f"Expected selected volume array (N,16,128,128), got {volumes.shape}")
    device = next(model.parameters()).device
    blocks: list[np.ndarray] = []
    for start in range(0, len(volumes), batch_size):
        tensor = torch.from_numpy(np.asarray(volumes[start : start + batch_size], dtype=np.float32)).to(device)
        blocks.append(torch.softmax(model(tensor), dim=1).cpu().numpy())
    probabilities = np.concatenate(blocks, axis=0)
    if not np.isfinite(probabilities).all() or not np.allclose(probabilities.sum(axis=1), 1, atol=1e-5):
        raise RuntimeError("Released-weight inference returned invalid probabilities")
    return probabilities
