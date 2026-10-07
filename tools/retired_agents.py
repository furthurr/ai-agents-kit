"""Bounded, offline retired-agent migration shared by all installers.

Exact hashes identify known bytes, not authorship. Unknown bytes always require
an exact absolute path and reviewed SHA-256. No version is inferred from a name.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import shlex
import uuid

CATALOG = Path(__file__).with_name("retired_agents.json")
PLATFORMS = {"copilot", "opencode", "kiro", "claude", "pi", "antigravity"}
IDS = {"architecture", "project-navigator"}
SCANNED_NAMES = {".agents", ".claude", ".github", ".kiro", ".pi", ".gemini", ".copilot", ".opencode"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_catalog(data: dict) -> list[dict]:
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        raise ValueError("catálogo de retirados: schema inválido")
    if not isinstance(data.get("baseline_commit"), str) or not re.fullmatch(r"[0-9a-f]{40}", data["baseline_commit"]):
        raise ValueError("catálogo de retirados: baseline inválido")
    entries = data.get("entries")
    if not isinstance(entries, list):
        raise ValueError("catálogo de retirados: entries inválidas")
    seen = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"id", "platform", "filename", "sha256", "adapter_sha256"}:
            raise ValueError("catálogo de retirados: entrada inválida")
        agent, platform = entry["id"], entry["platform"]
        if not isinstance(agent, str) or not isinstance(platform, str) or agent not in IDS or platform not in PLATFORMS:
            raise ValueError("catálogo de retirados: ID/plataforma inválido")
        filename = agent + (".agent.md" if platform == "copilot" else ".md")
        if entry["filename"] != filename:
            raise ValueError("catálogo de retirados: ruta inválida")
        for key in ("sha256", "adapter_sha256"):
            if not isinstance(entry[key], str) or not re.fullmatch(r"[0-9a-f]{64}", entry[key]):
                raise ValueError("catálogo de retirados: hash inválido")
        pair = (platform, agent)
        if pair in seen:
            raise ValueError("catálogo de retirados: duplicado")
        seen.add(pair)
    if seen != {(p, a) for p in PLATFORMS for a in IDS}:
        raise ValueError("catálogo de retirados: cobertura incompleta")
    return entries


def load_catalog() -> list[dict]:
    return validate_catalog(json.loads(CATALOG.read_text(encoding="utf-8")))


def safe_path(path: Path) -> Path:
    """Check every component without resolving away links (including junctions)."""
    path = Path(os.path.abspath(path))
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise OSError(f"symlink/reparse point bloqueado: {part}")
        if part != path and not stat.S_ISDIR(info.st_mode):
            raise OSError(f"componente padre no es directorio: {part}")
    return path


def safe_directory(path: Path) -> Path:
    """Allow absent directories, but reject existing files and unsafe parents."""
    path = safe_path(path)
    if path.exists() and not stat.S_ISDIR(path.lstat().st_mode):
        raise OSError(f"no es directorio: {path}")
    return path


def read_regular(path: Path) -> tuple[bytes, tuple]:
    path = safe_path(path)
    if not stat.S_ISREG(path.lstat().st_mode):
        raise OSError(f"no es archivo regular: {path}")
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0))
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise OSError(f"no es archivo regular: {path}")
        data = stream.read()
        after = os.fstat(stream.fileno())
    if identity(before) != identity(after) or identity(after) != identity(path.lstat()):
        raise OSError(f"archivo cambió durante lectura: {path}")
    return data, identity(after)


def identity(info: os.stat_result) -> tuple:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def validate_backup(backup: Path, destinations: list[Path]) -> Path:
    backup = safe_directory(backup)
    for component in [backup, *backup.parents]:
        if component.name.casefold() in SCANNED_NAMES or (component.name.casefold() == "opencode" and component.parent.name.casefold() == ".config"):
            raise OSError(f"backup dentro de árbol escaneado: {backup}")
    for destination in destinations:
        root = safe_path(destination).parent
        if backup == root or root in backup.parents or backup in root.parents:
            raise OSError(f"backup solapa árbol activo: {root}")
    configured = [Path(os.environ[variable]) for variable in ("CLAUDE_CONFIG_DIR", "PI_CODING_AGENT_DIR") if os.environ.get(variable)]
    if os.environ.get("XDG_CONFIG_HOME"):
        configured.append(Path(os.environ["XDG_CONFIG_HOME"]) / "opencode")
    for root in configured:
        root = Path(os.path.abspath(root))
        if root == backup or root in backup.parents or backup in root.parents:
            raise OSError(f"backup solapa host configurado: {root}")
    return backup


def approvals_from_args(paths: list[str], hashes: list[str], destinations: list[Path], platform: str) -> dict[str, str]:
    if len(paths) != len(hashes):
        raise ValueError("cada --approve-retired-file requiere --approve-retired-sha256")
    allowed = {str(Path(os.path.abspath(d)) / e["filename"]) for d in destinations for e in load_catalog() if e["platform"] == platform}
    approvals = {}
    for path, sha in zip(paths, hashes):
        if path not in allowed or not Path(path).is_absolute() or not re.fullmatch(r"[0-9a-f]{64}", sha) or path in approvals:
            raise ValueError(f"aprobación inválida; requiere ruta absoluta exacta y SHA-256: {path}")
        approvals[path] = sha
    return approvals


def shell_command(arguments: list[str], shell: str | None = None) -> str:
    shell = shell or ("powershell" if os.name == "nt" else "posix")
    if shell == "powershell":
        return "& " + " ".join("'" + argument.replace("'", "''") + "'" for argument in arguments)
    return shlex.join(arguments)


def approval_hint(path: str, sha: str, platform: str, destinations: list, backup_root, *, shell: str | None = None) -> str:
    """Executable Python invocation, with exact literal arguments for each shell."""
    shell = shell or ("powershell" if os.name == "nt" else "posix")
    primary = Path(destinations[0])
    arguments = ["python" if shell == "powershell" else "python3", str(Path(__file__).absolute().with_name("install_preflight.py")),
                 "--platform", platform, "--migrate-retired-agents", "--agents-dest", str(primary),
                 "--skills-dest", str(primary.parent / "skills"), "--backup-root", str(backup_root)]
    for destination in destinations[1:]:
        arguments.extend(["--additional-agents-dest", str(destination)])
    arguments.extend(["--approve-retired-file", str(path), "--approve-retired-sha256", sha])
    return shell_command(arguments, shell)


def write_backup(root: Path, filename: str, data: bytes) -> Path:
    safe_path(root)
    root.mkdir(parents=True, exist_ok=True)
    folder = root / uuid.uuid4().hex
    folder.mkdir(mode=0o700)
    target = folder / filename
    with target.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if read_regular(target)[0] != data:
        raise OSError(f"backup no verificado: {target}")
    return target


def restore(backup: Path, destination: Path, sha256: str) -> None:
    data, _ = read_regular(backup)
    if digest(data) != sha256:
        raise OSError("hash de recuperación no coincide")
    destination = safe_path(destination)
    # Exclusive creation: never replace new user work, even with identical bytes.
    with destination.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if read_regular(destination)[0] != data:
        raise OSError("recuperación no verificada")


def remove_verified(path: Path, expected_identity: tuple) -> None:
    """Recheck identity immediately before unlink; anchor the parent on POSIX.

    Portable APIs cannot atomically compare bytes and unlink. Windows falls back
    to a final lstat; POSIX dir_fd avoids following a swapped parent at unlink.
    """
    path = safe_path(path)
    if os.unlink in os.supports_dir_fd:
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
        try:
            parent = path.parent.lstat()
            opened = os.fstat(fd)
            if (parent.st_dev, parent.st_ino) != (opened.st_dev, opened.st_ino):
                raise OSError("padre cambió antes de retirada")
            info = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            if identity(info) != expected_identity or not stat.S_ISREG(info.st_mode):
                raise OSError("candidato cambió antes de unlink")
            os.unlink(path.name, dir_fd=fd)
        finally:
            os.close(fd)
    else:
        if identity(path.lstat()) != expected_identity:
            raise OSError("candidato cambió antes de unlink")
        path.unlink()


def migrate(platform: str, destinations: list[Path], backup_root: Path, *, approvals: dict[str, str] | None = None, dry_run: bool = False) -> int:
    if platform not in PLATFORMS:
        raise ValueError(f"plataforma desconocida: {platform}")
    entries = [e for e in load_catalog() if e["platform"] == platform]
    approvals = approvals or {}
    failed = False
    try:
        backup_root = validate_backup(backup_root, destinations)
    except OSError as error:
        print(f"migración bloqueada: {error}")
        return 1
    print(f"Migración {'plan (dry-run)' if dry_run else 'autorizada'}: destinos {destinations}; backup {backup_root}")
    for dest in destinations:
        for entry in entries:
            path = Path(os.path.abspath(dest)) / entry["filename"]
            backup = None
            try:
                safe_path(path)
                if not path.exists():
                    continue
                data, identity = read_regular(path)
                sha = digest(data)
                known = sha == entry["sha256"]
                approved = approvals.get(str(path)) == sha
                print(f"{'copia conocida' if known else 'incierto (sin baseline personalizado fiable)'}: {path} SHA-256={sha}")
                if str(path) in approvals and not approved:
                    raise OSError("SHA aprobado no coincide con bytes actuales")
                if not known and not approved:
                    print(f"pendiente: {approval_hint(str(path), sha, platform, destinations, backup_root)}")
                    failed = True
                    continue
                print(f"respaldo único previsto: {backup_root}/<uuid>/{path.name}; después retirada")
                if dry_run:
                    continue
                backup = write_backup(validate_backup(backup_root, destinations), path.name, data)
                print(f"backup verificado: {backup} SHA-256={sha}")
                current, current_identity = read_regular(path)
                if current_identity != identity or current != data or read_regular(backup)[0] != data:
                    raise OSError("original/copia cambió antes de retirada")
                remove_verified(path, identity)
                if path.exists() or path.is_symlink():
                    raise OSError("destino reapareció tras retirada")
                print(f"retirado: {path}")
            except OSError as error:
                failed = True
                print(f"pendiente/error: {path}: {error}")
                if backup is not None and not path.exists() and not path.is_symlink():
                    try:
                        restore(backup, path, sha)
                        print(f"original recuperado sin overwrite: {path}")
                    except OSError as recovery_error:
                        print(f"recuperación pendiente: {recovery_error}")
            finally:
                if backup is not None:
                    command = ["python3", str(Path(__file__).absolute()), "--restore-backup", str(backup), "--restore-dest", str(path), "--sha256", sha]
                    if os.name == "nt":
                        command[0] = "python"
                    print(f"Recuperar sin overwrite: {shell_command(command)}")
    print("Migración pendiente." if failed else ("Plan completo; no se escribió nada." if dry_run else "Migración completada."))
    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recuperación sin sobrescribir archivos existentes")
    parser.add_argument("--restore-backup", required=True, type=Path)
    parser.add_argument("--restore-dest", required=True, type=Path)
    parser.add_argument("--sha256", required=True)
    args = parser.parse_args()
    try:
        restore(args.restore_backup, args.restore_dest, args.sha256)
    except OSError as error:
        parser.exit(1, f"recuperación: {error}\n")
