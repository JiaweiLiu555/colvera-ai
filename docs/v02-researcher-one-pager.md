# Colvera v0.2 — one-page researcher brief

## The question

Can a public rectal-MRI deep-learning release be reproduced transparently enough to become a sound starting point for Colvera's future hospital-facing evidence platform?

## Why this matters

Zhu et al. reported strong pretreatment prediction of pathological response to nCRT in locally advanced rectal cancer (ADC AUROC 0.851; T2 AUROC 0.721) on a 200-patient chronological test cohort. A reproducible foundation is necessary before extending any model toward richer clinical pathways or longitudinal surveillance.

## What we built

- cloned and hash-audited the official GitHub release;
- created a release-record manifest that never pretends anonymous arrays are patient IDs;
- reconstructed the released Keras 2.1.6 HDF5 architecture in modern PyTorch;
- checked deterministic and finite inference before a locked test pass;
- preserved v0.1 and added a v0.2 transparency view to the Streamlit MMP.

## Key finding

The public release does **not** support a patient-level reproduction. It has 323 unnamed development array records—not a verified 500-patient development cohort—and no patient IDs, augmentation lineage, channel names, original-image linkage, or clinical metadata. Under a predeclared but unverified mapping of array channels to ADC/T2, the released weights produced AUROC 0.500 and 0.498 on the 200-record test array, not the published values. This is an indeterminate/failed public-release reproduction check, not a model-performance claim.

## What we are not claiming

No new model was trained. No fusion, calibration, patient retrieval, subgroup result, clinical recommendation, diagnosis, local-regrowth prediction, or clinical validation is claimed. Pretreatment response and watch-and-wait local regrowth are distinct endpoints.

## Exact request to a potential collaborator/source author

Could you share or confirm the four NPZ channel names, one-hot class ordering, preprocessing/normalization used by the released weights, a 10-case expected-prediction fixture, and—if permitted—a patient/augmentation manifest for the 500 development cases? These assets would allow a clean patient-level reproduction before any extension.

## Immediate next step

Run the 10-case numerical-parity check. If it passes, build a locked patient-level temporal development/external-validation protocol; only then compare an interpretable baseline, source-faithful ADC model, T2 model, and predeclared late fusion.
