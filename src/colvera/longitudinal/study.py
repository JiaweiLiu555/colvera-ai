"""Model-facing study specifications for approved longitudinal data.

Specifications contain no weights or performance claims. They make each future
comparison explicit before data are opened, preventing a longitudinal outcome
from being accidentally redefined during model work.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .contract import current_only_records, longitudinal_pairs, validate_manifest


@dataclass(frozen=True)
class StudySpecification:
    identifier: str
    target: str
    description: str
    required_evidence: tuple[str, ...]
    requires_prior_visit: bool
    clinical_evidence_allowed: bool
    retrieval_pool_rule: str

    def prepare_development_inputs(self, manifest: pd.DataFrame, split: str = "train") -> pd.DataFrame:
        """Prepare exposure-free input rows for a development split only."""
        if split not in {"train", "validation"}:
            raise ValueError("Model development views may only be prepared from train or validation splits")
        validate_manifest(manifest)
        if self.requires_prior_visit:
            return longitudinal_pairs(manifest, outcome_name=self.target, split=split, required_modality="T2")
        return current_only_records(manifest, outcome_name=self.target, split=split)


CURRENT_ONLY = StudySpecification(
    identifier="current_only",
    target="owner_defined_outcome",
    description="Current MRI evidence only → outcome.",
    required_evidence=("mri:T2",),
    requires_prior_visit=False,
    clinical_evidence_allowed=False,
    retrieval_pool_rule="If used, retrieve from training patients only; never a validation/test patient.",
)

LONGITUDINAL = StudySpecification(
    identifier="longitudinal",
    target="owner_defined_outcome",
    description="Previous + current MRI evidence from the same patient → outcome.",
    required_evidence=("mri:T2", "prior_visit"),
    requires_prior_visit=True,
    clinical_evidence_allowed=False,
    retrieval_pool_rule="If used, retrieve from training patients only; never a validation/test patient.",
)

MULTIMODAL_LONGITUDINAL = StudySpecification(
    identifier="multimodal_longitudinal",
    target="owner_defined_outcome",
    description="Previous/current MRI plus time-aligned approved clinical evidence → outcome.",
    required_evidence=("mri:T2", "prior_visit", "clinical_or_laboratory"),
    requires_prior_visit=True,
    clinical_evidence_allowed=True,
    retrieval_pool_rule="If used, retrieve from training patients only; never a validation/test patient.",
)

FULL_COLVERA = StudySpecification(
    identifier="full_colvera",
    target="local_regrowth",
    description="Serial MRI + endoscopy + clinical trajectory + training-only comparable trajectories → local regrowth.",
    required_evidence=("mri:T2", "prior_visit", "endoscopy", "clinical_or_laboratory", "local_regrowth_event"),
    requires_prior_visit=True,
    clinical_evidence_allowed=True,
    retrieval_pool_rule="Retrieval must use trajectories from training patients only and never present similarity as a diagnosis.",
)

STUDY_REGISTRY = {spec.identifier: spec for spec in (CURRENT_ONLY, LONGITUDINAL, MULTIMODAL_LONGITUDINAL, FULL_COLVERA)}
