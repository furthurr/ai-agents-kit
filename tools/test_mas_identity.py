#!/usr/bin/env python3
"""Contract tests for the MAS identity across canonical and generated prompts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MARKERS = ("Multi-Agent System", "MAS:", "@<agente>", "MASVS", "MASWE", "MASTG")
PASSED = 0
FAILED = 0


def check(condition: bool, message: str) -> None:
    global PASSED, FAILED
    if condition:
        PASSED += 1
        print(f"  PASS {message}")
    else:
        FAILED += 1
        print(f"  FAIL {message}")


def content_has_identity(path: Path, label: str) -> None:
    check(path.is_file(), f"{label}: existe")
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8")
    check(all(marker in content for marker in MARKERS), f"{label}: conserva identidad MAS")


def main() -> int:
    print("Contrato de identidad MAS — fuentes canónicas y artefactos generados")

    docs = ROOT / "docs" / "mas.md"
    content_has_identity(docs, "docs/mas.md")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    check(bool(re.fullmatch(r"0\.1\.0", version)), "VERSION: primera release 0.1.0")
    check((ROOT / ".release" / "README.md").is_file(), ".release/README.md: existe")
    check((ROOT / ".release" / "config.md").is_file(), ".release/config.md: existe")
    check((ROOT / "CHANGELOG.md").is_file(), "CHANGELOG.md: existe")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    check("## [0.1.0] - 2026-09-15" in changelog, "CHANGELOG.md: incluye 0.1.0")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for agent_id in manifest["agents"]:
        content_has_identity(ROOT / "canonical" / "agents" / f"{agent_id}.md", f"canonical agent {agent_id}")
    for skill_id in manifest["skills"]:
        content_has_identity(ROOT / "canonical" / "skills" / skill_id / "SKILL.md", f"canonical skill {skill_id}")

    for platform in manifest["platforms"]:
        adapter_root = ROOT / "adapters" / platform
        for agent_id in manifest["agents"]:
            adapter = json.loads((adapter_root / "agents" / f"{agent_id}.json").read_text(encoding="utf-8"))
            filename = adapter["filename"]
            content_has_identity(ROOT / "generated" / platform / "agents" / filename, f"{platform} agent {agent_id}")
        for skill_id in manifest["skills"]:
            content_has_identity(
                ROOT / "generated" / platform / "skills" / skill_id / "SKILL.md",
                f"{platform} skill {skill_id}",
            )

    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
