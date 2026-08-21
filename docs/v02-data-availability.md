# v0.2 data availability: Zhu et al. pretreatment response release

## Bottom line

The official public repository was cloned read-only at commit `507c357359aff085f5d9853d2f3c51d0c61d8dde` into `data/v02/raw/rectal_MR_DL`. It contains processed four-channel image arrays, one-hot labels, and pretrained ADC/T2 Keras HDF5 weights for the `good_response` task. It does **not** contain a patient manifest, original DICOM/NIfTI study linkage for this task, clinical covariates, per-record scanner/date metadata, a named channel-to-modality map, ROI provenance, or a license file.

The source paper is [Zhu et al., *Frontiers in Oncology*, 2020](https://doi.org/10.3389/fonc.2020.574337); the code/data release is [radiologypkucancer/rectal_MR_DL](https://github.com/radiologypkucancer/rectal_MR_DL).

## What the paper reports

| Property | Paper |
|---|---:|
| Study population | 700 LARC participants, one institution |
| Chronological development group | 500 participants, Dec 2009–Mar 2015 |
| Chronological test group | 200 participants, Mar 2015–Jul 2016 |
| Primary endpoint | Good response = ypT0–1 **and** ypN0 after NCRT/TME pathology |
| Development outcome counts | 116 GR / 384 non-GR |
| Test outcome counts | 60 GR / 140 non-GR |
| Imaging | Pretreatment ADC and T2-weighted MRI; 1.5T and 3T |
| Reference/labels | Surgical pathology reviewed by two pathologists in consensus |

The paper says its processed data and trained networks are available in the official repository. Its methods describe manual radiologist ROI delineation, cropping, zero-padding to 64 × 64 × 16, and training-only augmentation. The public NPZ release instead has arrays of shape `N × 4 × 16 × 128 × 128`; this mismatch is documented rather than reconciled by assumption.

## What was actually released and audited

| Release array | Records | Class index 0 | Class index 1 | Patient IDs / augmentation lineage |
|---|---:|---:|---:|---|
| `training_*_00001.npz` | 200 | 97 | 103 | Not released |
| `validation_*_00064.npz` | 123 | 52 | 71 | Not released |
| `test_*_00001.npz` | 200 | 60 | 140 | Not released |

The 200 test records and 60/140 label-index prevalence agree numerically with the paper's test cohort. The 323 released development records do **not** establish that the complete 500-patient development cohort, individual patient rows, or augmentation lineage are present. The development class proportions also differ markedly from the paper's 116/384 patient counts.

`data/v02/patient_manifest.csv` is therefore a **release-record manifest**, not a patient manifest: every unavailable field is explicitly marked `not available in release`. It includes a SHA-256 digest per array record and a split label, but it must never be interpreted as a longitudinal patient table.

## Data quality, diversity, access, and bias

- All released array values are finite; no exact duplicate full four-channel records were found across the three array files.
- This does not eliminate patient leakage: without patient IDs or augmentation lineage, near-duplicate augmented views and repeated patients cannot be detected.
- Per-record age, sex, ethnicity, comorbidities, scanner vendor/field strength, scan date, site, and image-quality score are not released. The paper reports 221 1.5T and 479 3T scans, but not their per-record release linkage.
- The paper is a single-centre retrospective dataset from Beijing Cancer Hospital. Participants with inadequate image quality/noise were excluded, so failure modes from a routine population are not represented.
- The four array channels have no source-supplied modality names. A numeric range cannot prove whether a channel is ADC or T2.
- Access is public GitHub, but no explicit `LICENSE` file is in the cloned repository. Public availability is not a blanket reuse license; contact the authors before redistribution, commercial use, or any clinical translation.

## Suitability decision

This release is suitable for a narrow, transparent **released-weight inference audit**. It is not suitable for a new patient-level five-fold model-selection study, a defensible novel train/validation/test result, subgroup analysis, calibration fitting, multimodal fusion, clinical-field modeling, or a patient-retrieval claim. All raw files remain outside version control under `data/v02/raw/`; hashes and audit outputs are under `outputs/v02/data-audit/`.
