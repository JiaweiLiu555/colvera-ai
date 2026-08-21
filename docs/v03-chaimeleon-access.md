# Colvera v0.3 — CHAIMELEON access verification

**Checked:** 2026-08-17. **Decision:** do not create a CHAIMELEON-based v0.3 experiment yet.

## Official current access result

The official [CHAIMELEON Open Challenges page](https://chaimeleon.grand-challenge.org/) is visible, but it does not expose a public rectal dataset download. The page currently provides **Sign In**, **Register**, and **Join** controls. Its public classification-phase documentation says the controlled training data were provided only after registration and acceptance via an emailed access link; that page describes prostate and lung tasks, not rectal data.

The rectal task belonged to the locked Championship phase. The official page says that phase was limited to the top 40 qualifying participants and ran from 2024-01-16 through 2024-02-29. The public overview now describes those dates as past, and the championship page is access-controlled. The project’s current site describes an infrastructure/repository transition to EUCAIM, not a publicly downloadable rectal benchmark.

## Exact blocker

No unauthenticated, current, patient-level CHAIMELEON rectal download or active train/validation/test package was available through the official access path. Access was historically controlled by accepted challenge participation, and the relevant phase is closed. We will not create an account, accept third-party terms, seek to bypass access controls, or call a past competition download a currently open public dataset.

## Consequence

There is **no Colvera v0.3 model, training run, held-out result, fusion analysis, or retrieval result**. The repository instead contains a longitudinal-ingest contract and four targeted data-request briefs. A future CHAIMELEON study can begin only after the organizers provide written access and a current data dictionary confirming patient count, labels, clinical fields, license/data-use terms, and fixed splits.

## Verification sources

- [Official Open Challenges overview](https://chaimeleon.grand-challenge.org/)
- [Official classification-phase access description](https://chaimeleon.grand-challenge.org/classification-phase/)
- [CHAIMELEON project transition/update](https://chaimeleon.eu/chaimeleon-project-concludes-tracing-its-legacy-and-lasting-impact/)

The frequently cited 331-patient, three-hospital rectal cohort is described in later research, but that is not proof of current public patient-level access and is not treated as one here.
