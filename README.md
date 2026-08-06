# Colvera AI

## Three launch goals

1. **Clinical definition:** Define and validate a focused local-regrowth surveillance problem for rectal-cancer watch-and-wait care.
2. **Data access:** Secure matched, longitudinal, patient-level MRI, endoscopy, clinical, and confirmed-outcome data.
3. **Evidence:** Build and rigorously evaluate a non-clinical multimodal research prototype with sensitivity, calibration, subgroup analysis, and safe abstention as first-class measures.

Colvera AI is a hospital-facing research platform for multimodal assessment of **local rectal-cancer regrowth during watch-and-wait surveillance**. It is designed to help multidisciplinary teams review longitudinal evidence, especially when MRI, endoscopy, examination findings, and biomarkers disagree.

> **Current status:** Non-clinical research and product-definition stage. Colvera AI has not been clinically validated, cleared or approved by the FDA, and must not be used to diagnose, exclude, monitor, or treat cancer or to make patient-care decisions.

## User

The initial users are multidisciplinary rectal-cancer teams caring for adults after neoadjuvant therapy who are enrolled in, or being followed through, an organ-preserving watch-and-wait pathway:

- colorectal surgeons;
- abdominal radiologists;
- gastroenterologists and endoscopists;
- medical and radiation oncologists;
- tumor-board coordinators and clinical researchers.

## Workflow

1. A clinical team performs standard watch-and-wait surveillance.
2. Longitudinal MRI, endoscopy, examination findings, CEA, treatment history, and timing are assembled for one patient.
3. Modality-specific components compare the current study with prior studies and extract relevant changes.
4. A fusion layer evaluates cross-modality agreement, disagreement, missingness, and uncertainty.
5. The research interface returns an auditable review packet for clinician and tumor-board review.
6. Confirmed local-regrowth or continued disease-free follow-up outcomes are recorded for retrospective evaluation.

## Inputs

- serial pelvic MRI, including relevant sequences and radiology findings;
- serial endoscopy images/video and endoscopy reports;
- digital rectal examination and other clinical examination findings;
- CEA values and trends;
- baseline tumor location, size, stage, and nodal status;
- neoadjuvant treatment regimen and timing;
- surveillance intervals and prior assessments;
- pathology, biopsy, salvage-surgery findings, or sufficiently mature longitudinal follow-up for outcome labeling.

## Outputs

- an experimental estimate of local-regrowth risk within a defined surveillance window;
- separate MRI, endoscopy, and clinical-evidence summaries;
- explicit identification of cross-modality agreement or disagreement;
- influential findings and changes from prior examinations;
- uncertainty, missing-data warnings, and an abstention state;
- a structured recommendation for multidisciplinary review or additional standard assessment.

Colvera AI will not output a definitive diagnosis or independently recommend treatment.

## Product boundary

The first research question is **local regrowth during watch-and-wait surveillance**, not colon cancer broadly and not immediate residual disease after treatment. Residual disease, incomplete response, and later local regrowth are related but distinct outcomes and must not be mixed in a single label without a prespecified clinical definition.

## Evaluation principles

- patient-level and institution-aware splitting;
- comparison with MRI-only, endoscopy-only, clinical-only, and simple-fusion baselines;
- sensitivity and false-negative rate as primary safety measures;
- specificity, precision-recall, AUROC, calibration, and confidence intervals;
- performance in MRI-endoscopy disagreement cases;
- subgroup and external-site evaluation;
- abstention coverage and safety;
- no performance claims without verified data and reproducible experiments.

## Repository map

```text
.
├── docs/                # Product, clinical, data, validation, and safety definitions
├── research/            # Literature and dataset notes; no patient data
├── src/                 # Future research code, separated by pipeline stage
├── tests/               # Unit, integration, and data-leakage tests
└── .github/             # Contribution templates and project hygiene
```

## Project launch

- **Milestone:** Project launch
- **Workstream:** Product and clinical research
- **Decision log:** maintained in the Colvera command-center Drive folder
- **Issue board:** maintained in GitHub Projects for this repository

## Data governance

Do not commit patient data, protected health information, credentials, access agreements, or institution-restricted datasets. Use synthetic fixtures for software tests until an approved institutional environment and protocol exist.

