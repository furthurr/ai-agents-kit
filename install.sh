#!/usr/bin/env bash
#
# install.sh — Restaura las skills y agentes de GitHub Copilot en esta máquina.
#
# Copia el contenido de este repositorio a las rutas globales:
#   - copilot/skills/  ->  ~/.copilot/skills/
#   - copilot/agents/  ->  ~/.copilot/agents/
#
# Antes de sobrescribir, hace una copia de seguridad de lo existente.
#
# Uso:
#   ./install.sh                 # instalación normal (con backup automático)
#   ./install.sh --force         # sobrescribe sin preguntar
#   ./install.sh --dry-run       # muestra lo que haría, sin copiar nada
#
set -euo pipefail

# --- Configuración ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
FORCE=0
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --force)   FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//' | sed '/^!/d'
      exit 0
      ;;
    *) echo "Argumento desconocido: $arg" >&2; exit 1 ;;
  esac
done

# --- Colores ---
if [ -t 1 ]; then
  BOLD="\033[1m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; RESET="\033[0m"
else
  BOLD=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi

info()  { printf "${BLUE}➜${RESET} %b\n" "$1"; }
ok()    { printf "${GREEN}✓${RESET} %b\n" "$1"; }
warn()  { printf "${YELLOW}⚠${RESET} %b\n" "$1"; }

# --- Rutas destino ---
COPILOT_HOME="$HOME/.copilot"
SKILLS_DEST="$COPILOT_HOME/skills"
AGENTS_DEST="$COPILOT_HOME/agents"

BACKUP_ROOT="$HOME/.copilot-backup/$TIMESTAMP"

# --- Función de copia con backup ---
# $1 = carpeta origen, $2 = carpeta destino, $3 = etiqueta
copy_dir() {
  local src="$1" dest="$2" label="$3"

  if [ ! -d "$src" ]; then
    warn "No existe el origen '$src' — se omite $label."
    return 0
  fi

  info "Instalando ${BOLD}$label${RESET} -> $dest"

  if [ "$DRY_RUN" -eq 1 ]; then
    find "$src" -type f -printf "    (dry-run) %p\n" 2>/dev/null || \
      find "$src" -type f -exec echo "    (dry-run) {}" \;
    return 0
  fi

  # Backup de lo existente
  if [ -d "$dest" ] && [ -n "$(ls -A "$dest" 2>/dev/null || true)" ]; then
    mkdir -p "$BACKUP_ROOT/$label"
    cp -R "$dest/." "$BACKUP_ROOT/$label/"
    warn "Backup del contenido previo en: $BACKUP_ROOT/$label"
  fi

  mkdir -p "$dest"
  cp -R "$src/." "$dest/"
  ok "$label instalado."
}

echo
printf "${BOLD}== Restauración de Skills y Agentes de GitHub Copilot ==${RESET}\n"
echo

if [ "$DRY_RUN" -eq 1 ]; then
  warn "Modo --dry-run: no se copiará nada."
fi

# --- Ejecutar copias ---
copy_dir "$SCRIPT_DIR/copilot/skills"  "$SKILLS_DEST"  "skills (~/.copilot/skills)"
copy_dir "$SCRIPT_DIR/copilot/agents"  "$AGENTS_DEST"  "agents (~/.copilot/agents)"

echo
ok "Restauración completada."
if [ "$DRY_RUN" -eq 0 ] && [ -d "$BACKUP_ROOT" ]; then
  info "Copias de seguridad guardadas en: $BACKUP_ROOT"
fi
echo
info "Reinicia tu cliente de Copilot para que detecte los cambios."
