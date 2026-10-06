#!/usr/bin/env bash
# Exporta solo el inventario instalado a imports/antigravity; no modifica fuentes.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ARGS=(antigravity --skills-dir "$HOME/.gemini/config/skills" --agents-dir "$HOME/.gemini/config/agents")
for arg in "$@"; do
  case "$arg" in
    --dry-run) ARGS+=(--dry-run) ;;
    -h|--help) printf 'Uso: antigravity.sh [--dry-run]\n'; exit 0 ;;
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
exec "$PYTHON" "$REPO_ROOT/tools/import_installed.py" "${ARGS[@]}"
