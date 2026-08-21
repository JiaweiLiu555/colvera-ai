"""Evaluation helpers. Metrics are exploratory because the released cohort is small."""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


@dataclass(frozen=True)
class MetricSet:
    auroc: float
    average_precision: float
    sensitivity: float
    specificity: float
    precision: float
    npv: float
    f1: float
    brier: float
    false_negative_rate: float
    tp: int
    fp: int
    tn: int
    fn: int

    def as_dict(self) -> dict:
        return asdict(self)


def metrics(y_true: np.ndarray, probability: np.ndarray, threshold: float = 0.5) -> MetricSet:
    y_true = np.asarray(y_true, dtype=int)
    probability = np.asarray(probability, dtype=float)
    predicted = (probability >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, predicted, labels=[0, 1]).ravel()
    specificity = tn / (tn + fp) if tn + fp else float("nan")
    npv = tn / (tn + fn) if tn + fn else float("nan")
    sensitivity = tp / (tp + fn) if tp + fn else float("nan")
    return MetricSet(
        auroc=float(roc_auc_score(y_true, probability)),
        average_precision=float(average_precision_score(y_true, probability)),
        sensitivity=float(sensitivity),
        specificity=float(specificity),
        precision=float(precision_score(y_true, predicted, zero_division=0)),
        npv=float(npv),
        f1=float(f1_score(y_true, predicted, zero_division=0)),
        brier=float(brier_score_loss(y_true, probability)),
        false_negative_rate=float(1 - sensitivity),
        tp=int(tp),
        fp=int(fp),
        tn=int(tn),
        fn=int(fn),
    )


def bootstrap_ci(
    y_true: np.ndarray,
    probability: np.ndarray,
    n_bootstrap: int = 2000,
    seed: int = 20260815,
) -> dict[str, list[float | None]]:
    """Nonparametric holdout bootstrap intervals; undefined resamples are skipped."""
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true, dtype=int)
    probability = np.asarray(probability, dtype=float)
    rows: list[dict] = []
    for _ in range(n_bootstrap):
        index = rng.integers(0, len(y_true), len(y_true))
        sample_y = y_true[index]
        if len(np.unique(sample_y)) < 2:
            continue
        rows.append(metrics(sample_y, probability[index]).as_dict())
    intervals: dict[str, list[float | None]] = {}
    for key in ["auroc", "average_precision", "sensitivity", "specificity", "precision", "npv", "f1", "brier"]:
        values = np.asarray([row[key] for row in rows], dtype=float)
        values = values[np.isfinite(values)]
        intervals[key] = [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))] if len(values) else [None, None]
    intervals["valid_bootstrap_resamples"] = [len(rows), n_bootstrap]
    return intervals


def calibration_data(y_true: np.ndarray, probability: np.ndarray) -> dict[str, list[float]]:
    observed, predicted = calibration_curve(y_true, probability, n_bins=3, strategy="quantile")
    return {"mean_predicted": predicted.tolist(), "observed_fraction": observed.tolist()}
