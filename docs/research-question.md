# Research question — Colvera v0.1

## Frozen study sentence

We will use the open Zenodo 8379940 dataset containing **71 unique patients** with five supplied clinicopathological/MRI variables and **2,144 pretreatment T2-weighted MRI radiomics features** to predict **binary nCRT non-response (TRG3/4) versus response (cCR/TRG1/TRG2)**, comparing a structured-variable logistic-regression baseline, a radiomics-only regularized logistic-regression baseline, and a fused structured-plus-radiomics model with development-set historical-case retrieval, using a patient-level 56/15 development/held-out split and AUROC, average precision, sensitivity, specificity, false-negative rate, Brier score, and bootstrap intervals.

## Exact cohort

- **Source:** Radulovic, Marinkovic, and Cavic, Zenodo record 8379940, DOI [10.5281/zenodo.8379940](https://zenodo.org/records/8379940), CC-BY-4.0.
- **Included:** every released row with a non-null de-identified patient ID and binary outcome: 71 unique patients.
- **Excluded:** four blank trailing workbook rows. No patient row with retained model features is missing a value.
- **Not inferable from the release:** age, sex, institution/site, scanner/vendor, raw MRI, segmentation, treatment schedule, follow-up time, endoscopy, DRE, CEA, and local-regrowth status.

## Prediction framing

- **Prediction time:** pretreatment, using the released pretreatment MRI-derived radiomics and supplied structured features.
- **Input:** five normalized supplied clinicopathological/MRI features and/or 2,144 normalized radiomics features. Patient IDs and outcome columns are excluded from every model input.
- **Primary label:** `1 = non-responder (TRG3 or TRG4)` and `0 = responder (cCR, TRG1, or TRG2)`, exactly as released.
- **Clinical boundary:** treatment response is not local regrowth. This is an enabling imaging/structured-data experiment for Colvera, not a watch-and-wait surveillance model.

## Models

1. **Structured baseline:** standardized logistic regression on the five released structured features.
2. **Radiomics baseline:** fold-internal variance filter, standardization, univariate feature selection, and L1 logistic regression on 2,144 radiomics features.
3. **Colvera-inspired fusion:** the same fold-internal procedure on all structured and radiomics features, plus a separate development-set nearest-neighbor retrieval view.

Hyperparameters are chosen only within a three-fold stratified development-set cross-validation. The one held-out split is never used in tuning.

## Endpoints and reporting

- **Primary:** held-out AUROC.
- **Secondary:** average precision, sensitivity, specificity, precision, NPV, F1, false-negative rate, Brier score, confusion matrix, and 2,000-resample nonparametric bootstrap intervals.
- **Exploratory:** qualitative historical-case retrieval constrained to development-set patients.

No subgroup or external-validation claim is possible from this release.

## Important source limitation

The release states that features are z-score normalized and explicitly calls the five structured variables “significantly associating with outcome.” The raw values, source-only normalization parameters, and preselection process are not released. Therefore source-level preprocessing or feature-selection leakage cannot be fully excluded. The experiment is reproducible and model-selection leakage is prevented inside the code, but all performance estimates remain exploratory.
