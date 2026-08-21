# v0.2 dataset audit

This is the human-readable companion to `outputs/v02/data-audit/audit.json` and `data/v02/patient_manifest.csv`.

## Provenance and immutability

- **Repository:** [radiologypkucancer/rectal_MR_DL](https://github.com/radiologypkucancer/rectal_MR_DL)
- **Commit audited:** `507c357359aff085f5d9853d2f3c51d0c61d8dde`
- **Raw location:** `data/v02/raw/rectal_MR_DL/` (not edited by Colvera)
- **Audit outputs:** `outputs/v02/data-audit/`
- **File identity:** SHA-256 for every material release file is saved in the audit JSON and the test lock.

## Release schema

All three image NPZ files have one array key, `arr_0`, and shape `N × 4 × 16 × 128 × 128` (`float32`). Their target NPZ files have one `N × 2` one-hot array (`float64`). There is no embedded patient ID, study ID, modality label, class-name label, date, scanner field, or metadata table.

| Split | Image shape | One-hot target shape | Exact full-record duplicates |
|---|---|---|---:|
| training | 200 × 4 × 16 × 128 × 128 | 200 × 2 | 0 |
| validation | 123 × 4 × 16 × 128 × 128 | 123 × 2 | 0 |
| test | 200 × 4 × 16 × 128 × 128 | 200 × 2 | 0 |

All released values are finite. Exact record hashes cannot identify near-duplicate augmentations, repeated patients, shared source images, or pre-processing leakage; patient-level separation remains unknowable.

## Paper-versus-release reconciliation

The paper reports 500 train and 200 chronological test patients. The test file has 200 records and class indices 60/140, compatible with the paper's test prevalence. The public development files have 323 records with class indices 149/174 combined, not the paper's 116/384 patient counts. No inference that 323 represents 323 independent patients is allowed.

The paper describes ADC/T2 processing to 64×64×16 patches. The public arrays are 4×16×128×128. The repository includes `weights_ADC.hdf5` and `weights_T2.hdf5` but does not document the correspondence between the four axes and those models.

## Feasibility conclusion

Patient-level split: unavailable. Biopsy/pathology linkage per record: unavailable. Clinical-field model: unavailable. Multimodal pairing/fusion: unsupported. Dataset license: not stated in the cloned repo. The only defensible action on the released data is a clearly caveated released-weight compatibility audit.
