#!/usr/bin/env python3
"""
Integrity test suite for ai-agents-kit.

Verifies that after any structural reorganization:
- All referenced paths exist and resolve correctly.
- Scripts reference the correct REPO_ROOT/tools/generated directories.
- Python tools resolve ROOT to the actual repo root.
- The manifest, canonical sources, adapters, and generated artifacts are consistent.
- No broken cross-references between components.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent

PASSED = 0
FAILED = 0


def ok(msg: str) -> None:
    global PASSED
    PASSED += 1
    print(f"  \033[32m✓\033[0m {msg}")


def fail(msg: str) -> None:
    global FAILED
    FAILED += 1
    print(f"  \033[31m✗\033[0m {msg}")


def check(condition: bool, msg: str) -> None:
    if condition:
        ok(msg)
    else:
        fail(msg)


# ---------------------------------------------------------------------------
# 1. Project structure: essential directories and files exist
# ---------------------------------------------------------------------------
def test_project_structure() -> None:
    print("\n\033[1m[1] Estructura del proyecto\033[0m")

    essential_dirs = [
        "canonical",
        "canonical/agents",
        "canonical/skills",
        "adapters",
        "adapters/copilot",
        "adapters/opencode",
        "adapters/kiro",
        "adapters/claude",
        "generated",
        "generated/copilot",
        "generated/opencode",
        "generated/kiro",
        "generated/claude",
        "tools",
        "scripts",
        "scripts/install",
        "scripts/backup",
    ]
    for d in essential_dirs:
        check((ROOT / d).is_dir(), f"Directorio existe: {d}/")

    essential_files = [
        "canonical/manifest.json",
        "tools/render.py",
        "tools/validate.py",
        "tools/measure_context.py",
        "tools/import_installed.py",
        "tools/check_links.py",
        "tools/test_links.py",
        "tools/test_model_recommendations.py",
        "tools/test_mas_identity.py",
        "README.md",
        ".gitignore",
    ]
    for f in essential_files:
        check((ROOT / f).is_file(), f"Archivo existe: {f}")


# ---------------------------------------------------------------------------
# 2. No orphaned scripts in root (old layout remnants)
# ---------------------------------------------------------------------------
def test_no_root_scripts() -> None:
    print("\n\033[1m[2] Sin scripts huérfanos en la raíz\033[0m")

    orphans = [
        "install.sh", "install.ps1",
        "install-opencode.sh", "install-opencode.ps1",
        "install-kiro.sh", "install-kiro.ps1",
        "install-claude.sh", "install-claude.ps1",
        "backup.sh", "backup.ps1",
        "backup-opencode.sh", "backup-opencode.ps1",
        "backup-kiro.sh", "backup-kiro.ps1",
        "backup-claude.sh", "backup-claude.ps1",
    ]
    for name in orphans:
        check(not (ROOT / name).exists(), f"No existe en raíz: {name}")


# ---------------------------------------------------------------------------
# 3. Scripts in new locations exist and are executable
# ---------------------------------------------------------------------------
def test_scripts_exist() -> None:
    print("\n\033[1m[3] Scripts en nueva ubicación\033[0m")

    platforms = ["copilot", "opencode", "kiro", "claude"]
    for platform in platforms:
        for ext in ("sh", "ps1"):
            install = ROOT / "scripts" / "install" / f"{platform}.{ext}"
            backup = ROOT / "scripts" / "backup" / f"{platform}.{ext}"
            check(install.is_file(), f"Existe: scripts/install/{platform}.{ext}")
            check(backup.is_file(), f"Existe: scripts/backup/{platform}.{ext}")


# ---------------------------------------------------------------------------
# 4. Bash scripts resolve REPO_ROOT correctly (not SCRIPT_DIR for paths)
# ---------------------------------------------------------------------------
def test_bash_repo_root_references() -> None:
    print("\n\033[1m[4] Referencias REPO_ROOT en scripts bash\033[0m")

    for script_path in (ROOT / "scripts").rglob("*.sh"):
        content = script_path.read_text(encoding="utf-8")
        rel = script_path.relative_to(ROOT)

        # Must define REPO_ROOT
        check('REPO_ROOT=' in content, f"{rel}: define REPO_ROOT")

        # Must NOT use $SCRIPT_DIR/generated or $SCRIPT_DIR/tools
        has_bad_ref = (
            "$SCRIPT_DIR/generated" in content
            or "$SCRIPT_DIR/tools" in content
            or '"$SCRIPT_DIR"/generated' in content
            or '"$SCRIPT_DIR"/tools' in content
        )
        check(not has_bad_ref, f"{rel}: no usa $SCRIPT_DIR para generated/tools")


# ---------------------------------------------------------------------------
# 5. PowerShell scripts resolve $RepoRoot correctly
# ---------------------------------------------------------------------------
def test_ps1_repo_root_references() -> None:
    print("\n\033[1m[5] Referencias $RepoRoot en scripts PowerShell\033[0m")

    for script_path in (ROOT / "scripts").rglob("*.ps1"):
        content = script_path.read_text(encoding="utf-8")
        rel = script_path.relative_to(ROOT)

        # Must define $RepoRoot
        check("$RepoRoot" in content or "$RepoRoot" in content, f"{rel}: define $RepoRoot")

        # Must NOT use $ScriptDir for generated or tools paths
        has_bad_ref = (
            '$ScriptDir\\tools' in content
            or '$ScriptDir\\generated' in content
            or "$ScriptDir\\tools" in content
            or "$ScriptDir\\generated" in content
            or '"$ScriptDir\\tools' in content
            or '"$ScriptDir\\generated' in content
        )
        check(not has_bad_ref, f"{rel}: no usa $ScriptDir para generated/tools")


# ---------------------------------------------------------------------------
# 6. Python tools ROOT resolves to actual repo root
# ---------------------------------------------------------------------------
def test_python_root_resolution() -> None:
    print("\n\033[1m[6] Python tools: ROOT resuelve a la raíz del repo\033[0m")

    tools = ["render.py", "validate.py", "import_installed.py", "measure_context.py"]
    for tool in tools:
        tool_path = ROOT / "tools" / tool
        content = tool_path.read_text(encoding="utf-8")
        # All use: ROOT = Path(__file__).resolve().parent.parent
        check("parent.parent" in content, f"tools/{tool}: ROOT usa parent.parent")
        # Verify it would resolve to the actual ROOT
        resolved = tool_path.resolve().parent.parent
        check(resolved == ROOT, f"tools/{tool}: ROOT resuelve a {ROOT.name}/")


# ---------------------------------------------------------------------------
# 7. Manifest integrity: all declared skills and agents have sources
# ---------------------------------------------------------------------------
def test_manifest_integrity() -> None:
    print("\n\033[1m[7] Integridad del manifiesto\033[0m")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))

    for skill_id in manifest["skills"]:
        skill_file = ROOT / "canonical" / "skills" / skill_id / "SKILL.md"
        check(skill_file.is_file(), f"Skill canónica existe: {skill_id}")

    for agent_id in manifest["agents"]:
        agent_file = ROOT / "canonical" / "agents" / f"{agent_id}.md"
        check(agent_file.is_file(), f"Agente canónico existe: {agent_id}")

    for platform in manifest["platforms"]:
        platform_json = ROOT / "adapters" / platform / "platform.json"
        check(platform_json.is_file(), f"Adaptador de plataforma existe: {platform}")

        for agent_id in manifest["agents"]:
            adapter = ROOT / "adapters" / platform / "agents" / f"{agent_id}.json"
            check(adapter.is_file(), f"Adaptador {platform}/{agent_id}.json existe")


# ---------------------------------------------------------------------------
# 8. Generated artifacts match manifest
# ---------------------------------------------------------------------------
def test_generated_artifacts() -> None:
    print("\n\033[1m[8] Artefactos generados completos\033[0m")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))

    for platform in manifest["platforms"]:
        gen_skills = ROOT / "generated" / platform / "skills"
        gen_agents = ROOT / "generated" / platform / "agents"

        check(gen_skills.is_dir(), f"generated/{platform}/skills/ existe")
        check(gen_agents.is_dir(), f"generated/{platform}/agents/ existe")

        for skill_id in manifest["skills"]:
            skill_dir = gen_skills / skill_id
            check(skill_dir.is_dir(), f"generated/{platform}/skills/{skill_id}/ existe")
            check((skill_dir / "SKILL.md").is_file(), f"generated/{platform}/skills/{skill_id}/SKILL.md existe")

        for agent_id in manifest["agents"]:
            adapter = json.loads(
                (ROOT / "adapters" / platform / "agents" / f"{agent_id}.json").read_text(encoding="utf-8")
            )
            filename = adapter["filename"]
            agent_file = gen_agents / filename
            check(agent_file.is_file(), f"generated/{platform}/agents/{filename} existe")


# ---------------------------------------------------------------------------
# 9. Kiro agents frontmatter: match field is array (the fix we applied)
# ---------------------------------------------------------------------------
def test_kiro_frontmatter_match_is_array() -> None:
    print("\n\033[1m[9] Kiro: permissions.rules[].match es array\033[0m")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))

    for agent_id in manifest["agents"]:
        adapter_path = ROOT / "adapters" / "kiro" / "agents" / f"{agent_id}.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        rules = adapter.get("frontmatter", {}).get("permissions", {}).get("rules", [])
        all_arrays = all(isinstance(rule.get("match"), list) for rule in rules)
        check(all_arrays, f"adapters/kiro/agents/{agent_id}.json: match es array")

        # Also check the generated artifact
        gen_path = ROOT / "generated" / "kiro" / "agents" / adapter["filename"]
        if gen_path.is_file():
            content = gen_path.read_text(encoding="utf-8")
            # In YAML, match as string would look like: match: "something"
            # match as array would look like: match:\n        - "something"
            bad_match = re.findall(r'^\s+match: "', content, re.MULTILINE)
            check(len(bad_match) == 0, f"generated/kiro/agents/{adapter['filename']}: match YAML es lista")


# ---------------------------------------------------------------------------
# 10. Claude agents are hidden from the VS Code/Copilot picker
# ---------------------------------------------------------------------------
def test_claude_agents_hidden_from_vscode() -> None:
    print("\n\033[1m[10] Claude: agentes ocultos del selector de VS Code\033[0m")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))

    for agent_id in manifest["agents"]:
        adapter_path = ROOT / "adapters" / "claude" / "agents" / f"{agent_id}.json"
        adapter = json.loads(adapter_path.read_text(encoding="utf-8"))
        frontmatter = adapter.get("frontmatter", {})
        check(
            frontmatter.get("user-invocable") is False,
            f"{adapter_path.relative_to(ROOT)}: user-invocable es false",
        )

        generated_path = ROOT / "generated" / "claude" / "agents" / adapter["filename"]
        content = generated_path.read_text(encoding="utf-8") if generated_path.is_file() else ""
        check(
            bool(re.search(r"^user-invocable: false$", content, re.MULTILINE)),
            f"{generated_path.relative_to(ROOT)}: selector de VS Code no lo muestra",
        )


# 11. validate.py passes (the gold standard)
# ---------------------------------------------------------------------------
def test_validate_passes() -> None:
    print("\n\033[1m[11] tools/validate.py pasa correctamente\033[0m")

    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "validate.py")],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    check(result.returncode == 0, f"validate.py exit code 0: {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"      stderr: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# 12. README references match actual file locations
# ---------------------------------------------------------------------------
def test_readme_references() -> None:
    print("\n\033[1m[12] README.md: referencias a rutas existentes\033[0m")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    # Check that README references the new script paths, not the old ones
    check("scripts/install/copilot.sh" in readme, "README referencia scripts/install/copilot.sh")
    check("scripts/install/opencode.sh" in readme, "README referencia scripts/install/opencode.sh")
    check("scripts/install/kiro.sh" in readme, "README referencia scripts/install/kiro.sh")
    check("scripts/install/claude.sh" in readme, "README referencia scripts/install/claude.sh")
    check("scripts/backup/" in readme, "README referencia scripts/backup/")

    # Should NOT reference old root scripts
    check("./install.sh" not in readme, "README no referencia ./install.sh (viejo)")
    check("./install-kiro.sh" not in readme, "README no referencia ./install-kiro.sh (viejo)")
    check("./backup.sh" not in readme, "README no referencia ./backup.sh (viejo)")


# ---------------------------------------------------------------------------
# 13. Negative test suite passes (tools/test_validate.py)
# ---------------------------------------------------------------------------
def test_negative_suite_passes() -> None:
    print("\n\033[1m[13] tools/test_validate.py (pruebas negativas) pasa\033[0m")

    suite = ROOT / "tools" / "test_validate.py"
    check(suite.is_file(), "tools/test_validate.py existe")
    result = subprocess.run(
        [sys.executable, str(suite)],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    check(result.returncode == 0, "test_validate.py exit code 0")
    if result.returncode != 0:
        print(f"      stderr: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# 14. Markdown link checks pass
# ---------------------------------------------------------------------------
def test_link_checker_passes() -> None:
    print("\n\033[1m[14] Enlaces Markdown\033[0m")

    for tool in ("check_links.py", "test_links.py"):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools" / tool)],
            capture_output=True, text=True, cwd=str(ROOT)
        )
        check(result.returncode == 0, f"tools/{tool} exit code 0")
        if result.returncode != 0:
            print(f"      stderr: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# 15. Model recommendation contracts pass
# ---------------------------------------------------------------------------
def test_model_recommendations_pass() -> None:
    print("\n\033[1m[15] Recomendaciones de modelo\033[0m")

    suite = ROOT / "tools" / "test_model_recommendations.py"
    result = subprocess.run(
        [sys.executable, str(suite)],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    check(result.returncode == 0, "test_model_recommendations.py exit code 0")
    if result.returncode != 0:
        print(f"      stderr: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# 16. Data & API interactive documentation workflow is present everywhere
# ---------------------------------------------------------------------------
def test_data_api_scalar_workflow() -> None:
    print("\n\033[1m[16] Data & API: flujo interactivo con Scalar\033[0m")

    reference = ROOT / "canonical" / "skills" / "data-api" / "references" / "api-docs.md"
    skill = (ROOT / "canonical" / "skills" / "data-api" / "SKILL.md").read_text(encoding="utf-8")
    agent = (ROOT / "canonical" / "agents" / "data-api.md").read_text(encoding="utf-8")

    check(reference.is_file(), "Referencia canónica de Scalar existe")
    reference_content = reference.read_text(encoding="utf-8") if reference.is_file() else ""
    for marker in ("@scalar/cli", "--install", "--serve", "document serve", "127.0.0.1"):
        check(marker in reference_content, f"Referencia Scalar contiene: {marker}")
    check("references/api-docs.md" in skill, "La skill carga la referencia de Scalar bajo demanda")
    check(
        "La ausencia de OpenAPI bloquea la ejecución del lanzador, no su creación." in reference_content,
        "La referencia crea el lanzador aunque falte OpenAPI",
    )
    check(
        "cualquier combinación con `--install` deben terminar con error" in reference_content,
        "La referencia bloquea instalación y servicio sin OpenAPI",
    )
    check(
        "Sin OpenAPI válido: no se genera ni se sirve la referencia" not in reference_content,
        "La referencia no conserva la regla contradictoria anterior",
    )
    check("estado `bloqueado`" in skill, "La skill documenta el estado bloqueado")
    check("aunque todavía falte OpenAPI" in agent, "El agente prepara el lanzador sin OpenAPI")

    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        generated = ROOT / "generated" / platform / "skills" / "data-api" / "references" / "api-docs.md"
        check(generated.is_file(), f"Referencia Scalar generada para {platform}")


# ---------------------------------------------------------------------------
# 17. MAS identity contract passes
# ---------------------------------------------------------------------------
def test_mas_identity_pass() -> None:
    print("\n\033[1m[17] Identidad MAS\033[0m")

    suite = ROOT / "tools" / "test_mas_identity.py"
    result = subprocess.run(
        [sys.executable, str(suite)],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    check(result.returncode == 0, "test_mas_identity.py exit code 0")
    if result.returncode != 0:
        print(f"      stderr: {result.stderr.strip()}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    print(f"\033[1m{'='*60}\033[0m")
    print(f"\033[1m  Test de Integridad — ai-agents-kit\033[0m")
    print(f"\033[1m  Raíz: {ROOT}\033[0m")
    print(f"\033[1m{'='*60}\033[0m")

    test_project_structure()
    test_no_root_scripts()
    test_scripts_exist()
    test_bash_repo_root_references()
    test_ps1_repo_root_references()
    test_python_root_resolution()
    test_manifest_integrity()
    test_generated_artifacts()
    test_kiro_frontmatter_match_is_array()
    test_claude_agents_hidden_from_vscode()
    test_validate_passes()
    test_readme_references()
    test_negative_suite_passes()
    test_link_checker_passes()
    test_model_recommendations_pass()
    test_data_api_scalar_workflow()
    test_mas_identity_pass()

    print(f"\n\033[1m{'='*60}\033[0m")
    total = PASSED + FAILED
    if FAILED == 0:
        print(f"\033[32m  Todos los tests pasaron: {PASSED}/{total}\033[0m")
    else:
        print(f"\033[31m  {FAILED} tests fallaron de {total}\033[0m")
    print(f"\033[1m{'='*60}\033[0m\n")

    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
