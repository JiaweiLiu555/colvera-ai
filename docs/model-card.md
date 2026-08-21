# Model card — `colvera-mri-clinical-v0.1`

## Intended research use

Explore whether pretreatment, released structured/MRI-derived radiomics features can distinguish the dataset-defined nCRT response groups. It is a reproducible research artifact and case-browser backend, not a clinical model.

## Not intended for

- local-regrowth detection;
- watch-and-wait surveillance decisions;
- diagnosis, prognosis, treatment selection, or triage;
- use with any individual patient;
- image interpretation, because no raw image model is present;
- claims of generalization beyond this small source cohort.

## Inputs and target

- 5 released normalized clinicopathological/MRI variables;
- 2,144 released normalized pretreatment MRI radiomics features;
- target: released binary non-response label, TRG3/4 versus cCR/TRG1/TRG2.

No patient ID, ordinal label, binary label, pathology after the prediction point, or future visit is sent into a model input.

## Method

The fused model applies, within development folds only: variance thresholding, standardization, univariate feature selection, and L1-regularized logistic regression. Grid search uses 3-fold stratified development-only AUROC. The fixed held-out set contains 15 unique patients.

The comparative component retrieves three nearest development-set cases using the fused model's selected feature representation. It does not change the fused model prediction and must not be read as evidence of clinical equivalence.

## Held-out findings

See `outputs/metrics/results.json` for exact generated artifacts. The fixed v0.1 run found:

| Model | Held-out AUROC | Sensitivity | Specificity | False-negative rate | Brier score |
|---|---:|---:|---:|---:|---:|
| Structured baseline | 0.714 | 0.750 | 0.571 | 0.250 | 0.249 |
| Radiomics only | 0.446 | 0.375 | 0.571 | 0.625 | 0.297 |
| Fused model | 0.679 | 0.500 | 0.714 | 0.500 | 0.234 |

The fused model did not improve on the structured baseline. The fused AUROC bootstrap 95% interval was 0.352–0.946, illustrating the instability of a 15-patient holdout. No case-level probability is displayed in the app because calibration is inadequate for interpretation.

## Known limitations

- Source-level z-score normalization and structured-variable preselection cannot be audited or undone.
- Sample size, test size, and single-source design are inadequate for reliable estimates.
- No raw MRI, quality metadata, site/scanner fields, demographics, or external validation.
- No repeated examinations or local-regrowth labels.

## Versioning

The source, split seed, parameter search, feature list, predictions, neighbors, metrics, and artifacts are saved with each run under `outputs/metrics/`. A result must never be compared across versions without recording the dataset checksum and model version.
