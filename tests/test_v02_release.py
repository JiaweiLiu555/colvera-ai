from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.v02.data import RELEASE_ROOT, all_release_splits

# The optional raw release is ignored by Git. Avoid importing the heavyweight
# inference runtime when the entire class will be skipped in a normal checkout.
if RELEASE_ROOT.exists():
    from colvera.v02.model import load_released_weights, released_probabilities


@unittest.skipUnless(RELEASE_ROOT.exists(), "Official v0.2 release is not present locally")
class ReleasedDataTests(unittest.TestCase):
    def test_release_arrays_and_labels_are_well_formed(self):
        splits = all_release_splits()
        self.assertEqual({name: split.n_records for name, split in splits.items()}, {"training": 200, "validation": 123, "test": 200})
        self.assertEqual(splits["test"].targets_one_hot.sum(axis=0).astype(int).tolist(), [60, 140])
        for split in splits.values():
            self.assertEqual(split.images.shape[1:], (4, 16, 128, 128))
            self.assertTrue(np.isfinite(split.images).all())
            self.assertTrue(np.allclose(split.targets_one_hot.sum(axis=1), 1))

    def test_released_weight_inference_is_deterministic_and_finite(self):
        model = load_released_weights(RELEASE_ROOT / "good_response" / "weights" / "weights_ADC.hdf5")
        volume = all_release_splits()["training"].images[:2, 0]
        one = released_probabilities(model, volume)
        two = released_probabilities(model, volume)
        self.assertTrue(np.array_equal(one, two))
        self.assertTrue(np.isfinite(one).all())
        self.assertTrue(np.allclose(one.sum(axis=1), 1))

    def test_patient_level_cv_is_refused_without_patient_ids(self):
        manifest = ROOT / "data" / "v02" / "patient_manifest.csv"
        self.assertTrue(manifest.exists())
        header = manifest.read_text().splitlines()[0]
        self.assertIn("patient_id", header)
        self.assertIn("not available in release", manifest.read_text())


if __name__ == "__main__":
    unittest.main()
