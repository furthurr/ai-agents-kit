#!/usr/bin/env python3
"""Opt-in cleanup of two known stale Developer resources in ONE explicit OpenCode profile.

Run the normal installer with backup first. This does not retire the developer ID,
install files, traverse projects, read configuration, or certify host resolution.
Unknown/customized bytes and symlinks block cleanup; there is no force override.
Default is a read-only plan. --apply requires a separately authorized destination.
Recovery uses retired_agents.py's exclusive per-file restore (never overwrite).
"""
from __future__ import annotations

import argparse
from pathlib import Path
import json
import sys

from retired_agents import digest, read_regular, remove_verified, safe_directory, validate_backup, write_backup

ROOT = Path(__file__).resolve().parent.parent
KNOWN = {
    "agents/developer.md": "9d77ba5d02eb92008f2db7f1dd0456b44bba53210a75ca5eb27b99826a7ce17a",
    "skills/developer/references/plan.md": "931ec9d55adaed7248611a74496b851452110f0298c214fdfe48a70eaa89a322",
}
CURRENT = {
    "agent/developer.md": "generated/opencode/agents/developer.md",
    "skills/developer/SKILL.md": "generated/opencode/skills/developer/SKILL.md",
}


def verify_current(profile: Path) -> None:
    for installed, source in CURRENT.items():
        if read_regular(profile / installed)[0] != read_regular(ROOT / source)[0]:
            raise OSError(f"contenido vigente no verificado: {installed}; conservar y revisar")


def clean(profile: Path, backup_root: Path, *, apply: bool = False) -> list[dict]:
    """All candidates are checked before writing; no ownership inferred from names.

    Bounded file operations, not a transactional deployment or an atomic CAS.
    Config overrides, aliases and other profiles must be verified separately.
    """
    profile = safe_directory(profile)
    destinations = [profile / name for name in ("agent", "agents", "skills")]
    backup_root = validate_backup(backup_root, destinations)
    verify_current(profile)
    candidates = []
    for relative, expected in KNOWN.items():
        path = profile / relative
        # Even dangling links must be rejected, not treated as absent.
        safe_directory(path.parent)
        if not path.exists() and not path.is_symlink():
            continue
        data, identity = read_regular(path)
        if digest(data) != expected:
            raise OSError(f"bytes desconocidos/personalizados: {relative}; conservados")
        candidates.append((path, data, identity))

    results = []
    for path, data, identity in candidates:
        result = {"path": str(path), "sha256": digest(data), "status": "planned"}
        if apply:
            verify_current(profile)
            current, current_identity = read_regular(path)
            if current != data or current_identity != identity:
                raise OSError(f"candidato cambió tras planificar: {path}")
            backup = write_backup(validate_backup(backup_root, destinations), path.name, data)
            # Record recovery information BEFORE a potentially failing removal.
            print(json.dumps({"backup": str(backup), **result}, ensure_ascii=False), flush=True)
            current, current_identity = read_regular(path)
            if current != data or current_identity != identity or read_regular(backup)[0] != data:
                raise OSError(f"candidato/backup cambió: {path}; conservar respaldo {backup}")
            remove_verified(path, identity)
            if path.exists() or path.is_symlink():
                raise OSError(f"recurso reapareció: {path}; conservar respaldo {backup}")
            result.update(status="removed", backup=str(backup))
        results.append(result)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--opencode-home", required=True, type=Path,
                        help="Un único perfil explícito; no se infiere HOME ni XDG")
    parser.add_argument("--backup-root", required=True, type=Path,
                        help="Fuera de todo árbol escaneado por el host")
    parser.add_argument("--apply", action="store_true", help="Ejecutar la limpieza autorizada; por defecto solo plan")
    args = parser.parse_args()
    try:
        results = clean(args.opencode_home, args.backup_root, apply=args.apply)
    except OSError as error:
        print(f"Developer: limpieza pendiente/error: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"mode": "apply" if args.apply else "dry-run", "files": results,
                      "scope": "solo dos rutas conocidas; overrides/aliases y runtime no certificados"},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
