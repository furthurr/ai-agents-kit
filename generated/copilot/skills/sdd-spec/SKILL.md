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

## Identidad del MAS

En este kit, `MAS` significa **Multi-Agent System** (sistema multiagente): agentes,
skills, orquestación, handoffs, adaptadores y artefactos generados. `MAS:` dirige
una instrucción al sistema completo; `@<agente>` dirige a un agente concreto. No
confundas `MAS` con un modelo/proveedor LLM ni con `MASVS`, `MASWE` o `MASTG` de OWASP.

Flujo SDD de 4 fases con gates, EARS y trazabilidad. Funciona con cualquier agente.

> **Precedencia:** si el agente `SDD (Spec-Driven Development)` y esta skill divergen, manda esta skill.

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

## Gate 0: recomendación de modelo

Antes de cargar contexto pesado o iniciar una fase, recomienda `BAJO`, `MEDIO` o
`ALTO`. Si la solicitud cumple claramente `direct`, usa los limites compactos de
esta skill y no cargues la referencia. En los demas casos usa
`references/model-selection.md`. No nombres modelos o proveedores ni cambies el
modelo del host.

`direct` recibe un aviso breve y no bloqueante. Quick Plan, `standard`, `deep` y
bugfix no trivial reciben una recomendación y un único hard stop. No repitas el
Gate 0 entre fases; si cambia el alcance o el riesgo, recalcula y detente solo si
cambia el nivel global.

## Contexto selectivo

Antes de consumir `.navigator/`, carga
`references/navigator-context.md`. Aplica su preflight y orden de fuentes en
exploración y en cada fase que necesite contexto nuevo. Navigator es auxiliar: su
ausencia o desfase no bloquea SDD y nunca autoriza escribir sus índices sin
aprobación explícita.

## Artefactos

Destino: `.sdd/specs/<ruta-spec>/`

`<ruta-spec>` admite uno o más segmentos. Conserva la ruta plana
`<nombre-feature>/` y permite agrupar por módulo, por ejemplo
`modo-invitado/android-contactos/`. La ruta relativa completa identifica la spec;
el nombre de la carpeta final por sí solo no es suficiente.

- La carpeta final es la raíz de la spec y contiene `requirements.md` o
  `bugfix.md`. Las carpetas intermedias solo agrupan y no son specs.
- Al crear sin ruta explícita, revisa las rutas de specs existentes. Si varias
  pertenecen claramente al mismo módulo, reutiliza `<módulo>/<nombre-feature>`;
  para specs aisladas conserva una ruta plana. No muevas specs existentes
  automáticamente ni añadas profundidad extra sin una necesidad real.
- Dentro de un módulo evita repetir su prefijo: usa
  `modo-invitado/android-contactos/`, no
  `modo-invitado/modo-invitado-android-contactos/`.
- Si el usuario proporciona una ruta, úsala exactamente tras comprobar que es
  relativa, no contiene `..` y permanece bajo `.sdd/specs/`.
- Para continuar sin ruta explícita, busca recursivamente `requirements.md` y
  `bugfix.md`. Si hay varias candidatas plausibles, muestra sus rutas relativas y
  pregunta; nunca elijas solo por el nombre de la carpeta final.

| Archivo | Fase | Contenido |
|---------|------|-----------|
| `requirements.md` (o `bugfix.md`) | 1 | Historias + criterios EARS |
| `design.md` | 2 | Arquitectura, modelos, diagramas, pruebas |
| `tasks.md` | 3 | Tareas discretas, trazadas y secuenciadas |
| `verification.md` | 4 | Matriz + evidencia + cierre |

## Flujo con gates

> **No avances de fase sin aprobación explícita del usuario.**
> Copilot no tiene una herramienta de «pregunta» dedicada.
> El gate se implementa de forma natural: termina tu turno
> con la pregunta y espera. Excepción: los gates de fase de Quick Plan; su Gate 0
> de modelo se conserva.

### Fase 1 — Requirements

1. Lee steering (`.github/copilot-instructions.md`, `AGENTS.md`, `.sdd/steering/*.md`). Si existe Navigator
   aplicable, ejecuta el preflight de `references/navigator-context.md` y usa solo
   la capa mínima antes del contexto de dominio.
2. Detecta dominio y lee solo su `README.md` de contexto (`.architecture/`,
   `.design/`, `.data/`, `.security/`, `.quality/`). Si falta, recomienda
   especialista; si el usuario continúa, captura lo imprescindible en `design.md`.
3. Descompón en historias de usuario.
4. Criterios en EARS:
   - `CUANDO <condición> EL SISTEMA DEBERÁ <comportamiento>`
   - `SI <error> ENTONCES EL SISTEMA DEBERÁ <manejo>`
   - `MIENTRAS <estado> EL SISTEMA DEBERÁ <comportamiento>`
   - `EL SISTEMA DEBERÁ <siempre activo>`
5. Cubre edge cases y errores; declara supuestos.
6. **GATE 1**: "¿Apruebas los requisitos o quieres iterarlos?"

### Fase 2 — Design

1. Repite el preflight de `references/navigator-context.md` si el alcance o sus
   artefactos cambiaron; usa índices no confiables solo como pistas verificadas.
2. Lee código existente y steering. Reutiliza `.architecture/`, `.design/`, `.data/` si aplica.
3. Carga `references/quality-bar.md`; el design debe satisfacerla (cita excepciones).
4. Arquitectura, componentes, modelos, errores, pruebas. Diagramas según caps del modo.
5. Elige y registra la estrategia adaptativa de pruebas y el PBT condicional según
   `references/testing.md`, incluidas las excepciones.
6. **GATE 2**: "¿Apruebas el diseño o quieres ajustarlo?"

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

Genera requirements, design y tasks en una pasada **sin gates de fase**, con
preguntas aclaratorias por adelantado. Omite Fase 4. Solo para features bien
entendidas; conserva el Gate 0 de modelo antes de empezar.
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
