#!/usr/bin/env python3
"""Validate local Markdown links in documentation and canonical sources."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")


def markdown_files(root: Path) -> list[Path]:
    files = [root / "README.md"]
    for directory in (root / "docs", root / "canonical"):
        if directory.is_dir():
            files.extend(directory.rglob("*.md"))
    return sorted(path for path in files if path.is_file())


def iter_links(path: Path) -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    in_code_fence = False
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        links.extend((line_number, match.group(1)) for match in INLINE_LINK.finditer(line))
        reference = REFERENCE_LINK.match(line)
        if reference:
            links.append((line_number, reference.group(1)))
    return links


def heading_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    duplicates: dict[str, int] = {}
    in_code_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence:
            continue
        match = HEADING.match(line)
        if not match:
            continue
        text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1)).casefold()
        slug = re.sub(r"[^\w\s-]", "", text)
        slug = re.sub(r"[\s-]+", "-", slug).strip("-")
        count = duplicates.get(slug, 0)
        duplicates[slug] = count + 1
        ids.add(slug if count == 0 else f"{slug}-{count}")
    return ids


def check_links(root: Path, files: list[Path] | None = None) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for source in files if files is not None else markdown_files(root):
        source = source.resolve()
        for line_number, target in iter_links(source):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            target_path = source if not parsed.path else (source.parent / unquote(parsed.path)).resolve()
            try:
                target_path.relative_to(root)
            except ValueError:
                errors.append(f"{source.relative_to(root)}:{line_number}: enlace fuera del repositorio: {target}")
                continue
            if not target_path.exists():
                errors.append(f"{source.relative_to(root)}:{line_number}: destino inexistente: {target}")
                continue
            if parsed.fragment and target_path.suffix.lower() == ".md":
                anchor = unquote(parsed.fragment).casefold()
                if anchor not in heading_ids(target_path):
                    errors.append(f"{source.relative_to(root)}:{line_number}: ancla inexistente: {target}")
    return errors


def main() -> int:
    errors = check_links(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Enlaces Markdown correctos: {len(markdown_files(ROOT))} archivos revisados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
