# Architecture Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `architecture` |
| Skill | [`architecture`](../../canonical/skills/architecture/SKILL.md) |
| Propósito | Documentar, auditar y explicar la arquitectura de un proyecto |
| Artefactos | `.architecture/` |
| Alcance | Módulos, capas, dependencias, patrones, decisiones y deuda arquitectónica |

Architecture Agent convierte la estructura real de un repositorio en contexto que
pueden usar el equipo y otros agentes. Es agnóstico a la tecnología y cita las
fuentes (`archivo:línea`) en lugar de inventar componentes.

## Cuándo usarlo

- Cuando necesitas entender o documentar módulos, capas y dependencias.
- Antes de una feature o refactor que requiera conocer la estructura del sistema.
- Para registrar una decisión técnica como ADR.
- Para auditar riesgos o deuda de arquitectura.
- Después de un cambio estructural que pueda dejar desactualizados los diagramas.

No es el agente adecuado para implementar una feature, modificar APIs, arreglar
seguridad o cambiar la UI.

## Qué skill utiliza

La skill `architecture` aplica:

- **arc42** para organizar el contexto y el alcance.
- **C4 en Mermaid** para contexto, contenedores y componentes.
- **ADRs** para decisiones importantes.
- Modos `lite` y `full` según el tamaño del proyecto.

## Cómo trabaja

1. Clasifica la petición y aclara cualquier ambigüedad.
2. En una tarea puntual lee el contexto existente y solo las fuentes afectadas.
3. En una primera inicialización detecta proyectos, tecnología y tamaño, y propone
   `lite` o `full` antes de crear documentación masiva.
4. Lee el estado de sincronización y revisa el historial de Git de forma incremental.
5. Actualiza los documentos afectados, diagramas, ADRs y deuda técnica.
6. Registra el commit documentado en `.architecture/README.md`.

## Qué produce

En modo `lite` crea un `.architecture/README.md` y, opcionalmente, `decisions/`.
La deuda se mantiene en una sección del README.

En modo `full` puede crear, entre otros:

```text
.architecture/
├── README.md
├── 01-overview.md
├── 02-context.md
├── 03-containers.md
├── 04-components.md
├── 05-runtime.md
├── 06-deployment.md
├── 07-crosscutting.md
├── 08-quality-risks.md
├── glossary.md
├── decisions/
└── arch-tech-debt.md
```

## Ejemplos de uso

```text
@architecture ¿Qué módulos existen y cómo dependen entre sí?
```

```text
@architecture Documenta la decisión de usar colas para el procesamiento asíncrono.
Propón un ADR y no modifiques código.
```

## Límites y confirmaciones

- Solo documenta, audita y recomienda arquitectura.
- No refactoriza ni modifica código de negocio, UI, datos, CI o Git remoto.
- En la primera ejecución presenta estudio y propuesta antes de escribir en masa.
- Solo usa Git en lectura y mantiene la documentación dentro de `.architecture/`.
- Nunca incluye secretos, tokens o credenciales.
