# Dataset report — Zenodo 8379940

## Provenance and access

- **Dataset:** *MRI Radiomics data of LARC patients who responded well and poorly to nCRT*.
- **Record / DOI:** [Zenodo 8379940](https://zenodo.org/records/8379940), [10.5281/zenodo.8379940](https://doi.org/10.5281/zenodo.8379940).
- **Associated paper:** Marinkovic et al., *Journal of Clinical Medicine* 2024;13:421, [PMCID: PMC10816962](https://pmc.ncbi.nlm.nih.gov/articles/PMC10816962/).
- **Institution:** Institute for Oncology and Radiology of Serbia and collaborators, as listed in the paper.
- **License / access:** CC-BY-4.0; open download with no account required.
- **Downloaded file:** `MRI RADIOMICS-rectal carcinoma data repository-nCRT - 71-patients.xlsx`.
- **Published MD5:** `c7596871db016ad9ffb729cfd2687f93`; verified during download.

## What was actually audited

| Item | Verified finding |
|---|---|
| Patient rows | 71 non-empty rows |
| Patient identifiers | 71 unique integer IDs; no duplicates |
| Released studies | One tabular row per patient; individual studies and DICOM series are not released |
| Class balance | 32 responders, 39 non-responders |
| Ordinal label distribution | cCR/TRG1: 23; TRG2: 9; TRG3: 29; TRG4: 10 |
| Structured inputs | 5 normalized clinicopathological/MRI variables |
| Radiomics inputs | 2,144 normalized pretreatment MRI radiomics features |
| Retained-model missingness | 0 missing cells |
| Blank workbook columns | 4 all-empty separator/unnamed columns, excluded before modeling |
| Zero-variance radiomics | 5, removed inside the pipeline |
| Raw MRI / device metadata | Not released |
| Longitudinal tracking | Not available; no repeated visits per patient in the table |
| Endoscopy / DRE / CEA | Not available |
| Local-regrowth label / timing | Not available |
| Demographics / sites | Not available in the workbook |

### Cohort-count discrepancy

The associated publication's cohort table reports 75 patients, whereas the Zenodo workbook described by the record and audited by Colvera contains 71 non-empty patient rows. Colvera v0.1 uses **71** everywhere because that is the released, reproducibly downloadable table. The discrepancy has not been resolved from the public materials and should be clarified with the source authors before any publication or clinical interpretation.

## Label and clinical meaning

The published work describes a continuous response ordering of cCR, TRG1, TRG2, TRG3, and TRG4. For its binary ROC analyses, it grouped cCR/TRG1/TRG2 as responders and TRG3/TRG4 as non-responders. Colvera v0.1 uses that released binary label without changing it.

This is **not** a local-regrowth outcome and not a direct test of watch-and-wait surveillance. cCR may be clinically relevant to eventual organ preservation, but cCR, pathological response, residual disease, and later local regrowth remain distinct concepts.

## Data quality and bias assessment

### Strengths

- Real, patient-level, rectal-cancer-specific data.
- Explicit de-identified patient IDs make a patient-level split possible.
- Open source, stable DOI, published checksum, and CC-BY-4.0 license make it immediately reproducible.
- Both structured and MRI-derived feature blocks enable a limited multimodal experiment.

### Major limitations

- Only 71 patients from a source cohort; no independent site is released.
- Precomputed radiomics prevent auditing segmentation, image quality, sequence variation, scanner differences, or extraction reproducibility.
- Features are already normalized across the released dataset. Original values and source-only preprocessing parameters are absent, so source-level preprocessing leakage cannot be fully ruled out.
- The release presents only five structured variables described as significantly associated with outcome, which can favor a structured baseline.
- No demographic fields permit equity, age, sex, or site-stratified assessment.
- No serial data permit a longitudinal comparison.

## Split and leakage controls implemented by Colvera

- Fixed, stratified, patient-level split: 56 development patients and 15 held-out patients; seed `20260815`.
- Unique patient ID and no train/test overlap are asserted before modeling.
- IDs and both outcome columns are excluded from feature matrices.
- Variance filtering, scaling, and feature selection are inside scikit-learn pipelines and fit only within development folds.
- Historical-case retrieval searches only the 56 development patients; a holdout patient cannot retrieve itself or another holdout patient.

These controls prevent **our model-pipeline leakage**. They cannot repair information potentially introduced before the public feature table was released.
