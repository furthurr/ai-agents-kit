"""Tests for the host-version compatibility helper.

These tests use fake ``kiro-cli`` / ``opencode`` executables in a temporary
PATH. They never touch the real host installation.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import host_compat  # noqa: E402

PASSED = 0
FAILED = 0


def ok(message: str) -> None:
    global PASSED
    PASSED += 1
    print(f"  \033[32m✓\033[0m {message}")


def fail(message: str, detail: str = "") -> None:
    global FAILED
    FAILED += 1
    print(f"  \033[31m✗\033[0m {message}")
    if detail:
        for line in detail.strip().splitlines():
            print(f"      {line}")


def check(condition: bool, message: str, detail: str = "") -> None:
    ok(message) if condition else fail(message, detail)


def capture(func, *args):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = func(*args)
    return code, stdout.getvalue(), stderr.getvalue()


def fake_command(directory: Path, name: str, body: str) -> None:
    path = directory / name
    path.write_text("#!/bin/sh\n" + body, encoding="utf-8")
    path.chmod(0o755)


@contextlib.contextmanager
def isolated_path(directory: Path):
    original = os.environ.get("PATH", "")
    os.environ["PATH"] = str(directory) + os.pathsep + original
    try:
        yield
    finally:
        os.environ["PATH"] = original


def test_parse_version() -> None:
    print("\n\033[1m[1] Parseo de versiones\033[0m")
    cases = {
        "kiro-cli 2.37.1": (2, 37, 1),
        "opencode 1.18.34": (1, 18, 34),
        "pi 0.99.2": (0, 99, 2),
        "Claude Code 2.1.322": (2, 1, 322),
        "sin versión": None,
    }
    for text, expected in cases.items():
        check(host_compat.parse_version(text) == expected, f"parse_version({text!r}) == {expected}")


def test_matrix_covers_manifest() -> None:
    print("\n\033[1m[2] La matriz cubre todas las plataformas\033[0m")
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    for platform in manifest["platforms"]:
        check(platform in host_compat.MATRIX, f"matriz incluye {platform}")
        row = host_compat.MATRIX.get(platform, {})
        check(all(row.get(key) for key in ("host", "minimum", "validated", "format", "legacy")),
              f"matriz completa para {platform}")


def test_kiro_v3_engine() -> None:
    print("\n\033[1m[3] Kiro CLI con V3 configurado\033[0m")
    with tempfile.TemporaryDirectory() as temporary:
        bin_dir = Path(temporary)
        fake_command(bin_dir, "kiro-cli", 'if [ "$1" = "--version" ]; then echo "kiro-cli 2.37.1"; exit 0; fi\n'
                                         'if [ "$1" = "settings" ]; then echo "v3"; exit 0; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code, out, err = capture(host_compat.check_kiro, False)
    check(code == 0, "exit 0 con motor V3")
    check("motor V3 configurado" in out, "informa compatibilidad")
    check("⚠" not in err, "sin warning cuando V3 está configurado")


def test_kiro_v2_default_warns() -> None:
    print("\n\033[1m[4] Kiro CLI 2.37 con V2 predeterminado\033[0m")
    with tempfile.TemporaryDirectory() as temporary:
        bin_dir = Path(temporary)
        fake_command(bin_dir, "kiro-cli", 'if [ "$1" = "--version" ]; then echo "kiro-cli 2.37.1"; exit 0; fi\n'
                                         'if [ "$1" = "settings" ]; then echo "No value associated with chat.agentEngine" >&2; exit 1; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code, out, err = capture(host_compat.check_kiro, False)
            strict_code, _, strict_err = capture(host_compat.check_kiro, True)
    check(code == 0, "warning no bloquea por defecto")
    check("chat.agentEngine v3" in out, "explica cómo activar V3")
    check("no se cargarán" in err, "advierte de que los .md no se cargan en V2")
    check(strict_code == 1, "--strict falla si V3 no está activo")
    check("Modo estricto" in strict_err, "--strict explica el aborto")


def test_kiro_v3_with_forced_v2_warns() -> None:
    print("\n\033[1m[4b] Kiro CLI 3.x con motor V2 forzado\033[0m")
    with tempfile.TemporaryDirectory() as temporary:
        bin_dir = Path(temporary)
        fake_command(bin_dir, "kiro-cli", 'if [ "$1" = "--version" ]; then echo "kiro-cli 3.0.0"; exit 0; fi\n'
                                         'if [ "$1" = "settings" ]; then echo "v2 (global)"; exit 0; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code, out, err = capture(host_compat.check_kiro, False)
            strict_code, _, _ = capture(host_compat.check_kiro, True)
    check(code == 0 and "V2 forzado" in err, "advierte si V3 está forzado a V2")
    check(strict_code == 1, "--strict falla con V2 forzado")


def test_kiro_old_cli_warns() -> None:
    print("\n\033[1m[5] Kiro CLI anterior a 2.37\033[0m")
    with tempfile.TemporaryDirectory() as temporary:
        bin_dir = Path(temporary)
        fake_command(bin_dir, "kiro-cli", 'if [ "$1" = "--version" ]; then echo "kiro-cli 2.34.0"; exit 0; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code, out, err = capture(host_compat.check_kiro, False)
            strict_code, _, _ = capture(host_compat.check_kiro, True)
    check(code == 0, "warning no bloquea por defecto")
    check("2.34.0" in err and "no leerá" in err, "advierte de incompatibilidad")
    check(strict_code == 1, "--strict falla con CLI antiguo")


def test_opencode_versions() -> None:
    print("\n\033[1m[6] OpenCode 1.x y 2.x\033[0m")
    with tempfile.TemporaryDirectory() as temporary:
        bin_dir = Path(temporary)
        fake_command(bin_dir, "opencode", 'if [ "$1" = "--version" ]; then echo "opencode 1.18.34"; exit 0; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code1, out1, _ = capture(host_compat.check_opencode, False)
        fake_command(bin_dir, "opencode", 'if [ "$1" = "--version" ]; then echo "opencode 2.2.7"; exit 0; fi\nexit 0\n')
        with isolated_path(bin_dir):
            code2, out2, _ = capture(host_compat.check_opencode, False)
    check(code1 == 0 and "formato nativo" in out1, "OpenCode 1.x: formato nativo")
    check(code2 == 0 and "V2 lo traduce" in out2, "OpenCode 2.x: aviso de compatibilidad V1")
    check("temperature" in out2, "explica la pérdida de temperature en V2")


def main() -> int:
    print("\033[1mTests de compatibilidad de hosts\033[0m")
    test_parse_version()
    test_matrix_covers_manifest()
    if sys.platform == "win32":
        print("\nLos ejecutables falsos POSIX se omiten en Windows.")
    else:
        test_kiro_v3_engine()
        test_kiro_v2_default_warns()
        test_kiro_v3_with_forced_v2_warns()
        test_kiro_old_cli_warns()
        test_opencode_versions()
    total = PASSED + FAILED
    print(f"\n{PASSED}/{total} pruebas correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
