# Instalación

Los instaladores copian los artefactos de `generated/<plataforma>/` a las rutas
globales de cada herramienta. **No edites `generated/` a mano**: se regenera por
completo en cada render.

## Requisitos

- **Python 3** — render, validación, métricas e importación
- **Bash** (macOS/Linux) o **PowerShell** (Windows) — scripts de install/backup
- **Git** — versionar cambios del kit (recomendado)
- La herramienta destino instalada (Copilot, OpenCode, Kiro, Claude Code, Pi o
  Antigravity 2.0, según el alcance de cada distribución)

## Flujo recomendado

Siempre en este orden:

1. Renderizar artefactos  
2. Validar paridad y reproducibilidad  
3. (Opcional) Medir coste de contexto  
4. Instalar la plataforma deseada  
5. Reiniciar la herramienta destino

### macOS / Linux

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/measure_context.py   # opcional

./scripts/install/copilot.sh       # GitHub Copilot
./scripts/install/opencode.sh      # OpenCode
./scripts/install/kiro.sh          # Kiro
./scripts/install/claude.sh        # Claude Code
./scripts/install/pi.sh            # Pi
./scripts/install/antigravity.sh   # Antigravity 2.0
```

### Windows (PowerShell)

```powershell
python tools/render.py
python tools/validate.py
python tools/measure_context.py    # opcional

