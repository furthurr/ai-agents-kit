# Guía de la skill architecture

## Resumen

| Campo | Información |
|---|---|
| Entrada responsable | `documentation-orchestrator` (agente) |
| Skill | [`architecture`](../../canonical/skills/architecture/SKILL.md) |
| Propósito | Documentar, auditar y explicar la arquitectura de un proyecto |
| Artefactos | `.architecture/` |
| Alcance | Módulos, capas, dependencias, patrones, decisiones y deuda arquitectónica |

La skill `architecture`, ejecutada localmente por Documentation Orchestrator,
convierte la estructura real de un repositorio en contexto que
pueden usar el equipo y otros agentes. Es agnóstico a la tecnología y cita las
fuentes (`archivo:línea`) en lugar de inventar componentes.

## Cuándo usarlo

- Cuando necesitas entender o documentar módulos, capas y dependencias.
- Antes de una feature o refactor que requiera conocer la estructura del sistema.
- Para registrar una decisión técnica como ADR.
- Para auditar riesgos o deuda de arquitectura.
- Después de un cambio estructural que pueda dejar desactualizados los diagramas.

No es el procedimiento adecuado para implementar una feature, modificar APIs, arreglar
seguridad o cambiar la UI.

## Qué skill utiliza

La skill `architecture` aplica:

- **arc42** para organizar el contexto y el alcance.
- **C4 en Mermaid** para contexto, contenedores y componentes.
- **ADRs** para decisiones importantes.
- Modos `lite` y `full` según el tamaño del proyecto.

## Recomendación de modelo

Las consultas y cambios incrementales reciben un aviso informativo `BAJO` o `MEDIO`
y continúan el trabajo autorizado en el mismo turno.
Antes de una inicialización, auditoría completa o arquitectura grande/ambigua,
clasifica con un preflight barato y recomienda `MEDIO` o `ALTO`; después continúa
sin esperar por el modelo. El cambio de modelo es manual; el aviso no sustituye
la aprobación de estudios o propuestas ni se repite si ya se comunicó para el
mismo alcance. Un cambio exclusivo de nivel se informa sin pausar el trabajo autorizado.

## Cómo trabaja

1. Clasifica la petición y aclara cualquier ambigüedad.
2. En una tarea puntual lee el contexto existente y solo las fuentes afectadas.
3. En una primera inicialización detecta proyectos, tecnología y tamaño, y propone
   `lite` o `full` antes de crear documentación masiva.
4. Lee el estado de sincronización y revisa el historial de Git de forma incremental.
5. Actualiza los documentos afectados, diagramas, ADRs y deuda técnica.
6. Si una deuda requiere implementación compleja, recomienda SDD con la referencia
   y espera que el usuario decida; nunca cambia de agente automáticamente.
7. Registra el commit documentado en `.architecture/README.md`.

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
@documentation-orchestrator inspect: ¿Qué módulos existen y cómo dependen entre sí?
Solo lectura; cita fuentes y límites, sin generar documentación.
```

```text
@documentation-orchestrator sync-domain architecture: documenta la decisión de usar colas para el procesamiento asíncrono.
Propón un ADR y no modifiques código.
```

```text
@documentation-orchestrator bootstrap-core: inicializa arquitectura y Navigator.
Presenta primero el plan; conserva los gates de ambas skills.
```

`inspect` no ejecuta generación documental ni acredita sincronización. Las skills
`architecture` y `project-navigator` permanecen separadas, con carpetas distintas.
`@architecture` es una entrada retirada, sin alias ejecutable; consulta la
[migración segura](../migracion-agentes.md) si aún aparece instalada.

## Límites y confirmaciones

- Solo documenta, audita y recomienda arquitectura.
- No refactoriza ni modifica código de negocio, UI, datos, CI o Git remoto.
- Puede recomendar SDD para implementar deuda que requiera requisitos, diseño,
  migraciones o coordinación, pero mantiene su prohibición de modificar código.
- En la primera ejecución presenta estudio y propuesta antes de escribir en masa.
- Solo usa Git en lectura y mantiene la documentación dentro de `.architecture/`.
- Nunca incluye secretos, tokens o credenciales.
