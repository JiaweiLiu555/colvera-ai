# v0.2 research question and registered scope

## Question

Can the released `good_response` ADC/T2 HDF5 models from Zhu et al. be reconstructed for deterministic inference on the official 200-record chronological test array, while transparently documenting whether the public files support a patient-level reproduction?

This is a reproduction-audit question, not a clinical model-development claim. The target is **pretreatment prediction of pathological good response to NCRT** in LARC, not watch-and-wait local regrowth, surveillance, diagnosis, or treatment selection.

## Outcome and unit of analysis

The paper defines a good responder as `ypT0–1 AND ypN0`, determined from pathology after NCRT and total mesorectal excision. The released test label index with prevalence 60/200 is treated as the provisional GR class only because it matches the reported paper prevalence. The NPZ does not attach per-record pathology labels or a class-name metadata field, so this semantic mapping requires author confirmation.

The public release's unit is an **array record**, not a verified patient. No patient IDs, scan dates, or augmentation lineage are available. A patient-level split, five-fold patient CV, patient-level confidence interval, or patient-retrieval evaluation cannot be truthfully performed.

## Preprocessing and source architecture

The HDF5 model configuration specifies a single input of `16 × 128 × 128`, channels first. The reconstructed inference graph retains five Conv2D → batch-normalization → max-pooling branches concatenated with centre crops, followed by a `4 × 4` convolution and dense layers. Saved Keras weights are loaded tensor-for-tensor into the PyTorch inference graph.

The public arrays contain four unnamed `16 × 128 × 128` channels per record. `weights_ADC.hdf5` and `weights_T2.hdf5` name the intended modalities, but the release does not name the corresponding array axes. The v0.2 check freezes a provisional source-informed mapping (`ADC = channel 0`, `T2 = channel 3`) solely to make a single reproducible audit possible; it is not an independently verified modality mapping and cannot justify a performance claim against the paper.

## Predeclared analysis

1. Audit files, byte hashes, shapes, one-hot labels, record counts, exact duplicates, and missing metadata before inference.
2. Confirm released HDF5 graph import on development inputs only: deterministic output, finite probabilities, duplicate-input consistency, and random-noise finite-probability sanity check.
3. Freeze the model, source-file checksums, provisional channel mapping, positive-class convention, and descriptive threshold before reading final test performance.
4. Run one saved evaluation on the official test array. Report AUROC, average precision, Brier score, descriptive sensitivity/specificity at softmax `p(GR) >= 0.5`, bootstrap intervals, reliability plot, and abstention coverage. No test-driven adjustment is allowed.
5. Do not fit a calibration map, fusion model, clinical model, retrieval model, or new trainable deep model with this release. A 323-record unnamed development collection is not a known 500-patient cohort.

## What would make the next experiment valid

An author-approved release or institutional dataset must provide stable patient IDs; per-study date; source/augmentation linkage; an explicit ADC/T2 map; pathology outcome mapping; original image/ROI lineage; temporal split; and a separate external test site. Only then can Colvera run patient-level CV, calibration selection, multimodal fusion, retrieval, abstention evaluation, and subgroup/external validation.
