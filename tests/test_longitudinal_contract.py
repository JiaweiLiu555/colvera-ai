from __future__ import annotations

import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.longitudinal import current_only_records, longitudinal_pairs, model_feature_columns, validate_manifest
from colvera.longitudinal.study import LONGITUDINAL


def example_manifest() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"patient_id": "p01", "visit_id": "p01_v0", "time_offset_days": 0, "evidence_type": "mri", "modality_or_measure": "T2", "resource_ref": "p01/v0/t2.nii.gz", "split": "train", "pcr": 0, "age_at_baseline": 55},
            {"patient_id": "p01", "visit_id": "p01_v1", "time_offset_days": 42, "evidence_type": "mri", "modality_or_measure": "T2", "resource_ref": "p01/v1/t2.nii.gz", "split": "train", "pcr": 0, "age_at_baseline": 55},
            {"patient_id": "p01", "visit_id": "p01_v1", "time_offset_days": 42, "evidence_type": "laboratory", "modality_or_measure": "CEA", "resource_ref": "p01/v1/cea.json", "split": "train", "pcr": 0, "age_at_baseline": 55},
            {"patient_id": "p02", "visit_id": "p02_v0", "time_offset_days": 0, "evidence_type": "mri", "modality_or_measure": "T2", "resource_ref": "p02/v0/t2.nii.gz", "split": "test", "pcr": 1, "age_at_baseline": 61},
        ]
    )


class LongitudinalContractTests(unittest.TestCase):
    def test_audit_and_patient_isolation(self):
        audit = validate_manifest(example_manifest())
        self.assertEqual(audit["patients"], 2)
        self.assertEqual(audit["visits"], 3)
        self.assertTrue(audit["patient_level_isolation"])

    def test_current_and_previous_current_views(self):
        frame = example_manifest()
        current = current_only_records(frame, outcome_name="pcr", split="train")
        pairs = longitudinal_pairs(frame, outcome_name="pcr", split="train", required_modality="T2")
        self.assertEqual(len(current), 2)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs.iloc[0].previous_visit_id, "p01_v0")
        self.assertEqual(pairs.iloc[0].current_visit_id, "p01_v1")

    def test_outcomes_and_identifiers_are_excluded_from_features(self):
        columns = model_feature_columns(example_manifest())
        self.assertEqual(columns, ["age_at_baseline"])

    def test_rejects_cross_split_patient_leakage_and_unsafe_reference(self):
        leaked = example_manifest()
        leaked.loc[3, "patient_id"] = "p01"
        with self.assertRaisesRegex(ValueError, "split leakage"):
            validate_manifest(leaked)
        unsafe = example_manifest()
        unsafe.loc[0, "resource_ref"] = "../not-allowed.nii.gz"
        with self.assertRaisesRegex(ValueError, "relative reference"):
            validate_manifest(unsafe)

    def test_development_spec_refuses_test_split(self):
        with self.assertRaisesRegex(ValueError, "train or validation"):
            LONGITUDINAL.prepare_development_inputs(example_manifest(), split="test")


if __name__ == "__main__":
    unittest.main()
