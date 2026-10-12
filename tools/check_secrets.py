#!/usr/bin/env python3
"""Run the same read-only control distributed with the git-commit skill."""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    try:
        runpy.run_path(str(ROOT / "canonical/skills/git-commit/scripts/check_secrets.py"),
                       run_name="__main__")
    except OSError:
        print("Evaluación incompleta: control canónico no disponible.", file=sys.stderr)
        raise SystemExit(2)
