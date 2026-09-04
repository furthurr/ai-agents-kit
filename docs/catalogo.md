# Catálogo de skills y agentes

Resumen de lo que incluye el kit. El detalle operativo vive en
`canonical/skills/<id>/SKILL.md` y `canonical/agents/<id>.md`.

Inventario oficial: `canonical/manifest.json` (10 skills, 9 agentes, 3 plataformas).

Para una explicación orientada a usuarios, consulta la [guía interna de agentes y
skills](agentes/README.md), con una ficha por agente, sus límites y ejemplos de uso.

## Skills

| ID | Descripción breve | Carpeta en el proyecto | Estándares / notas |
|----|-------------------|------------------------|--------------------|
| `architecture` | Documenta y audita arquitectura; no modifica código de negocio | `.architecture/` | arc42, C4 (Mermaid), ADRs; modos lite/full |
| `code-quality` | Audita y remedia calidad de código paso a paso | `.quality/` | SonarQube (reglas públicas), Clean Code; foco móvil |
| `data-api` | Datos, APIs, DTOs, contratos e integraciones | `.data/` | OpenAPI/JSON Schema (+ GraphQL/AsyncAPI/gRPC si aplica); ER Mermaid |
| `documentation-orchestrator` | Comprueba, inicializa y sincroniza documentación mediante especialistas | — | Gate 0 de modelo; no crea una fuente documental propia |
| `security` | Auditoría y remediación de seguridad guiada | `.security/` | OWASP MASVS/MASWE/MASTG, Mobile Top 10, CWE |
| `ui-design` | Sistema visual: tokens, componentes, deuda de UI | `.design/` | Agnóstica a tecnología |
| `sdd-spec` | Spec-Driven Development en 4 fases con gates | `.sdd/specs/<feature>/` | EARS, trazabilidad; modos direct/standard/deep |
| `git-commit` | Commits Conventional Commits en español y push con confirmación | — | No versiona ni crea tags |
| `release-management` | SemVer, tags anotados, CHANGELOG; perfiles por tecnología | `.release/` | Android/iOS/Flutter de fábrica; resto auto-extensible |
| `project-navigator` | Navega el repo con mínimo de tokens (capas 0–4) | `.navigator/` | Bootstrap/update asistido; solo lectura fuera de `.navigator/` |

## Agentes

| ID | Nombre | Skills que usa | Rol |
|----|--------|----------------|-----|
| [`architecture`](agentes/architecture.md) | Architecture Agent | `architecture` | Solo documenta/audita/recomienda en `.architecture/` |
| [`code-quality`](agentes/code-quality.md) | Code Quality Agent | `code-quality` | Calidad, mantenibilidad, pruebas; deriva seguridad |
| [`data-api`](agentes/data-api.md) | Data & API Agent | `data-api` | Capa de datos y contratos; identifica PII |
| [`documentation-orchestrator`](agentes/documentation-orchestrator.md) | Documentation Orchestrator | `documentation-orchestrator` + especialistas seleccionadas | Coordina estado, bootstrap, sincronización y release-check documental |
| [`security`](agentes/security.md) | Security Agent | `security` | Solo seguridad; micro-pasos con confirmación |
| [`ui-design`](agentes/ui-design.md) | UI Design Agent | `ui-design` | Solo lo visual; no toca negocio ni APIs |
| [`sdd`](agentes/sdd.md) | Agente SDD | `sdd-spec` | Specs, gates de aprobación e implementación trazable |
| [`git-release-manager`](agentes/git-release-manager.md) | Git & Release Manager | `git-commit` + `release-management` | Commits, push, versiones, tags, CHANGELOG |
| [`project-navigator`](agentes/project-navigator.md) | Project Navigator | `project-navigator` | Investigación/navegación; bootstrap de índices en `.navigator/` |

## Mapa skill ↔ agente ↔ carpeta

```text
project-navigator ──────► Project Navigator       → .navigator/
documentation-orch. ────► Documentation Orchestrator
                          └─ coordina las carpetas existentes; no crea una propia
architecture  ──────────► Architecture Agent      → .architecture/
code-quality  ──────────► Code Quality Agent      → .quality/
data-api      ──────────► Data & API Agent        → .data/
security      ──────────► Security Agent          → .security/
ui-design     ──────────► UI Design Agent         → .design/
sdd-spec      ──────────► Agente SDD              → .sdd/
git-commit    ──┐
                ├──► Git & Release Manager
release-mgmt  ──┘                                 → .release/ (releases)
```

## Cuándo usar cada uno

| Necesitas… | Usa |
|------------|-----|
| Onboarding, localizar módulos/símbolos sin reexplorar el repo | Project Navigator |
| Comprobar o sincronizar varias carpetas documentales | Documentation Orchestrator |
| Entender o documentar módulos, capas, ADRs | Architecture |
| Limpiar smells, complejidad, cobertura, convenciones | Code Quality |
| Endpoints, DTOs, OpenAPI, repositorios, ER | Data & API |
| Secretos, TLS, auth, permisos, hardening | Security |
| Colores, tipografía, componentes, temas | UI Design |
| Feature o bugfix con requisitos y diseño antes de codear | SDD |
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

Guía de instalación: [instalacion.md](instalacion.md).  
Cómo invocarlos: [uso.md](uso.md).