.\scripts\install\copilot.ps1
.\scripts\install\opencode.ps1
.\scripts\install\kiro.ps1
.\scripts\install\claude.ps1
.\scripts\install\pi.ps1
.\scripts\install\antigravity.ps1
```

Puedes instalar **varias plataformas** en la misma máquina; cada script es
independiente.

## Opciones de los instaladores

| Opción | Bash | PowerShell | Efecto |
|--------|------|------------|--------|
| Dry-run | `--dry-run` | `-DryRun` | Muestra qué haría sin copiar |
| Force | `--force` | `-Force` | Omite el backup previo de lo instalado |
| Ayuda | `-h` / `--help` | (según script) | Uso del script |

Ejemplos:

```bash
./scripts/install/opencode.sh --dry-run
./scripts/install/opencode.sh --force
```

## Destinos de instalación

| Plataforma | Skills | Agentes |
|------------|--------|---------|
| Copilot | `~/.copilot/skills/` | `~/.copilot/agents/` |
| OpenCode | `~/.config/opencode/skills/` (o `$XDG_CONFIG_HOME/opencode/skills/`) | `~/.config/opencode/agent/` |
| Kiro | `~/.kiro/skills/` | `~/.kiro/agents/` |
| Claude Code | `~/.claude/skills/` (o `$CLAUDE_CONFIG_DIR/skills/`) | `~/.claude/agents/` (o `$CLAUDE_CONFIG_DIR/agents/`) |
| Pi | `<agent-dir>/skills/` | `<agent-dir>/prompts/` |
| Antigravity 2.0 | `~/.gemini/config/skills/` | `~/.gemini/config/agents/` |

### Antigravity 2.0

El alcance inicial es global: diez directorios de skills con sus recursos y ocho
agentes `<id>.md`. Bash resuelve `~` desde HOME; PowerShell usa USERPROFILE, no
un carácter `~` literal. La instalación no modifica credenciales, settings,
`GEMINI.md`, `AGENTS.md` ni `.agents/rules/*.md`.
El bridge `GEMINI.md` → `AGENTS.md` **no está implementado**; declarar fuentes
de steering no equivale a crear ese puente.

```bash
./scripts/install/antigravity.sh --dry-run
./scripts/install/antigravity.sh
# Solo si decides omitir el respaldo previo:
./scripts/install/antigravity.sh --force
```

```powershell
.\scripts\install\antigravity.ps1 -DryRun
.\scripts\install\antigravity.ps1
# Solo si decides omitir el respaldo previo:
.\scripts\install\antigravity.ps1 -Force
```

En ambos shells, las skills se copian por **fusión**: se conservan elementos
ajenos al inventario y recursos propios dentro de skills existentes; también
pueden quedar recursos antiguos. Los agentes del inventario se sustituyen por
archivo. No hay borrado espejo ni rollback transaccional automático: un fallo de
copia puede dejar cambios parciales, devuelve error y requiere revisión manual.
El respaldo previo, si lo hubo, permite recuperar elementos sobrescritos.

La copia de archivos y el preflight no prueban descubrimiento ni funcionamiento
del host. Los scripts de instalación/exportación tienen evidencia de ejecución
con fixtures en Linux, macOS y Windows: **22/22 pruebas nativas por OS**, Python
3.10, [run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
**Runtime Antigravity: PENDIENTE** para descubrimiento 8/10, selección UI, carga
de referencias e `invoke_subagent`. La versión de referencia de la aplicación
será la registrada en un smoke completo exitoso, no el build de CI del kit.
El CLI usa otra ruta global de skills (`~/.gemini/antigravity-cli/skills/`);
este instalador no cubre esa ruta ni certifica agentes personalizados del IDE
standalone. Recarga y selección real: [antigravity-smoke.md](antigravity-smoke.md).

### Pi

Pi descubre las skills como Agent Skills nativos y los agentes como prompt
templates invocables. Tras instalar y reiniciar Pi:

- **Skills:** `/skill:<nombre>` — por ejemplo, `/skill:sdd-spec`.
- **Agentes:** `/<nombre> <tarea>` — por ejemplo, `/sdd implementar login`.

El directorio de Pi se toma de `$PI_CODING_AGENT_DIR` o `~/.pi/agent` por
defecto. Los agentes son plantillas de prompt dentro de la sesión activa: no
crean subagentes aislados ni aplican permisos distintos por agente.

### Copilot y Claude Code en VS Code

VS Code descubre tanto los agentes Copilot de `~/.copilot/agents/` como los
agentes con formato Claude de `~/.claude/agents/`. Si instalas ambas plataformas,
el kit conserva los agentes en las dos rutas para que cada herramienta funcione,
pero marca la copia Claude con `user-invocable: false`: Claude Code la sigue
cargando y VS Code muestra solo la copia `*.agent.md` de Copilot. Después de
actualizar una instalación, reinicia VS Code para refrescar el selector.

Antes de sobrescribir, los instaladores (salvo `--force`) crean un backup local
timestamped. Rutas por plataforma:

| Plataforma | Raíz de backup |
|------------|----------------|
| Copilot | `~/.copilot-backup/<AAAAMMDD-HHMMSS>/` |
| OpenCode | `~/.opencode-kit-backup/<AAAAMMDD-HHMMSS>/` |
| Kiro | `~/.kiro-kit-backup/<AAAAMMDD-HHMMSS>/` |
| Claude Code | `~/.claude-kit-backup/<AAAAMMDD-HHMMSS>/` |
| Pi | `~/.pi-kit-backup/<AAAAMMDD-HHMMSS>/` |
| Antigravity | `~/.antigravity-kit-backup/<timestamp>/` |

Dentro de cada backup, el contenido previo queda en `skills/` y `agents/`.
En Antigravity solo se respaldan elementos existentes que se van a sobrescribir;
no es una instantánea completa del perfil. Una colisión de timestamp se resuelve
sin reutilizar ni borrar un respaldo anterior.

## Garantías del instalador

Los instaladores delegan en `tools/install_preflight.py`, que toma
`canonical/manifest.json` como fuente de verdad. De ahí se derivan tres
garantías verificadas por `tools/test_install.py`:

El contrato de Antigravity se comprueba además con
`tools/test_antigravity_install.py`; sus ejecuciones por OS deben acreditarse por
separado y no equivalen a una prueba runtime del host. El run citado acredita
22/22 en cada uno de los tres OS; el SHA y los resultados por job se detallan en
[evidencia automatizada de CI](antigravity-smoke.md#evidencia-automatizada-de-ci).

1. **No instalan de menos en silencio.** Si falta cualquier skill o agente
   declarado en el manifest, el script aborta con código distinto de cero
   **antes** de tocar el destino y no imprime que la instalación se completó.
   Una instalación parcial es peor que ninguna: se manifiesta como un agente que
   parece ignorar su alcance cuando en realidad falta un archivo.
2. **`--dry-run` no escribe nada.** No crea ni modifica directorios, ni siquiera
   los de destino.
3. **Verifican antes de declarar éxito.** Al terminar, comprueban que el destino
   contiene lo que el manifest declara. El preflight comprueba presencia de
   archivos principales, no YAML, hashes ni todos los recursos de referencia;
   esas comprobaciones corresponden a validación y pruebas de copia completa.

Si el preflight aborta, casi siempre falta regenerar:

```bash
python3 tools/render.py
python3 tools/validate.py
```

Los instaladores también **informan** de skills o agentes presentes en el destino
que el manifest no declara (propios tuyos, o restos de una versión anterior del
kit). Solo lo informan: **nunca borran nada**, porque no hay forma fiable de
distinguir un artefacto obsoleto del kit de una skill propia. Retíralos a mano si
ya no aplican (ver *Desinstalar*).

## Actualizar a Code Review

El kit sustituye los agentes `code-quality` y `security` por `code-review` en las
distribuciones del catálogo de seis plataformas. **Las skills `code-quality` y `security` siguen existiendo**,
igual que `.quality/`, `.security/` y sus IDs `QLT`/`SEC`: no hay migración de datos.

1. Regenera y valida el kit e instala tu plataforma con su script habitual.
2. Revisa el backup de la instalación anterior. Los instaladores informan de
   agentes extra pero no los borran automáticamente.
3. Si confirmas que son las copias anteriores del kit, retira manualmente solo
   `code-quality.md` y `security.md` del directorio **de agentes** de esa plataforma
   (Copilot: `code-quality.agent.md` y `security.agent.md`; Pi: directorio `prompts/`).
   Conserva archivos personalizados y las carpetas homónimas **de skills**.
4. Cierra y reinicia la herramienta (OpenCode incluido) para cargar `code-review`
   y refrescar el selector. En Pi la invocación es `/code-review <tarea>`.

Los nombres retirados no tienen aliases en el catálogo nuevo. Las peticiones de
solo calidad, solo seguridad o revisión completa se hacen al mismo agente.
No necesitas borrar documentación ni hallazgos existentes de tus proyectos.

## Tras instalar

1. **Reinicia** la herramienta para que cargue skills y agentes nuevos.
2. Comprueba que aparecen los agentes del [catálogo](catalogo.md).
3. Abre un proyecto de prueba y prueba una petición simple (p. ej. documentar
   arquitectura o preparar un commit en dry-run conversacional).

Detalle de uso diario: [uso.md](uso.md).

## Importar cambios hechos en la instalación local

Si editaste skills/agentes **ya instalados** en tu máquina y quieres revisarlos
sin pisar la fuente del repo:

```bash
./scripts/backup/copilot.sh --dry-run
./scripts/backup/opencode.sh --dry-run
./scripts/backup/kiro.sh --dry-run
./scripts/backup/claude.sh --dry-run
./scripts/backup/pi.sh --dry-run
./scripts/backup/antigravity.sh --dry-run
```

En Windows: `scripts\backup\*.ps1`.

Antigravity, simulación y exportación efectiva:

```bash
./scripts/backup/antigravity.sh --dry-run
./scripts/backup/antigravity.sh
```

```powershell
.\scripts\backup\antigravity.ps1 -DryRun
.\scripts\backup\antigravity.ps1
```

Estos scripts exportan lo instalado **ahora** a
`imports/antigravity/<timestamp>/{skills,agents}/`; no recuperan el contenido
anterior de `~/.antigravity-kit-backup/<timestamp>/`. La exportación tolera
elementos no instalados con avisos: un import parcial no demuestra instalación
completa. Los errores de copia se propagan como salida distinta de cero.
El importador compartido usa timestamps con precisión de segundos: evita dos
exportaciones en el mismo segundo. Si ya existe una carpeta de skill, la colisión
produce error; en una instalación parcial con solo agentes puede sobrescribir
archivos de la exportación anterior. No reutilices deliberadamente ese destino.
Este límite del importador no afecta al respaldo previo del instalador Antigravity,
que reserva una carpeta nueva con sufijo ante colisiones.

Comportamiento:

- **No sobrescriben** `canonical/` ni `adapters/`.
- Copian solo elementos declarados en el manifest a `imports/<plataforma>/<fecha>/`.
- Skills o agentes ajenos al kit se listan como aviso y **no se copian**.
- Tú decides qué promover manualmente a `canonical/` o `adapters/`.

## Restaurar un backup

Cada instalación sin `--force` deja el estado anterior en su raíz de backup (ver
*Destinos de instalación*). Para volver atrás, elige el backup por fecha y copia
su contenido sobre el destino. Ejemplo con Kiro:

```bash
ls ~/.kiro-kit-backup/                       # elige la marca de tiempo
BK=~/.kiro-kit-backup/20260831-120000        # ajusta a la tuya

cp -R "$BK"/skills/. ~/.kiro/skills/
cp -R "$BK"/agents/. ~/.kiro/agents/
```

Para las otras plataformas cambia la raíz de backup y el destino:

| Plataforma | Origen | Destino skills | Destino agentes |
|------------|--------|----------------|-----------------|
| Copilot | `~/.copilot-backup/<fecha>/` | `~/.copilot/skills/` | `~/.copilot/agents/` |
| OpenCode | `~/.opencode-kit-backup/<fecha>/` | `~/.config/opencode/skills/` | `~/.config/opencode/agent/` |
| Kiro | `~/.kiro-kit-backup/<fecha>/` | `~/.kiro/skills/` | `~/.kiro/agents/` |
| Claude Code | `~/.claude-kit-backup/<fecha>/` | `~/.claude/skills/` | `~/.claude/agents/` |
| Pi | `~/.pi-kit-backup/<fecha>/` | `~/.pi/agent/skills/` | `~/.pi/agent/prompts/` |
| Antigravity | `~/.antigravity-kit-backup/<timestamp>/` | `~/.gemini/config/skills/` | `~/.gemini/config/agents/` |

En Windows (PowerShell):

```powershell
$BK = "$env:USERPROFILE\.kiro-kit-backup\20260831-120000"
Copy-Item -Path "$BK\skills\*" -Destination "$env:USERPROFILE\.kiro\skills" -Recurse -Force
Copy-Item -Path "$BK\agents\*" -Destination "$env:USERPROFILE\.kiro\agents" -Recurse -Force
```

Restaurar **fusiona**: recupera lo anterior, pero no elimina lo que el kit añadió
después. Si quieres partir de cero, desinstala primero y restaura luego.

Ejemplo Antigravity, ajustando el timestamp tras revisar el respaldo. Las carpetas
`skills` o `agents` pueden faltar si no había elementos previos de ese tipo:

```bash
BK="$HOME/.antigravity-kit-backup/20261006-120000"
mkdir -p "$HOME/.gemini/config/skills" "$HOME/.gemini/config/agents"
if [ -d "$BK/skills" ]; then cp -R "$BK/skills/." "$HOME/.gemini/config/skills/"; fi
if [ -d "$BK/agents" ]; then cp -R "$BK/agents/." "$HOME/.gemini/config/agents/"; fi
```

```powershell
$BK = "$env:USERPROFILE\.antigravity-kit-backup\20261006-120000"
$Skills = "$env:USERPROFILE\.gemini\config\skills"
$Agents = "$env:USERPROFILE\.gemini\config\agents"
New-Item -ItemType Directory -Path $Skills, $Agents -Force | Out-Null
if (Test-Path -LiteralPath "$BK\skills") {
    Get-ChildItem -LiteralPath "$BK\skills" -Force | Copy-Item -Destination $Skills -Recurse -Force
}
if (Test-Path -LiteralPath "$BK\agents") {
    Get-ChildItem -LiteralPath "$BK\agents" -Force | Copy-Item -Destination $Agents -Recurse -Force
}
```

Revisa los archivos recuperados y recarga el host siguiendo el smoke. Esta
restauración manual de skills **y** agentes no retira archivos añadidos después
ni recupera elementos sin respaldo (por ejemplo, tras `--force`/`-Force`).

## Desinstalar

Los instaladores no traen un modo de desinstalación automática: borrar en el
`HOME` del usuario es irreversible y el destino puede contener skills propias
junto a las del kit. El procedimiento es manual y explícito.

Primero revisa qué hay instalado y qué declara el manifest:

```bash
python3 tools/install_preflight.py --platform kiro --check-installed \
  --skills-dest ~/.kiro/skills --agents-dest ~/.kiro/agents
```

Lo que aparezca como *no declarado en el manifest* **no** pertenece al kit
(o es de una versión anterior): decide caso por caso.

Para retirar solo lo que el kit instaló, lista los nombres y bórralos tras
revisarlos. Con Kiro:

```bash
# 1. Ver qué se borraría (no borra nada)
python3 -c "import json;print('\n'.join(json.load(open('canonical/manifest.json'))['skills']))"

# 2. Borrar las skills del kit, una vez revisada la lista
for s in $(python3 -c "import json;print(' '.join(json.load(open('canonical/manifest.json'))['skills']))"); do
  rm -rf ~/.kiro/skills/"$s"
done

# 3. Borrar los agentes del kit
for a in ~/.kiro/agents/*.md; do echo "$a"; done   # revisa antes de borrar
```

Revisa siempre la lista del paso 1 antes de ejecutar el paso 2. Si tienes skills
propias con el mismo nombre que una del kit, respáldalas primero.

Alternativa sin borrar nada: restaura el backup previo a la primera instalación.

La carpeta `imports/` está en `.gitignore` (puede contener configuración local).

Herramienta relacionada: `tools/import_installed.py` (usada por el flujo de
importación).

## Actualizar el kit

```bash
git pull
python3 tools/render.py
python3 tools/validate.py
./scripts/install/<plataforma>.sh
# reiniciar la herramienta
```

## Seguridad

- No incluyas secretos, tokens ni credenciales en fuentes, adapters, generated o
  imports.
- Revisa siempre el dry-run si no estás seguro del destino.
- Los agentes de Git/release **exigen confirmación** antes de commit, push o tag;
  eso no sustituye tu criterio al instalar en una máquina compartida.
