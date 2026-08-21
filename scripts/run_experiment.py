"""Run the reproducible Colvera v0.1 exploratory experiment.

This is intentionally a small, patient-level, held-out experiment. It does not
make clinical claims and cannot remove source-level preprocessing limitations.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay
from sklearn.model_selection import GridSearchCV, StratifiedKFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera import MODEL_VERSION  # noqa: E402
from colvera.data import feature_matrix, load_config, load_rectal_cohort, patient_level_split  # noqa: E402
from colvera.evaluation import bootstrap_ci, calibration_data, metrics  # noqa: E402
from colvera.models import clinical_pipeline, high_dimensional_pipeline, parameter_grid  # noqa: E402
from colvera.retrieval import retrieve_neighbors  # noqa: E402


def fit_model(name: str, x_train: np.ndarray, y_train: np.ndarray):
    pipeline = clinical_pipeline() if name == "clinical" else high_dimensional_pipeline()
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=20260815)
    search = GridSearchCV(
        pipeline,
        parameter_grid(name if name != "fusion" else "fusion"),
        scoring="roc_auc",
        cv=cv,
        refit=True,
        n_jobs=1,
        error_score="raise",
    )
    return search.fit(x_train, y_train)


def selected_feature_names(search, feature_names: list[str]) -> list[str]:
    if "select" not in search.best_estimator_.named_steps:
        return list(feature_names)
    variance = search.best_estimator_.named_steps["variance"].get_support()
    retained = np.asarray(feature_names, dtype=object)[variance]
    selected = search.best_estimator_.named_steps["select"].get_support()
    return [str(x) for x in retained[selected]]


def make_figures(predictions: pd.DataFrame, result_rows: list[dict]) -> None:
    figures = ROOT / "outputs" / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    counts = predictions.drop_duplicates("patient_id")["true_outcome"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(5.3, 3.4))
    ax.bar(["Responder\n(cCR/TRG1/TRG2)", "Non-responder\n(TRG3/TRG4)"], [32, 39], color=["#3b82a0", "#bf5b4b"])
    ax.set_ylabel("Patients in released cohort")
    ax.set_title("Released dataset class balance (N=71)")
    for i, value in enumerate([32, 39]): ax.text(i, value + 0.8, str(value), ha="center", fontweight="bold")
    fig.tight_layout(); fig.savefig(figures / "class_balance.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.8, 4.1))
    for model_name, group in predictions.groupby("model"):
        RocCurveDisplay.from_predictions(group.true_outcome, group.probability, name=model_name, ax=ax)
    ax.set_title("Held-out ROC curves (N=15; exploratory)")
    fig.tight_layout(); fig.savefig(figures / "roc.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.8, 4.1))
    for model_name, group in predictions.groupby("model"):
        PrecisionRecallDisplay.from_predictions(group.true_outcome, group.probability, name=model_name, ax=ax)
    ax.set_title("Held-out precision–recall curves (N=15; exploratory)")
    fig.tight_layout(); fig.savefig(figures / "precision_recall.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.8, 4.1))
    for model_name, group in predictions.groupby("model"):
        data = calibration_data(group.true_outcome.to_numpy(), group.probability.to_numpy())
        ax.plot(data["mean_predicted"], data["observed_fraction"], marker="o", label=model_name)
    ax.plot([0, 1], [0, 1], linestyle="--", color="#64748b", label="ideal")
    ax.set(xlabel="Mean predicted probability", ylabel="Observed non-responder fraction", title="Held-out calibration view (3 quantile bins)")
    ax.legend(); fig.tight_layout(); fig.savefig(figures / "calibration.png", dpi=180); plt.close(fig)

    names = [row["model"] for row in result_rows]
    aucs = [row["metrics"]["auroc"] for row in result_rows]
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    bars = ax.bar(names, aucs, color=["#708090", "#3b82a0", "#0f766e"])
    ax.set_ylim(0, 1); ax.set_ylabel("AUROC"); ax.set_title("Held-out model comparison (exploratory)")
    for bar, value in zip(bars, aucs): ax.text(bar.get_x()+bar.get_width()/2, value+.025, f"{value:.2f}", ha="center", fontweight="bold")
    fig.tight_layout(); fig.savefig(figures / "model_comparison.png", dpi=180); plt.close(fig)


def main() -> None:
    cohort = load_rectal_cohort()
    cfg = load_config()
    train, test = patient_level_split(cohort)
    y_train = train[cohort.outcome_binary].to_numpy()
    y_test = test[cohort.outcome_binary].to_numpy()
    feature_sets = {
        "clinical": cohort.clinical_columns,
        "radiomics": cohort.radiomics_columns,
        "fusion": cohort.feature_columns,
    }
    result_rows: list[dict] = []
    prediction_rows: list[pd.DataFrame] = []
    fitted: dict[str, object] = {}

    for name, columns in feature_sets.items():
        search = fit_model(name, feature_matrix(train, columns), y_train)
        probability = search.predict_proba(feature_matrix(test, columns))[:, 1]
        result = metrics(y_test, probability)
        fitted[name] = search
        result_rows.append(
            {
                "model": name,
                "input_count": len(columns),
                "best_parameters": {key: (int(value) if isinstance(value, np.integer) else value) for key, value in search.best_params_.items()},
                "inner_cv_auroc": float(search.best_score_),
                "metrics": result.as_dict(),
                "bootstrap_95_ci": bootstrap_ci(y_test, probability),
            }
        )
        prediction_rows.append(
            pd.DataFrame(
                {
                    "patient_id": test[cohort.patient_id].to_numpy(),
                    "true_outcome": y_test,
                    "model": name,
                    "probability": probability,
                    "predicted_outcome": (probability >= 0.5).astype(int),
                    "split": "held_out_test",
                }
            )
        )

    fusion_selected = selected_feature_names(fitted["fusion"], cohort.feature_columns)
    neighbors = retrieve_neighbors(
        train,
        test,
        fusion_selected,
        cohort.patient_id,
        cohort.outcome_binary,
        neighbors=3,
    )
    predictions = pd.concat(prediction_rows, ignore_index=True)
    metrics_dir = ROOT / "outputs" / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(metrics_dir / "held_out_predictions.csv", index=False)
    neighbors.to_csv(metrics_dir / "held_out_neighbors.csv", index=False)
    test_case = test[[cohort.patient_id, cohort.outcome_ordinal, cohort.outcome_binary, *cohort.clinical_columns]].copy()
    test_case.columns = ["patient_id", "outcome_ordinal", "true_outcome", "mucinous", "emvi", "basophils", "circumferential_growth", "n_stage"]
    test_case.to_csv(metrics_dir / "held_out_case_features.csv", index=False)

    artifact_dir = ROOT / "outputs" / "model_artifacts"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(fitted["fusion"], artifact_dir / "colvera_mri_clinical_v0_1.joblib")
    metadata = {
        "model_version": MODEL_VERSION,
        "run_date": str(date.today()),
        "dataset": cfg["name"],
        "dataset_doi": cfg["doi"],
        "task": "Pretreatment binary treatment-response prediction: nonresponder (TRG3/4) versus responder (cCR/TRG1/TRG2).",
        "holdout": {"train_patients": int(len(train)), "test_patients": int(len(test)), "seed": cfg["random_seed"]},
        "research_boundary": "This experiment is not a local-regrowth model, not longitudinal, and not suitable for patient care.",
        "source_preprocessing_warning": "The released table is already z-score normalized and includes five variables described as outcome-associated. Source-level preprocessing/feature-selection leakage cannot be fully excluded.",
        "models": result_rows,
        "fusion_selected_features": fusion_selected,
        "retrieval": {
            "representation": "Final fusion model's fold-selected features after refitting on the development set.",
            "neighbors_per_held_out_case": 3,
            "restriction": "Neighbors are drawn only from the development set; no holdout case retrieves itself or another holdout case.",
        },
    }
    (metrics_dir / "results.json").write_text(json.dumps(metadata, indent=2) + "\n")
    make_figures(predictions, result_rows)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
