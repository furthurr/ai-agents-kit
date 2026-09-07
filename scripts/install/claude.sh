#!/usr/bin/env bash
#
# install-claude.sh — Instala las skills y agentes de este repo en Claude Code.
#
# Instala en las rutas personales de Claude Code:
#   generated/claude/skills/ -> ${CLAUDE_CONFIG_DIR:-~/.claude}/skills/
#   generated/claude/agents/ -> ${CLAUDE_CONFIG_DIR:-~/.claude}/agents/
#
# CLAUDE.md y settings.json no forman parte del kit y nunca se modifican.
#
# Uso:
#   ./scripts/install/claude.sh              # instala con backup de lo previo
#   ./scripts/install/claude.sh --force      # instala sin crear backup
#   ./scripts/install/claude.sh --dry-run    # muestra lo que haría, sin copiar
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
CLAUDE_HOME="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SKILLS_DEST="$CLAUDE_HOME/skills"
AGENTS_DEST="$CLAUDE_HOME/agents"
BACKUP_ROOT="$HOME/.claude-kit-backup/$TIMESTAMP"

SKILLS_SRC="$REPO_ROOT/generated/claude/skills"
AGENTS_SRC="$REPO_ROOT/generated/claude/agents"

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
  "$PYTHON" "$REPO_ROOT/tools/install_preflight.py" --platform claude "$@"
}

# --- Copia con exclusión de basura ---
copy_tree() { # $1=origen $2=destino
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude='.DS_Store' "$1/" "$2/"
  else
    mkdir -p "$2"
    cp -R "$1/." "$2/"
    rm -f "$2/.DS_Store" 2>/dev/null || true
  fi
}

backup_item() { # $1=ruta existente $2=subcarpeta-etiqueta
  [ "$FORCE" -eq 1 ] && return 0
  local path="$1" label="$2"
  [ -e "$path" ] || return 0
  mkdir -p "$BACKUP_ROOT/$label"
  cp -R "$path" "$BACKUP_ROOT/$label/"
  warn "backup: $(basename "$path") -> $BACKUP_ROOT/$label/"
}

# --- Instalar skills de un directorio origen ---
install_skills_from() { # $1=dir origen
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

install_skills() {
  if [ ! -d "$SKILLS_SRC" ]; then
    err "No existe $SKILLS_SRC"; exit 1
  fi
  info "Instalando ${BOLD}skills${RESET} -> $SKILLS_DEST"
  if [ "$DRY_RUN" -eq 0 ]; then mkdir -p "$SKILLS_DEST"; fi
  install_skills_from "$SKILLS_SRC"
}

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
printf "${BOLD}== Instalación de Skills y Agentes en Claude Code ==${RESET}\n"
echo
[ "$DRY_RUN" -eq 1 ] && warn "Modo --dry-run: no se copiará nada."
[ "$FORCE" -eq 1 ]   && warn "Modo --force: no se crearán backups."

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
info "Reinicia Claude Code para que detecte las nuevas skills y agentes."
