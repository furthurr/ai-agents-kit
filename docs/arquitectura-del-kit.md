# Arquitectura del kit

Cómo se construyen los artefactos instalables. No describe la arquitectura de
*tus* proyectos (eso lo hace la skill `architecture`); describe **este
repositorio**.

## Vista general

```text
┌─────────────────────────────────────────────────────────────┐
│  canonical/                                                 │
│    manifest.json      inventario skills / agents / platforms│
│    skills/<id>/       SKILL.md + references/ (+ extras)     │
│    agents/<id>.md     prompt común sin frontmatter de tool  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  adapters/<platform>/                                       │
│    platform.json      sustituciones globales {{tokens}}     │
│    agents/<id>.json   filename + frontmatter + overrides    │
│    skills/<id>.json   opcional                              │
└────────────────────────────┬────────────────────────────────┘
                             │  tools/render.py
┌────────────────────────────▼────────────────────────────────┐
│  generated/<platform>/                                      │
│    skills/<id>/       listo para copiar                     │
│    agents/<file>      con frontmatter de la herramienta     │
└────────────────────────────┬────────────────────────────────┘
                             │  scripts/install/*
                             ▼
              ~/.copilot  ·  ~/.config/opencode  ·  ~/.kiro
```

## Capas y responsabilidades

| Capa | Responsabilidad | ¿Se edita a mano? |
|------|-----------------|-------------------|
| `canonical/` | Comportamiento y texto compartido | Sí |
| `adapters/` | Diferencias por herramienta | Sí |
| `generated/` | Salida determinista del render | **No** |
| `tools/` | Render, validación, métricas, import, tests | Sí (con cuidado) |
| `scripts/` | Install y backup multi-OS | Sí |
| `imports/` | Instantáneas locales para revisión | Generado; gitignored |

## `manifest.json`

Fuente de verdad del inventario:

```json
{
  "skills": [ "architecture", "code-quality", "..." ],
  "agents": [ "architecture", "code-quality", "..." ],
  "platforms": [ "copilot", "opencode", "kiro" ]
}
```

El render itera estas listas. Si falta un agent adapter en una plataforma
declarada, la validación o el render fallarán según el caso.

## Adaptadores

### `platform.json`

Define sustituciones de texto aplicadas a skills (y al combinar con el adapter
del agente). Ejemplos de tokens:

| Token | Uso típico |
|-------|------------|
| `{{platform_name}}` | Nombre legible de la herramienta |
| `{{sdd_agent}}` | Cómo referenciar al agente SDD (`@sdd`, `sdd`, …) |
| `{{sdd_start_instruction}}` | Texto de “cómo arrancar SDD” en esa UI |
| `{{gate_instruction}}` | Cómo se explica un gate de aprobación |
| `{{steering_paths}}` | Rutas de steering / AGENTS.md |

Cualquier `{{token}}` sin resolver aborta el render.

### Adapter de agente (`agents/<id>.json`)

Campos habituales:

- `filename` — nombre del archivo en `generated/<platform>/agents/`
- `frontmatter` — YAML que entiende la herramienta (name, description, tools,
  permissions, mode, temperature, argument-hint, …)
- `substitutions` — opcionales, se fusionan sobre las globales

Diferencias notables entre plataformas:

| Aspecto | Copilot | OpenCode | Kiro |
|---------|---------|----------|------|
| Extensión agente | `.agent.md` | `.md` | `.md` |
| Nombre del agente | campo `name` en frontmatter | vía archivo / config | nombre de archivo (sin `name`) |
| Permisos | lista `tools` | `permission` (edit, bash, …) | `tools` + `permissions.rules` |
| Default shell sensible | según tool | confirmación (`ask`) | `ask` por defecto; `deny` en destructivos |

### Adapter de skill

Opcional. Si no existe `adapters/<platform>/skills/<id>.json`, la skill se copia
desde canonical aplicando solo las sustituciones de `platform.json`.

## Pipeline de render (`tools/render.py`)

Para cada plataforma del manifest:

1. Borra `generated/<platform>/` si existe.
2. Por cada skill: copia el árbol de la skill y reescribe `SKILL.md` con
   sustituciones.
3. Por cada agente: lee el markdown canónico, aplica sustituciones, antepone el
   frontmatter del adapter y escribe `filename`.

Salida **determinista**: mismo canonical + adapters ⇒ mismo generated.

## Validación (`tools/validate.py`)

Comprueba, entre otras cosas:

- Coherencia del manifest con archivos presentes.
- Adapters requeridos.
- Que un re-render reproduce `generated/` (reproducibilidad).
- Paridad esperada entre plataformas donde aplica.

Ejecutar siempre antes de instalar o de commitear cambios de prompts.

## Otras herramientas

| Script | Función |
|--------|---------|
| `tools/measure_context.py` | Palabras en agentes, skills y references (coste de contexto) |
| `tools/import_installed.py` | Apoyo a importar lo instalado hacia `imports/` |
| `tools/test_integrity.py` | Tests de integridad del repo/pipeline |

## Scripts de instalación y backup

```text
scripts/
  install/   copilot|opencode|kiro  .sh / .ps1
  backup/    copilot|opencode|kiro  .sh / .ps1
```

- **install:** `generated/<p>/` → rutas globales de la tool; backup timestamped
  salvo `--force`.
- **backup:** instalación local → `imports/<p>/<fecha>/` solo ids del manifest;
  no escribe en canonical.

Detalle de uso: [instalacion.md](instalacion.md).

## Permisos y seguridad en runtime

El kit declara límites en dos niveles:

1. **Prompt** — alcance inviolable, confirmaciones, no exponer secretos.
2. **Frontmatter de plataforma** — tools permitidos y reglas shell
   (deny/ask en comandos irreversibles de git y `rm`).

OpenCode tiende a pedir confirmación en shell por defecto. Kiro usa `ask` como
efecto por defecto y niega patrones destructivos explícitos. Copilot expone el
conjunto de tools declarado en el adapter.

Ninguna de estas capas sustituye el criterio humano en máquinas compartidas o
CI.

## Extensibilidad

Añadir skill, agente o plataforma: pasos en [desarrollo.md](desarrollo.md).

Principio de diseño: **ampliar adapters y, solo si hace falta, el renderer**;
no ramificar copias del texto canónico por herramienta.

## Relación con el “Project Navigator”

[PROJECT-NAVIGATOR-FRAMEWORK.md](../PROJECT-NAVIGATOR-FRAMEWORK.md) propone un
sistema futuro de capas de contexto (`.navigator/`) para navegar cualquier repo
con menos tokens. Es independiente del pipeline de render actual y aún no está
implementado como skill/agente del manifest.
