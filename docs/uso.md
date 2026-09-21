# Uso diario

Tras [instalar](instalacion.md), eliges el **agente** (o dejas que la herramienta
active la **skill** por relevancia) y describes la tarea en lenguaje natural.

Consulta la [guía interna de agentes y skills](agentes/README.md) para conocer el
alcance, el flujo, los artefactos y ejemplos de cada agente.

El sistema se denomina **MAS** (*Multi-Agent System*). Usa `MAS:` para una
instrucción dirigida al sistema completo y `@<agente>` para un especialista.
Consulta la [guía de MAS](mas.md) para la terminología completa.

## Skill vs agente (en la práctica)

| | Skill | Agente |
|---|--------|--------|
| Qué es | Procedimiento y estándares | Rol + límites + permisos de la plataforma |
| Cuándo se nota | Pasos, plantillas, gates | Selector de agente / mención `@…` |
| Precedencia | Si hay conflicto, manda la skill | Debe cargar y seguir su skill |

Para el día a día: **elige el especialista del dominio** y pide la tarea. El
agente cargará la skill correspondiente.

## Cómo invocar por plataforma

Los nombres exactos del selector pueden variar según versión de la herramienta.
IDs estables del kit:

| ID | Nombre visible típico |
|----|------------------------|
| `project-navigator` | Project Navigator |
| `architecture` | Architecture Agent |
| `code-quality` | Code Quality Agent |
| `data-api` | Data & API Agent |
| `documentation-orchestrator` | Documentation Orchestrator |
| `security` | Security Agent |
| `ui-design` | UI Design Agent |
| `sdd` | Agente SDD / SDD |
| `git-release-manager` | Git & Release Manager |

### OpenCode

- Selecciona el agente (p. ej. `@architecture`, `@sdd`, `@security`).
- Las skills viven en `~/.config/opencode/skills/` y pueden cargarse por
  relevancia del prompt.
- Ejemplo: con `@sdd` — *“Planifica el login biométrico en modo standard”*.

### GitHub Copilot

- Agentes instalados como `*.agent.md` en `~/.copilot/agents/`.
- Usa el selector de agentes personalizados del IDE/CLI y elige el del kit.
- Las skills van a `~/.copilot/skills/`.

### Kiro

- Agentes en `~/.kiro/agents/` (el nombre sale del archivo, p. ej. `sdd.md`).
- Skills en `~/.kiro/skills/`; también puedes invocar por comando de skill
  (p. ej. `/sdd-spec` según la UI de Kiro).
- Steering del proyecto: `.kiro/steering/*.md` y/o `AGENTS.md` si existen.

### Claude Code

- Agentes en `~/.claude/agents/` o `$CLAUDE_CONFIG_DIR/agents/`; se invocan con
  una petición de delegación o mención `@architecture`, `@sdd`, etc.
- Skills en `~/.claude/skills/` o `$CLAUDE_CONFIG_DIR/skills/`; también puedes
  invocarlas con `/sdd-spec`, `/security`, etc.
- Steering del proyecto: `CLAUDE.md`, `.claude/CLAUDE.md` y `.claude/rules/*.md`.
- El instalador no crea ni modifica `CLAUDE.md` ni `.claude/settings.json`.

Si no ves un agente tras instalar, **reinicia** la herramienta y verifica la
ruta de destino en [instalacion.md](instalacion.md).

## Guía rápida por intención

| Dices algo como… | Agente |
|------------------|--------|
| “¿Qué es este repo?”, “¿dónde está X?”, “bootstrap del navigator” | Project Navigator |
| “¿Está actualizada la documentación?”, “actualiza lo que tenemos”, “release-check” | Documentation Orchestrator |
| “Documenta la arquitectura”, “añade un ADR”, “¿qué módulos hay?” | Architecture |
| “Revisa code smells”, “baja complejidad”, “mejora este archivo” | Code Quality |
| “Catálogo de endpoints”, “DTO de login”, “diagrama ER” | Data & API |
| “Auditoría de seguridad”, “¿hay secretos en claro?”, “hardening TLS” | Security |
| “Extrae el design system”, “unifica colores”, “deuda de UI” | UI Design |
| “Especifica esta feature”, “bugfix estructurado”, “tasks de la spec” | SDD |
| “Haz commit”, “pushea”, “prepara la release 1.4.0” | Git & Release Manager |

