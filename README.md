# AI Agents Kit

Fuente versionada de skills y agentes para GitHub Copilot, OpenCode y Kiro. La
lógica común se mantiene una sola vez y se renderiza para cada herramienta.

## Estructura del Proyecto

```text
canonical/
  manifest.json                       # Inventario estable de skills, agentes y plataformas
  skills/<id>/                        # Lógica común de cada skill
    SKILL.md                          # Prompt principal
    references/                       # Archivos de apoyo cargados bajo demanda
  agents/<id>.md                      # Prompt común de cada agente, sin frontmatter

adapters/
  copilot/                            # Frontmatter, nombres y sustituciones de Copilot
  opencode/                           # Frontmatter, permisos y sustituciones de OpenCode
  kiro/                               # Frontmatter, tools, permisos y sustituciones de Kiro

generated/                            # Artefactos instalables (NO editar a mano)
  copilot/
  opencode/
  kiro/

tools/                                # Herramientas de desarrollo (Python 3)
  render.py                           # Generador determinista
  validate.py                         # Paridad y reproducibilidad
  measure_context.py                  # Métrica de contexto cargado y bajo demanda
  import_installed.py                 # Importación segura para revisar cambios locales

scripts/                              # Scripts de instalación e importación
  install/                            # Instalan artefactos generados en cada plataforma
    copilot.sh / copilot.ps1
    opencode.sh / opencode.ps1
    kiro.sh / kiro.ps1
  backup/                             # Importan artefactos instalados a imports/ para revisión
    copilot.sh / copilot.ps1
    opencode.sh / opencode.ps1
    kiro.sh / kiro.ps1
```

El kit incluye **8 skills** (`architecture`, `code-quality`, `data-api`,
`git-commit`, `release-management`, `sdd-spec`, `security`, `ui-design`) y **7
agentes**. `Git & Release Manager` orquesta las skills de commit y release.

## Flujo de Trabajo

1. Edita la lógica, comportamiento y contenido común en `canonical/`.
2. Edita exclusivamente las diferencias de plataforma en `adapters/`.
3. Ejecuta `python3 tools/render.py`.
4. Ejecuta `python3 tools/validate.py`.
5. Ejecuta `python3 tools/measure_context.py` para revisar el coste de contexto.
6. Revisa los cambios en `generated/` e instala la plataforma necesaria.

No edites `generated/` a mano: se reemplaza por completo en cada render.

## Instalar

Ejecuta siempre renderización y validación antes de instalar.

### macOS / Linux

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/measure_context.py

# Elige la plataforma:
./scripts/install/copilot.sh         # GitHub Copilot
./scripts/install/opencode.sh        # OpenCode
./scripts/install/kiro.sh            # Kiro
```

### Windows (PowerShell)

```powershell
python tools/render.py
python tools/validate.py
python tools/measure_context.py

# Elige la plataforma:
.\scripts\install\copilot.ps1
.\scripts\install\opencode.ps1
.\scripts\install\kiro.ps1
```

### Opciones

Los instaladores aceptan `--dry-run` / `-DryRun` y `--force` / `-Force`.

- `--dry-run`: muestra lo que haría sin copiar nada.
- `--force`: omite el backup previo.

### Destinos de instalación

| Plataforma | Destino                                     |
|------------|---------------------------------------------|
| Copilot    | `~/.copilot/skills/` y `~/.copilot/agents/` |
| OpenCode   | `~/.config/opencode/skills/` y `~/.config/opencode/agent/` |
| Kiro       | `~/.kiro/skills/` y `~/.kiro/agents/`       |

Reinicia Copilot, OpenCode o Kiro después de instalar para cargar los cambios.

## Importar Cambios Locales

Los scripts de backup no sobrescriben la fuente canónica. Importan solo elementos
declarados por el manifest a `imports/<plataforma>/<fecha>/`, donde puedes revisar
y promover manualmente los cambios apropiados a `canonical/` o `adapters/`.

```bash
./scripts/backup/copilot.sh --dry-run
./scripts/backup/opencode.sh --dry-run
./scripts/backup/kiro.sh --dry-run
```

En Windows usa `scripts\backup\copilot.ps1`, `scripts\backup\opencode.ps1` y
`scripts\backup\kiro.ps1`. Skills o agentes que no pertenecen al kit se muestran
como aviso y nunca se copian.

## Adaptadores

Los adaptadores solo pueden declarar datos propios de la herramienta:

- **Copilot**: nombre visible, `argument-hint`, herramientas y extensión
  `.agent.md`.
- **OpenCode**: `mode`, `temperature`, permisos, aliases y extensión `.md`.
- **Kiro**: `tools` por etiquetas (`read`, `write`, `shell`, `web`),
  `permissions.rules` y extensión `.md`. El nombre del agente proviene del nombre
  de archivo (sin campo `name`).

### Permisos en Kiro

Kiro usa `ask` como efecto por defecto (cualquier acción sin regla que coincida
pide confirmación) y añade reglas `deny` para comandos de shell irreversibles
(`rm *`, `rm -rf *`, `git reset --hard*`, `git checkout -f*`, `git checkout
--force*`, `git branch -D*`, `git clean*`).

### Permisos en OpenCode

OpenCode queda con confirmación por defecto para comandos de shell. Sus prompts
imponen restricciones de alcance y las operaciones sensibles requieren
confirmación explícita.

## Añadir Una Plataforma

1. Añade el identificador a `canonical/manifest.json`.
2. Crea `adapters/<plataforma>/platform.json`.
3. Crea un adaptador por agente con el frontmatter y nombre de salida requeridos.
4. Amplía `tools/render.py` solo si la nueva plataforma exige una estructura de
   salida distinta.
5. Renderiza, valida y añade su instalador en `scripts/install/`.

## Requisitos

- Python 3 para renderización, validación e importación.
- Bash o PowerShell para los scripts de instalación según el sistema.
- Git para versionar los cambios.

No incluyas secretos, tokens ni credenciales en ninguna fuente, adaptador,
artefacto generado o importación.

## Licencia

Apache-2.0
