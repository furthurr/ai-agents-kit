# Uso diario

Tras [instalar](instalacion.md), eliges el **agente** (o dejas que la herramienta
active la **skill** por relevancia) y describes la tarea en lenguaje natural.

Consulta la [guía interna de agentes y skills](agentes/README.md) para conocer el
alcance, el flujo, los artefactos y ejemplos de cada agente.

El sistema se denomina **MAS** (*Multi-Agent System*). Usa `MAS:` para una
instrucción dirigida al sistema completo y `@<agente>` como notación semántica
del kit para un especialista; no garantiza una invocación nativa del host.
Consulta la [guía de MAS](mas.md) para la terminología completa.

## Skill vs agente (en la práctica)

| | Skill | Agente |
|---|--------|--------|
| Qué es | Procedimiento y estándares | Rol + límites + permisos de la plataforma |
| Cuándo se nota | Pasos, plantillas, gates | Selector de agente / mención `@…` |
| Precedencia | Si hay conflicto, manda la skill | Debe cargar y seguir su skill |

Para el día a día: **elige el especialista del dominio** y pide la tarea. El
agente cargará la skill correspondiente.

## Elegir el agente según la tarea

| Quieres… | Empieza con… | Flujo |
|----------|---------------|-------|
| Entender capas o localizar código | `documentation-orchestrator` | `inspect`, consulta de solo lectura |
| Actualizar el contexto ya existente | `documentation-orchestrator` | `sync-existing`, plan documental aprobado |
| Revisar calidad o seguridad | `code-review` | Auditoría del dominio; remediación con aprobación por micro-paso |
| Cambiar solo APIs/datos | `data-api` | Trabajo dentro de la capa de datos y contratos |
| Cambiar solo lo visual | `ui-design` | Trabajo dentro de UI y diseño |
| Planificar o implementar una feature/bugfix | `sdd` | Alcance completo validado y profundidad elegible |
| Publicar cambios o versionar | `git-release-manager` | Commit/push o release con autorización explícita |

Mantener contexto también tiene un coste: las carpetas canónicas deben reflejar
las fuentes actuales. Las consultas verifican frescura y recurren al código si
el contexto está desfasado; actualizar índices o documentación es una operación
solicitada y aprobada, no un efecto automático de consultar.

## Cómo invocar por plataforma

Los nombres exactos del selector pueden variar según versión de la herramienta.
IDs estables del kit:

| ID | Nombre visible típico |
|----|------------------------|
| `code-review` | Code Review Agent |
| `data-api` | Data & API Agent |
| `documentation-orchestrator` | Documentation Orchestrator |
| `ui-design` | UI Design Agent |
| `sdd` | Agente SDD / SDD |
| `git-release-manager` | Git & Release Manager |

### OpenCode

- Selecciona el agente (p. ej. `@documentation-orchestrator`, `@sdd`, `@code-review`).
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
  una petición de delegación o mención `@documentation-orchestrator`, `@sdd`, etc.
- Skills en `~/.claude/skills/` o `$CLAUDE_CONFIG_DIR/skills/`; también puedes
  invocarlas con `/sdd-spec`, `/security`, etc.
- Steering del proyecto: `CLAUDE.md`, `.claude/CLAUDE.md` y `.claude/rules/*.md`.
- El instalador no crea ni modifica `CLAUDE.md` ni `.claude/settings.json`.

### Pi

- Agentes como plantillas de prompt en `~/.pi/agent/prompts/` (o
  `$PI_CODING_AGENT_DIR/prompts/`): `/<id> <tarea>`, por ejemplo `/sdd planifica login`.
- Skills en el directorio `skills/` del mismo perfil: `/skill:<nombre>`.
- Las plantillas usan la sesión activa; no crean subagentes aislados.

### Antigravity 2.0

- Agentes globales en `~/.gemini/config/agents/<id>.md`; selecciona el principal
  mediante el mecanismo de la UI que se observe en tu versión. **La selección
  real está pendiente de smoke**: no se prescribe un nombre de menú no comprobado.
