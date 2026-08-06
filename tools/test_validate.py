#!/usr/bin/env python3
"""Negative tests for tools/validate.py and tools/render.py.

Each test builds a minimal, isolated kit fixture in a temporary directory,
injects a single defect, and asserts that validation (or render) rejects it.
Positive paths are covered by test_integrity.py and validate.py itself.
"""

from __future__ import annotations

import importlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import render as render_module  # noqa: E402
import validate as validate_module  # noqa: E402

PASSED = 0
FAILED = 0


def ok(msg: str) -> None:
    global PASSED
    PASSED += 1
    print(f"  \033[32m\u2713\033[0m {msg}")


def fail(msg: str) -> None:
    global FAILED
    FAILED += 1
    print(f"  \033[31m\u2717\033[0m {msg}")


def check(condition: bool, msg: str) -> None:
    ok(msg) if condition else fail(msg)


def build_fixture(base: Path) -> Path:
    """Create a minimal but valid kit under ``base`` and return its root."""
    root = base / "kit"
    (root / "canonical" / "skills" / "demo").mkdir(parents=True)
    (root / "canonical" / "agents").mkdir(parents=True)
    (root / "adapters" / "acme" / "agents").mkdir(parents=True)
    (root / "generated").mkdir(parents=True)

    (root / "canonical" / "manifest.json").write_text(
        json.dumps({"skills": ["demo"], "agents": ["demo"], "platforms": ["acme"]}),
        encoding="utf-8",
    )
    (root / "canonical" / "skills" / "demo" / "SKILL.md").write_text(
        "# Demo skill for {{platform_name}}\n", encoding="utf-8"
    )
    (root / "canonical" / "agents" / "demo.md").write_text(
        "Agent body for {{platform_name}}\n", encoding="utf-8"
    )
    (root / "adapters" / "acme" / "platform.json").write_text(
        json.dumps({"substitutions": {"{{platform_name}}": "Acme"}}), encoding="utf-8"
    )
    (root / "adapters" / "acme" / "agents" / "demo.json").write_text(
        json.dumps({"filename": "demo.md", "frontmatter": {"name": "demo"}}),
        encoding="utf-8",
    )
    return root


def with_kit(root: Path):
    """Point render/validate modules at the fixture root and reload nothing."""
    render_module.ROOT = root
    render_module.CANONICAL = root / "canonical"
    render_module.ADAPTERS = root / "adapters"
    render_module.GENERATED = root / "generated"
    validate_module.ROOT = root


def restore_modules() -> None:
    importlib.reload(render_module)
    importlib.reload(validate_module)


def run_validate(root: Path) -> int:
    with_kit(root)
    try:
        return validate_module.main()
    finally:
        restore_modules()


def render_first(root: Path) -> None:
    """Render the fixture so generated/ matches; reproducibility stays valid."""
    render_module.render()


# ---------------------------------------------------------------------------


