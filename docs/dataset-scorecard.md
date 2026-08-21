# Dataset scorecard

Scores are 0–5 across ten dimensions: clinical relevance, longitudinal value, imaging value, outcome quality, sample size, accessibility, reproducibility, first-paper usefulness, first-product usefulness, and ability to demonstrate a Colvera insight. Scores are decision aids, not performance claims. “Not reported” means the cited record/paper page did not establish the item.

| Rank | Candidate | Provenance and access | Patients / studies | Best supported outcome | Score / 50 | Why it is not the current primary |
|---:|---|---|---|---|---:|---|
| 1 | **Zenodo 8379940 LARC MRI radiomics** | [Open Zenodo, CC-BY-4.0](https://zenodo.org/records/8379940) | **71 patients**, 1 row/patient | nCRT response: cCR/TRG1–4; binary response label | **37** | **Selected.** Immediate, patient-level, MRI-derived and outcome-linked; lacks raw MRI, serial exams, endoscopy, and regrowth. |
| 2 | International Watch & Wait Database (IWWD) | [IWWD registry publication](https://www.sciencedirect.com/science/article/pii/S014067361831078X) | 880 cCR patients, 47 centers / 15 countries in 2018 analysis | Local regrowth and follow-up | 36 | Strongest future surveillance cohort, but the registry is not an open image download and raw MRI/endoscopy availability is not established. |
| 3 | Organ-preservation MRI+DWI follow-up cohort | [72 patients / 440 MRI follow-ups](https://pmc.ncbi.nlm.nih.gov/articles/PMC4902833/) | 72 patients, 440 follow-up MRI exams; 12 regrowth events | Local regrowth | 34 | Excellent longitudinal scientific fit, but no public reusable image archive was located; too few events for an immediate independent model. |
| 4 | OPRA MRI response analysis | [277 analysable restaging MRI forms](https://pmc.ncbi.nlm.nih.gov/articles/PMC11427875/) | 277 participants in analysis | Residual disease, organ preservation, local-regrowth association | 33 | Highly relevant trial population, but this publication does not release a reusable raw MRI dataset. Research collaboration/request is needed. |
| 5 | Rectal-RadioSAM cohort | [Published study and code](https://pmc.ncbi.nlm.nih.gov/articles/PMC12226370/) | 378 patients / 756 pre- and post-nCRT cases reported | Pathologic complete response | 30 | Offers longitudinal pre/post MRI in the paper, but the patient images are not openly released. |
| 6 | Zenodo 18098176 derived radiomics | [Open Zenodo record](https://zenodo.org/records/18098176) | Count not established from the record page reviewed | Synchronous distant metastasis | 25 | Open and reproducible but wrong outcome and no watch-and-wait framing. Backup only for pipeline testing. |
| 7 | TRIUNITE-01 spatial molecular dataset | [Open Zenodo record](https://zenodo.org/records/15532918) | Count not established from record page; pre/post IMC images + clinical table | Response-related trial data | 23 | Multimodal and open but molecular imaging rather than pelvic MRI/endoscopy; not a usable Colvera surveillance starting point. |
| 8 | TCIA TCGA-READ | [TCIA collection](https://www.cancerimagingarchive.net/collection/tcga-read/) | 3 imaging subjects | Genomic/pathology context; no nCRT response or regrowth | 16 | Public raw MR/CT but far too small and clinically mismatched. |
| 9 | TCIA PDMR Texture Analysis | [TCIA collection](https://www.cancerimagingarchive.net/collection/pdmr-texture-analysis/) | 175 mice, 514 serial studies | Tissue-characterization research | 14 | Genuine serial MRI but animal PDX data spanning cancers, not a human rectal-cancer model. |
| 10 | TCIA EXACT anal-cancer MRI | [TCIA collection](https://www.cancerimagingarchive.net/collection/exact/) | 30 subjects / 6,400 images | Expert staging | 12 | Wrong disease, staging rather than response/regrowth, and access is currently unavailable under TCIA controlled-data policy. |

## Selection decision

### Primary dataset — selected and downloaded

**Zenodo 8379940.** It is the strongest dataset we can use immediately and legitimately to produce a reproducible result. Its narrow scope forces an honest first study: pretreatment MRI-derived radiomics and supplied structured variables for nCRT response.

### Backup dataset — accessible but not clinically equivalent

**Zenodo 18098176.** It is open and small enough to audit rapidly, but its distant-metastasis endpoint makes it a backup for generic rectal-cancer radiomics pipeline validation, not a Colvera-specific study.

### Future permission-based dataset — highest clinical value

**IWWD, ideally linked to serial MRI/endoscopy at contributing sites.** This is the priority collaboration target because it has watch-and-wait local-regrowth outcomes across many centers. Before use, we need documented patient IDs, surveillance times, modality availability, confirmation methods, follow-up maturity, access agreement, and ethics/governance review.

## What this search established

No openly downloadable dataset located in this search provides the full Colvera target: patient-level serial pelvic MRI + endoscopy + clinical evidence + temporal local-regrowth labels. Therefore Colvera v0.1 is deliberately an **enabling response-prediction experiment**, while the long-term product definition remains unchanged.
