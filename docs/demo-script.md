# Three-minute research demo

1. **Open with the boundary (15 seconds).** “Colvera is a research platform for eventually making rectal-cancer watch-and-wait surveillance longitudinal, multimodal, and comparative. This version is not a surveillance model and is not for patient care.”
2. **Name the honest starting point (20 seconds).** “We chose an open CC-BY dataset with 71 real LARC patients, pretreatment MRI-derived radiomics, five structured variables, and response labels. It has no serial exams or regrowth labels, so we scoped v0.1 to response prediction.”
3. **Show transparency (20 seconds).** Point to the dataset card: 56 development / 15 held-out patients, model version, missing modalities, and source-preprocessing warning.
4. **Browse a held-out case (35 seconds).** Select any research case ID. Show only the actual released normalized evidence and say raw MRI and timeline are unavailable, rather than drawing a fake image or history.
5. **Show comparative retrieval (25 seconds).** “These are the three nearest development-set cases in the learned feature representation. They are descriptive historical context, not proof of an outcome.”
6. **Show all three models (30 seconds).** Point out the saved held-out metrics. “The fused model did not beat the structured baseline. We kept that result in the interface.”
7. **Show figures and limitation panel (20 seconds).** “The uncertainty is large, calibration is not adequate for case-level interpretation, and no probability is shown.”
8. **Close with a specific collaboration ask (15 seconds).** “The next study needs serial MRI plus endoscopy and confirmed, dated local-regrowth outcomes. We are looking for a group where we can contribute to dataset audit, baseline reproduction, and longitudinal evaluation.”

## Do not say

- “The model detects regrowth.”
- “The model has X% accuracy.”
- “Similar cases predict what will happen.”
- “This is ready for hospital use.”
