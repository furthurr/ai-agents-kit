#!/usr/bin/env bash
# Importa los artefactos declarados de Claude Code a imports/ para revisión.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DRY_RUN="${1:-}"
case "$DRY_RUN" in
  "") ;;
  --dry-run) ;;
  -h|--help) printf 'Uso: ./backup-claude.sh [--dry-run]\n'; exit 0 ;;
  *) printf 'Argumento desconocido: %s\n' "$DRY_RUN" >&2; exit 1 ;;
esac

CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
args=(claude --skills-dir "$CLAUDE_HOME/skills" --agents-dir "$CLAUDE_HOME/agents")
[ "$DRY_RUN" = "--dry-run" ] && args+=(--dry-run)
python3 "$REPO_ROOT/tools/import_installed.py" "${args[@]}"
