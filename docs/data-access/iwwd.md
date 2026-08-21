# Data-access brief — International Watch & Wait Database (IWWD)

## Who we are

Colvera is a student-led, mentor-advised, non-commercial research project developing rigorous methods for longitudinal, multimodal, comparative rectal-cancer surveillance analysis. We are seeking collaboration and guidance, not a shortcut to a clinical product.

## Research question

Across institutions, does combining serial MRI with time-aligned endoscopy, DRE, CEA, response status, and prior patient trajectories improve detection of local regrowth compared with current imaging alone?

## What we have already built

We have created a research-only codebase with explicit patient-level isolation rules, a manifest contract for serial evidence, calibration/uncertainty tooling, training-only comparative retrieval boundaries, and a transparent MMP. We have also documented failed or unsuitable public-data routes rather than treating them as clinical evidence.

## Exact data requested

Under IWWD governance and a non-commercial agreement, we request the minimum necessary de-identified data:

- stable patient and visit/study IDs; dates or approved relative time offsets;
- serial MRI with sequence mapping and permitted acquisition metadata;
- endoscopy assessments/images if available, DRE, CEA, cCR/near-cCR status;
- local-regrowth event/date/site/confirmation and last follow-up;
- treatment, surgery/salvage, and center metadata as permitted;
- dataset dictionary, missingness rules, and approved cohort/split guidance.

## Exact experiment

We would create an institution-aware, temporally anchored benchmark: current MRI only versus previous + current MRI versus multimodal longitudinal evidence. Comparable historical trajectories would always be retrieved from training centers/patients only. External/site-held-out validation, calibration, event-time/lead-time analysis, and false-negative review would be preregistered before final evaluation.

## Privacy and contribution

We will use only de-identified research data, apply the owner’s governance controls, keep data outside version control, and make no public case-level outputs. We can contribute a transparent longitudinal baseline suite, leakage/lineage audits, reproducible code, and a careful evaluation of what additional modalities add beyond MRI.

## Why IWWD

IWWD is an ultimate collaboration target because it represents real watch-and-wait follow-up across centers. This brief does not assume that raw imaging or individual longitudinal data are publicly available; any use depends on registry approval and collaboration.
