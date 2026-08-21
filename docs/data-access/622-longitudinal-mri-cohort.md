# Data-access brief — 622-patient longitudinal multiparametric MRI cohort

## Who we are

Colvera is a student-led, mentor-advised, non-commercial medical-AI research project. We are building rigorous infrastructure for longitudinal, multimodal, comparative analysis in rectal cancer; it is research-use only and is not a clinical product.

## Research question

Does pairing a patient's pretreatment and post-treatment multiparametric MRI improve pCR prediction relative to a current/single-timepoint MRI model, and does adding time-aligned CEA add complementary signal?

## What we have already built

We have built a reproducibility and safety-first codebase: patient-level split controls, calibration/uncertainty tooling, training-only comparable-case retrieval interfaces, a transparent Streamlit research MMP, and a longitudinal manifest contract. We also documented why two prior public releases are not adequate for a valid longitudinal claim rather than overstating their results.

## Exact data requested

For the original 622-patient cohort, under an academic non-commercial agreement:

- stable de-identified patient IDs and visit IDs;
- pretreatment and post-treatment MRI, with explicit sequence mapping for T1, contrast T1, T2, and DWI/ADC as available;
- time offsets for each MRI and treatment milestone;
- CEA before/after treatment with units and missingness indicators;
- pCR ground-truth labels and label definition;
- original training, internal-validation, and external-validation cohort assignment;
- tumor annotations/segmentations and annotation provenance, if available;
- preprocessing specification, acquisition/site metadata permitted by the agreement, and an approved data dictionary.

## Exact experiment

We would preregister and compare, using the original development cohorts only for all choices:

1. current/single-timepoint MRI → pCR;
2. paired pre/post MRI → pCR;
3. paired MRI + CEA → pCR;
4. training-only embedding retrieval as an explanatory comparative analysis.

The final internal and external cohorts would remain locked. We would report AUROC/AUPRC, calibration, sensitivity, specificity, PPV/NPV, CIs, error review, subgroup feasibility, and abstention coverage—not accuracy alone.

## Privacy and contribution

We seek only de-identified research data; we will not redistribute images, publish case-level information, train commercial systems, or use data outside the approved agreement. In return, we can contribute a clean reproducibility audit, a patient-level temporal evaluation harness, documented baselines, transparent negative-result reporting, and reusable non-PHI code/analysis artifacts for the research group to review.

## Source / access route

The paper reports that original clinical/MRI data may be requested by academic affiliates for non-commercial research under a signed data-access agreement, through corresponding authors X. Wu and F. Gao. [Jin et al., *Nature Communications* 2021](https://doi.org/10.1038/s41467-021-22188-y). Deployment code is public at [3D RP-Net](https://github.com/Heng14/3D_RP-Net); it does not replace a data agreement.
