"""Download the approved public Zenodo source and verify its published MD5 checksum."""

from __future__ import annotations

import json
import os
import shutil
import ssl
import sys
import tempfile
import urllib.request
from pathlib import Path

import certifi

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from colvera.data import RAW_FILE, load_config, md5sum  # noqa: E402


def main() -> None:
    cfg = load_config()
    url = "https://zenodo.org/api/records/8379940/files/MRI%20RADIOMICS-rectal%20carcinoma%20data%20repository-nCRT%20-%2071-patients.xlsx/content"
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {cfg['name']}…")
    context = ssl.create_default_context(cafile=certifi.where())
    with tempfile.NamedTemporaryFile(dir=RAW_FILE.parent, suffix=".partial", delete=False) as handle:
        temporary = Path(handle.name)
        with urllib.request.urlopen(url, context=context) as response:
            shutil.copyfileobj(response, handle)
    observed = md5sum(temporary)
    if observed != cfg["expected_md5"]:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Checksum mismatch: expected {cfg['expected_md5']}, got {observed}.")
    os.replace(temporary, RAW_FILE)
    provenance = {
        "source": cfg["record_url"],
        "doi": cfg["doi"],
        "license": cfg["license"],
        "filename": RAW_FILE.name,
        "md5": observed,
    }
    (ROOT / "data" / "raw" / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"Verified MD5 {observed}; saved {RAW_FILE}")


if __name__ == "__main__":
    main()
