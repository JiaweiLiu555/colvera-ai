"""Audit the released table before any model is fit."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.data import load_config, load_rectal_cohort, md5sum, patient_level_split  # noqa: E402


def main() -> None:
    cohort = load_rectal_cohort()
    train, test = patient_level_split(cohort)
    frame = cohort.frame
    profile = {
        "dataset": load_config()["name"],
        "checksum_md5": md5sum(ROOT / "data" / "raw" / "rectal_mri_radiomics_71.xlsx"),
        "patient_rows": int(len(frame)),
        "unique_patient_ids": int(frame[cohort.patient_id].nunique()),
        "duplicate_patient_ids": int(frame[cohort.patient_id].duplicated().sum()),
        "patient_id_range": [int(frame[cohort.patient_id].min()), int(frame[cohort.patient_id].max())],
        "studies_per_patient": "One released tabular row per patient; raw studies are unavailable.",
        "binary_outcome_counts": {str(int(k)): int(v) for k, v in frame[cohort.outcome_binary].value_counts().sort_index().items()},
        "ordinal_outcome_counts": {str(int(k)): int(v) for k, v in frame[cohort.outcome_ordinal].value_counts().sort_index().items()},
        "clinical_feature_count": len(cohort.clinical_columns),
        "radiomics_feature_count": len(cohort.radiomics_columns),
        "missing_input_cells": int(frame[cohort.feature_columns].isna().sum().sum()),
        "all_missing_source_columns": [str(c) for c in frame.columns if frame[c].isna().all()],
        "zero_variance_radiomics": int((frame[cohort.radiomics_columns].nunique(dropna=False) <= 1).sum()),
        "train_patients": int(len(train)),
        "test_patients": int(len(test)),
        "train_patient_ids": [int(x) for x in train[cohort.patient_id].tolist()],
        "test_patient_ids": [int(x) for x in test[cohort.patient_id].tolist()],
        "available_metadata": "No age, sex, site, scanner, raw MRI, endoscopy, serial examinations, follow-up timing, or local-regrowth outcome fields are released in the workbook.",
        "source_preprocessing_warning": "The record describes clinicopathological and radiomics features as z-score normalized. Original unnormalized values and training-only normalization parameters are not released, so source-level preprocessing leakage cannot be ruled out.",
    }
    out = ROOT / "outputs" / "metrics" / "dataset_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(profile, indent=2) + "\n")
    print(json.dumps(profile, indent=2))


if __name__ == "__main__":
    main()
