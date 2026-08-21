# v0.2 error analysis

## Aggregate error pattern

The predeclared ADC candidate assigned no record a provisional GR probability at or above 0.50. Its confusion matrix under the provisional label convention was TP 0, FP 0, TN 140, FN 60. The T2 candidate classified nearly every record as GR: TP 53, FP 122, TN 18, FN 7. These opposite degenerate patterns, plus near-chance AUROCs, point to a release/inference compatibility question rather than a clinically interpretable model failure pattern.

## What cannot be inspected responsibly

No error review is performed per patient. Record indices are not patient IDs, the image axes are unnamed, source ROIs and raw MRI are unavailable, and the outcome semantics are inferred from prevalence. Looking for visual explanations or claiming lesion-level failure modes would turn unverified arrays into fabricated clinical stories.

## Leading technical hypotheses to test with the authors

1. The fixed channels may not correspond to ADC/T2 in the saved models.
2. The weights may expect a source-specific normalization or array representation not preserved/documented in the current NPZ files.
3. The archived HDF5 assets and NPZ arrays may come from different preprocessing/training versions.
4. The one-hot class order may not match the prevalence-derived convention.
5. Numerical differences between legacy Keras/TensorFlow and reconstructed inference remain possible, though the layer graph/tensors were inspected and transferred directly.

The valid next action is a fixed author-provided input/output fixture and metadata, not test-channel sweeping or re-tuning.