def test_baseline_valid() -> None:
    print("\n\033[1m[1] Fixture base es válido\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        with_kit(root)
        render_module.render()
        code = validate_module.main()
        restore_modules()
        check(code == 0, "fixture base pasa validación (exit 0)")


def test_unresolved_token() -> None:
    print("\n\033[1m[2] Token sin resolver\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        # Introduce a token with no substitution.
        (root / "canonical" / "agents" / "demo.md").write_text(
            "Body with {{unknown_token}}\n", encoding="utf-8"
        )
        code = run_validate(root)
        check(code == 1, "token sin adaptador rechazado (exit 1)")


def test_incomplete_adapter() -> None:
    print("\n\033[1m[3] Adapter incompleto\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        (root / "adapters" / "acme" / "agents" / "demo.json").write_text(
            json.dumps({"frontmatter": {"name": "demo"}}), encoding="utf-8"
        )
        code = run_validate(root)
        check(code == 1, "adapter sin filename rechazado (exit 1)")


def test_path_traversal_filename() -> None:
    print("\n\033[1m[4] Path traversal en filename\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        (root / "adapters" / "acme" / "agents" / "demo.json").write_text(
            json.dumps({"filename": "../../escape.md", "frontmatter": {"name": "demo"}}),
            encoding="utf-8",
        )
        code = run_validate(root)
        check(code == 1, "filename con .. rechazado por validate (exit 1)")

        # render must also refuse to write outside agents/
        with_kit(root)
        raised = False
        try:
            render_module.render()
        except ValueError:
            raised = True
        finally:
            restore_modules()
        check(raised, "render aborta ante path traversal")


def test_absolute_filename() -> None:
    print("\n\033[1m[5] Filename absoluto\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        (root / "adapters" / "acme" / "agents" / "demo.json").write_text(
            json.dumps({"filename": "/etc/passwd", "frontmatter": {"name": "demo"}}),
            encoding="utf-8",
        )
        code = run_validate(root)
        check(code == 1, "filename absoluto rechazado (exit 1)")


def test_duplicate_filename_collision() -> None:
    print("\n\033[1m[6] Colisión de filename entre agentes\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        # Add a second agent that renders to the same filename.
        manifest = json.loads((root / "canonical" / "manifest.json").read_text())
        manifest["agents"] = ["demo", "demo2"]
        (root / "canonical" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        (root / "canonical" / "agents" / "demo2.md").write_text("Body two\n", encoding="utf-8")
        (root / "adapters" / "acme" / "agents" / "demo2.json").write_text(
            json.dumps({"filename": "demo.md", "frontmatter": {"name": "demo2"}}),
            encoding="utf-8",
        )
        code = run_validate(root)
        check(code == 1, "filenames colisionantes rechazados (exit 1)")


def test_duplicate_manifest_id() -> None:
    print("\n\033[1m[7] ID duplicado en manifest\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        (root / "canonical" / "manifest.json").write_text(
            json.dumps({"skills": ["demo", "demo"], "agents": ["demo"], "platforms": ["acme"]}),
            encoding="utf-8",
        )
        code = run_validate(root)
        check(code == 1, "skill duplicada en manifest rechazada (exit 1)")


def test_orphan_canonical_skill() -> None:
    print("\n\033[1m[8] Skill canónica huérfana\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        (root / "canonical" / "skills" / "ghost").mkdir()
        (root / "canonical" / "skills" / "ghost" / "SKILL.md").write_text("# ghost\n", encoding="utf-8")
        code = run_validate(root)
        check(code == 1, "skill no declarada en manifest rechazada (exit 1)")


def test_stale_generated() -> None:
    print("\n\033[1m[9] Artefacto generado desactualizado\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        with_kit(root)
        render_module.render()
        restore_modules()
        # Corrupt a generated file so it no longer matches canonical render.
        stale = root / "generated" / "acme" / "agents" / "demo.md"
        stale.write_text("stale content\n", encoding="utf-8")
        code = run_validate(root)
        check(code == 1, "generated desactualizado rechazado (exit 1)")


def test_validate_non_destructive() -> None:
    print("\n\033[1m[10] validate.py no altera generated/\033[0m")
    with tempfile.TemporaryDirectory() as tmp:
        root = build_fixture(Path(tmp))
        with_kit(root)
        render_module.render()
        restore_modules()
        gen = root / "generated"
        before = {
            str(p.relative_to(gen)): p.read_bytes()
            for p in sorted(gen.rglob("*"))
            if p.is_file()
        }
        code = run_validate(root)
        after = {
            str(p.relative_to(gen)): p.read_bytes()
            for p in sorted(gen.rglob("*"))
            if p.is_file()
        }
        check(code == 0, "fixture renderizado pasa validación (exit 0)")
        check(before == after, "generated/ intacto tras validación")


def main() -> int:
    print(f"\033[1m{'='*60}\033[0m")
    print("\033[1m  Pruebas negativas — validate.py / render.py\033[0m")
    print(f"\033[1m{'='*60}\033[0m")

    test_baseline_valid()
    test_unresolved_token()
    test_incomplete_adapter()
    test_path_traversal_filename()
    test_absolute_filename()
    test_duplicate_filename_collision()
    test_duplicate_manifest_id()
    test_orphan_canonical_skill()
    test_stale_generated()
    test_validate_non_destructive()

    print(f"\n\033[1m{'='*60}\033[0m")
    total = PASSED + FAILED
    if FAILED == 0:
        print(f"\033[32m  Todas las pruebas negativas pasaron: {PASSED}/{total}\033[0m")
    else:
        print(f"\033[31m  {FAILED} pruebas fallaron de {total}\033[0m")
    print(f"\033[1m{'='*60}\033[0m\n")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
