"""Held-out metrics, CIs, calibration, and abstention summaries for v0.2."""

from __future__ import annotations

import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, confusion_matrix, roc_auc_score


def binary_metrics(y_true: np.ndarray, probability: np.ndarray, threshold: float) -> dict[str, float | int]:
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probability, dtype=float)
    prediction = (p >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, prediction, labels=[0, 1]).ravel()
    return {
        "auroc": float(roc_auc_score(y, p)),
        "average_precision": float(average_precision_score(y, p)),
        "sensitivity": float(tp / (tp + fn)) if tp + fn else float("nan"),
        "specificity": float(tn / (tn + fp)) if tn + fp else float("nan"),
        "precision": float(tp / (tp + fp)) if tp + fp else float("nan"),
        "npv": float(tn / (tn + fn)) if tn + fn else float("nan"),
        "false_negative_rate": float(fn / (tp + fn)) if tp + fn else float("nan"),
        "brier": float(brier_score_loss(y, p)),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn),
    }


def bootstrap_intervals(y_true: np.ndarray, probability: np.ndarray, threshold: float, seed: int = 20260816, n_bootstrap: int = 2000) -> dict[str, list[float | None]]:
    y = np.asarray(y_true, dtype=int)
    p = np.asarray(probability, dtype=float)
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n_bootstrap):
        take = rng.integers(0, len(y), len(y))
        if len(np.unique(y[take])) == 2:
            rows.append(binary_metrics(y[take], p[take], threshold))
    answer: dict[str, list[float]] = {}
    for key in ("auroc", "average_precision", "sensitivity", "specificity", "precision", "npv", "brier"):
        values = np.asarray([row[key] for row in rows], dtype=float)
        values = values[np.isfinite(values)]
        answer[key] = [float(np.quantile(values, 0.025)), float(np.quantile(values, 0.975))] if len(values) else [None, None]
    answer["valid_resamples"] = [float(len(rows)), float(n_bootstrap)]
    return answer


def calibration_summary(y_true: np.ndarray, probability: np.ndarray) -> dict[str, object]:
    """Descriptive held-out calibration; never used to refit a deployed model."""
    y = np.asarray(y_true, dtype=int)
    p = np.clip(np.asarray(probability, dtype=float), 1e-6, 1 - 1e-6)
    observed, predicted = calibration_curve(y, p, n_bins=5, strategy="quantile")
    logit = np.log(p / (1 - p)).reshape(-1, 1)
    regression = LogisticRegression(C=1e6, solver="lbfgs").fit(logit, y)
    ece = float(np.mean(np.abs(observed - predicted)))
    return {
        "reliability": {"mean_predicted": predicted.tolist(), "observed_fraction": observed.tolist()},
        "calibration_intercept": float(regression.intercept_[0]),
        "calibration_slope": float(regression.coef_[0][0]),
        "ece_unweighted_five_bin": ece,
    }


def abstention_summary(y_true: np.ndarray, probability: np.ndarray, threshold: float, margin: float = 0.10) -> dict[str, object]:
    p = np.asarray(probability, dtype=float)
    retained = np.abs(p - threshold) > margin
    result: dict[str, object] = {"rule": f"abstain when |p - {threshold:.4f}| <= {margin:.2f}", "coverage": float(retained.mean()), "abstained_cases": int((~retained).sum())}
    if retained.any() and len(np.unique(np.asarray(y_true)[retained])) == 2:
        result["retained_metrics"] = binary_metrics(np.asarray(y_true)[retained], p[retained], threshold)
    return result
