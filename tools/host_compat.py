#!/usr/bin/env python3
"""Detect installed host versions and explain the compatibility contract.

The kit keeps one distributive format per platform unless an older host cannot
read it. This helper makes that trade-off visible at install time instead of
letting an old host silently ignore the generated artifacts.

It never edits host configuration. Warnings are informational by default;
``--strict`` turns a known-incompatible host into a non-zero exit so CI or a
deliberate installation can fail before copying anything.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "canonical" / "manifest.json"

# Minimums and validated versions for the human-facing compatibility page.
# Keep this table aligned with docs/compatibilidad-hosts.md.
MATRIX: dict[str, dict[str, str]] = {
    "copilot": {
        "host": "GitHub Copilot CLI / VS Code",
        "minimum": "CLI 1.x o VS Code actual",
        "validated": "CLI 1.0.109; VS Code 1.145.3",
        "format": "`~/.copilot/skills` + `~/.copilot/agents/*.agent.md`",
        "legacy": "El formato `.agent.md` y los alias de tools son estables.",
    },
    "opencode": {
        "host": "OpenCode",
        "minimum": "1.18+ (formato V1) / 2.x lo traduce",
        "validated": "1.18.34 (V1) y 2.2.7 (V2)",
        "format": "`~/.config/opencode/skills` + `~/.config/opencode/agent/*.md`",
        "legacy": "Se conserva el frontmatter V1; V2 lo traduce. `temperature` no se aplica en V2.",
    },
    "kiro": {
        "host": "Kiro IDE / Kiro CLI",
        "minimum": "IDE 1.0+; CLI 2.37+ con motor V3, o CLI 3.x",
        "validated": "IDE 1.4.154; CLI 2.37.1 (V3 opt-in)",
        "format": "`~/.kiro/skills` + `~/.kiro/agents/*.md` (Markdown V3)",
        "legacy": "CLI 2.x en modo V2 ignora los `.md`; conserva tus JSON y usa `--v3` o `chat.agentEngine v3`.",
    },
    "claude": {
        "host": "Claude Code",
        "minimum": "2.1+",
        "validated": "2.1.322",
        "format": "`~/.claude/skills` + `~/.claude/agents/*.md`",
        "legacy": "`user-invocable` no es un campo de subagente de Claude Code: se ignora.",
    },
    "pi": {
        "host": "Pi",
        "minimum": "0.99+ (rutas estables en 1.x)",
        "validated": "0.99.2 y 1.5.2",
        "format": "`~/.pi/agent/skills` + `~/.pi/agent/prompts/*.md`",
        "legacy": "Los prompt templates y `$ARGUMENTS` siguen siendo compatibles.",
    },
    "antigravity": {
        "host": "Google Antigravity App / CLI",
        "minimum": "2.31+",
        "validated": "2.31.0",
        "format": "`~/.gemini/config/skills` + `~/.gemini/config/agents/*.md`",
        "legacy": "El CLI también lee `~/.gemini/antigravity-cli/skills` y `~/.gemini/skills` con prioridad.",
    },
}

VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")


def parse_version(text: str) -> tuple[int, int, int] | None:
    """Return the first semantic-looking version in *text*."""
    match = VERSION_RE.search(text or "")
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch or 0)


def _run(command: str, *args: str, timeout: int = 5) -> subprocess.CompletedProcess[str] | None:
    executable = shutil.which(command)
    if not executable:
        return None
    try:
        return subprocess.run(
            [executable, *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def command_version(command: str) -> tuple[int, int, int] | None:
    result = _run(command, "--version")
    if result is None:
        return None
    return parse_version((result.stdout or "") + "\n" + (result.stderr or ""))


def info(message: str) -> None:
    print(f"  · {message}")


def ok(message: str) -> None:
    print(f"  ✓ {message}")


def warn(message: str) -> None:
    print(f"  ⚠ {message}", file=sys.stderr)


def kiro_engine() -> str | None:
    """Return the configured Kiro engine, or None when unset/unavailable."""
    result = _run("kiro-cli", "settings", "chat.agentEngine")
    if result is None:
        return None
    text = ((result.stdout or "") + " " + (result.stderr or "")).strip().lower()
    for engine in ("v3", "v2", "v1"):
        if re.search(rf"\b{engine}\b", text):
            return engine
    return None


def check_kiro(strict: bool) -> int:
    version = command_version("kiro-cli")
    if version is None:
        info("Kiro CLI no detectado; se asume IDE o instalación manual. Se instala Markdown V3.")
        return 0

    label = ".".join(str(part) for part in version)
    if version >= (3, 0, 0):
        if kiro_engine() == "v2":
            warn(f"Kiro CLI {label} tiene el motor V2 forzado; los agentes Markdown no se cargarán.")
            info("Quita la preferencia con `kiro-cli settings -d chat.agentEngine` o usa V3.")
            if strict:
                warn("Modo estricto: instalación abortada.")
                return 1
            return 0
        ok(f"Kiro CLI {label}: motor V3; los agentes Markdown son compatibles.")
        return 0

    if version >= (2, 37, 0):
        engine = kiro_engine()
        if engine == "v3":
            ok(f"Kiro CLI {label} con motor V3 configurado; los agentes Markdown son compatibles.")
            return 0
        warn(
            f"Kiro CLI {label} detectado con motor V2 (predeterminado). "
            "Los agentes Markdown V3 no se cargarán hasta activar V3."
        )
        info("Actívalo con `kiro-cli settings chat.agentEngine v3` o usa `kiro-cli --v3`.")
        info("Tus agentes JSON existentes en ~/.kiro/agents no se modifican.")
        if strict:
            warn("Modo estricto: instalación abortada. Actualiza/activa V3 o usa el IDE.")
            return 1
        return 0

    warn(
        f"Kiro CLI {label} detectado: no incluye el motor V3 estable y no leerá los agentes Markdown."
    )
    info("Actualiza a Kiro CLI 2.37+ (motor V3) o 3.x, o usa Kiro IDE 1.x.")
    info("Tus agentes JSON existentes en ~/.kiro/agents no se modifican.")
    if strict:
        warn("Modo estricto: instalación abortada.")
        return 1
    return 0


def check_opencode(_strict: bool) -> int:
    version = command_version("opencode")
    if version is None:
        info("OpenCode no detectado; se instala el frontmatter V1 compatible con 1.x y 2.x.")
        return 0

    label = ".".join(str(part) for part in version)
    if version[0] >= 2:
        info(
            f"OpenCode {label} detectado. Se instala el frontmatter V1: V2 lo traduce y "
            "mantiene la compatibilidad con 1.x. `temperature` no se aplica en V2."
        )
        return 0

    ok(f"OpenCode {label} detectado; el frontmatter V1 es el formato nativo.")
    return 0


def check_pi(_strict: bool) -> int:
    version = command_version("pi")
    if version is None:
        info("Pi no detectado; se usan las rutas estables de 0.99+ y 1.x.")
        return 0
    label = ".".join(str(part) for part in version)
    if version[0] < 1:
        info(f"Pi {label} detectado; las rutas y `$ARGUMENTS` siguen siendo compatibles. Se recomienda 1.x.")
    else:
        ok(f"Pi {label} detectado; rutas de skills y prompt templates compatibles.")
    return 0


CHECKS = {
    "kiro": check_kiro,
    "opencode": check_opencode,
    "pi": check_pi,
}


def print_matrix() -> None:
    print("| Plataforma | Host | Mínimo | Validado | Formato | Comportamiento legacy |")
    print("|---|---|---|---|---|---|")
    for platform, row in MATRIX.items():
        print(
            f"| `{platform}` | {row['host']} | {row['minimum']} | {row['validated']} | "
            f"{row['format']} | {row['legacy']} |"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", choices=sorted(CHECKS), help="Host cuya versión se comprueba")
    parser.add_argument("--strict", action="store_true", help="Falla si el host no puede leer el formato distribuido")
    parser.add_argument("--matrix", action="store_true", help="Imprime la matriz de compatibilidad en Markdown")
    args = parser.parse_args(argv)

    if args.matrix:
        print_matrix()
        return 0
    if not args.check:
        parser.error("indica --check o --matrix")
    return CHECKS[args.check](args.strict)


if __name__ == "__main__":
    raise SystemExit(main())
