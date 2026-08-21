"""Run the single locked v0.2 released-weight test evaluation exactly once."""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import PrecisionRecallDisplay, RocCurveDisplay

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.v02.data import RELEASE_ROOT, load_release_split, sha256  # noqa: E402
from colvera.v02.metrics import abstention_summary, binary_metrics, bootstrap_intervals, calibration_summary  # noqa: E402
from colvera.v02.model import load_released_weights, released_probabilities  # noqa: E402


TEST_CHANNEL_LOCK = {
    "published_adc_reproduction": {"weight": "weights_ADC.hdf5", "channel": 0, "intended_modality": "ADC"},
    "published_t2_reproduction": {"weight": "weights_T2.hdf5", "channel": 3, "intended_modality": "T2-weighted MRI"},
}
PAPER_RESULTS = {
    "published_adc_reproduction": {"auroc": 0.851, "sensitivity": 0.943, "specificity": 0.683, "ppv": 0.874, "npv": 0.837},
    "published_t2_reproduction": {"auroc": 0.721},
}


def native(value):
    if isinstance(value, np.generic):
        value = value.item()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: native(item) for key, item in value.items()}
    if isinstance(value, list):
        return [native(item) for item in value]
    return value


def save_figures(predictions: pd.DataFrame, output: Path) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(6.1, 4.4))
    for model, group in predictions.groupby("model"):
        RocCurveDisplay.from_predictions(group.true_good_response, group.p_good_response, name=model, ax=ax)
    ax.set_title("Locked released-weight test check (N=200 array records)")
    fig.tight_layout()
    fig.savefig(output / "roc.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.1, 4.4))
    for model, group in predictions.groupby("model"):
        PrecisionRecallDisplay.from_predictions(group.true_good_response, group.p_good_response, name=model, ax=ax)
    ax.set_title("Precision–recall: provisional GR mapping")
    fig.tight_layout()
    fig.savefig(output / "precision_recall.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.1, 4.4))
    for model, group in predictions.groupby("model"):
        summary = calibration_summary(group.true_good_response.to_numpy(), group.p_good_response.to_numpy())
        reliability = summary["reliability"]
        ax.plot(reliability["mean_predicted"], reliability["observed_fraction"], marker="o", label=model)
    ax.plot([0, 1], [0, 1], "--", color="#64748b", label="ideal")
    ax.set(xlabel="Mean predicted P(GR)", ylabel="Observed GR frequency", title="Descriptive held-out calibration (not recalibrated)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "calibration.png", dpi=180)
    plt.close(fig)


def main() -> None:
    output = ROOT / "outputs" / "v02" / "final-test"
    result_path = output / "final_results.json"
    if result_path.exists():
        raise SystemExit(f"Final-test lock already consumed: {result_path}. Do not rerun this evaluation.")
    if not (ROOT / "docs" / "v02-final-model-lock.md").exists() or not (ROOT / "data" / "v02" / "test_lock.json").exists():
        raise SystemExit("Refusing final evaluation without the model and data locks.")
    output.mkdir(parents=True, exist_ok=True)
    test = load_release_split("test")
    # Predeclared convention: test class-0 count is 60, matching reported GR count.
    y_good = (test.label_index == 0).astype(int)
    if y_good.sum() != 60 or len(y_good) != 200:
        raise RuntimeError("Locked target prevalence differs from release audit; aborting.")

    prediction_rows: list[pd.DataFrame] = []
    results: list[dict[str, object]] = []
    weight_root = RELEASE_ROOT / "good_response" / "weights"
    for model_name, setting in TEST_CHANNEL_LOCK.items():
        weight_path = weight_root / setting["weight"]
        model = load_released_weights(weight_path, device="cpu")
        probability = released_probabilities(model, test.images[:, setting["channel"]])[:, 0]
        metric = binary_metrics(y_good, probability, threshold=0.5)
        intervals = bootstrap_intervals(y_good, probability, threshold=0.5)
        calibration = calibration_summary(y_good, probability)
        abstention = abstention_summary(y_good, probability, threshold=0.5, margin=0.10)
        published = PAPER_RESULTS[model_name]
        auc_gap = float(metric["auroc"] - published["auroc"])
        results.append(
            {
                "model": model_name,
                "released_weight": str(weight_path.relative_to(ROOT)),
                "weight_sha256": sha256(weight_path),
                "predeclared_channel": setting["channel"],
                "intended_modality": setting["intended_modality"],
                "mapping_status": "unverified: source NPZ does not name its four image channels",
                "outcome_mapping": "class index 0 treated provisionally as GR because prevalence is 60/200, matching the publication; author confirmation required",
                "threshold": 0.5,
                "threshold_status": "descriptive softmax threshold only; not selected from this test set and not confirmed as the published operating threshold",
                "metrics": metric,
                "bootstrap_95_ci": intervals,
                "descriptive_held_out_calibration": calibration,
                "abstention": abstention,
                "published_reference": published,
                "auroc_difference_from_published": auc_gap,
                "reproduction_strength": "not assigned: channel and per-record outcome mapping cannot be independently verified from the release",
            }
        )
        prediction_rows.append(
            pd.DataFrame(
                {
                    "release_record_id": [f"test_{idx:04d}" for idx in range(len(test.images))],
                    "model": model_name,
                    "predeclared_channel": setting["channel"],
                    "true_good_response": y_good,
                    "p_good_response": probability,
                    "predicted_good_response_at_0_5": (probability >= 0.5).astype(int),
                }
            )
        )
    predictions = pd.concat(prediction_rows, ignore_index=True)
    predictions.to_csv(output / "final_predictions.csv", index=False)
    save_figures(predictions, output)
    result = {
        "evaluated_utc": datetime.now(timezone.utc).isoformat(),
        "evaluation_type": "single locked released-weight inference check, not patient-level validation",
        "test_array": "good_response/data/test_images_00001.npz + test_targets_00001.npz",
        "test_records": 200,
        "test_patient_ids": "not released",
        "target_prevalence": {"provisional_good_response": 60, "other_class": 140},
        "lock": "docs/v02-final-model-lock.md and data/v02/test_lock.json",
        "models": results,
        "global_limitations": [
            "Only 323 unnamed development array records are released; no patient-level CV or new-model training was performed.",
            "The NPZ lacks a channel-to-modality mapping, patient identifiers, dates, scanner linkage, clinical covariates, and augmentation lineage.",
            "These estimates do not establish external validation, patient-level generalization, calibration, or clinical utility.",
        ],
    }
    result_path.write_text(json.dumps(native(result), indent=2) + "\n")
    print(json.dumps(native(result), indent=2))


if __name__ == "__main__":
    main()
