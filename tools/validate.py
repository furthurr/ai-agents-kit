#!/usr/bin/env python3
"""Validate canonical definitions, adapters, and reproducible generated artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLATFORM_MARKERS = ("GitHub Copilot", "opencode", ".github/copilot-instructions.md", "VS Code")


def digest_tree(path: Path) -> dict[str, str]:
    return {
        str(file.relative_to(path)): hashlib.sha256(file.read_bytes()).hexdigest()
        for file in sorted(path.rglob("*"))
        if file.is_file()
    }


def main() -> int:
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    errors: list[str] = []
    platform_substitutions: dict[str, set[str]] = {}
    for platform in manifest["platforms"]:
        platform_dir = ROOT / "adapters" / platform
        if not (platform_dir / "platform.json").is_file():
            errors.append(f"Falta el adaptador de plataforma: {platform}")
            continue
        platform_substitutions[platform] = set(json.loads((platform_dir / "platform.json").read_text(encoding="utf-8")).get("substitutions", {}))
        for skill_id in manifest["skills"]:
            if not (ROOT / "canonical" / "skills" / skill_id / "SKILL.md").is_file():
                errors.append(f"Falta la skill canónica: {skill_id}")
        for agent_id in manifest["agents"]:
            if not (ROOT / "canonical" / "agents" / f"{agent_id}.md").is_file():
                errors.append(f"Falta el agente canónico: {agent_id}")
            adapter = platform_dir / "agents" / f"{agent_id}.json"
            if not adapter.is_file():
                errors.append(f"Falta el adaptador {platform} del agente {agent_id}")
                continue
            data = json.loads(adapter.read_text(encoding="utf-8"))
            if not data.get("filename") or not data.get("frontmatter"):
                errors.append(f"Adaptador incompleto: {adapter.relative_to(ROOT)}")

    canonical_files = list((ROOT / "canonical" / "agents").glob("*.md")) + list((ROOT / "canonical" / "skills").glob("*/SKILL.md"))
    for path in canonical_files:
        content = path.read_text(encoding="utf-8")
        for marker in PLATFORM_MARKERS:
            if marker.lower() in content.lower():
                errors.append(f"Referencia específica de plataforma en {path.relative_to(ROOT)}: {marker}")
        tokens = set(re.findall(r"\{\{[^{}]+\}\}", content))
        for platform, substitutions in platform_substitutions.items():
            missing = tokens - substitutions
            if missing:
                errors.append(f"Tokens sin adaptador para {platform} en {path.relative_to(ROOT)}: {', '.join(sorted(missing))}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    before = {platform: digest_tree(ROOT / "generated" / platform) for platform in manifest["platforms"]}
    with tempfile.TemporaryDirectory() as temporary:
        backup = Path(temporary) / "generated"
        (ROOT / "generated").rename(backup)
        try:
            subprocess.run([sys.executable, str(ROOT / "tools" / "render.py")], check=True)
            after = {platform: digest_tree(ROOT / "generated" / platform) for platform in manifest["platforms"]}
        finally:
            shutil_path = ROOT / "generated"
            if shutil_path.exists():
                import shutil
                shutil.rmtree(shutil_path)
            backup.rename(shutil_path)
    if before != after:
        print("Los artefactos generados no coinciden con la fuente canónica. Ejecuta tools/render.py.", file=sys.stderr)
        return 1

    print(f"Validación correcta: {len(manifest['skills'])} skills y {len(manifest['agents'])} agentes en {len(manifest['platforms'])} plataformas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
