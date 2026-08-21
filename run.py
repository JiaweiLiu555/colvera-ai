"""Rebuild saved research artifacts, then open the Colvera product demo."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "raw" / "rectal_mri_radiomics_71.xlsx"


def run(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


if __name__ == "__main__":
    if not DATA.exists():
        run("scripts/download_dataset.py")
    run("scripts/audit_dataset.py")
    run("scripts/run_experiment.py")
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.headless=true",
            "--browser.gatherUsageStats=false",
        ],
        cwd=ROOT,
        check=True,
    )