- Skills globales en `~/.gemini/config/skills/<skill-name>/`; el mecanismo
  documentado es `/<skill-name>`, por ejemplo `/sdd-spec`. Comprueba además que el
  agente carga `SKILL.md` y sus referencias, tanto principal como subagente.
- Tras instalar o actualizar, reinicia la superficie objetivo y comprueba otra
  vez el descubrimiento 6/10; registra el mecanismo de recarga realmente observado
  en [antigravity-smoke.md](antigravity-smoke.md).
- `@sdd` y `@<agente>` expresan routing del kit, **no sintaxis nativa confirmada**.
  La sustitución `{{sdd_agent}}` produce el identificador nominal `sdd`, no un
  comando. `/agents` pertenece a la documentación del **CLI**; no se atribuye a
  Antigravity 2.0 sin prueba.
- El CLI documenta otra ruta de skills, `~/.gemini/antigravity-cli/skills/`; el
  instalador 2.0 no la cubre. Agentes personalizados del IDE standalone: no
  verificados. Scripts con fixtures: **22/22 pruebas nativas por OS** en Linux,
  macOS y Windows, Python 3.10, en el
  [run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
  Runtime (descubrimiento 6/10, UI, referencias e `invoke_subagent`): **PENDIENTE**.
- Steering admitido: `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`; el instalador
  no crea ni sobrescribe estas reglas ni settings del usuario.
  El bridge `GEMINI.md` → `AGENTS.md` no está implementado.
- Los seis agentes declaran `model: inherit`, `mainAgent: true`, `subagent: true`
  y herramientas por rol. Esto no cambia automáticamente el modelo ni constituye
  un sandbox por carpeta/comando. Las skills se descubren globalmente: no se
  declara un campo `skills` explícito cuya resolución de rutas es ambigua.

No hay delegación automática. El handoff sigue siendo explícito y portable; una
invocación nativa de prueba requiere un padre del host con `invoke_subagent`, una
petición explícita del usuario y contexto autorizado completo. Los seis roles
del kit no reciben esa herramienta para encadenar delegaciones.

Si no ves un agente tras instalar, **reinicia** la herramienta y verifica la
ruta de destino en [instalacion.md](instalacion.md).

## Guía rápida por intención

| Dices algo como… | Agente |
|------------------|--------|
| “¿Qué es este repo?”, “¿dónde está X?” | Documentation Orchestrator → `inspect` |
| “¿Está actualizada la documentación?”, “actualiza lo que tenemos”, “release-check” | Documentation Orchestrator |
| “Documenta la arquitectura”, “añade un ADR”, “bootstrap del core” | Documentation Orchestrator → mantenimiento core autorizado |
| “Solo calidad: revisa code smells”, “baja complejidad” | Code Review — `code-quality` |
| “Catálogo de endpoints”, “DTO de login”, “diagrama ER” | Data & API |
| “Solo seguridad”, “¿hay secretos en claro?”, “hardening TLS” | Code Review — `security` |
| “Revisión completa de calidad y seguridad del módulo” | Code Review — ambas skills |
| “Extrae el design system”, “unifica colores”, “deuda de UI” | UI Design |
| “Especifica esta feature”, “bugfix estructurado”, “tasks de la spec” | SDD |
| “Haz commit”, “pushea”, “prepara la release 1.4.0” | Git & Release Manager |

Catálogo completo: [catalogo.md](catalogo.md).

## Buenas prácticas

1. **Respeta el alcance del agente** — no pidas al de UI que arregle la API.
   Code Review puede revisar calidad y seguridad en la misma sesión, o solo uno.
2. **Primera vez en un repo** — usa Documentation Orchestrator con `inspect` para
   investigar sin persistencia, o solicita `bootstrap-core` para proponer
   `.navigator/` y `.architecture/`; cada skill conserva sus gates y su carpeta.
   Ningún agente recomienda niveles o selección de modelos LLM. Las escrituras
   conservan los gates efectivos de estudio, propuesta y autorización; el Orchestrator
   no añade una pausa por modelo.
3. **SDD antes de features grandes** — elige entre exactamente tres profundidades:
   `direct`, sin spec; `lite`, para trabajo acotado con garantías verificables;
   y `standard`, fallback seguro. Primero define alcance y criterios; después
   califica y recomienda: 1–3 direct si trivial, 4–9 lite si elegible, 10/10+
   standard para el conjunto y opción de dividir. El usuario elige; una elección
   explícita compatible previa no se vuelve a preguntar.
   Presenta alcance funcional completo (comportamientos, reglas, criterios, errores,
   exclusiones y supuestos) y espera validación explícita antes de artefactos/código.
   Elegir solo modo no lo valida; ajustes requieren presentar el conjunto actualizado.
   Validación y elección pueden resolverse juntas; no sustituyen Gate 1 de standard.
   Quick Plan es obligatorio y exclusivo de `lite`; no tiene Gates 1-3 ni Gate 4.
   Combinar Quick Plan con otro modo es inválido.
   `standard` conserva los Gates 1-4; los bugfixes no triviales usan `standard`.
   Tras definir el alcance, SDD emite una sola vez su nota de esfuerzo prevista,
   registrando referente, justificación y supuestos en la spec según la
   [rúbrica ReserveLab](../canonical/skills/sdd-spec/references/feature-level.md).
   Evalúa implementar y verificar, no predice recursos; orienta la recomendación
   pero no demuestra elegibilidad. Puede mostrar naranja bajo 8 con complicaciones
   concretas controlables. Entregas se evalúan individualmente, aunque sigan 10/10+.
   No la muestra antes
   de definir alcance ni la repite por fase; no recomienda ni selecciona LLM y no
   pausa el flujo por modelo. Se espera solo por gates reales o decisiones pendientes,
   y planificar no autoriza implementar.
   Una modificación comprueba specs relacionadas localmente. Si cambia un requisito,
   se trata como enmienda conservando modo/gates y revalidando evidencia afectada;
   nota baja no habilita direct para evitarlos. La política de continuidad se carga
   bajo demanda, sin auditoría completa rutinaria de `.sdd`.
   Si hay `.navigator/`, SDD comprueba primero su disponibilidad y frescura para
   orientar la exploración. Un índice desfasado solo aporta rutas candidatas: la
   documentación aplicable y el código real confirman las decisiones. Su ausencia
   no bloquea el flujo ni provoca bootstrap/update automático.
4. **Escalado recomendado, no automático** — Documentation Orchestrator, Code Review, Data & API
   y UI Design evalúan si una mejora necesita más requisitos o diseño. Si
   recomiendan SDD, explican el motivo, citan el hallazgo y se detienen antes del
   código; tú decides si cambias de agente. SDD no amplía el alcance del especialista.
5. **Git y releases** — el agente propondrá el plan; **tú confirmas** commit, push,
   tag o changelog aplicado.
6. **Seguridad y calidad** — la remediación va en micro-pasos con confirmación;
   no esperes un “arregla todo el repo” de un golpe.
   Una auditoría documental autorizada registra todos los hallazgos verificados
   sin volver a elegir severidades. Las consultas son sin escrituras y no autorizan
   remediación. `.quality/` y `.security/` conservan sus IDs y estándares.
7. **Contexto del proyecto** — si existe `CLAUDE.md`, `AGENTS.md` o steering de
   Kiro, los agentes de SDD lo leen de forma selectiva según la plataforma.
8. **Testing adaptativo en SDD** — una feature normal usa TDD focalizado; TDD
   estricto está retirado. Es independiente de la profundidad: `direct` puede
   incluir un microciclo TDD y elegir `standard` no obliga a un ciclo más fuerte.
   Si solicitas TDD estricto, SDD propone TDD focalizado y espera aceptación.

## Orquestación documental

Elige `documentation-orchestrator` cuando la petición cruza varias carpetas. No
crea `.documentation/`. También es la entrada para consultas y mantenimiento core:
ejecuta localmente `architecture` y `project-navigator`, que siguen siendo skills
separadas. Para datos, UI y calidad/seguridad carga la skill o emite un handoff al
agente vigente; nunca ambas vías para la misma acción.

| Intención | Modo detectado |
|-----------|----------------|
| “Estado de la documentación” / `sync-check` | `status` |
| “Explica las capas” / “Localiza autenticación” | `inspect` (solo lectura core) |
| “Inicializa el core” | `bootstrap-core` (`.navigator/` + `.architecture/`) |
| “Actualiza el core existente” | `sync-core` |
| “Actualiza las carpetas que ya tenemos” | `sync-existing` |
| “Actualiza solo datos y seguridad” | `sync-domain` |
| “¿Está listo para release?” | `release-check` |

Antes de cualquier modo, el agente hace un preflight mínimo sin recomendar niveles,
modelos ni proveedores LLM. `status` y `release-check` inspeccionan e informan;
las escrituras conservan la aprobación del plan global y los gates reales.

Si necesitas continuar con el agente especialista real, pídelo explícitamente.
Los receptores documentales son `data-api`, `ui-design` y `code-review`; el core
se ejecuta localmente sin handoff ni alias a agentes retirados.
El orquestador entrega un bloque `## Handoff`; cópialo al agente indicado y
devuelve después su bloque `## Handoff Result` al orquestador. Para una misma
acción se usa la skill local o el handoff, nunca ambos. `write_scope` es una
restricción lógica: no sustituye los permisos efectivos de la plataforma.
Calidad y seguridad se derivan a `code-review`; `scope` es una lista con una o
ambas carpetas. Solo se agrupan con la misma acción, proyecto y vía autorizada.

## Qué deja cada especialista en tu repo

| Agente | Artefactos típicos |
|--------|-------------------|
| Code Review | `.quality/` y/o `.security/` (hallazgos, estándares, evidencia por dominio) |
| Data & API | `.data/` (catálogo, modelos, contratos, ER) + lanzador Scalar para REST, bloqueado hasta disponer de OpenAPI válido |
| Documentation Orchestrator | `.navigator/` mediante `project-navigator`; `.architecture/` mediante `architecture`; coordina otros dominios, sin carpeta propia |
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

- La skill Project Navigator **no** implementa features ni escribe fuera de `.navigator/`
  (salvo export opt-in a `AGENTS.md` con confirmación); no recomienda ni selecciona modelos.
- Documentation Orchestrator no modifica producto, no recomienda ni selecciona
  modelos y no administra `.sdd/`, `.release/` ni `graphify-out/`.
- La skill Architecture **no** refactoriza código de negocio.
- Code Review usa `security` para riesgos, no los corrige con criterios de calidad;
  una revisión de solo calidad no autoriza ampliar a seguridad.
- Data & API **no** implementa pantallas.
- Code Review **no** expone secretos reales en la documentación.
- Git & Release **no** hace commit/push/tag sin confirmación explícita;
  acciones destructivas piden doble confirmación.
- SDD **no** recomienda ni selecciona modelos, ni marca tareas hechas sin evidencia
  (integrity gate). Su nivel de feature es una clasificación del alcance, no del LLM.

## Ejemplo de flujo completo

Los agentes pueden consumir contexto core directamente sin handoff: entrar por
`.architecture/README.md` y resolver config/instancia de `.navigator/` para leer
`ai-context.md` o `module-map.json`. Verificar baseline y cambios relevantes;
escalar a símbolos/grafo solo si hace falta. Si falta contexto, es ambiguo,
ilegible o desfasado, continuar con fuentes directas y declarar límites.
Código, steering y contratos son autoridad; un índice viejo solo orienta.
Consultar no autoriza crear, sincronizar ni exportar contexto.

Las menciones `@architecture` y `@project-navigator` ya no son receptores vigentes.
Reformula la petición a `@documentation-orchestrator`; no se transfiere ninguna
autorización antigua. Si el host no resuelve la mención retirada, selecciona el
agente vigente manualmente. Consulta [migración segura](migracion-agentes.md).

Los `@<agente>` siguientes identifican roles del kit; en Antigravity usa la
selección comprobada en el smoke, sin interpretar estas líneas como comandos.

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
