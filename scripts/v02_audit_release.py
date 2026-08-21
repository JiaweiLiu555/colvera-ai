"""Audit the official Zhu et al. repository before any v0.2 inference.

This script writes metadata and hashes only.  It does not write beneath the
raw release directory, alter the official files, train a model, or create a
claim about unreleased patient identities.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.v02.data import RELEASE_ROOT, all_release_splits, release_file_inventory  # noqa: E402


def _record_digest(volume: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(volume).tobytes()).hexdigest()


def main() -> None:
    if not RELEASE_ROOT.exists():
        raise SystemExit("Official source repository is missing. Clone it into data/v02/raw/rectal_MR_DL first.")
    splits = all_release_splits()
    out_dir = ROOT / "outputs" / "v02" / "data-audit"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "data" / "v02" / "patient_manifest.csv"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    fingerprints: dict[str, list[str]] = {}
    for split_name, release in splits.items():
        for index, (volume, target) in enumerate(zip(release.images, release.targets_one_hot)):
            digest = _record_digest(volume)
            fingerprints.setdefault(digest, []).append(f"{split_name}:{index}")
            # The training/validation semantic class mapping is not documented in the NPZ.
            # The test mapping is inferred only from the published 60/140 prevalence and is
            # recorded as an inference, never as an independently verified pathology field.
            label = "good_responder_inferred_from_published_prevalence" if split_name == "test" and target[0] == 1 else (
                "non_good_responder_inferred_from_published_prevalence" if split_name == "test" else f"release_class_index_{int(target.argmax())}"
            )
            rows.append(
                {
                    "release_record_id": f"{split_name}_{index:04d}",
                    "patient_id": "not available in release",
                    "split": split_name,
                    "source_file": f"good_response/data/{split_name}_images_*.npz",
                    "array_row": index,
                    "release_class_index": int(target.argmax()),
                    "label_interpretation": label,
                    "label_confirmation": "pathology stated in paper; per-record pathology linkage not released",
                    "scan_date": "not available in release",
                    "scanner_field_strength": "not available per record",
                    "adc_available": "not independently documented; channel mapping absent",
                    "t2_available": "not independently documented; channel mapping absent",
                    "image_shape": "4x16x128x128",
                    "finite_values": bool(np.isfinite(volume).all()),
                    "zero_fraction": float((volume == 0).mean()),
                    "record_sha256": digest,
                    "image_quality_status": "release-level preprocessing only; no original-image quality metadata",
                }
            )
    manifest = pd.DataFrame(rows)
    manifest.to_csv(manifest_path, index=False)

    duplicate_groups = [entries for entries in fingerprints.values() if len(entries) > 1]
    counts = {}
    channel_stats = {}
    for name, release in splits.items():
        labels = release.label_index
        counts[name] = {
            "records": release.n_records,
            "class_index_0": int((labels == 0).sum()),
            "class_index_1": int((labels == 1).sum()),
            "shape": list(release.images.shape),
            "finite_values": bool(np.isfinite(release.images).all()),
            "exact_duplicate_records_within_or_across_release_arrays": int(sum(len(group) for group in duplicate_groups)),
        }
        channel_stats[name] = []
        for channel in range(release.images.shape[1]):
            values = release.images[:, channel]
            channel_stats[name].append(
                {
                    "channel_index": channel,
                    "min": float(values.min()), "p01": float(np.quantile(values, 0.01)),
                    "median": float(np.quantile(values, 0.5)), "p99": float(np.quantile(values, 0.99)),
                    "max": float(values.max()), "zero_fraction": float((values == 0).mean()),
                }
            )

    subprocess_result = subprocess.run(
        ["git", "-C", str(RELEASE_ROOT), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    )
    paper_training_claim = {"patients": 500, "good_responders": 116, "non_good_responders": 384}
    paper_test_claim = {"patients": 200, "good_responders": 60, "non_good_responders": 140}
    audit = {
        "audit_created_utc": datetime.now(timezone.utc).isoformat(),
        "source_repository": "https://github.com/radiologypkucancer/rectal_MR_DL",
        "source_repository_commit": subprocess_result.stdout.strip(),
        "raw_source_policy": "Read-only source files retained under data/v02/raw; outputs are written outside raw/.",
        "paper": {
            "citation": "Zhu HT et al., Frontiers in Oncology (2020), DOI 10.3389/fonc.2020.574337",
            "primary_outcome": "Good response: ypT0-1 AND ypN0; pathology after nCRT/TME.",
            "reported_training": paper_training_claim,
            "reported_test": paper_test_claim,
        },
        "release_arrays": counts,
        "release_development_total_records": int(counts["training"]["records"] + counts["validation"]["records"]),
        "release_development_limit": "323 array records are released (200 training + 123 validation), not a verified 500-patient development cohort. No patient IDs or augmentation lineage are supplied.",
        "patient_level_split_feasibility": "Not feasible: no patient IDs, dates, or augmentation lineage are released. The release must not be used for a claimed patient-level CV experiment.",
        "label_mapping_limit": "Test class-0 prevalence is 60/200 and therefore consistent with the paper's GR prevalence, but per-record outcome semantics are not embedded in the NPZ metadata.",
        "per_record_modality_mapping_limit": "The four image channels have no names or modality metadata in the NPZ. ADC/T2 channel assignment is not independently verifiable from the release.",
        "exact_duplicate_groups": duplicate_groups,
        "known_biases": [
            "Single-center retrospective study from Beijing Cancer Hospital; no external cohort in this release.",
            "Participants with insufficient image quality/noise were excluded in the paper, so real-world failure distribution is not represented.",
            "Release arrays are cropped/preprocessed and omit patient IDs, original DICOM, ROI provenance, scanner details, demographics, and date linkage.",
            "Development arrays have class proportions unlike the paper's 116/384 patient counts, consistent with transformed or otherwise undocumented records.",
        ],
        "licensing_and_access": "Public GitHub repository; no explicit LICENSE file found in the cloned release. Contact repository/paper authors before any reuse beyond research inspection.",
        "file_inventory": release_file_inventory(),
        "channel_statistics": channel_stats,
    }
    (out_dir / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")

    fig, axis = plt.subplots(figsize=(6.6, 3.6))
    labels = ["Released dev\nrecords", "Released test\nrecords", "Paper train\npatients", "Paper test\npatients"]
    values = [323, 200, 500, 200]
    bars = axis.bar(labels, values, color=["#4c78a8", "#f58518", "#9ecae9", "#f9c784"])
    axis.set_ylabel("Count")
    axis.set_title("Release arrays are not a verified 700-patient manifest")
    for bar, value in zip(bars, values):
        axis.text(bar.get_x() + bar.get_width() / 2, value + 10, str(value), ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_dir / "release_vs_paper_counts.png", dpi=180)
    plt.close(fig)

    lock = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Freeze official NPZ/HDF5 byte hashes before a single v0.2 released-weight test evaluation.",
        "test_cohort": "official release test_images/test_targets, 200 array records; patient IDs unavailable",
        "forbidden_before_final": "No result-driven model/channel/threshold changes; no training on test data.",
        "source_commit": subprocess_result.stdout.strip(),
        "file_hashes": [row for row in audit["file_inventory"] if row["path"].startswith("good_response/data/") or row["path"].startswith("good_response/weights/")],
    }
    lock_path = ROOT / "data" / "v02" / "test_lock.json"
    lock_path.write_text(json.dumps(lock, indent=2) + "\n")
    print(json.dumps({"manifest": str(manifest_path), "audit": str(out_dir / "audit.json"), "test_lock": str(lock_path)}, indent=2))


if __name__ == "__main__":
    main()
