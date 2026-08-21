# Decision log

## 2026-08-15 — Select Zenodo 8379940 as the primary dataset

- **Decision:** Use the open 71-patient LARC radiomics table for Colvera v0.1.
- **Why:** It is the only identified candidate that is immediately downloadable, patient-level, rectal-cancer-specific, MRI-derived, outcome-linked, licensed for reuse, and sufficiently documented for a reproducible experiment.
- **Alternatives:** IWWD; an MRI/DWI follow-up study; OPRA; TCIA collections; other Zenodo records.
- **Evidence:** `docs/dataset-scorecard.md`.
- **Revisit when:** a verified public or permitted cohort with serial MRI/endoscopy and local-regrowth labels becomes available.

## 2026-08-15 — Scope the first study to nCRT response, not local regrowth

- **Decision:** Predict released nCRT response labels and state explicitly that this is not surveillance.
- **Why:** The primary dataset contains no repeated surveillance exams or local-regrowth outcome/timing.
- **Alternatives:** Relabel response as regrowth or build a simulated surveillance model.
- **Evidence:** Dataset audit and source workbook schema.
- **Revisit when:** a cohort has a prespecified local-regrowth reference standard at dated surveillance visits.

## 2026-08-15 — Use a fixed patient-level holdout plus development-only tuning

- **Decision:** Stratified 56/15 patient split, seed `20260815`; three-fold inner development CV for hyperparameters.
- **Why:** Patient IDs are unique and permit reproducible leakage checks. A separate held-out set is more interpretable than reporting tuning performance alone.
- **Alternatives:** image-level split, random repeated reporting without holdout, training-set scores.
- **Evidence:** `tests/test_data_and_retrieval.py` and `src/colvera/data.py`.
- **Revisit when:** a larger cohort supports an institution-aware external test set.

## 2026-08-15 — Preserve the negative fusion result

- **Decision:** Keep the fusion model, exact results, and failure message in the app and report.
- **Why:** On the held-out set, fusion AUROC (0.679) was below the structured baseline (0.714), with a higher false-negative rate (0.500 vs 0.250).
- **Alternatives:** tune further until fusion wins, omit the baseline, or present only inner-CV performance.
- **Evidence:** `outputs/metrics/results.json`.
- **Revisit when:** a preregistered new experiment on an independent cohort supports a different conclusion.

## 2026-08-15 — Make comparative retrieval descriptive only

- **Decision:** Show nearest development-set cases as context and label their limitations.
- **Why:** Similarity can illustrate the comparative product concept, but with this small precomputed feature cohort it cannot establish prognosis or causal relevance.
- **Alternatives:** use neighbors to override predictions or display their outcomes as a case-level risk estimate.
- **Evidence:** `src/colvera/retrieval.py` and `docs/model-card.md`.
- **Revisit when:** clinically curated longitudinal features and evaluation criteria for retrieval relevance are available.
