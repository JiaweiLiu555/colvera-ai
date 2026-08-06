# Data requirements

## Minimum patient-level record

- stable de-identified patient identifier;
- dates relative to treatment and surveillance milestones;
- serial pelvic MRI with device/protocol metadata;
- serial endoscopy images or video and reports;
- clinical examination findings;
- CEA measurements;
- baseline tumor and treatment characteristics;
- confirmed outcome and confirmation method;
- institution/site identifier for external validation design.

## Non-negotiable quality checks

- split by patient, never by image or frame;
- prevent study-series and temporal leakage;
- audit missingness by site, modality, and subgroup;
- document label adjudication and follow-up maturity;
- retain provenance without storing PHI in this repository.

