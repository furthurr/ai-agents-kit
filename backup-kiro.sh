#!/usr/bin/env bash
# Importa los artefactos declarados de Kiro a imports/ para revisión.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN="${1:-}"
case "$DRY_RUN" in
  "") ;;
  --dry-run) ;;
  -h|--help) printf 'Uso: ./backup-kiro.sh [--dry-run]\n'; exit 0 ;;
  *) printf 'Argumento desconocido: %s\n' "$DRY_RUN" >&2; exit 1 ;;
esac

KIRO_HOME="$HOME/.kiro"
args=(kiro --skills-dir "$KIRO_HOME/skills" --agents-dir "$KIRO_HOME/agents")
[ "$DRY_RUN" = "--dry-run" ] && args+=(--dry-run)
python3 "$SCRIPT_DIR/tools/import_installed.py" "${args[@]}"
