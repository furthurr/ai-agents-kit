#!/usr/bin/env python3
"""Measure source-text volume for an explicitly observed prompt flow.

This reports file bytes, characters, lines and words, not model tokens. List each
agent, skill and reference actually loaded for the task; omit files not observed.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def text_stats(data: bytes) -> dict[str, int]:
    text = data.decode("utf-8")
    return {"bytes": len(data), "characters": len(text), "lines": len(text.splitlines()),
            "words": len(text.split())}


def measure(paths: list[str], baseline_ref: str | None = None) -> dict:
    """Measure unique, repository-relative source files without token estimates."""
    files = []
    seen: set[str] = set()
    for raw in paths:
        candidate = Path(raw)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"ruta debe ser relativa al repo: {raw}")
        source = ROOT / candidate
        if source.is_symlink():
            raise ValueError(f"symlink no admitido: {raw}")
        resolved = source.resolve()
        if not resolved.is_relative_to(ROOT):
            raise ValueError(f"ruta fuera del repo o symlink no admitido: {raw}")
        if not resolved.is_file():
            raise ValueError(f"archivo no encontrado: {raw}")
        relative = resolved.relative_to(ROOT).as_posix()
        if relative in seen:
            continue
        seen.add(relative)
        data = resolved.read_bytes()
        item = {"path": relative, **text_stats(data)}
        if baseline_ref:
            baseline = subprocess.run(["git", "show", f"{baseline_ref}:{relative}"],
                                      cwd=ROOT, capture_output=True, timeout=30)
            if baseline.returncode == 0:
                base = text_stats(baseline.stdout)
                item["baseline"] = base
                item["delta"] = {key: item[key] - base[key] for key in base}
            else:
                item["baseline"] = None
                item["delta"] = None
        files.append(item)
    result = {
        "measurement": "static source-text volume; not actual prompt/token usage",
        "files": files,
        "totals": {
            key: sum(item[key] for item in files)
            for key in ("bytes", "characters", "lines", "words")
        },
        "file_count": len(files),
    }
    comparable = [item for item in files if item.get("baseline") is not None]
    baselines = [item["baseline"] for item in comparable]
    if baseline_ref:
        result["baseline_ref"] = baseline_ref
        result["baseline_file_count"] = len(baselines)
        result["compared_file_count"] = len(comparable)
        result["compared_current_totals"] = {
            key: sum(item[key] for item in comparable)
            for key in ("bytes", "characters", "lines", "words")
        }
        result["baseline_totals"] = {
            key: sum(item[key] for item in baselines)
            for key in ("bytes", "characters", "lines", "words")
        }
        result["delta_totals"] = {
            key: result["compared_current_totals"][key] - result["baseline_totals"][key]
            for key in result["baseline_totals"]
        }
    return result


def inventory() -> dict:
    """Return repository-wide source inventory, explicitly not a task flow."""
    groups = {
        "agents": sorted((ROOT / "canonical/agents").glob("*.md")),
        "skills": sorted((ROOT / "canonical/skills").glob("*/SKILL.md")),
        "references": sorted((ROOT / "canonical/skills").glob("*/references/*.md")),
    }
    result = {name: measure([path.relative_to(ROOT).as_posix() for path in paths])
              for name, paths in groups.items()}
    return {"measurement": "repository inventory; not a task flow or actual tokens", "groups": result}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="Observed, repo-relative prompt sources; omit files not loaded")
    parser.add_argument("--label", default="observed-flow", help="Human-readable scenario label")
    parser.add_argument("--compare-ref", help="Optional Git ref for source-volume comparison")
    args = parser.parse_args(argv)
    try:
        if args.files:
            result = measure(args.files, args.compare_ref)
            result["label"] = args.label
        else:
            result = inventory()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"No se pudo medir: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
