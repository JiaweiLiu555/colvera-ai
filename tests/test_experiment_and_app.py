from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.data import load_rectal_cohort, patient_level_split
from colvera.demo import get_demo_manifest
from colvera.longitudinal.contract import validate_manifest


class ExperimentArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((ROOT / "outputs" / "metrics" / "results.json").read_text())
        cls.predictions = pd.read_csv(ROOT / "outputs" / "metrics" / "held_out_predictions.csv")
        cls.neighbors = pd.read_csv(ROOT / "outputs" / "metrics" / "held_out_neighbors.csv")
        cls.cohort = load_rectal_cohort()
        cls.train, cls.test = patient_level_split(cls.cohort)

    def test_expected_models_and_held_out_predictions(self):
        self.assertEqual([item["model"] for item in self.results["models"]], ["clinical", "radiomics", "fusion"])
        self.assertEqual(len(self.predictions), 45)
        self.assertEqual(self.predictions.patient_id.nunique(), 15)
        self.assertTrue((self.predictions.groupby("patient_id").size() == 3).all())
        self.assertTrue(self.predictions.probability.between(0, 1).all())

    def test_retrieval_never_draws_from_holdout(self):
        train_ids = set(self.train[self.cohort.patient_id])
        test_ids = set(self.test[self.cohort.patient_id])
        self.assertTrue(set(self.neighbors.neighbor_patient_id).issubset(train_ids))
        self.assertFalse(set(self.neighbors.neighbor_patient_id) & test_ids)
        self.assertTrue(set(self.neighbors.query_patient_id).issubset(test_ids))

    def test_synthetic_demo_fixture_matches_longitudinal_contract(self):
        manifest = get_demo_manifest()
        audit = validate_manifest(manifest)
        self.assertEqual(audit["patients"], 1)
        self.assertEqual(audit["visits"], 4)
        self.assertEqual(audit["mri_evidence_rows"], 4)
        self.assertEqual(audit["endoscopy_evidence_rows"], 4)
        self.assertTrue((manifest.data_origin == "synthetic_demo_only").all())

    def test_app_loads_product_demo_and_every_workspace_control(self):
        app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
        app.run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Today\'s surveillance reviews" in item.value for item in app.markdown))

        open_patient = next(button for button in app.button if button.label == "Open patient workspace")
        open_patient.click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Current surveillance assessment" in item.value for item in app.markdown))

        workspace = next(radio for radio in app.radio if radio.label == "Workspace navigation")
        workspace.set_value("Timeline").run()
        self.assertFalse(app.exception)
        timeline = next(radio for radio in app.radio if radio.label == "Surveillance visit")
        timeline.set_value("Jan 2026").run()
        self.assertFalse(app.exception)

        workspace = next(radio for radio in app.radio if radio.label == "Workspace navigation")
        workspace.set_value("Compare exams").run()
        self.assertFalse(app.exception)
        modality = next(radio for radio in app.radio if radio.label == "Comparison modality")
        modality.set_value("Endoscopy").run()
        self.assertFalse(app.exception)
        overlay = next(radio for radio in app.radio if radio.label == "Change overlay")
        overlay.set_value("Overlay off").run()
        self.assertFalse(app.exception)

        workspace = next(radio for radio in app.radio if radio.label == "Workspace navigation")
        workspace.set_value("Evidence").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Similar surveillance trajectories" in item.value for item in app.markdown))

        back = next(button for button in app.button if button.label == "← Today’s reviews")
        back.click().run()
        self.assertFalse(app.exception)
        archive = next(button for button in app.button if button.label == "Research archive")
        archive.click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Exploratory research artifacts" in item.value for item in app.title))


if __name__ == "__main__":
    unittest.main()
