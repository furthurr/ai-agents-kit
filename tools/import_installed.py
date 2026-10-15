#!/usr/bin/env python3
"""Import declared installed artifacts for review without changing canonical sources."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from datetime import datetime
from pathlib import Path

from retired_agents import read_regular, safe_directory, safe_path


ROOT = Path(__file__).resolve().parent.parent


def snapshot(source: Path, target: Path, directories: list[Path], files: list[tuple[Path, bytes, int]]) -> None:
    """Validate and read before writing; shared helpers reject links/reparse points.

    Requires a stable source tree, not an adversarial concurrently modified host.
    read_regular also uses O_NOFOLLOW where available and checks file identity.
    """
    source = safe_path(source)
    info = source.lstat()
    if stat.S_ISDIR(info.st_mode):
        directories.append(target)
        for child in sorted(source.iterdir()):
            if child.name != ".DS_Store":
                snapshot(child, target / child.name, directories, files)
    else:
        data, _ = read_regular(source)  # Rejects FIFOs, sockets and nonregular files.
        files.append((target, data, stat.S_IMODE(info.st_mode)))


def source_directory(path: Path, *, windows: bool | None = None) -> Path | None:
    """Validate the selected root itself, then canonicalize trusted OS parents.

    macOS exposes temporary files through `/var -> /private/var`; that system alias
    is outside the imported tree. Reject a symlink at the selected root and every
    link below it, while using the resolved parent to avoid treating OS aliases as
    content links.
    """
    if windows is None:
        windows = os.name == "nt"
    if ".." in path.parts:
        raise OSError(f"ruta de origen con '..' no permitida: {path}")
    raw = Path(os.path.abspath(path))
    try:
        info = raw.lstat()
    except FileNotFoundError:
        return None
    if raw.is_symlink() or getattr(info, "st_file_attributes", 0) & 0x400:
        raise OSError(f"raíz de origen enlazada: {raw}")
    if not stat.S_ISDIR(info.st_mode):
        raise OSError(f"raíz de origen no es directorio: {raw}")
    if windows:
        # Windows may canonicalize a valid 8.3 short path (e.g. RUNNER~1) to its
        # long name. Inspect supplied components directly; safe_directory rejects
        # actual symlinks, junctions and reparse points.
        return safe_directory(raw)
    canonical = raw.resolve(strict=True)
    if raw != canonical:
        # `/var` is a documented macOS system alias for `/private/var`; permit
        # only this OS-owned parent alias, not an arbitrary linked parent.
        macos_var_alias = (
            sys.platform == "darwin"
            and raw.is_relative_to(Path("/var"))
            and canonical == Path("/private/var") / raw.relative_to(Path("/var"))
        )
        if not macos_var_alias:
            raise OSError(f"raíz bajo un padre enlazado: {raw}")
    return safe_directory(canonical)


def main() -> int:
    manifest = json.loads((ROOT / "canonical" / "manifest.json").read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=tuple(manifest["platforms"]))
    parser.add_argument("--skills-dir", required=True, type=Path)
    parser.add_argument("--agents-dir", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    expected_skills = set(manifest["skills"])
    expected_agents = {
        json.loads((ROOT / "adapters" / arguments.platform / "agents" / f"{agent_id}.json").read_text(encoding="utf-8"))["filename"]
        for agent_id in manifest["agents"]
    }
    label = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    destination = ROOT / "imports" / arguments.platform / label
    copied = 0
    directories: list[Path] = []
    files: list[tuple[Path, bytes, int]] = []
    try:
        for source_root, expected, section in ((arguments.skills_dir, expected_skills, "skills"), (arguments.agents_dir, expected_agents, "agents")):
            requested_root = source_root
            source_root = source_directory(source_root)
            if source_root is None:
                print(f"No existe {requested_root}; se omite {section}.")
                continue
            entries = {entry.name: entry for entry in source_root.iterdir() if entry.name != ".DS_Store"}
            for name in sorted(entries):
                if name not in expected:
                    print(f"Se ignora elemento ajeno al kit: {section}/{name}")
            for name in sorted(expected):
                if Path(name).name != name or name in ("", ".", ".."):
                    raise OSError(f"nombre de artefacto inseguro: {name!r}")
                source = entries.get(name)
                if source is None:
                    print(f"No instalado: {section}/{name}")
                    continue
                target = destination / section / name
                snapshot(source, target, directories, files)
                print(f"Importar {source} -> {target}")
                copied += 1
        if copied:
            safe_directory(destination)
        if copied and not arguments.dry_run:
            destination.mkdir(parents=True, exist_ok=False)
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
            for target, data, mode in files:
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("xb") as stream:
                    stream.write(data)
                target.chmod(mode)
            print(f"Importación creada en {destination}. Revisa y promociona los cambios manualmente a canonical/ o adapters/.")
    except OSError as error:
        print(f"Importación rechazada: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
