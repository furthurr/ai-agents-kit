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

> **Precedencia:** si el agente `{{sdd_agent}}` y esta skill divergen, manda esta skill.

## Modos de profundidad

| Modo | Cuándo | Qué produce | Coste |
|------|--------|-------------|-------|
| `direct` | Trivial | Sin spec 4 fases | Mínimo |
| `standard` | **Default** | 4 fases, design corto, 0–5 invariantes, tests ejemplo | Baseline +~10 % |
| `deep` | Usuario lo pide | + glosario, más diagramas, PBT real si aplica | +40–80 % |

Default = `standard`. No actives `deep` solo. Caps standard: design ~≤250 líneas; máx. 5 invariantes; 1 flowchart + 1 sequence; glosario solo en `deep` o si el usuario lo pide.

## Artefactos

Destino: `.sdd/specs/<nombre-feature>/`

| Archivo | Fase | Contenido |
|---------|------|-----------|
| `requirements.md` (o `bugfix.md`) | 1 | Historias + criterios EARS |
| `design.md` | 2 | Arquitectura, modelos, diagramas, pruebas |
| `tasks.md` | 3 | Tareas discretas, trazadas y secuenciadas |
| `verification.md` | 4 | Matriz + evidencia + cierre |

## Flujo con gates

> **No avances de fase sin aprobación explícita del usuario.**
> {{gate_instruction}} Termina tu turno con la pregunta y espera. Excepción: Quick Plan.

### Fase 1 — Requirements

1. Lee steering ({{steering_paths}}, `.sdd/steering/*.md`). Detecta dominio y lee
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

1. Lee código existente y steering. Reutiliza `.architecture/`, `.design/`, `.data/` si aplica.
2. Carga `references/quality-bar.md`; el design debe satisfacerla (cita excepciones).
3. Arquitectura, componentes, modelos, errores, pruebas. Diagramas según caps del modo.
4. PBT condicional (`references/testing.md`): en standard, 0–5 invariantes narrativos opcionales.
5. **GATE 2**: "¿Apruebas el diseño o quieres ajustarlo?"

### Fase 3 — Tasks

1. Tareas discretas, numeradas, trazadas a requisitos `(Req X)`.
2. Secuencia por dependencias; marca `[P]` (paralelo) y `[opcional]`.
3. Incluye grafo de waves. Consulta `references/templates.md` para formato.
4. **GATE 3**: "¿Apruebo el plan y empiezo a implementar?"

### Implementación

- Una tarea a la vez o en waves. Estados: `[ ]` → 🔵 → `[x]`.
- Antes de `[x]`: `references/integrity-gate.md`.
- Al escribir tests: `references/testing.md` (PBT condicional).
- Waves UI/datos: revisar `references/quality-bar.md`.
- Si existe carpeta canónica del dominio y creas algo reutilizable, documéntalo con la skill del especialista.

### Fase 4 — Verificación y cierre

Prerrequisito: `[x]` con artefacto real (o `[omitido: razón]`).
1. `references/integrity-gate.md`: validar cada `[x]` ↔ disco/evidencia.
2. Suite de tests + spot-check `quality-bar` y 3–5 RNF del spec.
3. `verification.md` con columna Evidencia (`templates.md`). No cerrar con huérfanos.
4. **GATE 4**: "¿Cierro la spec o cubrimos los huecos?"

## Variante Bugfix

`bugfix.md` con tres bloques EARS:
- Actual: `CUANDO <...> EL SISTEMA <incorrecto>`
- Esperado: `CUANDO <...> EL SISTEMA DEBERÁ <correcto>`
- Inalterado: `EL SISTEMA DEBERÁ SEGUIR <...>`

Diseño con causa raíz + invariantes si aplican. Tareas con tests de regresión.

## Variante Quick Plan

Genera requirements, design y tasks en una pasada **sin gates**, con preguntas
aclaratorias por adelantado. Omite Fase 4. Solo para features bien entendidas.
Al implementar, aplica integrity-gate y caps `standard`.

## Reglas de calidad

- **Proporcionalidad:** trivial → `direct`, sin spec.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Implementación → `design.md`, no `requirements.md`.
- Cada requisito ≥1 tarea. Respeta steering. Sin cumplimiento inventado.
- Consulta `references/ears-reference.md` para patrones EARS.
