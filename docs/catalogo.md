# Catálogo de skills y agentes

Resumen de lo que incluye el kit. El detalle operativo vive en
`canonical/skills/<id>/SKILL.md` y `canonical/agents/<id>.md`.

Inventario oficial: `canonical/manifest.json` (10 skills, 6 agentes, 6 plataformas).

Todos los componentes forman **MAS** (*Multi-Agent System*), el sistema
multiagente de este kit. La convención para referirse al sistema o a un agente
concreto está documentada en [mas.md](mas.md).

Para una explicación orientada a usuarios, consulta la [guía interna de agentes y
skills](agentes/README.md), con una ficha por agente, sus límites y ejemplos de uso.

## Skills

| ID | Descripción breve | Carpeta en el proyecto | Estándares / notas |
|----|-------------------|------------------------|--------------------|
| `architecture` | Documenta y audita arquitectura; no modifica código de negocio | `.architecture/` | arc42, C4, ADRs; modos lite/full |
| `code-quality` | Audita y remedia calidad de código paso a paso | `.quality/` | SonarQube y Clean Code |
| `data-api` | Datos, APIs, DTOs, contratos e integraciones | `.data/` | OpenAPI/JSON Schema; ER Mermaid; lanzador Scalar bloqueado hasta disponer de OpenAPI válido |
| `documentation-orchestrator` | Comprueba, inicializa y sincroniza documentación mediante especialistas | — | Preflight y gates por modo; no crea una fuente documental propia |
| `security` | Auditoría y remediación de seguridad guiada | `.security/` | OWASP MASVS/MASWE/MASTG y CWE |
| `ui-design` | Sistema visual: tokens, componentes, deuda de UI | `.design/` | Agnóstica a tecnología |
| `sdd-spec` | Spec-Driven Development con profundidades `direct`, `lite` y `standard` | `.sdd/specs/<ruta-spec>/` | `Nivel de feature: <n> <emoji>` una vez definido alcance (1–7 🟢, 8–9 🟠, 10 🔴); `lite`: Quick Plan; `standard`: Gates 1-4 |
| `git-commit` | Commits Conventional Commits en español y push con confirmación | — | No versiona ni crea tags |
| `release-management` | SemVer, tags anotados, CHANGELOG; perfiles por tecnología | `.release/` | Android/iOS/Flutter de fábrica; resto auto-extensible |
| `project-navigator` | Navega el repo con mínimo de tokens (capas 0–4) | `.navigator/` | Bootstrap/update asistido; solo lectura fuera de `.navigator/` |

## Agentes

| ID | Nombre | Skills que usa | Rol |
|----|--------|----------------|-----|
| [`code-review`](agentes/code-review.md) | Code Review Agent | `code-quality` + `security` según alcance | Calidad, mantenibilidad, pruebas y seguridad; registros separados |
| [`data-api`](agentes/data-api.md) | Data & API Agent | `data-api` | Capa de datos y contratos; identifica PII |
| [`documentation-orchestrator`](agentes/documentation-orchestrator.md) | Documentation Orchestrator | `documentation-orchestrator` + `architecture` y/o `project-navigator` bajo demanda; otras especialistas según alcance | Consultas core (`inspect`), arquitectura, navegación y mantenimiento documental |
| [`ui-design`](agentes/ui-design.md) | UI Design Agent | `ui-design` | Solo lo visual; no toca negocio ni APIs |
| [`sdd`](agentes/sdd.md) | Agente SDD | `sdd-spec` | Selecciona `lite` para trabajo acotado de bajo riesgo; nivel de feature una vez definido el alcance; specs, gates e implementación trazable |
| [`git-release-manager`](agentes/git-release-manager.md) | Git & Release Manager | `git-commit` + `release-management` | Commits, push, versiones, tags, CHANGELOG |

## Mapa skill ↔ agente ↔ carpeta

