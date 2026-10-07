#!/usr/bin/env bash
#
# install-pi.sh — Instala las skills y agentes de este repo en Pi.
#
# Pi descubre skills desde <agent-dir>/skills/ y prompt templates desde
# <agent-dir>/prompts/. El directorio se toma de $PI_CODING_AGENT_DIR o
# ~/.pi/agent por defecto.
#
#   generated/pi/skills/  ->  <agent-dir>/skills/
#   generated/pi/agents/  ->  <agent-dir>/prompts/
#
# Los artefactos se generan desde canonical/ y adapters/pi/ mediante
# tools/render.py. No se instalan fuentes editables ni overlays.
#
# Antes de sobrescribir, respalda lo existente (salvo --force).
#
# Uso:
#   --migrate-retired-agents: retirada opt-in con backup obligatorio.
#   --approve-retired-file RUTA --approve-retired-sha256 SHA: repetibles, ruta exacta.
#   --additional-agents-dest RUTA: destino local adicional para migración explícita.
#   ./scripts/install/pi.sh              # instala con backup de lo previo
#   ./scripts/install/pi.sh --force      # instala sin crear backup
#   ./scripts/install/pi.sh --dry-run    # muestra lo que haría, sin copiar nada
#
set -euo pipefail

# --- Configuración ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
FORCE=0
DRY_RUN=0
MIGRATE=0
MIGRATION_ARGS=(--backup-root "$HOME/.ai-agents-kit-retired-backups")

while [ "$#" -gt 0 ]; do
  arg="$1"; shift
  case "$arg" in
    --force)   FORCE=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --migrate-retired-agents) MIGRATE=1 ;;
    --approve-retired-file|--approve-retired-sha256|--additional-agents-dest)
      [ "$#" -gt 0 ] || { echo "Falta valor para $arg" >&2; exit 2; }
      MIGRATION_ARGS+=("$arg" "$1"); shift ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \{0,1\}//' | sed '/^!/d'
      exit 0
      ;;
    *) echo "Argumento desconocido: $arg" >&2; exit 2 ;;
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
PI_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
SKILLS_DEST="$PI_DIR/skills"
AGENTS_DEST="$PI_DIR/prompts"
BACKUP_ROOT="$HOME/.pi-kit-backup/$TIMESTAMP"

SKILLS_SRC="$REPO_ROOT/generated/pi/skills"
AGENTS_SRC="$REPO_ROOT/generated/pi/agents"

# --- Preflight compartido ---
PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then PYTHON="$candidate"; break; fi
done

preflight() {
  if [ -z "$PYTHON" ]; then
    err "Se requiere Python 3 para verificar la instalación."
    return 1
  fi
  "$PYTHON" "$REPO_ROOT/tools/install_preflight.py" --platform pi "$@"
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

# --- Instalar agentes como prompt templates ---
install_agents() {
  if [ ! -d "$AGENTS_SRC" ]; then
    err "No existe $AGENTS_SRC"; exit 1
  fi
  info "Instalando ${BOLD}prompt templates${RESET} -> $AGENTS_DEST"
  if [ "$DRY_RUN" -eq 0 ]; then mkdir -p "$AGENTS_DEST"; fi
  local src name dest
  for src in "$AGENTS_SRC"/*.md; do
    [ -f "$src" ] || continue
    name="$(basename "$src")"
    dest="$AGENTS_DEST/$name"
    if [ "$DRY_RUN" -eq 1 ]; then
      printf "    (dry-run) template %s -> %s\n" "$name" "$dest"
      continue
    fi
    backup_item "$dest" "prompts"
    cp "$src" "$dest"
    ok "template: $name"
  done
}

echo
printf "${BOLD}== Instalación de Skills y Agentes en Pi ==${RESET}\n"
echo
[ "$DRY_RUN" -eq 1 ] && warn "Modo --dry-run: no se copiará nada."
[ "$FORCE" -eq 1 ]   && warn "Modo --force: omite backup de sobrescritura vigente; retirada siempre con backup."

VALIDATION_ARGS=(--agents-dest "$AGENTS_DEST" --skills-dest "$SKILLS_DEST")
[ "$MIGRATE" -eq 0 ] || VALIDATION_ARGS+=(--migration-requested)
preflight --validate-migration "${VALIDATION_ARGS[@]}" "${MIGRATION_ARGS[@]}"
if ! preflight --check-source; then
  err "Instalación abortada. Regenera los artefactos: python3 tools/render.py"
  exit 1
fi

install_skills
echo
install_agents
echo

if [ "$DRY_RUN" -eq 1 ]; then
  [ "$MIGRATE" -eq 0 ] || preflight --migrate-retired-agents --dry-run --agents-dest "$AGENTS_DEST" "${MIGRATION_ARGS[@]}"
  ok "Dry-run finalizado: no se escribió nada."
  exit 0
fi

if ! preflight --check-installed --skills-dest "$SKILLS_DEST" --agents-dest "$AGENTS_DEST"; then
  err "La instalación quedó incompleta; no se declara completada."
  exit 1
fi

[ "$MIGRATE" -eq 0 ] || preflight --migrate-retired-agents --skills-dest "$SKILLS_DEST" --agents-dest "$AGENTS_DEST" "${MIGRATION_ARGS[@]}"
ok "Instalación completada."
if [ "$FORCE" -eq 0 ] && [ -d "$BACKUP_ROOT" ]; then
  info "Backups del contenido previo en: $BACKUP_ROOT"
  info "Para restaurar: cp -R \"$BACKUP_ROOT\"/skills/. \"$SKILLS_DEST\"/"
fi
echo
info "Reinicia Pi para que detecte las nuevas skills y comandos."
info "Skills: /skill:<nombre>  ·  Agentes: /<nombre> <tarea>"
