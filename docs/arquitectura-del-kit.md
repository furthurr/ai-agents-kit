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
del agente). Tokens declarados hoy:

| Token | Uso típico |
|-------|------------|
| `{{sdd_agent}}` | Cómo referenciar al agente SDD (`@sdd`, `sdd`, …) |
| `{{gate_instruction}}` | Matiz de plataforma sobre el gate; vacío si no hace falta |
| `{{steering_paths}}` | Rutas de steering / AGENTS.md |

Reglas:

- Cualquier `{{token}}` sin resolver aborta el render.
- Un token usado en canonical debe estar declarado en **todas** las plataformas
  del manifest, aunque el valor sea la cadena vacía.
- Una sustitución declarada y **no** usada en canonical también falla la
  validación: la config muerta se desincroniza de los prompts que dice adaptar.
- `render.py` solo sustituye en `SKILL.md`. Un token dentro de `references/`
  llegaría literal al modelo, así que la validación lo rechaza.

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

- Coherencia del manifest con archivos presentes (tipos, campos, IDs únicos).
- Adapters requeridos, `filename` seguro y `frontmatter` válido.
- Que un re-render en un directorio temporal reproduce `generated/` sin
  modificarlo (validación **no destructiva**): una interrupción no altera
  `generated/`.
- Ausencia de duplicados, colisiones de salida y artefactos huérfanos.

`tools/render.py` acepta `--output <dir>` para renderizar fuera de `generated/`.

Ejecutar siempre antes de instalar o de commitear cambios de prompts.

## Otras herramientas

| Script | Función |
|--------|---------|
| `tools/measure_context.py` | Palabras en agentes, skills y references (coste de contexto) |
| `tools/import_installed.py` | Apoyo a importar lo instalado hacia `imports/` |
| `tools/check_links.py` | Enlaces Markdown internos de docs y fuentes canónicas |
| `tools/test_integrity.py` | Tests de integridad del repo/pipeline |
| `tools/test_validate.py` | Pruebas negativas de `validate.py` y `render.py` |

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

## Project Navigator en el kit

Project Navigator está implementado como skill y agente del manifest. Usa capas
de contexto en `.navigator/` para responder con la fuente más barata suficiente:
contexto raíz, mapa de módulos, símbolos opt-in, grafo opt-in y código puntual.

### Autoridad documental

La única autoridad de comportamiento runtime es
[`canonical/skills/project-navigator/SKILL.md`](../canonical/skills/project-navigator/SKILL.md).
Sus contratos y procedimientos bajo `references/` se copian a las tres
plataformas mediante el pipeline normal. Las plantillas son ejemplos; los
contratos normativos de índices viven en `references/schemas.md`.

### Decisiones de diseño

- Navigator no sustituye a Architecture: localiza y resume; Architecture
  documenta decisiones, límites y deuda estructural.
- El comportamiento es agnóstico al proveedor y al modelo. El agente puede
  recomendar un cambio manual para procesos pesados, pero nunca seleccionarlo.
- Capas 0–1 forman el MVP; símbolos y grafo son opt-in y no bloquean bootstrap.
- Los límites declarados por prompts no equivalen a un sandbox. Los adapters
  reducen o solicitan permisos según las capacidades reales de cada host.
- Métricas de ahorro son hipótesis hasta disponer de la evidencia definida en
  [mejoras.md](mejoras.md) y [navigator-smoke.md](navigator-smoke.md).

## Documentation Orchestrator en el kit

Documentation Orchestrator sigue el mismo patrón canónico de skill + agente, pero
coordina procedimientos de varios dominios. No depende de APIs de subagentes de
una plataforma: carga secuencialmente las skills aplicables, lo que conserva la
misma semántica en Copilot, OpenCode y Kiro.

### Límites y autoridad

- `documentation-orchestrator` gobierna clasificación, orden, Gate 0 de modelo y
  cierre global.
- Cada skill especialista sigue siendo autoridad dentro de su propia carpeta y
  conserva sus gates.
- El agente no crea `.documentation/`; el estado permanece en los READMEs y
  artefactos ya definidos por cada especialista.
- SDD, Release Management y Graphify son workflows externos de solo lectura para
  este agente.
- La recomendación de modelo es genérica (`bajo`/`medio`/`alto`) y manual; ningún
  adapter permite que el agente seleccione el modelo del host.

Smoke test: [documentation-orchestrator-smoke.md](documentation-orchestrator-smoke.md).