```text
project-navigator ──┐
architecture ───────┼───► Documentation Orchestrator → .navigator/ y .architecture/
documentation-orch. ┘     Skills separadas; core local; no carpeta propia
code-quality  ──┐
                ├──────► Code Review Agent       → .quality/ y .security/
security      ──┘                                 (según dominio solicitado)
data-api      ──────────► Data & API Agent        → .data/
ui-design     ──────────► UI Design Agent         → .design/
sdd-spec      ──────────► Agente SDD              → .sdd/
git-commit    ──┐
                ├──► Git & Release Manager
release-mgmt  ──┘                                 → .release/ (releases)
```

## Cuándo usar cada uno

| Necesitas… | Usa |
|------------|-----|
| Onboarding, localizar módulos/símbolos sin reexplorar el repo | Documentation Orchestrator → `inspect` con `project-navigator` |
| Comprobar o sincronizar varias carpetas documentales | Documentation Orchestrator |
| Entender o documentar módulos, capas, ADRs | Documentation Orchestrator → `inspect` o mantenimiento con `architecture` |
| Limpiar smells, complejidad, cobertura, convenciones | Code Review — solo calidad |
| Endpoints, DTOs, OpenAPI, repositorios, ER | Data & API |
| Secretos, TLS, auth, permisos, hardening | Code Review — solo seguridad |
| Revisar calidad y seguridad en la misma sesión | Code Review — revisión completa |
| Colores, tipografía, componentes, temas | UI Design |
| Feature o bugfix con requisitos y diseño antes de codear | SDD (`standard` para bugfixes no triviales) |
| Commit / push del día a día | Git & Release Manager → flujo commit |
| Bump de versión, tag, CHANGELOG | Git & Release Manager → flujo release |

## Contenido de una skill típica

```text
canonical/skills/<id>/
  SKILL.md              # Prompt principal (se carga al activar la skill)
  references/           # Detalle bajo demanda (plantillas, estándares, gates)
  technologies/         # Solo algunas skills (p. ej. perfiles de release)
```

Las referencias no se meten enteras en el contexto inicial: el agente las abre
cuando el procedimiento lo pide. Eso reduce tokens en tareas simples.

## Plataformas

| ID | Destino de instalación |
|----|------------------------|
| `copilot` | `~/.copilot/skills/` y `~/.copilot/agents/` |
| `opencode` | `~/.config/opencode/skills/` y `~/.config/opencode/agent/` |
| `kiro` | `~/.kiro/skills/` y `~/.kiro/agents/` |
| `claude` | `~/.claude/skills/` y `~/.claude/agents/` (o `$CLAUDE_CONFIG_DIR`) |
| `pi` | `~/.pi/agent/skills/` y `~/.pi/agent/prompts/` (o `$PI_CODING_AGENT_DIR`) |
| `antigravity` | `~/.gemini/config/skills/` y `~/.gemini/config/agents/` (Antigravity 2.0) |

Antigravity distribuye los mismos seis agentes y diez skills, con recursos
asociados. El alcance nativo inicial es **Antigravity 2.0**, no soporte completo
del CLI ni del IDE standalone. El CLI documenta skills globales en
`~/.gemini/antigravity-cli/skills/`, destino distinto que este instalador no usa;
los agentes personalizados del IDE no están verificados. Los scripts se probaron
con fixtures en Linux, macOS y Windows: **22/22 pruebas nativas por OS**, Python
3.10, [CI 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
El runtime Antigravity (descubrimiento 6/10, UI, referencias e `invoke_subagent`)
sigue **PENDIENTE**. Véase la evidencia automatizada y el
[procedimiento de smoke](antigravity-smoke.md).

Guía de instalación: [instalacion.md](instalacion.md).  
Cómo invocarlos: [uso.md](uso.md).

`architecture` y `project-navigator` son skills vigentes, no agentes receptores ni
aliases. Sus [guías de arquitectura](agentes/architecture.md) y
[navegación](agentes/project-navigator.md) se conservan. Para instalaciones previas,
consulta [migración y recuperación](migracion-agentes.md).
