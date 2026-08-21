# Source-code workspace

`src/colvera/` now contains the v0.1 data loader, patient-level splitting guards, simple baselines, evaluation helpers, and development-only historical-case retrieval. The current implementation uses released tabular features rather than raw imaging.

Future code should keep the following stages separable and testable:

1. data ingestion and provenance;
2. MRI preprocessing and modeling;
3. endoscopy preprocessing and modeling;
4. clinical-variable modeling;
5. multimodal fusion;
6. calibration and uncertainty;
7. abstention and safety logic;
8. clinician-facing research outputs.
