#!/usr/bin/env bash
#
# install-kiro.sh — Instala las skills y agentes de este repo en Kiro.
#
# A diferencia de install.sh (GitHub Copilot en ~/.copilot/) e install-opencode.sh
# (opencode en ~/.config/opencode/), este script instala en las rutas globales de
# Kiro:
#   generated/kiro/skills/  ->  ~/.kiro/skills/
#   generated/kiro/agents/  ->  ~/.kiro/agents/
#
# Los artefactos se generan desde canonical/ y adapters/kiro/ mediante
# tools/render.py. No se instalan fuentes editables ni overlays.
#
# Antes de sobrescribir, respalda lo existente (salvo --force).
#
# Uso:
#   ./install-kiro.sh              # instala con backup de lo previo
#   ./install-kiro.sh --force      # instala sin crear backup
#   ./install-kiro.sh --dry-run    # muestra lo que haría, sin copiar nada
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

# --- Rutas ---
KIRO_HOME="$HOME/.kiro"
SKILLS_DEST="$KIRO_HOME/skills"
AGENTS_DEST="$KIRO_HOME/agents"
BACKUP_ROOT="$HOME/.kiro-kit-backup/$TIMESTAMP"

SKILLS_SRC="$SCRIPT_DIR/generated/kiro/skills"
AGENTS_SRC="$SCRIPT_DIR/generated/kiro/agents"

# --- Copia con exclusión de basura ---
copy_tree() {  # $1=origen $2=destino
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.DS_Store' "$1/" "$2/"
  else
    mkdir -p "$2"
    cp -R "$1/." "$2/"
    rm -f "$2/.DS_Store" 2>/dev/null || true
  fi
}

backup_item() {  # $1=ruta existente $2=subcarpeta-etiqueta
  [ "$FORCE" -eq 1 ] && return 0
  local path="$1" label="$2"
  [ -e "$path" ] || return 0
  mkdir -p "$BACKUP_ROOT/$label"
  cp -R "$path" "$BACKUP_ROOT/$label/"
  warn "backup: $(basename "$path") -> $BACKUP_ROOT/$label/"
}

# --- Instalar skills de un directorio origen ---
install_skills_from() {  # $1=dir origen
  local base="$1" src name dest
  [ -d "$base" ] || return 0
  for src in "$base"/*/; do
    [ -d "$src" ] || continue
    name="$(basename "$src")"
    dest="$SKILLS_DEST/$name"
    if [ "$DRY_RUN" -eq 1 ]; then
      printf "    (dry-run) skill %s -> %s\n" "$name" "$dest"
      continue
    fi
    backup_item "$dest" "skills"
    copy_tree "$src" "$dest"
    ok "skill: $name"
  done
}

# --- Instalar skills generadas ---
install_skills() {
  if [ ! -d "$SKILLS_SRC" ]; then
    warn "No hay skills que instalar."; return 0
  fi
  info "Instalando ${BOLD}skills${RESET} -> $SKILLS_DEST"
  mkdir -p "$SKILLS_DEST"
  install_skills_from "$SKILLS_SRC"
}

# --- Instalar agentes (uno por uno) ---
install_agents() {
  [ -d "$AGENTS_SRC" ] || { warn "No existe $AGENTS_SRC — se omiten agentes."; return 0; }
  info "Instalando ${BOLD}agentes${RESET} -> $AGENTS_DEST"
  mkdir -p "$AGENTS_DEST"
  local src name dest
  for src in "$AGENTS_SRC"/*.md; do
    [ -f "$src" ] || continue
    name="$(basename "$src")"
    dest="$AGENTS_DEST/$name"
    if [ "$DRY_RUN" -eq 1 ]; then
      printf "    (dry-run) agente %s -> %s\n" "$name" "$dest"
      continue
    fi
    backup_item "$dest" "agents"
    cp "$src" "$dest"
    ok "agente: $name"
  done
}

echo
printf "${BOLD}== Instalación de Skills y Agentes en Kiro ==${RESET}\n"
echo
[ "$DRY_RUN" -eq 1 ] && warn "Modo --dry-run: no se copiará nada."
[ "$FORCE" -eq 1 ]   && warn "Modo --force: no se crearán backups."

install_skills
echo
install_agents

echo
ok "Instalación completada."
if [ "$DRY_RUN" -eq 0 ] && [ "$FORCE" -eq 0 ] && [ -d "$BACKUP_ROOT" ]; then
  info "Backups del contenido previo en: $BACKUP_ROOT"
fi
echo
info "Reinicia Kiro para que detecte las nuevas skills y agentes."
