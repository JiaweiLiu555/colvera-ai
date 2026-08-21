"""Structured synthetic patient data used by the product demo.

These fixtures intentionally resemble the approved-data longitudinal manifest:
one row per patient visit and evidence item.  They never enter model training,
evaluation, or validation reporting.
"""

from __future__ import annotations

from dataclasses import dataclass

@dataclass(frozen=True)
class DemoVisit:
    """One synthetic surveillance visit for display in the product UI."""

    visit_id: str
    date: str
    short_date: str
    time_offset_days: int
    role: str
    mri: str
    endoscopy: str
    cea: float
    dre: str
    imaging_change_score: int
    mri_annotation: str
    endoscopy_annotation: str


@dataclass(frozen=True)
class DemoPatient:
    """A synthetic surveillance case, kept independent from Streamlit."""

    patient_id: str
    age_range: str
    sex: str
    pathway: str
    treatment_history: str
    surveillance_duration: str
    last_visit: str
    next_follow_up: str
    review_status: str
    visits: tuple[DemoVisit, ...]

    @property
    def current_visit(self) -> DemoVisit:
        return self.visits[-1]

    @property
    def previous_visit(self) -> DemoVisit:
        return self.visits[-2]

    @property
    def has_interval_change(self) -> bool:
        """Whether the synthetic case is designed as a review-recommended pattern."""
        return self.review_status == "Review recommended"


PATIENT_024 = DemoPatient(
    patient_id="024",
    age_range="60–64",
    sex="Male",
    pathway="Watch & Wait Surveillance",
    treatment_history="Total neoadjuvant therapy completed · May 2025",
    surveillance_duration="15 months",
    last_visit="18 Aug 2026",
    next_follow_up="Expected Oct 2026",
    review_status="Review recommended",
    visits=(
        DemoVisit(
            visit_id="P024-2026-01",
            date="15 Jan 2026",
            short_date="Jan 2026",
            time_offset_days=0,
            role="Baseline",
            mri="Post-treatment scar without focal restricted diffusion.",
            endoscopy="Flat scar with no nodularity.",
            cea=1.8,
            dre="Soft scar; no palpable mass.",
            imaging_change_score=16,
            mri_annotation="Reference appearance of treated tumor bed",
            endoscopy_annotation="Flat scar contour",
        ),
        DemoVisit(
            visit_id="P024-2026-04",
            date="16 Apr 2026",
            short_date="Apr 2026",
            time_offset_days=91,
            role="Interval",
            mri="Stable treated tumor bed; no focal interval finding.",
            endoscopy="Stable scar; no new mucosal irregularity.",
            cea=1.9,
            dre="No interval clinical change.",
            imaging_change_score=14,
            mri_annotation="No material interval change",
            endoscopy_annotation="Stable scar contour",
        ),
        DemoVisit(
            visit_id="P024-2026-07",
            date="16 Jul 2026",
            short_date="Jul 2026",
            time_offset_days=182,
            role="Previous",
            mri="Stable treated tumor bed; no focal signal change.",
            endoscopy="Stable scar with smooth margins.",
            cea=2.1,
            dre="No major interval change.",
            imaging_change_score=15,
            mri_annotation="Stable treated tumor bed",
            endoscopy_annotation="Smooth scar margin",
        ),
        DemoVisit(
            visit_id="P024-2026-08",
            date="18 Aug 2026",
            short_date="Aug 2026",
            time_offset_days=215,
            role="Current",
            mri="New focal signal change at the treated tumor bed compared with July.",
            endoscopy="New focal superficial irregularity at the scar margin.",
            cea=3.0,
            dre="No major interval change.",
            imaging_change_score=52,
            mri_annotation="Focal interval signal change",
            endoscopy_annotation="Focal scar-margin irregularity",
        ),
    ),
)


