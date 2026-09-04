# Guía interna de agentes y skills

Esta guía explica, en lenguaje de usuario, qué hace cada agente del kit, qué skill
utiliza y cómo pedirle trabajo. La fuente normativa sigue siendo el agente y la
skill canónicos en `canonical/`; estas páginas sirven como orientación rápida.

## Cómo elegir un agente

| Necesitas… | Agente | Skill principal | Escribe principalmente en… |
|---|---|---|---|
| Entender el repositorio, módulos o símbolos | [Project Navigator](project-navigator.md) | `project-navigator` | `.navigator/` |
| Documentar decisiones y estructura técnica | [Architecture](architecture.md) | `architecture` | `.architecture/` |
| Catálogo de APIs, DTOs o persistencia | [Data & API](data-api.md) | `data-api` | `.data/` |
| Documentar colores, componentes o temas | [UI Design](ui-design.md) | `ui-design` | `.design/` |
| Revisar mantenibilidad, tests o complejidad | [Code Quality](code-quality.md) | `code-quality` | `.quality/` y cambios de calidad aprobados |
| Auditar secretos, auth, red o permisos | [Security](security.md) | `security` | `.security/` |
| Comprobar o sincronizar documentación | [Documentation Orchestrator](documentation-orchestrator.md) | `documentation-orchestrator` + especialistas | Carpetas documentales aplicables |
| Definir una feature o bugfix antes de implementarlo | [SDD](sdd.md) | `sdd-spec` | `.sdd/` y código aprobado por las tareas |
| Crear commits, push o preparar releases | [Git & Release Manager](git-release-manager.md) | `git-commit` + `release-management` | Git, versión, tag y CHANGELOG |

## Agente frente a skill

- El **agente** define el rol, el alcance, los límites y la forma de interactuar
  con la plataforma.
- La **skill** define el procedimiento, los artefactos, los estándares y los
  gates de aprobación.
- Si ambos textos difieren, manda la skill.
- Un agente no debe recibir tareas de otro dominio solo porque pueda leer esos
  archivos.

## Uso por plataforma

Los IDs estables son los mismos en las tres plataformas:

| Plataforma | Forma habitual de invocación |
|---|---|
| OpenCode | Selecciona el agente o menciónalo, por ejemplo `@architecture`, `@sdd` o `@security`. |
| GitHub Copilot | Selecciona el agente personalizado instalado; los nombres salen del catálogo. |
| Kiro | Selecciona el agente de `~/.kiro/agents/`; para una skill también puede usarse su comando, según la UI. |

Una petición útil indica el resultado, el alcance y el nivel de autonomía esperado:

```text
@architecture documenta la arquitectura del módulo de autenticación.
Solo analiza ese módulo, cita archivo y línea, y propón primero el plan.
```

## Gates que debes esperar

- **Documentación:** el Orchestrator hace un preflight, recomienda un modelo y
  presenta un plan antes de escribir.
- **Navigator:** bootstrap y updates son explícitos; los procesos pesados tienen
  aviso de modelo y gate de disponibilidad.
- **Architecture, Data & API y UI Design:** la primera documentación masiva parte
  de un estudio y una propuesta.
- **Quality y Security:** primero auditan en solo lectura; después requieren
  confirmación de alcance y remediación en micro-pasos.
- **SDD:** no avanza de fase sin aprobación explícita, salvo Quick Plan solicitado.
- **Git y releases:** commit, push, cambios de versión, tags y CHANGELOG requieren
  confirmación explícita; las acciones destructivas requieren doble confirmación.

## Fichas detalladas

| Agente | Ficha | Skill(s) |
|---|---|---|
| Architecture Agent | [architecture.md](architecture.md) | `architecture` |
| Code Quality Agent | [code-quality.md](code-quality.md) | `code-quality` |
| Data & API Agent | [data-api.md](data-api.md) | `data-api` |
| Documentation Orchestrator | [documentation-orchestrator.md](documentation-orchestrator.md) | `documentation-orchestrator` + especialistas aplicables |
| Git & Release Manager | [git-release-manager.md](git-release-manager.md) | `git-commit` + `release-management` |
| Project Navigator Agent | [project-navigator.md](project-navigator.md) | `project-navigator` |
| Agente SDD | [sdd.md](sdd.md) | `sdd-spec` |
| Security Agent | [security.md](security.md) | `security` |
| UI Design Agent | [ui-design.md](ui-design.md) | `ui-design` |

## Fuentes canónicas

- Inventario: [`canonical/manifest.json`](../../canonical/manifest.json).
- Agentes: [`canonical/agents/`](../../canonical/agents/).
- Skills: [`canonical/skills/`](../../canonical/skills/).
- Uso general del kit: [Cómo usarlo](../uso.md).
- Catálogo resumido: [Catálogo](../catalogo.md).
