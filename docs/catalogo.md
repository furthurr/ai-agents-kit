# Catálogo de skills y agentes

Resumen de lo que incluye el kit. El detalle operativo vive en
`canonical/skills/<id>/SKILL.md` y `canonical/agents/<id>.md`.

Inventario oficial: `canonical/manifest.json` (11 skills, 5 agentes, 6 plataformas).

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
| `data-api` | Datos, APIs, DTOs, contratos e integraciones | `.data/` | OpenAPI/JSON Schema; ER Mermaid cuando hay persistencia; catálogo de endpoints si no existe OpenAPI |
| `documentation-orchestrator` | Comprueba, inicializa y sincroniza documentación mediante especialistas | — | Preflight y gates por modo; no crea una fuente documental propia |
| `developer` | Planifica e implementa características completas en UI, datos/APIs y negocio | — | PLAN conversacional propio, verificación y aviso documental condicional; no usa SDD |
| `security` | Auditoría y remediación de seguridad guiada | `.security/` | OWASP MASVS/MASWE/MASTG y CWE |
| `ui-design` | Sistema visual: tokens, componentes, deuda de UI | `.design/` | Agnóstica a tecnología |
| `sdd-spec` | Spec-Driven Development: `direct`, SDD-Tiny y SDD-Lite; `standard` legacy solo bajo solicitud explícita | `.sdd/specs/<ruta-spec>/` | Recomendación de feature por nota; Tiny usa `spec.md` único y gates 3/4; SDD-Lite conserva Quick Plan; `standard` explícito conserva Gates 1-4 |
| `git-commit` | Commits Conventional Commits en español y push con confirmación | — | No versiona ni crea tags |
| `release-management` | SemVer, tags anotados, CHANGELOG; perfiles por tecnología | `.release/` | Android/iOS/Flutter de fábrica; resto auto-extensible |
| `project-navigator` | Navega el repo con mínimo de tokens (capas 0–4) | `.navigator/` | Bootstrap/update asistido; solo lectura fuera de `.navigator/` |

## Agentes

| ID | Nombre | Skills que usa | Rol |
|----|--------|----------------|-----|
| [`code-review`](agentes/code-review.md) | Code Review Agent | `code-quality` + `security` según alcance | Calidad, mantenibilidad, pruebas y seguridad; registros separados |
| [`developer`](agentes/developer.md) | Developer Agent | `developer` + `data-api`/`ui-design` bajo demanda | Implementa producto a través de UI, datos/APIs y negocio; planifica y verifica |
| [`documentation-orchestrator`](agentes/documentation-orchestrator.md) | Documentation Orchestrator | `documentation-orchestrator`, core y skills `data-api`/`ui-design` locales; `code-review` solo por handoff | Consultas core (`inspect`), arquitectura, navegación y mantenimiento documental |
| [`sdd`](agentes/sdd.md) | Agente SDD | `sdd-spec` | Presenta/valida alcance completo, califica y recomienda profundidad con elección manual; atención, entregas y continuidad; specs, gates e implementación trazable |
| [`git-release-manager`](agentes/git-release-manager.md) | Git & Release Manager | `git-commit` + `release-management` | Commits, push, versiones, tags, CHANGELOG |

## Mapa skill ↔ agente ↔ carpeta

```text
project-navigator ──┐
architecture ───────┼───► Documentation Orchestrator → .navigator/ y .architecture/
documentation-orch. ┘     Skills separadas; core local; no carpeta propia
code-quality  ──┐
                ├──────► Code Review Agent       → .quality/ y .security/
security      ──┘                                 (según dominio solicitado)
data-api      ──┐
ui-design     ──┼───────► Developer Agent (implementación) / Documentation Orchestrator (documentación)
developer     ──┘          → producto; skills documentales conservan .data/ y .design/
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
| Implementar API, DTOs, repositorios o cambios de UI/negocio | Developer |
| Actualizar catálogo `.data/` o sistema visual `.design/` | Documentation Orchestrator (skills `data-api`/`ui-design` locales) |
| Secretos, TLS, auth, permisos, hardening | Code Review — solo seguridad |
| Revisar calidad y seguridad en la misma sesión | Code Review — revisión completa |
| Colores, tipografía, componentes, temas | Documentation Orchestrator para documentación; Developer para implementación |
| Feature o bugfix | Developer; SDD solo cuando el usuario selecciona explícitamente su metodología |
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

Antigravity distribuye los mismos cinco agentes y once skills, con recursos
asociados. El alcance nativo inicial es **Antigravity 2.0**, no soporte completo
del CLI ni del IDE standalone. El CLI documenta skills globales en
`~/.gemini/antigravity-cli/skills/`, destino distinto que este instalador no usa;
los agentes personalizados del IDE no están verificados. Los scripts se probaron
con fixtures en Linux, macOS y Windows: **22/22 pruebas nativas por OS**, Python
3.10, [CI 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
El runtime Antigravity (descubrimiento 5/11, UI, referencias e `invoke_subagent`)
sigue **PENDIENTE**. Véase la evidencia automatizada y el
[procedimiento de smoke](antigravity-smoke.md).

Guía de instalación: [instalacion.md](instalacion.md).  
Cómo invocarlos: [uso.md](uso.md).

`architecture` y `project-navigator` son skills vigentes, no agentes receptores ni
aliases. Sus [guías de arquitectura](agentes/architecture.md) y
[navegación](agentes/project-navigator.md) se conservan. Para instalaciones previas,
consulta [migración y recuperación](migracion-agentes.md).
