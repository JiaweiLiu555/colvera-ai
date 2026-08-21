"""Validate a de-identified longitudinal evidence manifest before modeling.

This is deliberately a data-contract layer, not a model.  It accepts only
relative image references and separates outcome/event columns from permissible
model inputs so a future current-only/longitudinal comparison cannot silently
leak outcome information.
"""

from __future__ import annotations

from pathlib import PurePosixPath

import pandas as pd


REQUIRED_MANIFEST_COLUMNS = (
    "patient_id",
    "visit_id",
    "time_offset_days",
    "evidence_type",
    "modality_or_measure",
    "resource_ref",
    "split",
)
OUTCOME_COLUMNS = {
    "outcome_name",
    "outcome_value",
    "outcome_date_offset_days",
    "event_date_offset_days",
    "local_regrowth",
    "pcr",
    "ccr_status",
}
IDENTIFIER_COLUMNS = {"patient_id", "visit_id", "resource_ref", "split"}
VALID_EVIDENCE_TYPES = {"mri", "endoscopy", "clinical", "laboratory", "dre", "outcome"}
VALID_SPLITS = {"train", "validation", "test", "external_test"}


def _is_safe_relative_reference(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_manifest(frame: pd.DataFrame) -> dict[str, object]:
    """Return a transparent audit or raise before any image/model operation.

    A row is one evidence item at a patient visit. An MRI visit may have several
    modality rows; a future dataset can add endoscopy, CEA/DRE, and outcomes
    without changing the key structure.
    """
    missing = [column for column in REQUIRED_MANIFEST_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Manifest missing required columns: {missing}")
    if frame.empty:
        raise ValueError("Manifest is empty")
    if frame[list(REQUIRED_MANIFEST_COLUMNS)].isna().any().any():
        raise ValueError("Required manifest fields may not be missing")
    if not pd.api.types.is_numeric_dtype(frame["time_offset_days"]):
        raise ValueError("time_offset_days must be numeric relative-to-baseline offsets")
    if not set(frame["evidence_type"].astype(str)).issubset(VALID_EVIDENCE_TYPES):
        raise ValueError(f"Unsupported evidence_type; allowed values are {sorted(VALID_EVIDENCE_TYPES)}")
    if not set(frame["split"].astype(str)).issubset(VALID_SPLITS):
        raise ValueError(f"Unsupported split; allowed values are {sorted(VALID_SPLITS)}")
    if not frame["resource_ref"].map(_is_safe_relative_reference).all():
        raise ValueError("resource_ref must be a non-empty relative reference without '..'")

    patient_split_count = frame.groupby("patient_id")["split"].nunique()
    overlapping_patients = patient_split_count[patient_split_count > 1].index.tolist()
    if overlapping_patients:
        raise ValueError(f"Patient-level split leakage: patients appear in multiple splits: {overlapping_patients[:10]}")
    duplicate_evidence = frame.duplicated(
        subset=["patient_id", "visit_id", "time_offset_days", "evidence_type", "modality_or_measure", "resource_ref"],
        keep=False,
    )
    if duplicate_evidence.any():
        raise ValueError("Duplicate evidence rows found; resolve lineage before model development")

    visit_times = frame[["patient_id", "visit_id", "time_offset_days"]].drop_duplicates()
    visit_time_count = visit_times.groupby(["patient_id", "visit_id"])["time_offset_days"].nunique()
    inconsistent_visits = visit_time_count[visit_time_count > 1]
    if not inconsistent_visits.empty:
        raise ValueError("A visit_id has conflicting time offsets")
    mri_rows = frame[frame["evidence_type"] == "mri"]
    return {
        "rows": int(len(frame)),
        "patients": int(frame["patient_id"].nunique()),
        "visits": int(visit_times.shape[0]),
        "mri_evidence_rows": int(len(mri_rows)),
        "endoscopy_evidence_rows": int((frame["evidence_type"] == "endoscopy").sum()),
        "clinical_evidence_rows": int((frame["evidence_type"] == "clinical").sum()),
        "laboratory_evidence_rows": int((frame["evidence_type"] == "laboratory").sum()),
        "outcome_rows": int((frame["evidence_type"] == "outcome").sum()),
        "patients_by_split": {str(key): int(value) for key, value in frame.groupby("split")["patient_id"].nunique().items()},
        "available_modalities_or_measures": sorted(frame["modality_or_measure"].astype(str).unique().tolist()),
        "patient_level_isolation": True,
        "resource_references": "relative only; no image bytes or PHI are read by the contract validator",
    }


def _visit_table(frame: pd.DataFrame, split: str | None = None) -> pd.DataFrame:
    scoped = frame if split is None else frame[frame["split"] == split]
    return scoped[["patient_id", "visit_id", "time_offset_days", "split"]].drop_duplicates().sort_values(
        ["patient_id", "time_offset_days", "visit_id"]
    )


def current_only_records(frame: pd.DataFrame, outcome_name: str, split: str) -> pd.DataFrame:
    """Prepare one current-visit row per available visit without outcome leakage."""
    validate_manifest(frame)
    visits = _visit_table(frame, split)
    if visits.empty:
        raise ValueError(f"No visits found for split={split!r}")
    rows = []
    for visit in visits.itertuples(index=False):
        evidence = frame[
            (frame.patient_id == visit.patient_id)
            & (frame.visit_id == visit.visit_id)
            & (frame.evidence_type != "outcome")
        ]
        rows.append(
            {
                "patient_id": visit.patient_id,
                "current_visit_id": visit.visit_id,
                "current_time_offset_days": visit.time_offset_days,
                "split": visit.split,
                "outcome_name_requested": outcome_name,
                "available_evidence_types": ";".join(sorted(evidence.evidence_type.astype(str).unique())),
                "available_modalities_or_measures": ";".join(sorted(evidence.modality_or_measure.astype(str).unique())),
            }
        )
    return pd.DataFrame(rows)


def longitudinal_pairs(frame: pd.DataFrame, outcome_name: str, split: str, required_modality: str = "T2") -> pd.DataFrame:
    """Create adjacent prior/current MRI pairs within a split only.

    This represents the next core experiment: current MRI versus previous +
    current MRI. No pair crosses patients or data splits.
    """
    validate_manifest(frame)
    mri = frame[(frame.evidence_type == "mri") & (frame.modality_or_measure == required_modality) & (frame.split == split)]
    visits = _visit_table(mri, split)
    rows = []
    for patient_id, patient_visits in visits.groupby("patient_id", sort=False):
        ordered = patient_visits.sort_values(["time_offset_days", "visit_id"])
        for previous, current in zip(ordered.itertuples(index=False), ordered.iloc[1:].itertuples(index=False)):
            rows.append(
                {
                    "patient_id": patient_id,
                    "previous_visit_id": previous.visit_id,
                    "previous_time_offset_days": previous.time_offset_days,
                    "current_visit_id": current.visit_id,
                    "current_time_offset_days": current.time_offset_days,
                    "interval_days": current.time_offset_days - previous.time_offset_days,
                    "modality": required_modality,
                    "split": split,
                    "outcome_name_requested": outcome_name,
                }
            )
    return pd.DataFrame(rows)


def model_feature_columns(frame: pd.DataFrame) -> list[str]:
    """Return permissible structured columns; never include IDs, paths, splits, outcomes or dates."""
    prohibited = IDENTIFIER_COLUMNS | OUTCOME_COLUMNS | {"time_offset_days", "evidence_type", "modality_or_measure"}
    return [column for column in frame.columns if column not in prohibited and not column.endswith("_date")]
