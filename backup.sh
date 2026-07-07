#!/usr/bin/env bash
#
# backup.sh — Actualiza este repositorio con las skills y agentes ACTUALES de tu máquina.
#
# Copia DESDE las rutas globales HACIA este repositorio (operación inversa a install.sh):
#   ~/.copilot/skills/   ->  copilot/skills/
#   ~/.copilot/agents/   ->  copilot/agents/
#
# Úsalo cuando hayas creado o modificado skills/agentes y quieras versionarlos.
#
# Uso:
#   ./backup.sh            # sincroniza el repo con tu entorno actual
#   ./backup.sh --dry-run  # muestra lo que haría, sin copiar nada
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

if [ -t 1 ]; then
  BOLD="\033[1m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; RESET="\033[0m"
else
  BOLD=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi
info()  { printf "${BLUE}➜${RESET} %b\n" "$1"; }
ok()    { printf "${GREEN}✓${RESET} %b\n" "$1"; }
warn()  { printf "${YELLOW}⚠${RESET} %b\n" "$1"; }

COPILOT_HOME="$HOME/.copilot"

# $1 = origen (global), $2 = destino (repo), $3 = etiqueta
sync_dir() {
  local src="$1" dest="$2" label="$3"
  if [ ! -d "$src" ]; then
    warn "No existe '$src' — se omite $label."
    return 0
  fi
  info "Respaldando ${BOLD}$label${RESET} <- $src"
  if [ "$DRY_RUN" -eq 1 ]; then
    find "$src" -type f -exec echo "    (dry-run) {}" \;
    return 0
  fi
  mkdir -p "$dest"
  # Limpia el destino para reflejar borrados, luego copia
  rm -rf "${dest:?}/"* 2>/dev/null || true
  cp -R "$src/." "$dest/"
  ok "$label respaldado."
}

echo
printf "${BOLD}== Respaldo de Skills y Agentes al repositorio ==${RESET}\n"
echo
[ "$DRY_RUN" -eq 1 ] && warn "Modo --dry-run: no se copiará nada."

sync_dir "$COPILOT_HOME/skills" "$SCRIPT_DIR/copilot/skills" "skills"
sync_dir "$COPILOT_HOME/agents" "$SCRIPT_DIR/copilot/agents" "agents"

echo
ok "Respaldo completado. Revisa los cambios con: git status && git diff"