PATIENT_018 = DemoPatient(
    patient_id="018",
    age_range="55–59",
    sex="Female",
    pathway="Watch & Wait Surveillance",
    treatment_history="Total neoadjuvant therapy completed · Mar 2025",
    surveillance_duration="17 months",
    last_visit="17 Aug 2026",
    next_follow_up="Expected Nov 2026",
    review_status="Stable surveillance pattern",
    visits=(
        DemoVisit("P018-2026-01", "14 Jan 2026", "Jan 2026", 0, "Baseline", "Stable treated tumor bed without focal restricted diffusion.", "Flat scar with no nodularity.", 1.6, "Soft scar; no palpable mass.", 13, "Reference appearance of treated tumor bed", "Flat scar contour"),
        DemoVisit("P018-2026-04", "15 Apr 2026", "Apr 2026", 91, "Interval", "Stable treated tumor bed; no focal interval finding.", "Stable scar with no new mucosal irregularity.", 1.5, "No interval clinical change.", 12, "No material interval change", "Stable scar contour"),
        DemoVisit("P018-2026-07", "15 Jul 2026", "Jul 2026", 182, "Previous", "Stable treated tumor bed; no focal signal change.", "Stable scar with smooth margins.", 1.6, "No major interval change.", 13, "Stable treated tumor bed", "Smooth scar margin"),
        DemoVisit("P018-2026-08", "17 Aug 2026", "Aug 2026", 215, "Current", "Stable treated tumor bed; no new focal signal change.", "Stable scar with smooth margins; no new irregularity.", 1.7, "No major interval change.", 14, "No new focal interval signal", "Stable smooth scar margin"),
    ),
)


PATIENT_031 = DemoPatient(
    patient_id="031",
    age_range="65–69",
    sex="Male",
    pathway="Watch & Wait Surveillance",
    treatment_history="Total neoadjuvant therapy completed · Apr 2025",
    surveillance_duration="16 months",
    last_visit="19 Aug 2026",
    next_follow_up="Expected Nov 2026",
    review_status="Stable surveillance pattern",
    visits=(
        DemoVisit("P031-2026-01", "16 Jan 2026", "Jan 2026", 0, "Baseline", "Post-treatment scar without focal restricted diffusion.", "Flat scar with no nodularity.", 2.2, "Soft scar; no palpable mass.", 18, "Reference appearance of treated tumor bed", "Flat scar contour"),
        DemoVisit("P031-2026-04", "17 Apr 2026", "Apr 2026", 91, "Interval", "Stable treated tumor bed; no focal interval finding.", "Stable scar without new mucosal irregularity.", 2.3, "No interval clinical change.", 15, "No material interval change", "Stable scar contour"),
        DemoVisit("P031-2026-07", "17 Jul 2026", "Jul 2026", 182, "Previous", "Stable treated tumor bed; no focal signal change.", "Stable scar with smooth margins.", 2.2, "No major interval change.", 16, "Stable treated tumor bed", "Smooth scar margin"),
        DemoVisit("P031-2026-08", "19 Aug 2026", "Aug 2026", 215, "Current", "Stable treated tumor bed; no new focal signal change.", "Stable scar with smooth margins; no new irregularity.", 2.3, "No major interval change.", 17, "No new focal interval signal", "Stable smooth scar margin"),
    ),
)


def get_demo_patients() -> tuple[DemoPatient, ...]:
    """Return the complete set of synthetic patient workspaces."""
    return (PATIENT_024, PATIENT_018, PATIENT_031)


def get_demo_patient(patient_id: str) -> DemoPatient:
    """Return a synthetic demo patient, preserving a safe default for the UI."""
    return next((patient for patient in get_demo_patients() if patient.patient_id == patient_id), PATIENT_024)


def get_demo_manifest(split: str = "train") -> "pd.DataFrame":
    """Return synthetic evidence rows compatible with the longitudinal contract.

    ``split`` is only provided so contract tests can verify the shape and
    leakage checks.  It does not designate these examples as a research cohort.
    The UI identifies every use of this fixture as synthetic demo data.
    """
    import pandas as pd

    rows: list[dict[str, object]] = []
    for visit in PATIENT_024.visits:
        evidence = (
            ("mri", "T2_DWI", f"demo/p024/{visit.visit_id}/mri.svg"),
            ("endoscopy", "white_light", f"demo/p024/{visit.visit_id}/endoscopy.svg"),
            ("laboratory", "CEA", f"demo/p024/{visit.visit_id}/cea.json"),
            ("dre", "digital_rectal_exam", f"demo/p024/{visit.visit_id}/dre.json"),
        )
        for evidence_type, measure, resource_ref in evidence:
            rows.append(
                {
                    "patient_id": PATIENT_024.patient_id,
                    "visit_id": visit.visit_id,
                    "time_offset_days": visit.time_offset_days,
                    "evidence_type": evidence_type,
                    "modality_or_measure": measure,
                    "resource_ref": resource_ref,
                    "split": split,
                    "data_origin": "synthetic_demo_only",
                }
            )
    return pd.DataFrame(rows)
