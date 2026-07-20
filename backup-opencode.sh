#!/usr/bin/env bash
# Importa los artefactos declarados de OpenCode a imports/ para revisión.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN="${1:-}"
case "$DRY_RUN" in
  "") ;;
  --dry-run) ;;
  -h|--help) printf 'Uso: ./backup-opencode.sh [--dry-run]\n'; exit 0 ;;
  *) printf 'Argumento desconocido: %s\n' "$DRY_RUN" >&2; exit 1 ;;
esac

OPENCODE_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
AGENTS_DIR="$OPENCODE_HOME/agent"
[ -d "$AGENTS_DIR" ] || AGENTS_DIR="$OPENCODE_HOME/agents"
args=(opencode --skills-dir "$OPENCODE_HOME/skills" --agents-dir "$AGENTS_DIR")
[ "$DRY_RUN" = "--dry-run" ] && args+=(--dry-run)
python3 "$SCRIPT_DIR/tools/import_installed.py" "${args[@]}"
