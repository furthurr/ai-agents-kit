# Visión del kit

## Qué es

**AI Agents Kit** es una fuente versionada de **skills** y **agentes** para
asistentes de código con IA:

- [GitHub Copilot](https://github.com/features/copilot)
- [OpenCode](https://opencode.ai)
- [Kiro](https://kiro.dev)

La lógica común se escribe **una sola vez** en `canonical/` y se renderiza para
cada herramienta mediante adaptadores declarativos. Así se evita mantener tres
copias del mismo prompt.

## Problema que resuelve

Sin especialización ni contexto persistente, un agente genérico suele:

- Reexplorar el repositorio en cada sesión.
- Mezclar dominios (UI + seguridad + datos en el mismo cambio).
- Dar respuestas inconsistentes porque no hay una fuente única de verdad.
- Gastar tokens leyendo código que ya podría estar documentado de forma estable.

## Solución

El kit combina tres ideas:

### 1. Especialistas con alcance fijo

Cada agente tiene un **dominio inviolable**. El de arquitectura no refactoriza
negocio; el de seguridad no implementa pantallas; el de Git no toca la UI.
Cuando la petición sale de su alcance, se detiene y redirige al especialista
adecuado.

### 2. Skills como procedimiento canónico

La **skill** define el cómo (pasos, plantillas, estándares, gates). El **agente**
define el rol, el tono y los límites. Si agente y skill divergen, **manda la
skill**.

### 3. Carpetas canónicas en el proyecto del usuario

Varios especialistas dejan documentación estructurada en el repo donde trabajan:

| Carpeta | Dominio |
|---------|---------|
| `.navigator/` | Contexto, módulos e índices de navegación |
| `.architecture/` | Arquitectura (arc42, C4, ADRs) |
| `.design/` | Sistema visual y tokens |
| `.data/` | APIs, DTOs, contratos, ER |
| `.security/` | Hallazgos y estándares de seguridad |
| `.quality/` | Deuda de calidad y reglas |
| `.sdd/` | Specs (requirements, design, tasks, verification) |
| `.release/` | Perfil de versionado del proyecto |

Eso da contexto reutilizable entre sesiones y entre agentes (por ejemplo, SDD
lee el README de contexto del dominio cuando existe).

## Principios

1. **Una fuente de verdad** — editar `canonical/` + `adapters/`; nunca `generated/` a mano.
2. **Alcance inviolable** — cada especialista se queda en su dominio.
3. **Confirmación explícita** — commit, push, tag, release y acciones destructivas piden OK del usuario.
4. **Sin secretos** — no incluir tokens ni credenciales en prompts, adapters ni artefactos.
5. **Contexto selectivo** — cargar solo lo necesario; las referencias pesadas van bajo demanda (`references/`).
6. **Español por defecto** — prompts y comunicación en español; se adaptan si el usuario escribe en otro idioma.

## Skill vs agente

```text
Usuario pide algo
       │
       ▼
   Agente (rol + límites + permisos de la plataforma)
       │
       ▼
   Skill (procedimiento, estándares, plantillas)
       │
       ▼
   Artefactos en el repo del usuario (si aplica)
   p. ej. .architecture/, .sdd/specs/...
```

Algunos agentes cargan **una** skill (`architecture` → `architecture`).
`Git & Release Manager` orquesta `git-commit` y `release-management`.
`Documentation Orchestrator` selecciona las skills documentales aplicables, pero
no sustituye su autoridad ni crea una carpeta propia.

## Multiplataforma

```text
canonical/     lógica y contenido común
    +
adapters/      frontmatter, nombres, permisos y sustituciones por herramienta
    │
    ▼  tools/render.py
generated/     artefactos listos para instalar (no editar)
    │
    ▼  scripts/install/*
~/.copilot/  ·  ~/.config/opencode/  ·  ~/.kiro/
```

Detalle técnico: [arquitectura-del-kit.md](arquitectura-del-kit.md).

## Project Navigator

Project Navigator forma parte del kit como **MVP instalable**. Materializa
contexto selectivo en `.navigator/` mediante capas: contexto raíz y mapa de
módulos obligatorios; símbolos y grafo opt-in; código puntual como último nivel.

La fuente operativa es
[`canonical/skills/project-navigator/SKILL.md`](../canonical/skills/project-navigator/SKILL.md)
y sus referencias. El uso diario se documenta en [uso.md](uso.md), la validación
manual en [navigator-smoke.md](navigator-smoke.md) y la evolución pendiente en
[mejoras.md](mejoras.md).

## Documentation Orchestrator

El orquestador ofrece una entrada única para comprobar, inicializar y sincronizar
las carpetas documentales. Su core de bootstrap es `.navigator/` más
`.architecture/`; Data y Design son condicionales, mientras Quality y Security
son assurance recomendado y se sincronizan cuando existen o se solicitan.

Antes de operar ejecuta un preflight barato, recomienda manualmente un nivel de
modelo y se detiene. El coste alto queda reservado para barridos iniciales,
monorepos complejos y auditorías profundas. El detalle operativo vive en
[`canonical/skills/documentation-orchestrator/SKILL.md`](../canonical/skills/documentation-orchestrator/SKILL.md).
