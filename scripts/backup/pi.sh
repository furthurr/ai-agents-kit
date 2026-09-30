#!/usr/bin/env bash
# Importa los artefactos declarados de Pi a imports/ para revisión.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DRY_RUN="${1:-}"
case "$DRY_RUN" in
  "") ;;
  --dry-run) ;;
  -h|--help) printf 'Uso: ./scripts/backup/pi.sh [--dry-run]\n'; exit 0 ;;
  *) printf 'Argumento desconocido: %s\n' "$DRY_RUN" >&2; exit 1 ;;
esac

PI_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
args=(pi --skills-dir "$PI_DIR/skills" --agents-dir "$PI_DIR/prompts")
[ "$DRY_RUN" = "--dry-run" ] && args+=(--dry-run)
python3 "$REPO_ROOT/tools/import_installed.py" "${args[@]}"
