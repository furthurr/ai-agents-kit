#!/usr/bin/env python3
"""Render platform artifacts from canonical prompts and declarative adapters."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "canonical"
ADAPTERS = ROOT / "adapters"
GENERATED = ROOT / "generated"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def yaml_value(value: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            yaml_key = key if key.replace("_", "").replace("-", "").isalnum() else json.dumps(key, ensure_ascii=False)
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}{yaml_key}:")
                lines.extend(yaml_value(item, indent + 2))
            else:
                lines.append(f"{prefix}{yaml_key}: {json.dumps(item, ensure_ascii=False)}")
        return lines
    if isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(yaml_value(item, indent + 2))
            else:
                lines.append(f"{prefix}- {json.dumps(item, ensure_ascii=False)}")
        return lines
    return [f"{prefix}{json.dumps(value, ensure_ascii=False)}"]


def frontmatter(data: dict[str, Any]) -> str:
    return "---\n" + "\n".join(yaml_value(data)) + "\n---\n\n"


def substitute(text: str, substitutions: dict[str, str], context: str) -> str:
    for source, target in substitutions.items():
        text = text.replace(source, target)
    if "{{" in text or "}}" in text:
        raise ValueError(f"Token sin resolver en {context}")
    return text


def render_platform(manifest: dict[str, Any], platform: str) -> None:
    platform_dir = ADAPTERS / platform
    config = load_json(platform_dir / "platform.json")
    output = GENERATED / platform
    if output.exists():
        shutil.rmtree(output)

    global_substitutions = config.get("substitutions", {})
    for skill_id in manifest["skills"]:
        skill_dir = CANONICAL / "skills" / skill_id
        skill = skill_dir / "SKILL.md"
        adapter_path = platform_dir / "skills" / f"{skill_id}.json"
        adapter = load_json(adapter_path) if adapter_path.exists() else {}
        substitutions = {**global_substitutions, **adapter.get("substitutions", {})}
        content = substitute(skill.read_text(encoding="utf-8"), substitutions, f"{platform} skill {skill_id}")
        destination_dir = output / "skills" / skill_id
        shutil.copytree(skill_dir, destination_dir)
        (destination_dir / "SKILL.md").write_text(content, encoding="utf-8")

    for agent_id in manifest["agents"]:
        agent = CANONICAL / "agents" / f"{agent_id}.md"
        adapter_path = platform_dir / "agents" / f"{agent_id}.json"
        adapter = load_json(adapter_path)
        substitutions = {**global_substitutions, **adapter.get("substitutions", {})}
        body = substitute(agent.read_text(encoding="utf-8"), substitutions, f"{platform} agent {agent_id}")
        destination = output / "agents" / f"{adapter['filename']}"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(frontmatter(adapter["frontmatter"]) + body, encoding="utf-8")


def main() -> int:
    manifest = load_json(CANONICAL / "manifest.json")
    for platform in manifest["platforms"]:
        render_platform(manifest, platform)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"render error: {error}", file=sys.stderr)
        raise SystemExit(1)
