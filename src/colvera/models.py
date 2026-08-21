"""Small, interpretable model families for the v0.1 experiment."""

from __future__ import annotations

from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def clinical_pipeline() -> Pipeline:
    return Pipeline(
        [
            ("scale", StandardScaler()),
            ("model", LogisticRegression(max_iter=20_000, solver="liblinear", penalty="l2", random_state=20260815)),
        ]
    )


def high_dimensional_pipeline() -> Pipeline:
    """All transforms are fit inside cross-validation folds to avoid model-selection leakage."""
    return Pipeline(
        [
            ("variance", VarianceThreshold()),
            ("scale", StandardScaler()),
            ("select", SelectKBest(score_func=f_classif, k=10)),
            ("model", LogisticRegression(max_iter=20_000, solver="liblinear", penalty="l1", random_state=20260815)),
        ]
    )


def parameter_grid(kind: str) -> dict[str, list]:
    if kind == "clinical":
        return {"model__C": [0.01, 0.1, 1.0, 10.0]}
    if kind in {"radiomics", "fusion"}:
        return {"select__k": [5, 10, 20], "model__C": [0.01, 0.1, 1.0, 10.0]}
    raise ValueError(f"Unknown model kind: {kind}")
