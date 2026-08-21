# v0.2 model evaluation plan and execution record

## Required metrics

For a valid future patient-level study, Colvera will report AUROC, average precision, sensitivity, specificity, PPV, NPV, false-negative rate, calibration slope/intercept, Brier score, reliability curve, confidence intervals, subgroup performance, and external validation. Accuracy alone is insufficient.

## What v0.2 actually evaluated

The locked released-weight check reported AUROC, average precision, Brier score, sensitivity/specificity/PPV/NPV/FNR at a **descriptive** 0.50 softmax threshold, nonparametric 2,000-resample CIs, a descriptive calibration curve/slope/intercept/ECE, and abstention coverage based on `|p−0.5|≤0.10`.

No calibration model, threshold, or abstention rule was fitted from these metrics. The reported check fails the minimum condition for clinical interpretation because neither channel identity nor patient-level data are verified.

## Split and leakage rules

- The original paper reports a chronological 500/200 patient split.
- The release has 323 unnamed development records and 200 unnamed test records.
- `data/v02/patient_manifest.csv` deliberately records `not available in release` for every patient ID; the test suite refuses to treat that as a patient-level CV-enabling manifest.
- Exact duplicate full records were checked across release files. That cannot rule out augmented/near-duplicate or same-patient leakage.
- The final outputs were locked before evaluation. A pre-output bootstrap failure was repaired only to emit a null interval for undefined precision; no candidate or inference choice changed.

## Required sanity tests

Completed in v0.2: deterministic duplicate-input output, finite probabilities, softmax sum-to-one, random-noise finite output, release shape/one-hot label check, and exact duplicate record scan. Not applicable/blocked: 10-sample overfit, shuffled-label chance check, patient-level split overlap test, patient-level CV, and retrieval evaluation—because training a model from anonymous potentially augmented records would be invalid.
