#!/usr/bin/env python3
"""Read-only, bounded secret check distributed with git-commit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
import sys

RULES = (
    ("private-key-header", re.compile(
        rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----")),
    ("github-token", re.compile(
        rb"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36}(?![A-Za-z0-9_])")),
    ("github-fine-grained-token", re.compile(
        rb"(?<![A-Za-z0-9_])github_pat_[A-Za-z0-9]{22}_[A-Za-z0-9]{59}(?![A-Za-z0-9_])")),
)


class CheckError(Exception):
    """Fixed public cause, without underlying exception or Git output."""


def scan_content(content: bytes) -> list[tuple[int, str]]:
    """Return sanitized finding locations, never values."""
    return sorted({(content.count(b"\n", 0, match.start()) + 1, rule)
                   for rule, pattern in RULES for match in pattern.finditer(content)})


def safe_label(path: str) -> str:
    value = os.fsencode(path)
    for _, pattern in RULES:
        value = pattern.sub(b"[REDACTED]", value)
    return json.dumps(os.fsdecode(value), ensure_ascii=True)


def relative_path(name: str) -> Path:
    path = Path(name)
    if (not name or path.is_absolute() or PureWindowsPath(name).is_absolute()
            or ".." in path.parts or ".." in PureWindowsPath(name).parts):
        raise CheckError("ruta relativa no admitida")
    return path


def read_file(root: Path, name: str) -> bytes:
    path = relative_path(name)
    current = root
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise CheckError("enlace no evaluado; revisar por separado")
    if not current.resolve().is_relative_to(root):
        raise CheckError("ruta fuera de la raíz")
    if not current.is_file():
        raise CheckError("archivo ausente o tipo no admitido")
    try:
        return current.read_bytes()
    except OSError:
        raise CheckError("lectura incompleta") from None


def git_bytes(root: Path, *args: str) -> bytes:
    env = os.environ.copy()
    # Scope Git to the selected repository, not an inherited alternate index/tree.
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_NAMESPACE"):
        env.pop(key, None)
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_NO_LAZY_FETCH"] = "1"
    try:
        result = subprocess.run(["git", "-c", "core.fsmonitor=false", "-c", "maintenance.auto=false",
                                 "-C", str(root), *args], env=env,
                                capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        raise CheckError("Git no disponible o evaluación agotada") from None
    if result.returncode:
        raise CheckError("evaluación Git incompleta")
    return result.stdout


def index_entries(root: Path) -> list[tuple[str, str]]:
    top = os.fsdecode(git_bytes(root, "rev-parse", "--show-toplevel").rstrip(b"\n"))
    if Path(top).resolve() != root:
        raise CheckError("--repo debe ser la raíz del repositorio")
    entries = []
    for record in git_bytes(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_name = record.split(b"\t", 1)
            mode, oid, stage = metadata.split()
        except ValueError:
            raise CheckError("metadatos del índice no admitidos") from None
        if stage != b"0" or mode not in (b"100644", b"100755"):
            raise CheckError("índice con conflicto, enlace o submódulo no evaluado")
        name = os.fsdecode(raw_name)
        relative_path(name)
        entries.append((name, oid.decode("ascii")))
    return entries


class SafeParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse's default error includes the supplied arguments, possibly values.
        raise CheckError("argumentos no admitidos; consultar --help")


def main(argv: list[str] | None = None) -> int:
    parser = SafeParser(description="Control acotado de solo lectura: claves privadas y tokens GitHub.")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--staged", action="store_true", help="Leer blobs del índice completo")
    modes.add_argument("--tracked", action="store_true", help="Leer archivos tracked del working tree")
    parser.add_argument("paths", nargs="*", help="Candidatos relativos, incluidos untracked")
    try:
        args = parser.parse_args(argv)
        if bool(args.paths) == bool(args.staged or args.tracked):
            raise CheckError("seleccionar un modo o rutas explícitas, no ambos")
        root = args.repo.resolve()
        if not root.is_dir():
            raise CheckError("raíz no disponible")
        # Accumulate only locations; any incomplete evaluation returns 2.
        findings: list[tuple[str, int, str]] = []
        if args.staged or args.tracked:
            entries = index_entries(root)
        else:
            entries = [(name, "") for name in args.paths]
        for name, oid in entries:
            content = (git_bytes(root, "cat-file", "blob", oid) if args.staged
                       else read_file(root, name))
            findings.extend((safe_label(name), line, rule) for line, rule in scan_content(content))
        for label, line, rule in findings:
            print(f"{label}:{line}: {rule}; contenido excluido, sin excepción de autorización")
        if findings:
            print(f"Control rechazado: {len(findings)} hallazgo(s); valores omitidos.")
            return 1
        print(f"Sin coincidencias soportadas: {len(entries)} archivo(s); no acredita ausencia universal de secretos.")
        return 0
    except CheckError as exc:
        print(f"Evaluación incompleta: {exc}.", file=sys.stderr)
        return 2
    except (OSError, ValueError, UnicodeError):
        print("Evaluación incompleta: entrada o lectura no admitida.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
