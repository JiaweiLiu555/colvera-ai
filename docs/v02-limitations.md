# v0.2 limitations and safety boundary

## Critical limitations

1. **No verified patient unit.** The release has array records but no patient identifiers, dates, source-image linkage, or augmentation lineage. Patient-level cross-validation and generalization claims are blocked.
2. **No named modality axes.** The four channels cannot be confirmed as ADC/T2. The published-weight checks are mapping-dependent and were deliberately not altered after test results.
3. **Incomplete development release.** The paper reports 500 development patients; the release has 323 development records with different class proportions. A model cannot responsibly be retrained, compared, or selected.
4. **No clinical context.** Age, sex, stage, treatment details per record, scanner/site linkage, pathology linkage, and outcomes beyond one-hot arrays are unavailable.
5. **No external or subgroup validation.** The source is single-centre and retrospective; fairness, domain shift, and patient-level calibration cannot be evaluated.
6. **No longitudinal relevance.** Pretreatment response is not local regrowth. The release has no watch-and-wait timeline, serial MRI, endoscopy, DRE, CEA, or local-regrowth outcome.
7. **Legal/reuse uncertainty.** Public GitHub access is not an explicit data license. There is no license file in the cloned repository.

## Safety logic for the MMP

The MMP labels v0.2 as a research audit, reports aggregate results only, and refuses case-level predictions. It does not ingest patient data, display patient-like records, claim the test result generalizes, or recommend any test, procedure, referral, or treatment.

## What would change this decision

An approved dataset/data-use agreement with patient IDs or a trusted linkage token, chronological dates, original MRI/ROI provenance, explicit modality/channel names, outcome labels, scanner metadata, and an external site is required. Then all preprocessing, split, calibration, threshold, abstention, and retrieval decisions must be made using development patients only before a one-time external test.
