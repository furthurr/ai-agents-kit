#!/usr/bin/env bash
#
# backup-opencode.sh — Actualiza este repositorio con las skills y agentes ACTUALES
# de opencode instalados en tu máquina. Operación inversa a install-opencode.sh.
#
# La instalación FUSIONA dos orígenes en un mismo destino, así que el respaldo tiene
# que DES-FUSIONAR usando el repo como referencia de qué es base y qué es override:
#   ~/.config/opencode/skills/<name>   ->  opencode/skills/<name>   (si <name> es override conocido)
#                                      ->  copilot/skills/<name>    (si <name> es base conocida)
#   ~/.config/opencode/agent/<name>.md ->  opencode/agents/<name>.md (si es agente conocido)
#
# Alcance (scoped): SÓLO respalda lo que el kit ya conoce. Las skills/agentes que
# tengas instalados pero NO existan en el repo se listan como aviso y NO se copian
# (así no arrastra contenido de otros orígenes del directorio global de opencode).
#
# No borra nada del repo: si algo del kit ya no está instalado, sólo te avisa para
# que tú decidas con git.
#
# Respeta XDG_CONFIG_HOME (igual que install-opencode.sh).
#
# Uso:
#   ./backup-opencode.sh            # sincroniza el repo con tu opencode actual
#   ./backup-opencode.sh --dry-run  # muestra lo que haría, sin copiar nada
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1
[ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ] && { grep '^#' "$0" | sed 's/^# \{0,1\}//' | sed '/^!/d'; exit 0; }

# --- Colores ---
if [ -t 1 ]; then
  BOLD="\033[1m"; GREEN="\033[32m"; YELLOW="\033[33m"; BLUE="\033[34m"; RESET="\033[0m"
else
  BOLD=""; GREEN=""; YELLOW=""; BLUE=""; RESET=""
fi
info()  { printf "${BLUE}➜${RESET} %b\n" "$1"; }
ok()    { printf "${GREEN}✓${RESET} %b\n" "$1"; }
warn()  { printf "${YELLOW}⚠${RESET} %b\n" "$1"; }

# --- Rutas de la instalación (origen) ---
OPENCODE_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
SKILLS_INSTALLED="$OPENCODE_HOME/skills"
AGENTS_INSTALLED="$OPENCODE_HOME/agent"
[ -d "$AGENTS_INSTALLED" ] || AGENTS_INSTALLED="$OPENCODE_HOME/agents"   # fallback plural

# --- Rutas del repo (destino) ---
BASE_SKILLS="$SCRIPT_DIR/copilot/skills"
OVERLAY_SKILLS="$SCRIPT_DIR/opencode/skills"
AGENTS_REPO="$SCRIPT_DIR/opencode/agents"

# --- Reemplaza el contenido de una skill conocida (refleja ediciones internas) ---
sync_tree() {  # $1=origen $2=destino
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude='.DS_Store' "$1/" "$2/"
  else
    rm -rf "${2:?}"; mkdir -p "$2"; cp -R "$1/." "$2/"; rm -f "$2/.DS_Store" 2>/dev/null || true
  fi
}

# --- Respaldar skills conocidas (des-fusión base/override) ---
backup_skills() {
  if [ ! -d "$SKILLS_INSTALLED" ]; then
    warn "No existe $SKILLS_INSTALLED — no hay skills de opencode instaladas."
    return 0
  fi
  info "Respaldando ${BOLD}skills${RESET} <- $SKILLS_INSTALLED"
  local src name dest kind
  for src in "$SKILLS_INSTALLED"/*/; do
    [ -d "$src" ] || continue
    name="$(basename "$src")"
    if [ -d "$OVERLAY_SKILLS/$name" ]; then
      dest="$OVERLAY_SKILLS/$name"; kind="override (opencode/skills)"
    elif [ -d "$BASE_SKILLS/$name" ]; then
      dest="$BASE_SKILLS/$name"; kind="base (copilot/skills)"
    else
      warn "skill ajena al kit, se ignora: $name"
      continue
    fi
    if [ "$DRY_RUN" -eq 1 ]; then
      printf "    (dry-run) skill %s -> %s\n" "$name" "$dest"
      continue
    fi
    sync_tree "${src%/}" "$dest"
    ok "skill: $name -> $kind"
  done
  # Avisar (sin borrar) de skills del kit que ya no están instaladas
  local repo_skill seen=""
  for repo_skill in "$BASE_SKILLS"/*/ "$OVERLAY_SKILLS"/*/; do
    [ -d "$repo_skill" ] || continue
    name="$(basename "$repo_skill")"
    case " $seen " in *" $name "*) continue ;; esac
    seen="$seen $name"
    [ -d "$SKILLS_INSTALLED/$name" ] || warn "en el repo pero NO instalada: $name (no se toca)"
  done
}

# --- Respaldar agentes conocidos (1:1) ---
backup_agents() {
  if [ ! -d "$AGENTS_INSTALLED" ]; then
    warn "No existe $AGENTS_INSTALLED — no hay agentes de opencode instalados."
    return 0
  fi
  info "Respaldando ${BOLD}agentes${RESET} <- $AGENTS_INSTALLED"
  local src name dest
  for src in "$AGENTS_INSTALLED"/*.md; do
    [ -f "$src" ] || continue
    name="$(basename "$src")"
    dest="$AGENTS_REPO/$name"
    if [ ! -f "$dest" ]; then
      warn "agente ajeno al kit, se ignora: $name"
      continue
    fi
    if [ "$DRY_RUN" -eq 1 ]; then
      printf "    (dry-run) agente %s -> %s\n" "$name" "$dest"
      continue
    fi
    cp "$src" "$dest"
    ok "agente: $name"
  done
  # Avisar (sin borrar) de agentes del kit que ya no están instalados
  local repo_agent
  for repo_agent in "$AGENTS_REPO"/*.md; do
    [ -f "$repo_agent" ] || continue
    name="$(basename "$repo_agent")"
    [ -f "$AGENTS_INSTALLED/$name" ] || warn "en el repo pero NO instalado: $name (no se toca)"
  done
}

echo
printf "${BOLD}== Respaldo de Skills y Agentes de opencode al repositorio ==${RESET}\n"
echo
[ "$DRY_RUN" -eq 1 ] && warn "Modo --dry-run: no se copiará nada."

backup_skills
echo
backup_agents

echo
ok "Respaldo completado. Revisa los cambios con: git status && git diff"
