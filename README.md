# Colvera

**Longitudinal AI for Rectal Cancer Surveillance**

Colvera is a research project and product demonstration for longitudinal, multimodal, comparative review of concerning change during rectal-cancer watch-and-wait surveillance. The default app is a polished **synthetic demonstration**: it compares a patient's serial MRI, endoscopy, CEA, and clinical evidence without claiming diagnosis or clinical validation.

> **Non-clinical status.** Colvera is not clinically validated, not a diagnostic device, and must not be used to diagnose, monitor, triage, or treat a patient. The in-app Patient 024 is entirely synthetic.

## Product demo

Launch the app and open Patient 024 to see the core workflow:

- **Longitudinal:** current evidence is read against the patient's own prior examinations.
- **Multimodal:** MRI, endoscopy, CEA, and clinical/DRE information are organized together.
- **Comparative:** synthetic demonstration trajectories show the future comparative-review concept.

The product UI is intentionally separated from the saved research artifacts. Use **Research archive** in the app to view the v0.1/v0.2 experiments and their limitations; those experiments do not validate the synthetic surveillance demo.

## Current data strategy

Colvera is in a focused data-access phase. We preserve the v0.1 baseline and v0.2 failed reproduction as transparent historical work, but neither is the foundation for the next model. CHAIMELEON’s public challenge page does not provide a current public rectal download; its controlled, gated rectal championship ended in 2024. Therefore **no v0.3 experiment has been manufactured from a substitute dataset**. See [the access verification](docs/v03-chaimeleon-access.md).

The primary dataset to pursue is the 622-patient, pre/post multiparametric-MRI rectal-cancer cohort from Jin et al. The paper makes original clinical/MRI data available to eligible academic researchers for non-commercial work under a signed data-access agreement. Colvera’s next experiment is fixed: **current MRI versus previous + current MRI**, then the same comparison with time-aligned clinical evidence. See [the request package](docs/data-access/README.md) and [longitudinal data contract](docs/longitudinal-data-contract.md).

## Current research question

We use [Zenodo 8379940](https://zenodo.org/records/8379940), an open 71-patient locally advanced rectal-cancer cohort, to compare structured variables, pretreatment MRI radiomics, and their fusion for the source-defined nCRT response label. This is an **enabling** study: the dataset cannot test watch-and-wait local regrowth because it has no serial surveillance exams, endoscopy, or regrowth labels.

## What v0.1 can do

- download and checksum-verify the open source data;
- audit 71 unique patient rows, labels, missingness, and feature schema;
- make a reproducible patient-level 56/15 development/holdout split;
- fit structured-only, radiomics-only, and fused regularized logistic baselines;
- save held-out predictions, calibration/ROC/PR/model-comparison figures, bootstrap intervals, and a transparent error set;
- retrieve comparable cases from the development set only;
- launch a Streamlit research case browser connected solely to saved experimental artifacts.

## What v0.1 cannot do

- assess local regrowth, serial change, MRI/endoscopy disagreement, or lead time;
- process raw MRI, endoscopy, DICOM, or patient uploads;
- show a calibrated individual probability, make a diagnosis, or make a care recommendation;
- establish external, subgroup, or clinical validity.

## v0.2: released-weight reproduction audit

v0.2 preserves v0.1 and adds a separate audit of the public release accompanying [Zhu et al. (2020)](https://doi.org/10.3389/fonc.2020.574337), which studied **pretreatment pathological good response to nCRT** in LARC. This is not a local-regrowth, surveillance, diagnostic, or care-recommendation model.

The official repository contains 323 unnamed development array records, 200 test array records, and released ADC/T2 HDF5 weights, but no patient IDs, augmentation lineage, named image channels, original-image linkage, clinical fields, or explicit license. We therefore do **not** train, tune, fuse, calibrate, retrieve, or claim patient-level validation in v0.2.

A predeclared one-pass released-weight check using provisional unverified channel mappings did not reproduce the paper's published results (AUROC 0.500 / 0.498 versus reported 0.851 / 0.721). That is a release-compatibility finding, not a performance claim about the source study or a clinical result. Read [the v0.2 report](docs/v02-research-report.md), [data availability](docs/v02-data-availability.md), and [final evaluation lock](docs/v02-final-model-lock.md) before interpreting it.

## Dataset

- **Source:** [Zenodo 8379940](https://zenodo.org/records/8379940), CC-BY-4.0.
- **N:** 71 unique patients, one released row per patient.
- **Inputs:** five supplied normalized clinicopathological/MRI variables and 2,144 supplied normalized pretreatment MRI radiomics features.
- **Outcome:** non-response (TRG3/4) versus response (cCR/TRG1/TRG2), as defined by the source.
- **Critical caveat:** the public table is already z-score normalized and identifies five variables as outcome-associated. Source-level preprocessing and feature-selection leakage cannot be fully audited.

## Results

On the fixed 15-patient held-out set, structured baseline AUROC was **0.714**, radiomics-only AUROC was **0.446**, and fusion AUROC was **0.679**. Fusion did not improve on the structured baseline. The fused result is exploratory; its AUROC bootstrap 95% interval was 0.352–0.946.

Exact predictions, metrics, configurations, and plots are written on each run to `outputs/`. Read [the research report](docs/research-report.md) before interpreting them.

## Install and run

```bash
git clone https://github.com/JiaweiLiu555/colvera-ai.git
cd colvera-ai
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip install -e .
.venv/bin/python run.py
```

`run.py` downloads the public source if needed, verifies its MD5, audits the cohort, reruns the fixed experiment, writes artifacts, and launches the MMP.

## Individual commands

```bash
.venv/bin/python scripts/download_dataset.py
.venv/bin/python scripts/audit_dataset.py
.venv/bin/python scripts/run_experiment.py
.venv/bin/python -m streamlit run app.py
.venv/bin/python -m unittest discover -s tests -v
```

### v0.2 audit commands

The raw official clone is intentionally ignored by Git and must be present at `data/v02/raw/rectal_MR_DL`.

```bash
.venv/bin/python scripts/v02_audit_release.py
.venv/bin/python scripts/v02_validate_released_weights.py
# One-time only after reviewing docs/v02-final-model-lock.md:
.venv/bin/python scripts/v02_run_final_evaluation.py
```

The final command refuses to overwrite a saved test result. Do not delete or rerun it to tune a result; use a newly versioned dataset and lock instead.

## Project structure

```text
app.py                    Streamlit product demo + research-archive entry point
configs/                  Dataset and experiment configuration
data/                     Downloaded local data only; ignored by Git
docs/                     Study, dataset, model, safety, roadmap, and outreach material
outputs/                  Generated metrics and figures; model binary artifacts are ignored
scripts/                  Download, audit, and reproducible experiment entry points
src/colvera/              Data, models, evaluation, retrieval, and demo fixtures
src/colvera/demo/         Structured synthetic Patient 024 fixture + generated visual assets
src/colvera/longitudinal/ Validated patient → visit → evidence → outcome ingest contract
tests/                    Dataset, split, and retrieval leakage tests
```

## Roadmap

The next valid study needs serial pelvic MRI plus endoscopy and temporally confirmed local-regrowth outcomes. See [the full extension map](docs/full-colvera-roadmap.md), [data requirements](docs/data-requirements.md), and [the researcher one-pager](docs/researcher-one-pager.md).

## Data governance

Never commit PHI, restricted data, access agreements, or credentials. Future institutional data work requires the partner's approval, governance controls, and appropriate research oversight.
