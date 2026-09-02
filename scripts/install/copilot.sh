#!/usr/bin/env bash
#
# install.sh — Restaura las skills y agentes de GitHub Copilot en esta máquina.
#
# Copia el contenido de este repositorio a las rutas globales:
#   - generated/copilot/skills/  ->  ~/.copilot/skills/
#   - generated/copilot/agents/  ->  ~/.copilot/agents/
#
# Antes de sobrescribir, hace una copia de seguridad de lo existente.
#
# Uso:
#   ./scripts/install/copilot.sh                 # instalación normal (con backup automático)
#   ./scripts/install/copilot.sh --force         # sobrescribe sin crear backup
#   ./scripts/install/copilot.sh --dry-run       # muestra lo que haría, sin copiar nada
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

# --- Rutas destino ---
COPILOT_HOME="$HOME/.copilot"
SKILLS_DEST="$COPILOT_HOME/skills"
AGENTS_DEST="$COPILOT_HOME/agents"

BACKUP_ROOT="$HOME/.copilot-backup/$TIMESTAMP"

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
  "$PYTHON" "$REPO_ROOT/tools/install_preflight.py" --platform copilot "$@"
}

# --- Función de copia con backup ---
# $1 = carpeta origen, $2 = carpeta destino, $3 = etiqueta legible, $4 = etiqueta de backup
copy_dir() {
  local src="$1" dest="$2" label="$3" slug="$4"

  if [ ! -d "$src" ]; then
    err "No existe el origen '$src'."
    exit 1
  fi

  info "Instalando ${BOLD}$label${RESET} -> $dest"

  if [ "$DRY_RUN" -eq 1 ]; then
    # Solo -print portable: la variante printf de GNU no existe en macOS/BSD.
    find "$src" -type f -print | sed 's|^|    (dry-run) |'
    return 0
  fi

  # Backup de lo existente, salvo que --force lo haya desactivado explícitamente.
  # La ruta usa el slug, no la etiqueta legible: así queda restaurable sin
  # lidiar con espacios, paréntesis ni '~' en el nombre del directorio.
  if [ "$FORCE" -eq 0 ] && [ -d "$dest" ] && [ -n "$(ls -A "$dest" 2>/dev/null || true)" ]; then
    mkdir -p "$BACKUP_ROOT/$slug"
    cp -R "$dest/." "$BACKUP_ROOT/$slug/"
    warn "Backup del contenido previo en: $BACKUP_ROOT/$slug"
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
[ "$FORCE" -eq 1 ] && warn "Modo --force: no se crearán backups."

# Verificar el origen antes de tocar el destino: una instalación incompleta es
# peor que ninguna, porque se manifiesta como un agente que ignora su alcance.
if ! preflight --check-source; then
  err "Instalación abortada. Regenera los artefactos: python3 tools/render.py"
  exit 1
fi

# --- Ejecutar copias ---
copy_dir "$REPO_ROOT/generated/copilot/skills"  "$SKILLS_DEST"  "skills (~/.copilot/skills)"  "skills"
copy_dir "$REPO_ROOT/generated/copilot/agents"  "$AGENTS_DEST"  "agents (~/.copilot/agents)"  "agents"

echo
if [ "$DRY_RUN" -eq 1 ]; then
  ok "Dry-run finalizado: no se escribió nada."
  exit 0
fi

if ! preflight --check-installed --skills-dest "$SKILLS_DEST" --agents-dest "$AGENTS_DEST"; then
  err "La instalación quedó incompleta; no se declara completada."
  exit 1
fi

ok "Restauración completada."
if [ -d "$BACKUP_ROOT" ]; then
  info "Copias de seguridad guardadas en: $BACKUP_ROOT"
  info "Para restaurar: cp -R \"$BACKUP_ROOT\"/skills/. \"$SKILLS_DEST\"/"
fi
echo
info "Reinicia tu cliente de Copilot para que detecte los cambios."
