---
name: sdd-spec
description: >-
  Aplica la metodología Spec-Driven Development (SDD) estilo Kiro: genera y
  refina specs (requirements.md, design.md, tasks.md, verification.md) con un
  flujo de 4 fases, gates de aprobación, notación EARS y trazabilidad. Úsala al
  planificar una feature, escribir requisitos, diseñar arquitectura, desglosar
  tareas o corregir un bug de forma estructurada (bugfix). Palabras clave: spec,
  SDD, especificación, EARS, requirements, design, tasks, bugfix, Kiro.
---

# Skill: SDD Spec

Flujo SDD de 4 fases con gates, EARS y trazabilidad. Funciona con cualquier agente.

> **Precedencia:** si el agente `SDD (Spec-Driven Development)` y esta skill divergen, manda esta skill.

## Artefactos

Destino: `.sdd/specs/<nombre-feature>/`

| Archivo | Fase | Contenido |
|---------|------|-----------|
| `requirements.md` (o `bugfix.md`) | 1 | Historias + criterios EARS |
| `design.md` | 2 | Arquitectura, modelos, diagramas, pruebas |
| `tasks.md` | 3 | Tareas discretas, trazadas y secuenciadas |
| `verification.md` | 4 | Matriz de trazabilidad + cierre |

## Flujo con gates

> **No avances de fase sin aprobación explícita del usuario.**
> Como Copilot no
> tiene una herramienta de "pregunta" dedicada, el gate se implementa de forma
> natural: Termina tu turno con la pregunta y espera. Excepción: Quick Plan.

### Fase 1 — Requirements

1. Lee steering (`.github/copilot-instructions.md`, `AGENTS.md`, `.sdd/steering/*.md`). Detecta dominio y lee
   solo su `README.md` de contexto (`.architecture/`, `.design/`, `.data/`,
   `.security/`, `.quality/`). Si falta, recomienda especialista; si el usuario
   continúa, captura lo imprescindible en `design.md`.
2. Descompón en historias de usuario.
3. Criterios en EARS:
   - `CUANDO <condición> EL SISTEMA DEBERÁ <comportamiento>`
   - `SI <error> ENTONCES EL SISTEMA DEBERÁ <manejo>`
   - `MIENTRAS <estado> EL SISTEMA DEBERÁ <comportamiento>`
   - `EL SISTEMA DEBERÁ <siempre activo>`
4. Cubre edge cases y errores; declara supuestos.
5. **GATE 1**: "¿Apruebas los requisitos o quieres iterarlos?"

### Fase 2 — Design

1. Lee código existente y steering. Reutiliza documentación de `.architecture/`,
   `.design/`, `.data/` cuando el requisito toque ese dominio.
2. Arquitectura, componentes, modelos de datos, interfaces/endpoints.
3. Diagramas Mermaid (flowchart + sequence), manejo de errores, estrategia de pruebas.
4. Deriva propiedades (PBT) desde los requisitos EARS.
5. **GATE 2**: "¿Apruebas el diseño o quieres ajustarlo?"

### Fase 3 — Tasks

1. Tareas discretas, numeradas, trazadas a requisitos `(Req X)`.
2. Secuencia por dependencias; marca `[P]` (paralelo) y `[opcional]`.
3. Incluye grafo de waves. Consulta `references/templates.md` para formato.
4. **GATE 3**: "¿Apruebo el plan y empiezo a implementar?"

### Implementación

- Una tarea a la vez o en waves. Actualiza estados: `[ ]` → 🔵 → `[x]`.
- Escribe tests (incl. PBT). Consulta `references/testing.md` para stack por tecnología.
- Si la carpeta canónica del dominio existe y creas algo reutilizable, documéntalo
  ahí cargando la skill del especialista.

### Fase 4 — Verificación y cierre

Prerrequisito: todas las tareas en `[x]`.
1. Ejecuta suite completa de tests.
2. Construye `verification.md` con matriz:

   | Requisito | Tarea(s) | Test(s) | Estado |
   |-----------|----------|---------|--------|
   | Req 1     | 1.1, 1.2 | `Test`  | ✅     |

3. Marca huecos y propón acción.
4. **GATE 4**: "¿Cierro la spec o cubrimos los huecos?" No cierres sin cobertura completa.

## Variante Bugfix

`bugfix.md` con tres bloques EARS:
- Actual: `CUANDO <...> EL SISTEMA <incorrecto>`
- Esperado: `CUANDO <...> EL SISTEMA DEBERÁ <correcto>`
- Inalterado: `EL SISTEMA DEBERÁ SEGUIR <...>`

Diseño con causa raíz + propiedades. Tareas con tests de regresión.

## Variante Quick Plan

Genera requirements, design y tasks en una pasada **sin gates**, con preguntas
aclaratorias por adelantado. Omite Fase 4. Solo para features bien entendidas.

## Reglas de calidad

- **Proporcionalidad:** tareas triviales → modo directo, sin spec.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Implementación → `design.md`, no `requirements.md`.
- Cada requisito debe tener ≥1 tarea que lo cubra.
- Respeta el steering del proyecto.
- No cierres la spec sin cobertura total.
- Consulta `references/ears-reference.md` para la tabla completa de patrones EARS.
