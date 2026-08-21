"""Dataset loading and leakage-safe split helpers for Colvera v0.1."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "configs" / "dataset.json"
RAW_FILE = ROOT / "data" / "raw" / "rectal_mri_radiomics_71.xlsx"


@dataclass(frozen=True)
class RectalCohort:
    frame: pd.DataFrame
    patient_id: str
    outcome_ordinal: str
    outcome_binary: str
    clinical_columns: list[str]
    radiomics_columns: list[str]

    @property
    def feature_columns(self) -> list[str]:
        return self.clinical_columns + self.radiomics_columns


def load_config() -> dict:
    return json.loads(CONFIG.read_text())


def md5sum(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_rectal_cohort(path: Path = RAW_FILE) -> RectalCohort:
    """Load the released Zenodo workbook without silently inventing fields."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run `python scripts/download_dataset.py` first."
        )
    source = pd.read_excel(path)
    patient_id = "Patient #"
    ordinal = "OUTCOME: 1=cCR+TRG1 2=TRG2 3=TRG3 4=TRG4"
    binary = "OUTCOME: binary:  0=responders(1,2) 1=nonresponders(3,4)"
    clinical = [
        "Mucinous tumor differentiation ",
        "EMVI by MRI exam",
        "Initial apsolute basophyls",
        "Type of circumferential tumor growth",
        "N stage",
    ]
    required = [patient_id, ordinal, binary, *clinical]
    missing = [column for column in required if column not in source.columns]
    if missing:
        raise ValueError(f"Unexpected dataset schema; missing columns: {missing}")

    frame = source.dropna(subset=[patient_id]).copy()
    frame[patient_id] = frame[patient_id].astype(int)
    frame[ordinal] = frame[ordinal].astype(int)
    frame[binary] = frame[binary].astype(int)
    if frame[patient_id].duplicated().any():
        raise ValueError("Patient identifiers are not unique; refusing to create a potentially leaky split.")

    radiomics = [column for column in source.columns[10:] if not str(column).startswith("Unnamed")]
    radiomics = [column for column in radiomics if frame[column].notna().any()]
    if len(frame) != load_config()["expected_patients"]:
        raise ValueError(f"Expected 71 patient rows; found {len(frame)}.")
    if len(radiomics) != 2144:
        raise ValueError(f"Expected 2,144 radiomics features; found {len(radiomics)}.")
    if frame[[*clinical, *radiomics]].isna().any().any():
        raise ValueError("Missing values found in retained model inputs; review the dataset before modeling.")
    return RectalCohort(frame, patient_id, ordinal, binary, clinical, radiomics)


def patient_level_split(cohort: RectalCohort) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create the single, reproducible patient-level holdout split."""
    cfg = load_config()
    train, test = train_test_split(
        cohort.frame,
        test_size=cfg["test_fraction"],
        stratify=cohort.frame[cohort.outcome_binary],
        random_state=cfg["random_seed"],
    )
    train = train.sort_values(cohort.patient_id).reset_index(drop=True)
    test = test.sort_values(cohort.patient_id).reset_index(drop=True)
    train_ids = set(train[cohort.patient_id])
    test_ids = set(test[cohort.patient_id])
    if train_ids & test_ids:
        raise AssertionError("Patient leakage: the same ID occurs in development and holdout data.")
    if len(train) + len(test) != len(cohort.frame):
        raise AssertionError("Split lost or duplicated rows.")
    return train, test


def feature_matrix(frame: pd.DataFrame, columns: list[str]) -> np.ndarray:
    return frame.loc[:, columns].to_numpy(dtype=float)
