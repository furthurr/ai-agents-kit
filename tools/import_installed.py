#!/usr/bin/env python3
"""Import declared installed artifacts for review without changing canonical sources."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=("copilot", "opencode", "kiro"))
    parser.add_argument("--skills-dir", required=True, type=Path)
    parser.add_argument("--agents-dir", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    expected_skills = set(manifest["skills"])
    expected_agents = {
        json.loads((ROOT / "adapters" / arguments.platform / "agents" / f"{agent_id}.json").read_text(encoding="utf-8"))["filename"]
        for agent_id in manifest["agents"]
    }
    label = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = ROOT / "imports" / arguments.platform / label
    copied = 0
    for source_root, expected, section in ((arguments.skills_dir, expected_skills, "skills"), (arguments.agents_dir, expected_agents, "agents")):
        if not source_root.is_dir():
            print(f"No existe {source_root}; se omite {section}.")
            continue
        entries = {entry.name: entry for entry in source_root.iterdir() if entry.name != ".DS_Store"}
        for name in sorted(entries):
            if name not in expected:
                print(f"Se ignora elemento ajeno al kit: {section}/{name}")
        for name in sorted(expected):
            source = entries.get(name)
            if source is None:
                print(f"No instalado: {section}/{name}")
                continue
            target = destination / section / name
            print(f"Importar {source} -> {target}")
            copied += 1
            if not arguments.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir():
                    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".DS_Store"))
                else:
                    shutil.copy2(source, target)
    if copied and not arguments.dry_run:
        print(f"Importación creada en {destination}. Revisa y promociona los cambios manualmente a canonical/ o adapters/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
