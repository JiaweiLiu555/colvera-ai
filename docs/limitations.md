# Limitations

Colvera v0.1 is deliberately constrained by the available public data. These limitations are not footnotes; they define what this project can and cannot claim.

## Dataset and labels

1. **Wrong endpoint for the long-term product.** The target is nCRT response, not local regrowth during watch-and-wait surveillance.
2. **No longitudinal evidence.** Each patient has one released feature row. There are no previous/current MRI pairs, no trajectory, and no lead-time measurement.
3. **No endoscopy or examination evidence.** MRI-endoscopy agreement and disagreement cannot be modeled or evaluated.
4. **No raw MRI.** Image quality, scanner protocol, segmentation, lesion localization, and acquisition artifacts are inaccessible.
5. **Uncertain source preprocessing.** The release is already normalized and includes a preidentified set of outcome-associated structured variables. Colvera cannot reconstruct training-only preprocessing from the original raw values.
6. **Outcome confirmation detail is limited in the table.** The source paper distinguishes cCR and surgical TRG outcomes, but patient-level confirmation route and temporal availability are not released in the data file.
7. **Cohort-count discrepancy.** The associated paper reports 75 patients while the released workbook has 71 usable rows; the public material does not explain the difference.

## Evaluation

1. **Small fixed holdout.** There are 15 held-out patients, so every point estimate has wide uncertainty.
2. **Single-source cohort.** No external-site, temporal, or scanner validation is possible.
3. **No subgroup audit.** Age, sex, race/ethnicity, site, and scanner metadata are absent.
4. **No threshold can be declared safe.** The observed false-negative rates are exploratory, not clinical safety evidence.
5. **Calibration is not adequate for individual interpretation.** The interface intentionally suppresses numerical case-level probabilities.

## Product boundary

The Streamlit interface is an experiment browser, not a hospital workflow. It has no patient upload, no DICOM viewer, no EHR connection, no alerts, no scheduling, no real order action, and no patient-care recommendations.

## What would change these conclusions

The next legitimate advance requires a multi-institution cohort with stable patient IDs, dated serial MRI and endoscopy, DRE/CEA where available, treatment history, explicit modality quality fields, and temporally anchored local-regrowth adjudication. That data must be split by patient and preferably by institution, with all transforms fit only in development data.
