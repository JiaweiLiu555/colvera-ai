# Colvera v0.1 — technical summary for research collaborators

## What Colvera is

Colvera is a research effort toward longitudinal, multimodal, comparative assessment of **local regrowth** during rectal-cancer watch-and-wait surveillance. The intended long-term value is not an opaque diagnosis score: it is to make patient-specific change, modality agreement/disagreement, missingness, and relevant historical trajectories easier to review.

## What we implemented

We implemented and evaluated a reproducible research MMP using [Zenodo 8379940](https://zenodo.org/records/8379940), an open CC-BY-4.0 rectal-cancer dataset. The repository includes checksum-verified download, data audit, fixed patient-level holdout, leakage assertions, three baseline families, bootstrap intervals, error-visible case browser, descriptive nearest-neighbor retrieval, generated figures, and a Streamlit research UI.

## Current experiment

- **Cohort:** 71 unique patients with locally advanced rectal cancer.
- **Inputs:** five supplied structured clinicopathological/MRI variables and 2,144 pretreatment MRI radiomics features.
- **Outcome:** source-defined nCRT non-response (TRG3/4) versus response (cCR/TRG1/TRG2).
- **Split:** 56 development / 15 held-out patients; IDs never enter models.
- **Models:** structured logistic regression; radiomics regularized logistic regression; fused model with descriptive historical-case retrieval.

## Real results

Held-out AUROC: structured baseline 0.714; radiomics-only 0.446; fusion 0.679. Fusion did not outperform the structured baseline. The fused model had sensitivity 0.500, specificity 0.714, and a wide AUROC bootstrap 95% interval of 0.352–0.946. These are exploratory results, not evidence for clinical use.

## Biggest limitation

The release is small and single-source, uses precomputed normalized features, and has no raw MRI, serial surveillance exams, endoscopy, DRE/CEA, local-regrowth label, timing, site, scanner, or demographic metadata. It cannot test the core Colvera hypothesis.

## Next data requirement

Patient-level, dated serial pelvic MRI and endoscopy during watch-and-wait, with treatment history, DRE/CEA when available, quality/missingness fields, and confirmed timed local-regrowth outcomes. The key first comparison will be current MRI alone versus current + previous MRI, then explicit MRI-endoscopy agreement/disagreement.

## Collaboration request

We are seeking guidance or collaboration around dataset definition, audit/reproduction, longitudinal-split design, outcome adjudication, model evaluation, and prototype development. We can contribute an immediately usable reproducible analysis scaffold rather than asking a group to adopt an untested product idea.
