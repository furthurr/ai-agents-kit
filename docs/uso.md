# Uso diario

Tras [instalar](instalacion.md), eliges el **agente** (o dejas que la herramienta
active la **skill** por relevancia) y describes la tarea en lenguaje natural.

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

Si no ves un agente tras instalar, **reinicia** la herramienta y verifica la
ruta de destino en [instalacion.md](instalacion.md).

## Guía rápida por intención

| Dices algo como… | Agente |
|------------------|--------|
| “¿Qué es este repo?”, “¿dónde está X?”, “bootstrap del navigator” | Project Navigator |
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
3. **SDD antes de features grandes** — requisitos y diseño con gates; implementación
   solo tras aprobación (salvo Quick Plan / trivial que el usuario pida en directo).
4. **Git y releases** — el agente propondrá el plan; **tú confirmas** commit, push,
   tag o changelog aplicado.
5. **Seguridad y calidad** — la remediación va en micro-pasos con confirmación;
   no esperes un “arregla todo el repo” de un golpe.
6. **Contexto del proyecto** — si existe `AGENTS.md` o steering de Kiro, los
   agentes de SDD lo leen de forma selectiva.

## Qué deja cada especialista en tu repo

| Agente | Artefactos típicos |
|--------|-------------------|
| Project Navigator | `.navigator/` (ai-context, module-map, config; symbols/graph opt-in) |
| Architecture | `.architecture/` (contexto, diagramas, ADRs, deuda) |
| Code Quality | `.quality/` (hallazgos, estándares cacheados) |
| Data & API | `.data/` (catálogo, modelos, contratos, ER) |
| Security | `.security/` (hallazgos, checklist, evidencia) |
| UI Design | `.design/` (tokens, componentes, deuda visual) |
| SDD | `.sdd/specs/<nombre>/` (requirements, design, tasks, verification) |
| Git & Release | Commits/tags/CHANGELOG; perfil en `.release/` si aplica |

Estas carpetas son **del proyecto en el que trabajas**, no del repo del kit.
Conviene versionarlas con el código para que el equipo y la IA compartan el
mismo contexto.

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
- Architecture **no** refactoriza código de negocio.
- Code Quality **deriva** vulnerabilidades al Security Agent.
- Data & API **no** implementa pantallas.
- Security / Quality **no** exponen secretos reales en la documentación.
- Git & Release **no** hace commit/push/tag sin confirmación explícita;
  acciones destructivas piden doble confirmación.
- SDD **no** marca tareas hechas sin evidencia (integrity gate).

## Ejemplo de flujo completo

```text
0. @project-navigator → “Bootstrap de .navigator/” / “¿qué es este repo?”
1. @architecture  → “Inicializa la documentación de arquitectura”
2. @data-api      → “Documenta los endpoints de autenticación”
3. @sdd           → “Spec standard para refresh token offline”
4. (implementación con el agente/skill que corresponda a las tasks)
5. @code-quality  → “Revisa los archivos tocados”
6. @security      → “Revisa almacenamiento del token”
7. @git-release-manager → “Prepara el commit” / “Release patch”
```

No es obligatorio seguir este orden en cada cambio; sirve como mapa cuando el
trabajo cruza varios dominios.
