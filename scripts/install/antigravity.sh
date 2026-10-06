#!/usr/bin/env bash
# Instala el inventario Antigravity en HOME; --dry-run no escribe, --force omite backup.
set -euo pipefail
trap 'printf "Instalación fallida; se conservan los backups previos.\n" >&2' ERR
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
FORCE=0
DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help) printf 'Uso: antigravity.sh [--dry-run] [--force]\n'; exit 0 ;;
    *) printf 'Argumento desconocido: %s\n' "$arg" >&2; exit 2 ;;
  esac
done
PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; sys.exit(sys.version_info.major != 3)' >/dev/null 2>&1; then
    PYTHON="$candidate"; break
  fi
done
if [ -z "$PYTHON" ]; then printf 'Se requiere Python 3.\n' >&2; exit 1; fi
SKILLS_DEST="$HOME/.gemini/config/skills"
AGENTS_DEST="$HOME/.gemini/config/agents"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_ROOT=""
preflight() {
  "$PYTHON" "$REPO_ROOT/tools/install_preflight.py" --platform antigravity "$@"
}
if ! preflight --check-source; then
  printf 'Instalación abortada: fuente incompleta.\n' >&2; exit 1
fi
# Read the declared inventory, not the directory listing. Command substitution
# propagates Python failure (unlike a process substitution feeding a loop).
INVENTORY="$("$PYTHON" - "$REPO_ROOT" <<'PY'
import json
import sys
from pathlib import Path
root = Path(sys.argv[1])
manifest = json.loads((root / 'canonical/manifest.json').read_text(encoding='utf-8'))
for section, names in [('skills', manifest['skills']), ('agents', manifest['agents'])]:
    for name in names:
        if section == 'agents':
            name = json.loads((root / 'adapters/antigravity/agents' / (name + '.json')).read_text(encoding='utf-8'))['filename']
        if not isinstance(name, str) or not name or name in ('.', '..') or any(c in name for c in '/\\\t\r\n'):
            raise ValueError('Nombre inseguro en inventario')
        if section == 'skills':
            canonical = root / 'canonical/skills' / name
            if not (canonical / 'SKILL.md').is_file():
                raise FileNotFoundError(f'Skill canonica ausente: {canonical}')
            for resource in canonical.rglob('*'):
                if resource.is_file():
                    source = root / 'generated/antigravity/skills' / name / resource.relative_to(canonical)
                    if not source.is_file():
                        raise FileNotFoundError(f'Recurso generado ausente: {source}')
        print(section + '\t' + name)
PY
)"
backup_item() {
  local path="$1" section="$2" suffix=0 candidate
  if [ "$FORCE" -eq 1 ] || { [ ! -e "$path" ] && [ ! -L "$path" ]; }; then return 0; fi
  if [ -z "$BACKUP_ROOT" ]; then
    mkdir -p "$HOME/.antigravity-kit-backup"
    candidate="$HOME/.antigravity-kit-backup/$TIMESTAMP"
    while ! mkdir "$candidate" 2>/dev/null; do
      if [ ! -e "$candidate" ]; then printf 'No se pudo crear backup: %s\n' "$candidate" >&2; return 1; fi
      suffix=$((suffix + 1))
      candidate="$HOME/.antigravity-kit-backup/$TIMESTAMP-$suffix"
    done
    BACKUP_ROOT="$candidate"
  fi
  mkdir -p "$BACKUP_ROOT/$section"
  cp -R "$path" "$BACKUP_ROOT/$section/"
  printf 'backup: %s -> %s/%s/\n' "$path" "$BACKUP_ROOT" "$section"
}
copy_tree() {
  mkdir -p "$2"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$1/" "$2/"
  else
    cp -R "$1/." "$2/"
  fi
}
while IFS=$'\t' read -r section name; do
  src="$REPO_ROOT/generated/antigravity/$section/$name"
  if [ "$section" = skills ]; then dest="$SKILLS_DEST/$name"; else dest="$AGENTS_DEST/$name"; fi
  if [ "$DRY_RUN" -eq 1 ]; then
    printf '(dry-run) %s: %s -> %s\n' "$section" "$src" "$dest"
    continue
  fi
  backup_item "$dest" "$section"
  if [ "$section" = skills ]; then
    copy_tree "$src" "$dest"
  else
    mkdir -p "$AGENTS_DEST"
    if [ -d "$dest" ]; then printf 'Destino de agente es directorio: %s\n' "$dest" >&2; exit 1; fi
    cp "$src" "$dest"
  fi
done <<< "$INVENTORY"
if [ "$DRY_RUN" -eq 1 ]; then printf 'Dry-run finalizado: no se escribió nada.\n'; exit 0; fi
if ! preflight --check-installed --skills-dest "$SKILLS_DEST" --agents-dest "$AGENTS_DEST"; then
  printf 'Instalación incompleta; se conservan los backups.\n' >&2; exit 1
fi
# The shared preflight checks entry points only. Verify every canonical resource
# and declared agent against its adapted source before announcing success.
"$PYTHON" - "$REPO_ROOT" "$SKILLS_DEST" "$AGENTS_DEST" <<'PY'
import json
import sys
from pathlib import Path
root, skills_dest, agents_dest = map(Path, sys.argv[1:])
manifest = json.loads((root / 'canonical/manifest.json').read_text(encoding='utf-8'))
for name in manifest['skills']:
    canonical = root / 'canonical/skills' / name
    for resource in canonical.rglob('*'):
        if resource.is_file():
            relative = resource.relative_to(canonical)
            source = root / 'generated/antigravity/skills' / name / relative
            installed = skills_dest / name / relative
            if not installed.is_file() or installed.read_bytes() != source.read_bytes():
                raise ValueError(f'Recurso instalado ausente o diferente: {installed}')
for agent_id in manifest['agents']:
    name = json.loads((root / 'adapters/antigravity/agents' / (agent_id + '.json')).read_text(encoding='utf-8'))['filename']
    source = root / 'generated/antigravity/agents' / name
    installed = agents_dest / name
    if not installed.is_file() or installed.read_bytes() != source.read_bytes():
        raise ValueError(f'Agente instalado ausente o diferente: {installed}')
PY
printf 'Instalación completada.\n'
if [ -n "$BACKUP_ROOT" ]; then printf 'Backup previo de skills y agents: %s\n' "$BACKUP_ROOT"; fi
