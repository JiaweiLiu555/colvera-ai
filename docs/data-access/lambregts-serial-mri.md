# Data-access brief — Lambregts serial-surveillance MRI cohort

## Who we are

Colvera is a student-led, mentor-advised, non-commercial research project focused on rigorous longitudinal and multimodal evidence analysis in rectal cancer. It is research-use only and not a patient-care system.

## Research question

For organ-preservation/watch-and-wait patients, does incorporating a patient’s own prior surveillance MRI improve local-regrowth detection compared with reviewing the current MRI alone?

## Why this cohort is uniquely valuable

The published cohort reports 72 organ-preservation patients, 440 follow-up MRIs, and 12 local regrowths, with T2/DWI MRI every three months in year one and every six months thereafter. It offers the exact paired comparison Colvera needs, even though it is too small to establish broad clinical generalization by itself. [Lambregts et al., *European Radiology*](https://doi.org/10.1007/s00330-015-4062-z)

## What we have already built

We built a longitudinal manifest contract with patient-level split isolation and current-only versus adjacent prior/current MRI interfaces. It can add endoscopy, DRE, CEA, and outcomes without redesign. We also keep an explicit boundary between valid research infrastructure and unsupported clinical claims.

## Exact data requested

For an approved non-commercial collaboration:

- stable de-identified patient and serial study/visit IDs;
- T2 and DWI/ADC MRI, sequence mapping, and approved acquisition/preprocessing metadata;
- visit dates or time offsets, including treatment and surveillance schedule;
- per-visit local-regrowth status/confidence, event date, site, and reference standard;
- endoscopy assessments/images if available, DRE, CEA, cCR/near-cCR, treatment and salvage details;
- original reader labels/scores, ROI/annotations if available, and data dictionary.

## Exact experiment

We would predefine one patient-level temporal development/holdout protocol and evaluate:

1. current T2/DWI MRI → local-regrowth status;
2. previous + current T2/DWI MRI → local-regrowth status;
3. optional MRI + clinical/endoscopic evidence if the approved data support it.

The result would emphasize sensitivity, false negatives, calibration, time-to-detection/lead time, uncertainty, and patient-level CIs. Any retrieval uses training patients only. The small number of events would be treated as a major limitation, not hidden.

## Privacy and contribution

We request de-identified research data only, under the data owner’s agreement and oversight; we will not redistribute images or expose patient-like cases. We can contribute a transparent current-only versus longitudinal benchmark, data-lineage checks, reproducible evaluation code, and a careful error/uncertainty analysis for investigator review.
