# Colvera v0.1 research report

## Abstract

We built a reproducible, research-only baseline study using an open dataset of 71 patients with locally advanced rectal cancer, five released structured clinicopathological/MRI variables, 2,144 pretreatment MRI radiomics features, and nCRT response labels. We compared structured-only, radiomics-only, and early-fusion regularized logistic-regression models on a fixed patient-level 56/15 development/held-out split. The fused model did not outperform the structured baseline on the holdout (AUROC 0.679 vs 0.714). The result is exploratory because of the small, single-source cohort and source-level preprocessing limitations. We therefore present v0.1 as an enabling response-prediction and research-interface project, not a validated local-regrowth model.

## Problem

Colvera aims to support review of rectal-cancer watch-and-wait surveillance by making longitudinal, multimodal, and comparative evidence explicit. No usable public dataset located in this search provided serial MRI, endoscopy, and confirmed local-regrowth outcomes together. The first question is therefore narrower: can the released pretreatment feature blocks support a reproducible response-prediction comparison?

## Dataset and cohort

The source is [Zenodo 8379940](https://zenodo.org/records/8379940), associated with Marinkovic et al. 2024. We audited 71 unique patient rows: 32 responders (cCR/TRG1/TRG2) and 39 non-responders (TRG3/TRG4). The release has no retained-input missing values, raw MRI, serial visits, endoscopy, demographic/site fields, or local-regrowth outcome.

## Methods

The held-out test set contains 15 patients selected with a fixed stratified patient-level split (seed `20260815`); 56 patients form the development set. We tuned logistic regression hyperparameters with three-fold stratified development-only cross-validation. All variance filtering, scaling, and univariate selection are inside pipelines. The comparative component retrieves three nearest cases only from development-set patients using the fusion representation.

## Baselines and Colvera contribution

- **Structured baseline:** five released normalized variables.
- **Radiomics baseline:** 2,144 pretreatment MRI radiomics features.
- **Fused experiment:** both feature blocks with fold-internal feature selection.
- **Comparative view:** development-set nearest historical cases shown descriptively, never as a diagnosis or probability.

## Held-out results

| Model | AUROC | Average precision | Sensitivity | Specificity | False-negative rate | Brier score |
|---|---:|---:|---:|---:|---:|---:|
| Structured baseline | 0.714 | 0.784 | 0.750 | 0.571 | 0.250 | 0.249 |
| Radiomics only | 0.446 | 0.528 | 0.375 | 0.571 | 0.625 | 0.297 |
| Fused model | 0.679 | 0.803 | 0.500 | 0.714 | 0.500 | 0.234 |

The fused model's AUROC bootstrap 95% interval was 0.352–0.946. Such wide intervals are expected from a 15-patient test set and make rank-order conclusions unstable.

## Error analysis

The fused model had 4 false negatives and 2 false positives at the prespecified 0.5 threshold. Radiomics-only performance was particularly poor, with 5 false negatives. The app exposes every held-out research case and its held-out prediction, so errors are inspectable rather than hidden. Image quality, site, scanner, demographics, and segmentations cannot be analyzed because the release does not include them.

## Interpretation

This experiment does not support the claim that adding this released radiomics block improves over the released structured baseline. That may reflect the small cohort, high-dimensional instability, preselected structured variables, no raw-image quality control, source-level preprocessing, or a genuinely unhelpful representation. It cannot distinguish these explanations.

## Next experiment

Obtain a multicenter, patient-level surveillance cohort with dated serial pelvic MRI, endoscopy, DRE/CEA where available, explicit modality quality/missingness, and temporally confirmed local-regrowth outcomes. Predefine a current-only versus current-plus-previous MRI comparison, hold out patients and institutions, and assess whether longitudinal change improves sensitivity at acceptable false-alert burden.
