#!/usr/bin/env python3
"""Contract tests for model-level recommendations across canonical agents."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPECIALISTS = ("architecture", "code-quality", "data-api", "security", "ui-design")

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


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return " ".join(text.split()).lower()


def test_specialist_contracts() -> None:
    for specialist in SPECIALISTS:
        agent = read(ROOT / "canonical" / "agents" / f"{specialist}.md")
        skill_dir = ROOT / "canonical" / "skills" / specialist
        skill = read(skill_dir / "SKILL.md")
        reference_path = skill_dir / "references" / "model-selection.md"
        check(reference_path.is_file(), f"{specialist}: incluye matriz bajo demanda")
        reference = read(reference_path) if reference_path.is_file() else ""
        compact = normalized(reference)

        check("gate obligatorio de modelo" in normalized(agent), f"{specialist}: agente aplica el gate")
        check(
            "la primera respuesta visible empieza" in normalized(agent),
            f"{specialist}: agente hace observable la recomendación",
        )
        check(
            "termina el turno sin herramientas, incluida la skill" in normalized(agent)
            and "prohibido inspeccionar el proyecto" in normalized(agent),
            f"{specialist}: agente detiene el trabajo pesado antes del barrido",
        )
        check(
            "también para lo puntual" in normalized(agent)
            and "termina el turno" in normalized(agent)
            and "sin confirmar el modelo" in normalized(agent),
            f"{specialist}: agente pausa en trabajo puntual y reanuda sin declarar modelo",
        )
        check("model-selection.md" in skill, f"{specialist}: skill enlaza la matriz")
        check(
            "nunca nombres modelos/proveedores ni cambies el modelo del host" in normalized(skill),
            f"{specialist}: la regla puntual permanece genérica y manual",
        )
        check(
            "la primera respuesta visible debe comenzar" in normalized(skill),
            f"{specialist}: skill define el formato visible",
        )
        check(
            "termina el turno sin más herramientas" in normalized(skill),
            f"{specialist}: skill prohíbe trabajo tras el hard stop",
        )
        check(
            "para lo puntual" in normalized(skill)
            and "termina el turno" in normalized(skill)
            and "sin confirmar el modelo" in normalized(skill),
            f"{specialist}: skill pausa también el preflight puntual",
        )
        check(
            all(level in reference for level in ("`BAJO`", "`MEDIO`", "`ALTO`")),
            f"{specialist}: usa los tres niveles genéricos",
        )
        check("hard stop" in compact, f"{specialist}: distingue operaciones bloqueantes")
        check(
            "| si |" in compact
            and "termina el turno" in compact
            and "sin confirmar el modelo" in compact,
            f"{specialist}: matriz pausa todas las operaciones y no exige modelo",
        )
        check(
            "no menciones nombres de modelos, proveedores" in compact,
            f"{specialist}: permanece agnóstico de proveedor",
        )
        check(
            "documentation orchestrator" in compact and "no repitas el aviso" in compact,
            f"{specialist}: evita duplicar el gate orquestado",
        )
        check(
            "nunca selecciones ni cambies el modelo del host" in compact,
            f"{specialist}: no cambia el modelo del host",
        )
        check(len(reference.split()) <= 230, f"{specialist}: referencia respeta presupuesto")


def test_existing_agents_and_git_exception() -> None:
    markers = {
        "documentation-orchestrator": "Gate 0 de modelo",
        "project-navigator": "Aviso de modelo",
        "sdd": "Gate 0 de `sdd-spec`",
    }
    for agent_id, marker in markers.items():
        agent = read(ROOT / "canonical" / "agents" / f"{agent_id}.md")
        check(marker.lower() in normalized(agent), f"{agent_id}: conserva recomendación existente")

    orchestrator = normalized(read(ROOT / "canonical" / "skills" / "documentation-orchestrator" / "references" / "workflows.md"))
    navigator = normalized(read(ROOT / "canonical" / "skills" / "project-navigator" / "references" / "bootstrap.md"))
    check("termina el turno" in orchestrator and "responde \"continua\"" in orchestrator
          and "sin declarar qué modelo elegiste" in orchestrator,
          "orquestador conserva pausa y permite reanudar sin declarar modelo")
    navigator_after = navigator.split("**después:**", maxsplit=1)[1].split("## bootstrap asistido", maxsplit=1)[0]
    check("termina el turno" in navigator and "sin confirmar el modelo" in navigator
          and "ya puedes cambiar manualmente" in navigator_after
          and "termina el turno" not in navigator_after,
          "Navigator conserva pausa previa y aviso final no bloqueante")

    git_agent = read(ROOT / "canonical" / "agents" / "git-release-manager.md")
    check(
        "model-selection.md" not in git_agent and "gate 0 de modelo" not in normalized(git_agent),
        "git-release-manager: no añade un gate de modelo innecesario",
    )


def test_generated_parity() -> None:
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        for specialist in SPECIALISTS:
            canonical_reference = (
                ROOT / "canonical" / "skills" / specialist / "references" / "model-selection.md"
            )
            generated_reference = (
                ROOT / "generated" / platform / "skills" / specialist / "references" / "model-selection.md"
            )
            check(generated_reference.is_file(), f"{platform}/{specialist}: genera la matriz")
            if generated_reference.is_file():
                check(
                    generated_reference.read_bytes() == canonical_reference.read_bytes(),
                    f"{platform}/{specialist}: matriz coincide con canonical",
                )


def main() -> int:
    print("Contrato de recomendación de modelo — cobertura, coste y paridad")
    test_specialist_contracts()
    test_existing_agents_and_git_exception()
    test_generated_parity()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} comprobaciones correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
