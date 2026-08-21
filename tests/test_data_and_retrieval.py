from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.data import load_rectal_cohort, patient_level_split
from colvera.retrieval import retrieve_neighbors


class DatasetAndRetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort = load_rectal_cohort()
        cls.train, cls.test = patient_level_split(cls.cohort)

    def test_expected_unique_patient_cohort(self):
        self.assertEqual(len(self.cohort.frame), 71)
        self.assertEqual(self.cohort.frame[self.cohort.patient_id].nunique(), 71)
        self.assertEqual(len(self.cohort.radiomics_columns), 2144)
        self.assertEqual(self.cohort.frame[self.cohort.feature_columns].isna().sum().sum(), 0)

    def test_patient_level_holdout_has_no_overlap(self):
        train_ids = set(self.train[self.cohort.patient_id])
        test_ids = set(self.test[self.cohort.patient_id])
        self.assertFalse(train_ids & test_ids)
        self.assertEqual(len(train_ids) + len(test_ids), 71)

    def test_outcomes_and_identifiers_never_enter_model_features(self):
        forbidden = {self.cohort.patient_id, self.cohort.outcome_binary, self.cohort.outcome_ordinal}
        self.assertFalse(forbidden & set(self.cohort.feature_columns))

    def test_retrieval_only_returns_development_cases(self):
        columns = self.cohort.clinical_columns
        retrieved = retrieve_neighbors(self.train, self.test.iloc[:2], columns, self.cohort.patient_id, self.cohort.outcome_binary)
        self.assertTrue(set(retrieved["neighbor_patient_id"]).issubset(set(self.train[self.cohort.patient_id])))
        self.assertFalse(set(retrieved["neighbor_patient_id"]) & set(self.test[self.cohort.patient_id]))


if __name__ == "__main__":
    unittest.main()
