#!/usr/bin/env python3
"""Contract tests for the MAS identity across canonical and generated prompts."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOC_MARKERS = ("Multi-Agent System", "MAS:", "@<agente>")
RENDERED_IDENTITY = "MAS significa **Multi-Agent System**"
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


def content_has_identity(path: Path, label: str, *, canonical: bool = False) -> None:
    check(path.is_file(), f"{label}: existe")
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8")
    expected = "{{mas_identity}}" if canonical else RENDERED_IDENTITY
    check(expected in content, f"{label}: identidad compartida presente")


def main() -> int:
    print("Contrato de identidad MAS — fuentes canónicas y artefactos generados")

    docs = ROOT / "docs" / "mas.md"
    check(docs.is_file(), "docs/mas.md: existe")
    if docs.is_file():
        docs_content = docs.read_text(encoding="utf-8")
        check(all(marker in docs_content for marker in DOC_MARKERS),
              "docs/mas.md: identidad y convención completas")

    shared_identity = ROOT / "canonical/shared/mas-identity.md"
    content_has_identity(shared_identity, "canonical/shared/mas-identity.md")
    shared_content = shared_identity.read_text(encoding="utf-8") if shared_identity.is_file() else ""
    check(all(marker in shared_content for marker in DOC_MARKERS),
          "fragmento compartido conserva la convención compacta")

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    check(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "VERSION: SemVer válida")
    check((ROOT / ".release" / "README.md").is_file(), ".release/README.md: existe")
    check((ROOT / ".release" / "config.md").is_file(), ".release/config.md: existe")
    check((ROOT / "CHANGELOG.md").is_file(), "CHANGELOG.md: existe")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    check(f"## [{version}] - " in changelog, f"CHANGELOG.md: incluye {version}")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for agent_id in manifest["agents"]:
        content_has_identity(ROOT / "canonical" / "agents" / f"{agent_id}.md",
                             f"canonical agent {agent_id}", canonical=True)
    for skill_id in manifest["skills"]:
        content_has_identity(ROOT / "canonical" / "skills" / skill_id / "SKILL.md",
                             f"canonical skill {skill_id}", canonical=True)

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

    security = ROOT / "canonical/skills/security/SKILL.md"
    check(security.is_file() and "MASVS" in security.read_text(encoding="utf-8"),
          "referencias OWASP permanecen en el dominio de seguridad, no en la identidad común")

    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
