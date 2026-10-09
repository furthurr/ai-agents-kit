# Desarrollo y contribución

Cómo modificar el kit de forma segura. Modelo mental y pipeline:
[arquitectura-del-kit.md](arquitectura-del-kit.md).

## Regla de oro

| Editas | No editas |
|--------|-----------|
| `canonical/` — lógica y contenido común | `generated/` — se regenera entero |
| `adapters/` — solo diferencias de plataforma | Instalaciones en `~/` salvo para probar |
| `tools/`, `scripts/` — tooling | Secretos en cualquier archivo |
| `docs/`, `README.md` — documentación | |

Las carpetas `copilot/` y `opencode/` en la raíz del repo, si existen, son
**legado / snapshots** y no forman parte del flujo canónico de render. El
camino oficial es `canonical` → `adapters` → `generated` → `scripts/install`.

## Flujo de trabajo habitual

```bash
# 1. Cambia canonical/ y/o adapters/
# 2. Regenera y valida
python3 tools/render.py
python3 tools/validate.py
python3 tools/measure_context.py   # opcional: coste de contexto
python3 tools/check_links.py       # enlaces Markdown internos

# 3. Revisa el diff en generated/
git diff generated/

# 4. Prueba instalación sin escribir (recomendado)
./scripts/install/opencode.sh --dry-run

# 5. Instala en tu máquina de desarrollo y reinicia la herramienta
./scripts/install/opencode.sh
```

## Dónde va cada cambio

### Contenido común (todas las plataformas)

- Prompt de skill: `canonical/skills/<id>/SKILL.md`
- Referencias: `canonical/skills/<id>/references/`
- Prompt de agente (sin frontmatter de plataforma): `canonical/agents/<id>.md`
- Inventario: `canonical/manifest.json`

### Solo una plataforma

- Sustituciones globales: `adapters/<plataforma>/platform.json`
- Frontmatter / nombre de archivo del agente: `adapters/<plataforma>/agents/<id>.json`
- Overrides de skill (si existen): `adapters/<plataforma>/skills/<id>.json`

Tokens de sustitución (`{{sdd_agent}}`, `{{gate_instruction}}`,
`{{steering_paths}}`) se resuelven en el render. Si queda un `{{...}}` sin
definir, `render.py` falla.

## Añadir una skill

1. Crea `canonical/skills/<id>/SKILL.md` con frontmatter `name` + `description`.
2. Añade `references/` si el procedimiento es largo (plantillas bajo demanda).
3. Declara el id en `canonical/manifest.json` → `skills`.
4. Si hace falta, crea adapter por plataforma en `adapters/*/skills/<id>.json`.
5. Si un agente nuevo la usa, crea o actualiza el agente (siguiente sección).
6. `render` + `validate` + instalar y probar.

## Añadir un agente

1. Crea `canonical/agents/<id>.md` (cuerpo del prompt, sin frontmatter YAML de
   plataforma).
2. Añade el id en `canonical/manifest.json` → `agents`.
3. Por cada plataforma en el manifest, crea
   `adapters/<plataforma>/agents/<id>.json` con al menos:
   - `filename` — nombre del archivo de salida
   - `frontmatter` — campos que exige esa herramienta (name, tools, permissions…)
4. `render` + `validate` + instalar y probar el selector de agentes.

## Añadir una plataforma

1. Añade el identificador en `canonical/manifest.json` → `platforms`.
2. Crea `adapters/<plataforma>/platform.json` (sustituciones mínimas).
3. Crea un adapter JSON por cada agente del manifest. Opcionalmente incluye
   `body_suffix` para añadir texto tras el cuerpo canónico (Pi lo usa para
   `$ARGUMENTS`).
4. Amplía `tools/render.py` **solo** si la estructura de salida es distinta.
5. Añade `scripts/install/<plataforma>.sh` y `.ps1` (y backup si aplica).
6. Renderiza, valida e instala en dry-run.

### Antigravity: contrato y evidencia

El catálogo incluye seis plataformas, seis agentes y diez skills. Antigravity
apunta inicialmente a **2.0**: cambios del host van en
`adapters/antigravity/`, contenido compartido en `canonical/` y salida en
`generated/antigravity/` mediante el renderer existente, nunca edición manual.

Los agentes usan `<id>.md`, `name`, `description`, `model: inherit`,
`mainAgent: true`, `subagent: true` y `tools` por rol. La descripción SDD conserva
`direct`, `lite`, `standard` y `Quick Plan`. `{{sdd_agent}}` produce `sdd`
nominal, no una invocación nativa `@sdd`. No añadas un campo `skills` explícito
con paths ambiguos: verifica descubrimiento global y carga de recursos.

