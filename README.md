# AI Agents Kit

Fuente versionada de skills y agentes para GitHub Copilot y OpenCode. La lógica
común se mantiene una sola vez y se renderiza para cada herramienta.

## Flujo de trabajo

1. Edita la lógica, comportamiento y contenido común en `canonical/`.
2. Edita exclusivamente las diferencias de plataforma en `adapters/`.
3. Ejecuta `python3 tools/render.py`.
4. Ejecuta `python3 tools/validate.py`.
5. Ejecuta `python3 tools/measure_context.py` para revisar el coste de contexto.
6. Revisa los cambios en `generated/` e instala la plataforma necesaria.

No edites `generated/` a mano: se reemplaza por completo en cada render.

## Estructura

```text
canonical/
  manifest.json                    # Inventario estable de skills, agentes y plataformas
  skills/<id>/                     # Lógica común de cada skill
  agents/<id>.md                   # Prompt común de cada agente, sin frontmatter
adapters/
  copilot/                         # Frontmatter, nombres y sustituciones de Copilot
  opencode/                        # Frontmatter, permisos y sustituciones de OpenCode
generated/
  copilot/                         # Artefactos instalables, generados y versionados
  opencode/                        # Artefactos instalables, generados y versionados
tools/
  render.py                        # Generador determinista
  validate.py                      # Paridad y reproducibilidad
  measure_context.py                # Métrica de contexto cargado y bajo demanda
  import_installed.py              # Importación segura para revisar cambios locales
```

El kit incluye 8 skills (`architecture`, `code-quality`, `data-api`,
`git-commit`, `release-management`, `sdd-spec`, `security`, `ui-design`) y 7
agentes. `Git & Release Manager` orquesta las skills de commit y release.

## Adaptadores

Los adaptadores solo pueden declarar datos propios de la herramienta:

- Copilot: nombre visible, `argument-hint`, herramientas y extensión
  `.agent.md`.
- OpenCode: `mode`, `temperature`, permisos, aliases y extensión `.md`.

OpenCode queda con confirmación por defecto para comandos de shell. Sus prompts
siguen imponiendo restricciones de alcance, y las operaciones sensibles requieren
confirmación explícita.

## Instalar

Ejecuta siempre renderización y validación antes de instalar.

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/measure_context.py
./install.sh                 # GitHub Copilot en macOS/Linux
./install-opencode.sh        # OpenCode en macOS/Linux
```

En Windows:

```powershell
python tools/render.py
python tools/validate.py
.\install.ps1
.\install-opencode.ps1
```

Los instaladores aceptan `--dry-run` / `-DryRun` y `--force` / `-Force`.
`--force` omite el backup previo. OpenCode respeta `XDG_CONFIG_HOME`.
Reinicia Copilot u OpenCode después de instalar para cargar los cambios.

## Importar Cambios Locales

Los backups no sobrescriben la fuente canónica. Importan solo elementos declarados
por el manifest a `imports/<plataforma>/<fecha>/`, donde puedes revisar y promover
manualmente los cambios apropiados a `canonical/` o `adapters/`.

```bash
./backup.sh --dry-run
./backup-opencode.sh --dry-run
```

En Windows usa `backup.ps1` y `backup-opencode.ps1`. Skills o agentes que no
pertenecen al kit se muestran como aviso y nunca se copian.

## Añadir Una Plataforma

1. Añade el identificador a `canonical/manifest.json`.
2. Crea `adapters/<plataforma>/platform.json`.
3. Crea un adaptador por agente con el frontmatter y nombre de salida requeridos.
4. Amplía `tools/render.py` solo si la nueva plataforma exige una estructura de
   salida distinta.
5. Renderiza, valida y añade su instalador.

## Requisitos

- Python 3 para renderización, validación e importación.
- Bash o PowerShell para los scripts de instalación según el sistema.
- Git para versionar los cambios.

No incluyas secretos, tokens ni credenciales en ninguna fuente, adaptador,
artefacto generado o importación.

## Licencia

Apache-2.0
