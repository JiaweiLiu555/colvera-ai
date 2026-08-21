"""Validate an approved de-identified longitudinal Colvera manifest.

Usage: .venv/bin/python scripts/validate_longitudinal_manifest.py path/to/manifest.csv
This performs no image loading, no training, and no external upload.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.longitudinal import validate_manifest  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_longitudinal_manifest.py path/to/deidentified_manifest.csv")
    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.is_file():
        raise SystemExit(f"Manifest not found: {path}")
    audit = validate_manifest(pd.read_csv(path))
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
