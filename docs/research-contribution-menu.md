# Contribution menu for research groups

Everything listed below is evidenced by code or documentation in this repository.

| Contribution | Evidence in Colvera v0.1 |
|---|---|
| Dataset provenance and audit | Checksum-verified downloader, schema audit, duplicate/missingness/class-balance report |
| Leakage-safe split design | Unique-ID checks; patient-level development/holdout split; test assertions |
| Baseline reproduction | Structured, radiomics, and fused regularized logistic pipelines with saved parameters and outputs |
| Evaluation and calibration review | AUROC, precision-recall, sensitivity, specificity, false-negative rate, Brier score, bootstrap intervals, ROC/PR/calibration figures |
| Error analysis tooling | Saved held-out predictions and a case browser that exposes errors rather than hiding them |
| Retrieval experiments | Development-only nearest-neighbor retrieval with explicit no-holdout-neighbor guarantee |
| Visualization / research UI | Lightweight Streamlit interface linked only to real saved artifacts and limitations |
| Literature and dataset synthesis | Candidate scorecard, evidence links, clinical definition, and data-requirements documents |
| Prototype development | Synthetic surveillance prototype review plus constrained real-data MMP design |

## What we will not claim yet

We will not claim to have a clinically validated model, an image-processing pipeline for raw pelvic MRI, longitudinal local-regrowth detection, a validated multimodal fusion method, hospital deployment capability, or an FDA-ready product.

## Strongest initial offers

1. Reproduce and strengthen a group's retrospective baseline with auditable patient-level splits and metrics beyond accuracy.
2. Clean and profile a permitted longitudinal surveillance dataset: patient IDs, dates, modality availability, missingness, and label maturity.
3. Build an internal researcher-facing case/retrieval/error-analysis interface around a group's approved experimental outputs.
