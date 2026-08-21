# From Colvera v0.1 to the full research program

| Stage | Evidence and capability | Required data / evaluation gate |
|---|---|---|
| **Current: v0.1** | Pretreatment structured + MRI-derived radiomics, response-label baselines, held-out case browser, descriptive retrieval | 71-patient public feature table; exploratory only |
| **Next: raw MRI** | Reproducible image preprocessing, quality checks, segmentation audit, current-exam MRI model | Raw DICOM/NIfTI, sequence metadata, tumor masks or annotation protocol, external test site |
| **Then: longitudinal MRI** | Previous/current comparison, change representations, time-horizon analysis | Dated serial MRI per patient; no future-data leakage; regrowth/outcome timing |
| **Then: MRI + endoscopy** | Separate modality encoders and explicit agreement/discordance state | Matched endoscopy images/reports at surveillance visits, quality fields, anatomical correlation process |
| **Then: clinical evidence** | DRE, CEA, treatment history, missingness-aware fusion and abstention | Date-stamped structured clinical data; prespecified availability windows |
| **Then: comparative trajectories** | Retrieval of clinically constrained historical trajectories with outcomes | Large multi-site longitudinal cohort; retrieval relevance review; no neighbor leakage |
| **Then: local-regrowth study** | Retrospective local-regrowth prediction / detection evaluation | Confirmed, timed local-regrowth labels; follow-up maturity; patient and site held-outs |
| **Before prospective use** | Prospective silent evaluation, workflow study, calibration and safety controls | Institutional collaborators, protocol/IRB, external validation, clinician-defined thresholds |

## Non-negotiable future cohort specification

One stable de-identified ID; treatment and surveillance dates; serial pelvic MRI with sequence/device metadata; serial endoscopy images/video and reports; DRE and CEA when recorded; baseline/treatment context; outcome confirmation method; local-regrowth date/location; sufficient negative follow-up; and institution/site identifier.

The long-term product goal remains **longitudinal + multimodal + comparative local-regrowth surveillance**. v0.1 is not a redefinition of that goal around whichever labels were easiest to download.
