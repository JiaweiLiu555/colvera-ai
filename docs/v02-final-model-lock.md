# v0.2 final evaluation lock

**Lock created:** 2026-08-16, before final test performance evaluation.

## Purpose

This lock prevents post-hoc choice among model architectures, channels, thresholds, or ensemble rules. It applies only to the official released 200-record `good_response` test array hashed in `data/v02/test_lock.json`.

## Fixed evaluation candidates

| Fixed identifier | HDF5 source | Fixed input | Output used | Status |
|---|---|---|---|---|
| `published_adc_reproduction` | `good_response/weights/weights_ADC.hdf5` | release channel 0 | softmax class 0, provisional GR | Released-weight reproduction audit |
| `published_t2_reproduction` | `good_response/weights/weights_T2.hdf5` | release channel 3 | softmax class 0, provisional GR | Released-weight reproduction audit |

The `ADC = channel 0` and `T2 = channel 3` assignments are **provisional and unverified** because the NPZ source omits channel names. They were fixed before evaluation based on the intended modalities in the filenames and release-array intensity/coverage inspection. They must not be changed after seeing test metrics. If either check fails to reproduce the paper reasonably, that is a result, not a reason to change the mapping.

## Fixed architecture and inference

- One `16 × 128 × 128` input per model, channels-first.
- Exact saved-weight architecture reconstructed from the HDF5 Keras configuration: five Conv2D/BN/max-pooling + centre-crop concatenation blocks, final convolution, dense 32 → 8 → 2, softmax.
- CPU inference, PyTorch in evaluation mode; dropout inactive, matching Keras `predict` behavior.
- Positive outcome: class 0 interpreted provisionally as GR because test prevalence is 60/200, matching the paper's reported 60 GR / 140 non-GR. The source does not supply class names in NPZ metadata.
- Descriptive decision threshold: `p(GR) >= 0.50`. This threshold is not claimed to be the authors' operating threshold and is not selected on the test cohort.

## Explicitly excluded candidates

- No novel `colvera_adc_v02` training run: patient identities/augmentation lineage are unavailable, so a patient-level development split and leakage check cannot be made.
- No ADC+T2 fusion: per-record channel identity/pairing is not verified and no valid development selection cohort exists.
- No clinical model: no released clinical fields.
- No learned retrieval: no verified patient-level training set; no retrieval metrics will be claimed.
- No calibration refit: calibration fitting would require a valid development cohort. Held-out calibration is descriptive only.

## One-pass rule

`scripts/v02_run_final_evaluation.py` refuses to overwrite an existing `outputs/v02/final-test/final_results.json`. It writes source weight hashes, predictions, bootstrap intervals, calibration, abstention summary, and figures on the one permitted final run. Any later analysis requires a new dataset/version and a new registered lock.

## Execution note

The first invocation on 2026-08-16 failed after deterministic ADC inference but before exposing a metric or writing any prediction/result artifact: a bootstrap precision interval had no finite resamples when its denominator was zero. The only repair permits a `null` confidence interval for an undefined metric; it does not change a candidate, weight, channel, class convention, threshold, test input, seed, or metric formula. The rerun is the recorded final saved execution.
