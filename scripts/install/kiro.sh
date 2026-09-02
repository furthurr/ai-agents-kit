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
#   ./scripts/install/kiro.sh              # instala con backup de lo previo
#   ./scripts/install/kiro.sh --force      # instala sin crear backup
#   ./scripts/install/kiro.sh --dry-run    # muestra lo que haría, sin copiar nada
#
set -euo pipefail

# --- Configuración ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
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
  BOLD="\033[1m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; RED="\033[31m"; RESET="\033[0m"
else
  BOLD=""; GREEN=""; YELLOW=""; BLUE=""; RED=""; RESET=""
fi
info()  { printf "${BLUE}➜${RESET} %b\n" "$1"; }
ok()    { printf "${GREEN}✓${RESET} %b\n" "$1"; }
warn()  { printf "${YELLOW}⚠${RESET} %b\n" "$1"; }
err()   { printf "${RED}✗${RESET} %b\n" "$1" >&2; }

# --- Rutas ---
KIRO_HOME="$HOME/.kiro"
SKILLS_DEST="$KIRO_HOME/skills"
AGENTS_DEST="$KIRO_HOME/agents"
BACKUP_ROOT="$HOME/.kiro-kit-backup/$TIMESTAMP"

SKILLS_SRC="$REPO_ROOT/generated/kiro/skills"
AGENTS_SRC="$REPO_ROOT/generated/kiro/agents"

# --- Preflight compartido ---
# tools/install_preflight.py define qué significa "instalación completa" para
# los seis instaladores, tomando canonical/manifest.json como fuente de verdad.
PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then PYTHON="$candidate"; break; fi
done

preflight() {
  if [ -z "$PYTHON" ]; then
    err "Se requiere Python 3 para verificar la instalación."
    return 1
  fi
  "$PYTHON" "$REPO_ROOT/tools/install_preflight.py" --platform kiro "$@"
}

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
    err "No existe $SKILLS_SRC"; exit 1
  fi
  info "Instalando ${BOLD}skills${RESET} -> $SKILLS_DEST"
  if [ "$DRY_RUN" -eq 0 ]; then mkdir -p "$SKILLS_DEST"; fi
  install_skills_from "$SKILLS_SRC"
}

# --- Instalar agentes (uno por uno) ---
install_agents() {
  if [ ! -d "$AGENTS_SRC" ]; then
    err "No existe $AGENTS_SRC"; exit 1
  fi
  info "Instalando ${BOLD}agentes${RESET} -> $AGENTS_DEST"
  if [ "$DRY_RUN" -eq 0 ]; then mkdir -p "$AGENTS_DEST"; fi
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

# Verificar el origen antes de tocar el destino: una instalación incompleta es
# peor que ninguna, porque se manifiesta como un agente que ignora su alcance.
if ! preflight --check-source; then
  err "Instalación abortada. Regenera los artefactos: python3 tools/render.py"
  exit 1
fi

install_skills
echo
install_agents
echo

if [ "$DRY_RUN" -eq 1 ]; then
  ok "Dry-run finalizado: no se escribió nada."
  exit 0
fi

if ! preflight --check-installed --skills-dest "$SKILLS_DEST" --agents-dest "$AGENTS_DEST"; then
  err "La instalación quedó incompleta; no se declara completada."
  exit 1
fi

ok "Instalación completada."
if [ "$FORCE" -eq 0 ] && [ -d "$BACKUP_ROOT" ]; then
  info "Backups del contenido previo en: $BACKUP_ROOT"
  info "Para restaurar: cp -R \"$BACKUP_ROOT\"/skills/. \"$SKILLS_DEST\"/"
fi
echo
info "Reinicia Kiro para que detecte las nuevas skills y agentes."
