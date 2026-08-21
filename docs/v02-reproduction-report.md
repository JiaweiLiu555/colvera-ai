# v0.2 released-weight reproduction report

## Result

The reconstructed released models **did not reproduce** the paper's reported test discrimination under the predeclared provisional channel mapping. This is a failed/indeterminate reproduction audit, not a claim about the paper's models or a replacement model.

| Fixed audit | Predeclared intended channel | Test AUROC | 95% bootstrap CI | Paper's AUROC | Difference |
|---|---|---:|---|---:|---:|
| `published_adc_reproduction` | release channel 0, provisional ADC | 0.500 | 0.500–0.500 | 0.851 | -0.351 |
| `published_t2_reproduction` | release channel 3, provisional T2 | 0.498 | 0.440–0.552 | 0.721 | -0.223 |

The ADC check returned an effectively constant low provisional GR probability: at the descriptive 0.50 threshold it had sensitivity 0.000 and specificity 1.000. The T2 check was similarly near-constant at a high provisional GR probability: sensitivity 0.883 and specificity 0.129. Neither result supports a reproduction claim; neither is a clinical performance estimate.

The paper reported test AUROC 0.851 (95% CI 0.789–0.914) for `DL_ADC` and 0.721 (95% CI 0.640–0.802) for `DL_T2` on 200 participants. It also reported `DL_ADC` sensitivity 94.3%, specificity 68.3%, PPV 87.4%, and NPV 83.7%. Those are publication results, not copied into Colvera results. See [Zhu et al. (2020)](https://doi.org/10.3389/fonc.2020.574337).

## What was reproduced faithfully

- The official repository was cloned at commit `507c357359aff085f5d9853d2f3c51d0c61d8dde`; release file hashes are saved in `outputs/v02/data-audit/audit.json` and `data/v02/test_lock.json`.
- Both HDF5 files identify Keras 2.1.6/TensorFlow-backend single-input, channels-first models with input shape `16 × 128 × 128`.
- The PyTorch reconstruction follows the saved graph: five convolution/batch-normalization/max-pooling + central crop concatenation blocks; `16→32→48→64→80→96` branch channels; final 4×4 convolution; dense 32→8→2; softmax.
- Kernels are transposed from Keras `(height, width, input, output)` to PyTorch `(output, input, height, width)`. Batch-normalization moving statistics and dense tensors were transferred from HDF5. Dropout is disabled at inference, as in Keras `predict`.
- Development-only integrity checks passed: deterministic identical-input outputs, finite probabilities, valid softmax row sums, and finite random-noise outputs.

## Why this is not a valid paper-level reproduction

1. The NPZ has four unnamed channels. The source gives no channel-to-ADC/T2 mapping, preprocessing recipe tied to the arrays, or sample/channel metadata. The mapping `0→ADC`, `3→T2` was fixed before evaluation but is an unverified assumption.
2. The released development arrays contain 323 records (200 training + 123 validation), not a verifiable 500-patient chronological cohort. They lack patient IDs and augmentation lineage, so patient-level five-fold CV and a new model cannot be performed.
3. The test labels have the published 60/140 class prevalence but carry no per-record semantic names. Class 0 is treated provisionally as GR from that prevalence only.
4. The original preprocessing in the paper describes 64×64×16 patches; public NPZ arrays are 4×16×128×128. The relationship is undocumented.
5. No original legacy runtime result was produced: Python 3.6/Keras 2.1.5/TensorFlow 1.4 is not a supported modern environment. The reconstruction is source/config-faithful, but numerical parity against the original runtime cannot be established without an author-provided reference prediction.

## Reproduction-strength classification

The planned AUROC-gap categories (strong ≤0.03, partial ≤0.05, failed >0.05) are **not assigned**. The observed gaps would be in the failed range, but assigning a model-level reproduction grade would imply channel and label mapping certainty that the public release does not provide. The appropriate conclusion is: *indeterminate public-release reproduction, with a predeclared mapping-dependent check that failed to match the published results.*

## Required author confirmation

The next message to the source authors should ask for: exact mapping of all four NPZ channels; test class-name/order; preprocessing/normalization values applied before saved-weight inference; a patient/augmentation manifest; expected predictions for a small checksum-identified sample; and release terms. A single author-provided ten-case input/output fixture would test numerical parity without reopening model selection.
