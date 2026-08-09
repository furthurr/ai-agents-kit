#!/usr/bin/env python3
"""Tests for tools/check_links.py."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check_links  # noqa: E402


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


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_valid_link_and_anchor() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "README.md"
        write(source, "[Guide](docs/guide.md#usage)\n[Site](https://example.com)\n")
        write(root / "docs" / "guide.md", "# Usage\n")
        check(check_links.check_links(root, [source]) == [], "acepta enlace local, ancla y URL externa")


def test_broken_destination() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "README.md"
        write(source, "[Missing](docs/missing.md)\n")
        errors = check_links.check_links(root, [source])
        check(len(errors) == 1 and "destino inexistente" in errors[0], "rechaza destino inexistente")


def test_broken_anchor_and_escape() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "README.md"
        write(source, "[Bad](guide.md#missing)\n[Escape](../outside.md)\n")
        write(root / "guide.md", "# Present\n")
        errors = check_links.check_links(root, [source])
        check(len(errors) == 2, "rechaza ancla inexistente y ruta fuera del repositorio")


def test_code_blocks_are_ignored() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        source = root / "README.md"
        write(source, "```markdown\n[Example](missing.md)\n```\n")
        check(check_links.check_links(root, [source]) == [], "ignora enlaces de ejemplos en bloques de codigo")


def main() -> int:
    print("Tests de enlaces Markdown")
    test_valid_link_and_anchor()
    test_broken_destination()
    test_broken_anchor_and_escape()
    test_code_blocks_are_ignored()
    total = PASSED + FAILED
    print(f"{PASSED}/{total} pruebas correctas")
    return 0 if FAILED == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
