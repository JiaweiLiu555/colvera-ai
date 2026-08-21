# Colvera v0.2 research report

## Executive summary

Colvera v0.2 audited and reconstructed the publicly released MRI models associated with Zhu et al.'s 2020 LARC neoadjuvant-therapy response paper. The work found that the public repository contains test arrays and pretrained HDF5 weights, but lacks the patient-level and modality metadata needed for a defensible new model-development study. A predeclared, locked inference check under a provisional channel mapping produced near-chance AUROCs (0.500 and 0.498), so it does not reproduce the publication's reported results and does not create a clinical model.

This negative result is useful: it identifies the exact reproducibility artifacts required before building a new multimodal or longitudinal Colvera system. The current direction remains hospital-facing evidence synthesis for rectal-cancer pathways; this v0.2 work is a narrow enabling audit of **pretreatment pathological response**, not a claim to predict local regrowth.

## Source and study target

The paper retrospectively enrolled 700 locally advanced rectal cancer patients at Beijing Cancer Hospital, chronologically split into 500 development and 200 test patients. It defined good response as `ypT0–1 AND ypN0` after nCRT and surgery, used pathology as ground truth, and reported `DL_ADC` test AUROC 0.851 and `DL_T2` test AUROC 0.721. See [the original paper](https://doi.org/10.3389/fonc.2020.574337) and [official release](https://github.com/radiologypkucancer/rectal_MR_DL).

## Data reality

The official release (commit `507c357359aff085f5d9853d2f3c51d0c61d8dde`) has 200 training, 123 validation, and 200 test arrays shaped `N×4×16×128×128`; one-hot test target counts are 60/140. It has pretrained `weights_ADC.hdf5` and `weights_T2.hdf5`. It does not contain a README/license, a patient manifest, channel names, sample/augmentation lineage, original-image linkage, clinical fields, or per-record scanner/date data.

The 323 development records cannot be equated with the paper's 500 patients. They cannot be used to produce a patient-level model, five-fold CV result, calibrated risk, fusion result, or retrieval result. Audit hashes, row-level release-record inventory, shape/missingness checks, and duplicate checks are preserved in `data/v02/` and `outputs/v02/data-audit/`.

## Method

The HDF5 architecture and tensors were inspected directly. A PyTorch implementation reconstructs the saved single-input channels-first network, imports convolution, batch-normalization, and dense weights, and runs deterministic inference. Development-only mechanical checks passed. Before test metrics were read, `docs/v02-final-model-lock.md` fixed the weight files, channel assumptions, class convention, CPU inference, and descriptive 0.50 threshold.

Two fixed audits were run once on the 200-record test array:

- `published_adc_reproduction`: ADC weight file with channel 0;
- `published_t2_reproduction`: T2 weight file with channel 3.

Both channel choices are provisional, not source-verified. A test class-0 convention as GR is likewise provisional because its 60/200 prevalence matches the paper's reported GR prevalence.

## Results

| Audit | AUROC (95% bootstrap CI) | Average precision | Brier | Interpretation |
|---|---:|---:|---:|---|
| ADC released weights, provisional channel 0 | 0.500 (0.500–0.500) | 0.300 | 0.300 | Effectively constant low GR output |
| T2 released weights, provisional channel 3 | 0.498 (0.440–0.552) | 0.298 | 0.644 | Near-constant high GR output |

The released-weight check does not beat, match, or meaningfully compare with the paper. The test result is a release-compatibility finding only, not a performance result for Colvera, the source authors, or a real patient population.

## Contribution

Colvera v0.2 contributes a reproducibility harness rather than an inflated model claim:

- immutable source/data hashes and a release-record manifest;
- direct inspection of an obsolete Keras model and a modern inference reconstruction;
- a test lock that prevents test-driven channel/model/threshold selection;
- transparent failed/indeterminate reproduction reporting;
- an MMP that preserves v0.1 and adds v0.2 without portraying anonymous arrays as patient cases.

## Next experiment

The single most valuable next experiment is an author-verified **10-case parity fixture**: channel names, preprocessed inputs, class order, and expected ADC/T2 outputs from the original environment. If parity succeeds, obtain a patient/augmentation manifest for the full 500-patient development cohort, freeze a patient-level temporal split, and reproduce `DL_ADC` before attempting any modern ADC, T2, fusion, calibration, abstention, or retrieval extension.
