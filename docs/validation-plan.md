# Validation plan

## Baselines

### v0.1, implemented

1. Five released structured clinicopathological/MRI variables only.
2. Pretreatment MRI-derived radiomics only.
3. Early fusion of those released feature blocks.
4. Descriptive historical-case retrieval restricted to the development set.

### Future surveillance study, not implemented

1. MRI only.
2. Endoscopy only.
3. Clinical-only.
4. Simple fusion.
5. Explicit disagreement-aware multimodal model.

## v0.1 evaluation

- fixed patient-level development/held-out split;
- development-only three-fold hyperparameter selection;
- AUROC, average precision, sensitivity, specificity, precision, NPV, F1, false-negative rate, Brier score, confusion matrix, and bootstrap intervals;
- inspection of all saved holdout errors;
- no clinical threshold or case-level probability display.

## Required evaluation for a future surveillance study

- patient-level development, validation, and held-out test sets;
- sensitivity, false-negative rate, specificity, precision-recall, and AUROC;
- calibration and confidence intervals;
- performance when MRI and endoscopy disagree;
- subgroup analysis;
- missing-modality and abstention analysis;
- external-site validation before any prospective clinical study.

No clinical study should begin until the retrospective protocol, ground truth, safety thresholds, and oversight pathway are defined with institutional partners.
