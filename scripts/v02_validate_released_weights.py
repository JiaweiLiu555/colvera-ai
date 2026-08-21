"""Development-only mechanical checks for the released-weight reconstruction."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.v02.data import RELEASE_ROOT, load_release_split  # noqa: E402
from colvera.v02.model import load_released_weights, released_probabilities  # noqa: E402


def main() -> None:
    weights = RELEASE_ROOT / "good_response" / "weights" / "weights_ADC.hdf5"
    model = load_released_weights(weights)
    # This uses development inputs only and deliberately never reads test labels.
    development = load_release_split("training").images[:10, 0]
    first = released_probabilities(model, development, batch_size=5)
    second = released_probabilities(model, development, batch_size=5)
    rng = np.random.default_rng(20260816)
    noise = rng.normal(size=(10, 16, 128, 128)).astype("float32")
    noise_probability = released_probabilities(model, noise, batch_size=5)
    result = {
        "weights": str(weights.relative_to(ROOT)),
        "development_records_used_for_mechanical_check": 10,
        "same_input_deterministic": bool(np.array_equal(first, second)),
        "finite_probabilities": bool(np.isfinite(first).all() and np.isfinite(noise_probability).all()),
        "probability_rows_sum_to_one": bool(np.allclose(first.sum(axis=1), 1) and np.allclose(noise_probability.sum(axis=1), 1)),
        "random_noise_check": "completed; no performance statistic was calculated or interpreted",
        "note": "This is an import/inference integrity check only. It is not a model-training or outcome-performance experiment.",
    }
    out = ROOT / "outputs" / "v02" / "reproduction"
    out.mkdir(parents=True, exist_ok=True)
    (out / "mechanical_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
