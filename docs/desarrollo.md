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

Tokens de sustitución (`{{platform_name}}`, `{{sdd_agent}}`, etc.) se resuelven
en el render. Si queda un `{{...}}` sin definir, `render.py` falla.

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
3. Crea un adapter JSON por cada agente del manifest.
4. Amplía `tools/render.py` **solo** si la estructura de salida es distinta.
5. Añade `scripts/install/<plataforma>.sh` y `.ps1` (y backup si aplica).
6. Renderiza, valida e instala en dry-run.

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
python3 tools/test_sdd_contract.py
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
