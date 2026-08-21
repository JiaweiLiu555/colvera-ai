"""Separate research surface for the saved v0.1/v0.2 Colvera artifacts.

The product demo deliberately does not surface exploratory research outputs in
the clinical-style workflow.  This module keeps those saved artifacts available
without conflating them with the synthetic surveillance experience.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st


def render_research_archive(root: Path) -> None:
    """Render the existing evidence-bound v0.1/v0.2 research materials."""
    metrics = root / "outputs" / "metrics"
    figures = root / "outputs" / "figures"
    required = ["results.json", "dataset_audit.json", "held_out_predictions.csv", "held_out_neighbors.csv", "held_out_case_features.csv"]
    st.markdown("<div class='archive-kicker'>RESEARCH ARCHIVE</div>", unsafe_allow_html=True)
    st.title("Exploratory research artifacts")
    st.markdown(
        "<div class='archive-notice'><span><strong>Research use only.</strong> These saved public-data experiments are not a clinical validation of the Colvera product demo, not a diagnostic device, and not for patient care.</span></div>",
        unsafe_allow_html=True,
    )
    if not all((metrics / name).exists() for name in required):
        st.info("Saved v0.1 artifacts are unavailable in this checkout. See the repository research documentation.")
        return

    results = json.loads((metrics / "results.json").read_text())
    audit = json.loads((metrics / "dataset_audit.json").read_text())
    predictions = pd.read_csv(metrics / "held_out_predictions.csv")
    neighbors = pd.read_csv(metrics / "held_out_neighbors.csv")
    cases = pd.read_csv(metrics / "held_out_case_features.csv")
    fusion_result = next(item for item in results["models"] if item["model"] == "fusion")
    clinical_result = next(item for item in results["models"] if item["model"] == "clinical")

    st.subheader("v0.1 — pretreatment response research")
    st.caption(
        "An enabling, patient-level-split experiment in locally advanced rectal cancer. It studies nCRT response—not "
        "watch-and-wait surveillance, serial exams, or local-regrowth risk."
    )
    cols = st.columns(4)
    cols[0].metric("Released patients", audit["patient_rows"])
    cols[1].metric("Development / holdout", f"{audit['train_patients']} / {audit['test_patients']}")
    cols[2].metric("Inputs", "Structured + MRI radiomics")
    cols[3].metric("Saved model", results["model_version"])
    st.caption(
        "Zenodo 8379940, CC-BY-4.0. The release has one de-identified row per patient; it has no raw MRI, endoscopy, "
        "serial surveillance exams, local-regrowth label, or scanner/site metadata."
    )

    case_ids = sorted(cases.patient_id.astype(int).tolist())
    selected_id = st.selectbox("Held-out research case ID", case_ids, key="archive_case")
    case = cases.loc[cases.patient_id == selected_id].iloc[0]
    prediction = predictions.loc[(predictions.patient_id == selected_id) & (predictions.model == "fusion")].iloc[0]
    left, middle, right = st.columns([1.0, 1.1, 1.5])
    with left:
        st.markdown("#### Case context")
        st.write(f"**Research case:** {selected_id}")
        st.write("Pretreatment nCRT-response cohort")
        st.write("Timeline and surveillance evidence unavailable")
    with middle:
        st.markdown("#### Released features")
        st.dataframe(
            pd.DataFrame(
                {
                    "normalized feature": ["Mucinous differentiation", "MRI EMVI", "Absolute basophils", "Circumferential growth", "N stage"],
                    "value": [case.mucinous, case.emvi, case.basophils, case.circumferential_growth, case.n_stage],
                }
            ),
            hide_index=True,
            width="stretch",
        )
    with right:
        st.markdown("#### Saved exploratory output")
        label = "non-responder" if prediction.predicted_outcome else "responder"
        st.info(f"Exploratory fused-model label: **{label}**")
        st.write("No individual probability is shown; calibration is inadequate for case-level interpretation.")

    st.markdown("#### Comparable historical research cases")
    st.caption("Neighbors are restricted to the development set; similarity is mathematical, not clinical equivalence.")
    case_neighbors = neighbors.loc[neighbors.query_patient_id == selected_id].copy()
    case_neighbors["historical_outcome"] = case_neighbors.historical_outcome_binary.map({0: "responder", 1: "non-responder"})
    st.dataframe(
        case_neighbors.rename(columns={"neighbor_patient_id": "historical case", "euclidean_distance": "feature-space distance"})[
            ["rank", "historical case", "feature-space distance", "historical_outcome"]
        ],
        hide_index=True,
        width="stretch",
    )
    rows = [
        {
            "model": item["model"],
            "held-out AUROC": item["metrics"]["auroc"],
            "sensitivity": item["metrics"]["sensitivity"],
            "specificity": item["metrics"]["specificity"],
            "false-negative rate": item["metrics"]["false_negative_rate"],
        }
        for item in results["models"]
    ]
    st.markdown("#### Held-out experiment")
    st.dataframe(pd.DataFrame(rows).round(3), hide_index=True, width="stretch")
    st.error(
        f"The fused model AUROC was {fusion_result['metrics']['auroc']:.3f}, below the structured baseline's "
        f"{clinical_result['metrics']['auroc']:.3f} on a 15-patient holdout. This does not support a fusion-improvement claim."
    )
    figures_columns = st.columns(3)
    for column, filename, caption in zip(
        figures_columns,
        ["model_comparison.png", "roc.png", "calibration.png"],
        ["Held-out model comparison", "Held-out ROC curves", "Exploratory calibration view"],
    ):
        with column:
            st.image(str(figures / filename), caption=caption)

    st.divider()
    st.subheader("v0.2 — released-weight reproduction audit")
    v02_audit_path = root / "outputs" / "v02" / "data-audit" / "audit.json"
    v02_results_path = root / "outputs" / "v02" / "final-test" / "final_results.json"
    if not v02_audit_path.exists() or not v02_results_path.exists():
        st.info("v0.2 artifacts have not been generated in this checkout. See `docs/v02-data-availability.md`.")
        return
    v02_audit = json.loads(v02_audit_path.read_text())
    v02_results = json.loads(v02_results_path.read_text())
    st.error(
        "This public release has no patient IDs, augmentation lineage, or named image channels. It reports a released-weight "
        "inference audit only—not patient-level validation, a clinical result, or evidence that either model reproduces the paper."
    )
    cols = st.columns(4)
    cols[0].metric("Paper cohort", "700 patients")
    cols[1].metric("Released dev arrays", f"{v02_audit['release_development_total_records']} records")
    cols[2].metric("Released locked test", f"{v02_results['test_records']} records")
    cols[3].metric("Verified patient IDs", "0")