Catálogo completo: [catalogo.md](catalogo.md).

## Buenas prácticas

1. **Un dominio por sesión de agente** — no pidas al de UI que arregle la API.
2. **Primera vez en un repo** — usa Project Navigator para bootstrap de
   `.navigator/` (mapa barato); luego deja que cada especialista inicialice su
   carpeta (`.architecture/`, `.design/`, etc.).
   Architecture, Data & API, UI Design, Quality y Security recomiendan nivel antes
   de operar: el aviso puntual no bloquea y las operaciones pesadas esperan
   confirmación. Si el Orchestrator ya mostró y confirmó ese nivel para el mismo
   alcance, el especialista no lo repite.
3. **SDD antes de features grandes** — elige entre exactamente cuatro profundidades:
   `direct`, sin spec; `lite`, automático para trabajo acotado, claro y de bajo
   riesgo; `standard`, fallback seguro; y `deep`, solo por petición explícita.
   Quick Plan es obligatorio y exclusivo de `lite`: requiere Gate 0 bloqueante,
   pero no Gates 1-3 ni Gate 4. Combinar Quick Plan con otro modo es inválido.
   `standard` y `deep` conservan los Gates 1-4; los bugfixes no triviales usan
   `standard`.
    Antes de cada proceso no trivial recomienda únicamente el nivel `BAJO`, `MEDIO`
    o `ALTO` de la próxima fase; el usuario puede cambiarlo manualmente o continuar
    con el actual. En las transiciones combina resumen, aprobación de la fase actual
    y recomendación de la siguiente, sin crear gates adicionales.
   Si hay `.navigator/`, SDD comprueba primero su disponibilidad y frescura para
   orientar la exploración. Un índice desfasado solo aporta rutas candidatas: la
   documentación aplicable y el código real confirman las decisiones. Su ausencia
   no bloquea el flujo ni provoca bootstrap/update automático.
4. **Escalado recomendado, no automático** — Architecture, Code Quality, Data & API,
   Security y UI Design evalúan si una mejora necesita más requisitos o diseño. Si
   recomiendan SDD, explican el motivo, citan el hallazgo y se detienen antes del
   código; tú decides si cambias de agente. SDD no amplía el alcance del especialista.
5. **Git y releases** — el agente propondrá el plan; **tú confirmas** commit, push,
   tag o changelog aplicado.
6. **Seguridad y calidad** — la remediación va en micro-pasos con confirmación;
   no esperes un “arregla todo el repo” de un golpe.
7. **Contexto del proyecto** — si existe `CLAUDE.md`, `AGENTS.md` o steering de
   Kiro, los agentes de SDD lo leen de forma selectiva según la plataforma.
8. **Testing adaptativo en SDD** — una feature normal usa TDD focalizado; TDD
   estricto solo se activa si lo pides. Es independiente de la profundidad:
   `direct` puede incluir un microciclo TDD y `deep` no implica TDD estricto.

## Orquestación documental

Elige `documentation-orchestrator` cuando la petición cruza varias carpetas. No
crea `.documentation/`: por cada acción carga la skill especialista o emite un
handoff portable para continuar con el agente real; nunca hace ambas cosas. Cada
especialista conserva la autoridad sobre su dominio.

| Intención | Modo detectado |
|-----------|----------------|
| “Estado de la documentación” / `sync-check` | `status` |
| “Inicializa el core” | `bootstrap-core` (`.navigator/` + `.architecture/`) |
| “Actualiza el core existente” | `sync-core` |
| “Actualiza las carpetas que ya tenemos” | `sync-existing` |
| “Actualiza solo datos y seguridad” | `sync-domain` |
| “¿Está listo para release?” | `release-check` |

