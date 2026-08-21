# Model card — Colvera v0.2 released-weight audit

## Identification

- **Version:** `colvera-pretreatment-response-v0.2`
- **Artifact type:** research-only reconstruction and evaluation harness for two externally released HDF5 models.
- **Task intended by source:** pretreatment prediction of pathological good response (`ypT0–1 AND ypN0`) to neoadjuvant chemoradiotherapy in locally advanced rectal cancer.
- **Not the task:** cancer diagnosis, local-regrowth detection, watch-and-wait surveillance, risk scoring, triage, treatment selection, or use on patient uploads.

## Inputs and outputs

| Item | Available / used | Boundary |
|---|---|---|
| Preprocessed image arrays | Four unnamed channels of 16×128×128 | Channel identities are not source-confirmed |
| ADC HDF5 model | `weights_ADC.hdf5`, channel 0 fixed provisionally | Mapping unverified |
| T2 HDF5 model | `weights_T2.hdf5`, channel 3 fixed provisionally | Mapping unverified |
| Clinical variables | Not released | No clinical model |
| Patient IDs / dates / scanner linkage | Not released | No patient-level split or longitudinal analysis |
| Output | Saved research probabilities and aggregate metrics | Never an individual clinical prediction |

## Training and validation status

Colvera did not train, tune, calibrate, fuse, or select a model in v0.2. The public development records cannot be verified as independent patients. Both HDF5 networks were released by the paper authors; Colvera only reconstructed their inference graph. The one locked test check is a release-integrity exercise, not independent validation.

## Performance

With unverified fixed mapping class 0 as provisional GR, the released-weight checks gave AUROC 0.500 (ADC candidate) and 0.498 (T2 candidate) on 200 release test records. These do not reproduce the published results and must not be used to estimate future performance. Full metrics and confidence intervals are in `outputs/v02/final-test/final_results.json`.

## Safety and fairness

- Single-centre retrospective source; no external validation.
- No per-record demographic, scanner, site, or date fields: no subgroup/fairness analysis is possible.
- Original image quality exclusions may conceal real-world failure conditions.
- No calibration fit or acceptable calibration has been established; descriptive ECE is poor in the mapping-dependent check.
- The UI exposes only aggregate release evidence. It deliberately does not show a case browser, raw images, patient-like identifiers, multimodal fusion, or retrieval output.

## Intended next validation

Obtain author-confirmed channel/label mappings and a patient-level, temporally split cohort with original-image/ROI provenance. Freeze the preprocessing and a 10-case numerical fixture, then run patient-level CV on development data and one external final test. Compare image-only, clinical-only, and late-fusion models; select calibration/threshold/abstention on validation only; and report subgroup and external performance.
