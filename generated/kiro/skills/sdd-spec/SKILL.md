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

> **Precedencia:** si el agente `sdd` y esta skill divergen, manda esta skill.

## Modos de profundidad

| Modo | Cuándo | Qué produce | Carga documental |
|------|--------|-------------|-------------------|
| `direct` | Cambio trivial verificable | Sin spec 4 fases | Mínima |
| `standard` | **Default** | 4 fases, design corto, 0–5 invariantes, testing adaptativo | Moderada |
| `deep` | Usuario lo pide | + glosario, más diagramas, PBT real si aplica | Alta |

Default = `standard`. No actives `deep` solo. Caps standard: design ~≤250 líneas; máx. 5 invariantes; 1 flowchart + 1 sequence; glosario solo en `deep` o si el usuario lo pide.

`direct` exige alcance claro, localizado y reversible, sin contrato público,
migración, decisión arquitectónica, cruce de capas ni riesgo relevante de seguridad,
concurrencia o integridad. Si falla una condición, usa `standard`.

Profundidad y testing son ejes independientes: sin cambio observable → sin test
nuevo; bug o legado → regresión/caracterización; comportamiento nuevo o modificado
→ TDD focalizado; TDD estricto solo si el usuario lo pide. `direct` puede incluir un
microciclo TDD y `deep` no activa TDD estricto. Detalle en `references/testing.md`.

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
> El gate se implementa de forma natural: termina tu turno
> con la pregunta y espera. Excepción: Quick Plan.

### Fase 1 — Requirements

1. Lee steering (`.kiro/steering/*.md`, `AGENTS.md`, `.sdd/steering/*.md`). Detecta dominio y lee
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
4. Elige y registra la estrategia adaptativa de pruebas y el PBT condicional según
   `references/testing.md`, incluidas las excepciones.
5. **GATE 2**: "¿Apruebas el diseño o quieres ajustarlo?"

### Fase 3 — Tasks

1. Tareas discretas, numeradas, trazadas a requisitos `(Req X)`.
2. Secuencia por dependencias; marca `[P]` (paralelo) y `[opcional]`.
3. Para TDD focalizado/estricto, cada tarea de comportamiento explicita el orden
   interno RED → GREEN → REFACTOR, sin crear tareas ceremoniales por cada paso.
4. Incluye grafo de waves. Consulta `references/templates.md` para formato.
5. **GATE 3**: "¿Apruebas el plan y empiezo a implementar?"

### Implementación

- Una tarea a la vez o en waves. Estados: `[ ]` → 🔵 → `[x]`.
- Antes de `[x]`: `references/integrity-gate.md`.
- Ejecuta el ciclo elegido en `references/testing.md`; no declares TDD sin haber
  observado un RED que falle por la razón esperada.
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

Usa el flujo y gates normales, salvo bug trivial `direct`. Diseño con causa raíz +
invariantes si aplican. Primero crea una regresión que falle por el defecto; usa
caracterización para comportamiento legado que deba preservarse. Si no puede
reproducirse, registra la limitación y no inventes un RED.

## Variante Quick Plan

Genera requirements, design y tasks en una pasada **sin gates**, con preguntas
aclaratorias por adelantado. Omite Fase 4. Solo para features bien entendidas.
Al implementar, aplica integrity-gate y caps `standard`. `design.md` registra la
estrategia y `tasks.md` ordena el ciclo. Como no hay `verification.md`, deja la
evidencia en las tareas y en el resumen final.

## Reglas de calidad

- **Proporcionalidad:** aplica los criterios verificables de `direct`; no confundas
  cambio pequeño con riesgo bajo.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Implementación → `design.md`, no `requirements.md`.
- Cada requisito ≥1 tarea. Respeta steering. Sin cumplimiento inventado.
- Consulta `references/ears-reference.md` para patrones EARS.
