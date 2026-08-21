# Colvera longitudinal data contract

## Goal

Colvera’s next scientific question is deliberately simple:

> Does the patient's own previous imaging improve prediction compared with the current examination alone?

The repository is ready to ingest an approved cohort structured as:

```text
patient (de-identified study key)
  └─ visit (relative time offset)
       ├─ MRI modality / image reference
       ├─ endoscopy evidence
       ├─ clinical, laboratory, and DRE evidence
       └─ outcome/event record
```

## Required manifest

One row represents one evidence item at one visit. Required columns are:

| Column | Requirement |
|---|---|
| `patient_id` | Stable de-identified research key; no PHI |
| `visit_id` | Stable visit/study key |
| `time_offset_days` | Numeric time relative to baseline; not an identifying calendar date |
| `evidence_type` | `mri`, `endoscopy`, `clinical`, `laboratory`, `dre`, or `outcome` |
| `modality_or_measure` | e.g. `T2`, `DWI`, `T1C`, `CEA`, `endoscopy_assessment` |
| `resource_ref` | Non-empty relative reference beneath an approved data root |
| `split` | `train`, `validation`, `test`, or `external_test`; one patient may appear in only one |

Outcome/event fields must remain outside model features. Add `outcome_name`, `outcome_value`, and an event time offset only after the data owner approves their use.

## Built-in safeguards

`src/colvera/longitudinal/contract.py` validates required fields, safe relative image references, visit-time consistency, duplicate evidence rows, and patient-level split isolation. It also constructs two leakage-safe study views:

- `current_only_records(...)`: current visit evidence only;
- `longitudinal_pairs(...)`: adjacent prior/current MRI visits of the same patient and split.

`src/colvera/longitudinal/study.py` makes four model-facing study specifications explicit—`current_only`, `longitudinal`, `multimodal_longitudinal`, and `full_colvera`. Development views reject test/external-test splits before a model is constructed.

It does not read images, train a model, infer an outcome, or upload data. Validate a received de-identified manifest with:

```bash
.venv/bin/python scripts/validate_longitudinal_manifest.py /approved-data/manifest.csv
```

## Future experiment sequence

1. Current MRI → outcome.
2. Previous + current MRI → outcome.
3. Previous/current MRI + time-aligned clinical evidence → outcome.
4. Serial MRI + serial endoscopy + clinical trajectory + training-only comparable trajectories → local-regrowth outcome.

All model selection, preprocessing, calibration, abstention, and retrieval design must use development patients only. Freeze them before one independent/external test pass.
