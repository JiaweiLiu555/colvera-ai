# Data-access brief — OPRA

## Who we are

Colvera is a student-led, mentor-advised, non-commercial rectal-cancer AI research project. Our central aim is to test whether longitudinal evidence improves surveillance assessment while preserving clinician control and never presenting research outputs as patient-care recommendations.

## Research question

Can a patient’s surveillance trajectory—serial MRI, endoscopy/DRE, CEA, treatment context, and response status—improve early detection of watch-and-wait local regrowth compared with the current MRI alone?

## What we have already built

The repository has transparent baseline/reproduction records, explicit limits on unsuitable public data, patient-level leakage checks, a longitudinal evidence contract, and an MMP designed to display only owner-approved, real held-out research outputs.

## Exact data requested

Subject to OPRA governance and the appropriate trial/data-access route, we request:

- stable de-identified patient/visit/study IDs and visit time offsets;
- serial pelvic MRI with sequence mapping and acquisition metadata permitted by the agreement;
- endoscopy assessments and images if available; DRE; CEA with units; cCR/near-cCR assessments;
- local-regrowth event status, date/time offset, site, and confirmation method;
- total neoadjuvant therapy assignment, timing, surgery/salvage treatment, and follow-up status;
- original trial/cohort assignment and data dictionary; tumor annotations if available.

## Exact experiment

With a predeclared temporal patient-level split, we would compare: (1) current MRI only; (2) previous + current MRI; (3) MRI + time-aligned clinical/endoscopic evidence; and (4) a training-only comparable-trajectory analysis. All selection would occur in development data; final held-out evaluation would report discrimination, calibration, false negatives, lead time, and clinically meaningful error review.

## Privacy and contribution

We request de-identified research data only for non-commercial work under the owner’s agreement and oversight. We can contribute a fully auditable longitudinal benchmark, data-quality/lineage checks, reproducible evaluation code, and a conservative research interface for investigator review. We will not redistribute data or make clinical claims.

## Why OPRA

OPRA is a high-value collaboration target because watch-and-wait response assessment and regrowth are central to Colvera’s intended clinical question. This brief does not assume that raw imaging or visit-level data are publicly available; access must be confirmed by trial leadership/data governance.
