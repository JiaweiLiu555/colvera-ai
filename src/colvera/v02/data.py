"""Read-only access to the Zhu et al. release and release audit helpers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
RELEASE_ROOT = PROJECT_ROOT / "data" / "v02" / "raw" / "rectal_MR_DL"
GOOD_RESPONSE_DATA = RELEASE_ROOT / "good_response" / "data"


@dataclass(frozen=True)
class ReleasedSplit:
    """One array pair in the official good-response release.

    `record_id` is a release-array row index, explicitly not a patient ID.
    """

    name: str
    images: np.ndarray
    targets_one_hot: np.ndarray

    @property
    def n_records(self) -> int:
        return int(self.images.shape[0])

    @property
    def label_index(self) -> np.ndarray:
        return self.targets_one_hot.argmax(axis=1).astype(int)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _unique_match(pattern: str) -> Path:
    matches = sorted(GOOD_RESPONSE_DATA.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected exactly one {pattern} in {GOOD_RESPONSE_DATA}; found {matches}")
    return matches[0]


def load_release_split(name: str) -> ReleasedSplit:
    """Load one official NPZ pair without altering it."""
    if name not in {"training", "validation", "test"}:
        raise ValueError(f"Unknown release split: {name}")
    image_path = _unique_match(f"{name}_images_*.npz")
    target_path = _unique_match(f"{name}_targets_*.npz")
    with np.load(image_path, allow_pickle=False) as image_npz:
        images = np.asarray(image_npz["arr_0"], dtype=np.float32)
    with np.load(target_path, allow_pickle=False) as target_npz:
        targets = np.asarray(target_npz["arr_0"], dtype=np.float32)
    if images.ndim != 5 or images.shape[1:] != (4, 16, 128, 128):
        raise ValueError(f"Unexpected released image shape: {images.shape}")
    if targets.shape != (images.shape[0], 2) or not np.allclose(targets.sum(axis=1), 1):
        raise ValueError(f"Unexpected one-hot target shape/content: {targets.shape}")
    return ReleasedSplit(name=name, images=images, targets_one_hot=targets)


def all_release_splits() -> dict[str, ReleasedSplit]:
    return {name: load_release_split(name) for name in ("training", "validation", "test")}


def release_file_inventory() -> list[dict[str, object]]:
    """Inventory material release files; raw source is never modified."""
    inventory: list[dict[str, object]] = []
    for path in sorted(RELEASE_ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        inventory.append(
            {
                "path": str(path.relative_to(RELEASE_ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    return inventory