Antes de cualquier modo, el agente hace un preflight mínimo, recomienda un nivel
de modelo (`bajo`, `medio` o `alto`) y espera respuesta. El usuario cambia el
modelo manualmente o responde “continúa con el actual”; el agente nunca lo cambia.

Si necesitas continuar con el agente especialista real, pídelo explícitamente.
El orquestador entrega un bloque `## Handoff`; cópialo al agente indicado y
devuelve después su bloque `## Handoff Result` al orquestador. Para una misma
acción se usa la skill local o el handoff, nunca ambos. `write_scope` es una
restricción lógica: no sustituye los permisos efectivos de la plataforma.

## Qué deja cada especialista en tu repo

| Agente | Artefactos típicos |
|--------|-------------------|
| Project Navigator | `.navigator/` (ai-context, module-map, config; symbols/graph opt-in) |
| Architecture | `.architecture/` (contexto, diagramas, ADRs, deuda) |
| Code Quality | `.quality/` (hallazgos, estándares cacheados) |
| Data & API | `.data/` (catálogo, modelos, contratos, ER) + lanzador Scalar para REST, bloqueado hasta disponer de OpenAPI válido |
| Documentation Orchestrator | No deja carpeta propia; coordina las anteriores |
| Security | `.security/` (hallazgos, checklist, evidencia) |
| UI Design | `.design/` (tokens, componentes, deuda visual) |
| SDD | `.sdd/specs/<ruta-spec>/` plana o agrupada por módulo (requirements, design, tasks, verification) |
| Git & Release | Commits/tags/CHANGELOG; perfil en `.release/` si aplica |

Estas carpetas son **del proyecto en el que trabajas**, no del repo del kit.
Conviene versionarlas con el código para que el equipo y la IA compartan el
mismo contexto.

En SDD, `lite` solo de planificación crea `requirements.md`, `design.md` y
`tasks.md`; si también implementa, añade un `verification.md` compacto. `direct`
no crea spec.

Project Navigator no versiona su caché local. Añade este bloque al `.gitignore`
del proyecto que indexas:

```gitignore
# project-navigator
.navigator/cache/
```

Si el grafo es grande o solo local, también puedes ignorar `.navigator/graph/`.

## Límites que debes esperar

- Project Navigator **no** implementa features ni escribe fuera de `.navigator/`
  (salvo export opt-in a `AGENTS.md` con confirmación); no selecciona el modelo.
- Documentation Orchestrator no modifica producto, no selecciona el modelo y no
  administra `.sdd/`, `.release/` ni `graphify-out/`.
- Architecture **no** refactoriza código de negocio.
- Code Quality **deriva** vulnerabilidades al Security Agent.
- Data & API **no** implementa pantallas.
- Security / Quality **no** exponen secretos reales en la documentación.
- Git & Release **no** hace commit/push/tag sin confirmación explícita;
  acciones destructivas piden doble confirmación.
- SDD **no** cambia el modelo del host ni marca tareas hechas sin evidencia
  (integrity gate).

## Ejemplo de flujo completo

```text
0. @documentation-orchestrator → “Inicializa la documentación core”
1. @data-api      → “Documenta los endpoints de autenticación”
2. @sdd           → “Spec standard para refresh token offline”
3. (implementación con el agente/skill que corresponda a las tasks)
4. @git-release-manager → “Prepara el commit del producto”
5. @documentation-orchestrator → “Actualiza la documentación existente”
6. @git-release-manager → “Prepara el commit documental”
7. @documentation-orchestrator → “Ejecuta release-check”
8. @git-release-manager → “Prepara la release patch”
```

No es obligatorio seguir este orden en cada cambio; sirve como mapa cuando el
trabajo cruza varios dominios.