La referencia de [Hooks](https://antigravity.google/docs/hooks/#supported-tools)
respalda nombres de herramientas; no demuestra su disponibilidad en cada build.
El [smoke](antigravity-smoke.md) registra selección real, herramientas individuales,
descubrimiento 6/10, recursos y un hijo solicitado explícitamente a un padre del
host con `invoke_subagent`. El kit no añade hooks ni delegación automática, y
las listas de tools no son aislamiento técnico por rol.

Prueba instaladores y exportación con HOME/USERPROFILE **temporales**, fuera del
perfil real. El contrato incluye preflight antes/después, flags Bash
`--dry-run`/`--force` y PowerShell `-DryRun`/`-Force`, copia por fusión sin borrar
extras, respaldo previo y fallos con código no cero. Preflight comprueba archivos
principales; validación y pruebas de copia completa cubren YAML y recursos.
Restaurar manualmente no es rollback transaccional. Exportar puede ser parcial
con avisos y no modifica fuentes ni adapters.

Para retirados aplica el contrato de [migración segura](migracion-agentes.md):
opt-in, aprobación exacta de personalizados/inciertos mediante pares repetibles
`--approve-retired-file PATH --approve-retired-sha256 SHA` (listas paralelas en
PowerShell), destinos locales explícitos con `--additional-agents-dest`, hashes históricos
verificables y respaldo obligatorio fuera de árboles escaneados incluso con
`--force`. Prueba dry-run, fallos y recuperación sin overwrite solo con fixtures.
La evidencia CI anterior no acredita este nuevo flujo.

La suite Python `tools/test_retired_agents.py` verifica bytes históricos de
artefactos y adaptadores contra el commit fijado en `tools/retired_agents.json`
(actualmente `d206ae811b14c44699c7040bdb59742eac1f122d`). El checkout de CI que
ejecute esa suite debe disponer de ese historial: usar `fetch-depth: 0` o traer
explícitamente el commit requerido. Esto es un requisito de la suite, no una
afirmación de que el workflow actual ya lo configure. Si falta la evidencia
histórica, fallar; no omitir los checks ni sustituirla por bytes generados actuales.
La migración/recuperación nativa en Windows queda **PENDIENTE**; revisar wrappers
PowerShell o verificar fixtures POSIX no equivale a esa ejecución ni acredita
atomicidad portable de la retirada.

La ejecución automatizada de scripts con fixtures está acreditada por el
[run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502),
SHA `57aaf7dd2190f6fe44c697179e93b8609a502433`, con **Python 3.10**: Ubuntu
(`validate`, incluidas 22/22 pruebas nativas), macOS (22/22 nativas) y Windows
(22/22 nativas, ejecución PowerShell), todos los jobs en verde. El detalle figura
en [evidencia automatizada de CI](antigravity-smoke.md#evidencia-automatizada-de-ci).

El harness prepara el directorio de caché PowerShell del fixture y deshabilita
`gather` en el proceso hijo; los snapshots no ignoran `AppData`. Esto permite
comprobar escrituras de los scripts en el entorno aislado sin modificar la
configuración global del usuario.

**Runtime Antigravity: PENDIENTE** para descubrimiento 6/10, UI, referencias e
`invoke_subagent`. El bridge `GEMINI.md` → `AGENTS.md` no está implementado.
Crear un workflow o pasar pruebas con fixtures no acredita estos comportamientos
de la aplicación. Registra comando, exit code, OS y entorno por ejecución.
La versión de referencia del host se fija con un smoke completo exitoso.
CLI (`~/.gemini/antigravity-cli/skills/`) e IDE standalone no se certifican por
haber copiado archivos en las rutas 2.0 (`~/.gemini/config/{skills,agents}`).

## Checklist antes de merge / release del kit

- [ ] Cambios solo donde corresponde (`canonical` / `adapters` / tools / docs)
- [ ] `python3 tools/render.py` sin errores
- [ ] `python3 tools/validate.py` OK (paridad y reproducibilidad)
- [ ] `python3 tools/measure_context.py` revisado si creció mucho el prompt
- [ ] Diff de `generated/` coherente con el cambio
- [ ] Sin secretos, tokens ni rutas personales sensibles
- [ ] Docs actualizadas si cambió el catálogo, destinos o flujo
- [ ] Prueba manual en al menos una plataforma

## Tests

```bash
python3 tools/test_integrity.py
python3 tools/test_links.py
python3 tools/test_model_recommendations.py
python3 tools/test_sdd_contract.py
python3 tools/test_handoff_contract.py
python3 tools/test_documentation_core.py
python3 tools/test_mas_identity.py
python3 tools/test_retired_agents.py
python3 tools/test_code_review_contract.py
python3 tools/test_validate.py
python3 tools/test_install.py
python3 tools/test_antigravity_install.py
python3 tools/test_antigravity_contract.py
```

Cubre integridad del pipeline y convenciones del repo. Ejecútalo junto a
`validate.py` y `check_links.py` cuando toques tools o la forma de los adapters.

## Importar mejoras hechas “en caliente”

Si ajustaste un agente ya instalado en tu home y quieres traer el diff al repo:

```bash
./scripts/backup/opencode.sh
# Revisa imports/opencode/<fecha>/
# Copia a mano lo bueno → canonical/ o adapters/
python3 tools/render.py && python3 tools/validate.py
```

Nunca copies a ciegas desde `imports/` a `generated/`.

## Convenciones de contenido

- **Idioma:** español por defecto en prompts y docs del kit.
- **Alcance:** cada skill/agente declara qué puede y qué tiene prohibido.
- **Confirmaciones:** git, release y destructivos siempre con OK explícito del usuario.
- **Secretos:** placeholders; nunca valores reales.
- **Contexto:** lo pesado en `references/`, no en el cuerpo inicial del skill.
- **Precedencia:** skill > agente si divergen.

## Documentación

Al cambiar comportamiento visible para usuarios o contribuidores, actualiza:

- [catalogo.md](catalogo.md) — skills/agentes nuevos o renombrados
- [uso.md](uso.md) / [instalacion.md](instalacion.md) — si cambia la UX o rutas
- [vision.md](vision.md) / [arquitectura-del-kit.md](arquitectura-del-kit.md) — si cambia el modelo
- [README.md](../README.md) — solo el resumen de aterrizaje

Para cambios SDD, contrasta también [agentes/sdd.md](agentes/sdd.md),
[sdd-effort-examples.md](sdd-effort-examples.md) y [sdd-smoke.md](sdd-smoke.md)
con las referencias canónicas de alcance, continuidad y testing. El contrato
automatizado comprueba instrucciones y paridad; los escenarios conversacionales
requieren evidencia runtime independiente.
