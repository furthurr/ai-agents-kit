---
name: sdd-spec
description: >-
  Aplica la metodología Spec-Driven Development (SDD) estilo Kiro: genera y
  refina specs (requirements.md, design.md, tasks.md, verification.md) con modos
  proporcionales, gates de aprobación, notación EARS y trazabilidad. Úsala al
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

Flujo SDD proporcional con gates, EARS y trazabilidad. La calificación de feature
solo puede emitirla el agente `{{sdd_agent}}`; cargar esta skill desde otro agente
no autoriza a mostrarla.

> **Precedencia:** si el agente `{{sdd_agent}}` y esta skill divergen, manda esta skill.

## Modos de profundidad

| Modo | Cuándo | Qué produce | Carga documental |
|------|--------|-------------|-------------------|
| `direct` | Cambio trivial verificable | Sin spec 4 fases | Mínima |
| `lite` | Cambio acotado, claro y de bajo riesgo | Quick Plan; verificación compacta si implementa | Ligera |
| `standard` | **Default** | 4 fases, design corto, 0–5 invariantes, testing adaptativo | Moderada |

SDD reconoce exactamente tres profundidades: `direct`, `lite` y `standard`. Tipo de
trabajo (feature, bugfix o exploración), profundidad, intención
(solo planificación o implementación) y estrategia de pruebas son ejes separados.

`standard` es el fallback seguro. No existe una profundidad más pesada que debas
activar: no rebajes una solicitud explícita de `standard`. Sus límites son design
~≤250 líneas, máx. 5 invariantes y 1 flowchart + 1 sequence. Un glosario o un
diagrama adicional solo se añade si el requisito lo necesita o el usuario lo pide;
no crea una profundidad nueva.

`direct` exige alcance claro, localizado y reversible, sin contrato público,
migración, decisión arquitectónica, cruce de capas ni riesgo relevante de seguridad,
concurrencia o integridad.

Tras descartar `direct`, selecciona `lite` solo si el resultado está claro, no hay
decisiones funcionales relevantes abiertas, el alcance es acotado, reutiliza
patrones existentes, tiene verificación viable y es reversible sin migración
compleja. Excluye `lite` ante contrato público/API, migración, arquitectura,
integración externa significativa, cruce relevante de capas o módulos, seguridad,
privacidad, concurrencia, integridad crítica, compliance, legado riesgoso o bugfix
no trivial. Si la elegibilidad de `lite` no puede demostrarse, usa `standard`.

Quick Plan es obligatorio y exclusivo de `lite`. Rechaza `direct` + Quick Plan,
`standard` + Quick Plan; una petición de Quick Plan solicita evaluar `lite`, pero no
evita sus límites. Un bugfix trivial puede ser `direct`; los demás bugfixes usan
`standard`.

Profundidad y testing son ejes independientes: sin cambio observable → sin test
nuevo; bug o legado → regresión/caracterización; comportamiento nuevo o modificado
→ TDD focalizado. `direct` puede incluir un microciclo TDD, pero no significa «sin
pruebas». TDD estricto no es una estrategia disponible. Detalle en
`references/testing.md`.

## Opciones retiradas y specs históricas

`deep` y TDD estricto ya no forman parte del contrato operativo. No deben
seleccionarse ni presentarse como alternativas vigentes, incluso si el usuario los
solicita explícitamente.

- Si una solicitud nueva pide `deep`, informa que la profundidad se retiró, propone
  `standard` y espera aceptación antes de iniciar el flujo.
- Si una solicitud nueva pide TDD estricto, informa que la estrategia se retiró,
  propone TDD focalizado y espera aceptación antes de iniciar el flujo.
- Si una spec existente declara cualquiera de esas opciones, conserva sus
  artefactos, evidencias y decisiones históricas; solicita aceptación de la
  sustitución antes de modificarla o reanudarla.
- La aceptación de la alternativa solo autoriza la sustitución de la opción. No
  aprueba Requirements, Design, Tasks ni ningún gate pendiente.
- Si faltan o se contradicen los marcadores de modo, fase, estado o gate, pide
  aclaración y no infiere aprobación por la existencia de archivos.

## Preflight técnico y calificación de feature

Antes de contexto pesado, realiza un preflight técnico breve para identificar el
tipo de trabajo, la siguiente operación y decisiones esenciales pendientes. No
recomiendes ni menciones modelos/proveedores LLM, no califiques fases o tareas y no
conviertas el preflight en un gate de usuario. Continúa el trabajo autorizado en el
mismo turno; solo una decisión esencial o un gate real puede requerir respuesta.

La calificación es exclusiva del agente `{{sdd_agent}}`, no de la skill aislada ni
de especialistas que la consulten. Solo aplica a una feature cuyo alcance e impacto
en el proyecto ya fueron analizados y definidos. Consulta
`references/feature-level.md` para rúbrica, escala y emisión. Bugs, exploraciones y
consultas no reciben puntuación de feature por defecto.

Publica `Nivel de feature: <n> <emoji>` una sola vez después del análisis del
alcance deseado: en `direct` antes de editar; en `lite` al concluir Quick Plan; en
`standard` en el resumen de Requirements junto a Gate 1. Usa el entero real 1–10
con emoji correspondiente; nunca un ejemplo fijo, nivel de tarea/fase o
recomendación de modelo. No pauses para pedir aprobación de la calificación ni la
repitas al cambiar de fase. Si cambia materialmente el alcance, analiza el nuevo
alcance antes de actualizarla.

La línea visible usa el valor calculado (p. ej. nivel 7 → `Nivel de feature: 7 🟢`);
los ejemplos de esta explicación no son puntuaciones prefijadas.

La calificación no sustituye ni determina profundidad SDD, testing, selección de
ejecutor, gates o permisos. En transiciones `standard`, presenta el resumen
verificable y gate actual; espera únicamente aprobación del gate SDD real. Tras
Implementación continúa con Verification sin gate intermedio. Después de
Verification muestra únicamente Gate 4.

## Contexto selectivo

Antes de consumir `.navigator/`, carga
`references/navigator-context.md`. Aplica su preflight y orden de fuentes en
exploración y en cada fase que necesite contexto nuevo. Navigator es auxiliar: su
ausencia o desfase no bloquea SDD y nunca autoriza escribir sus índices sin
aprobación explícita.

## Recomendación de agente por dominio

Resuelve la decisión de ejecutor antes de la primera modificación: no uses
herramientas de escritura ni comandos que modifiquen archivos mientras falte una
elección esencial entre especialista y SDD. Cargar esta skill y, ante UI/datos,
leer `references/agent-routing.md` precede a esa escritura; no basta con descubrir
la skill en el catálogo. Abrir SDD no es una decisión de rechazar al especialista.
La lista v1 es cerrada a `ui-design` y `data-api`; no enumeres otros agentes como
alternativas; no enumeres ni recomiendes otros agentes. Si el usuario elige
explícitamente un especialista, entrega el contexto manual y detente en SDD; la
elección de especialista significa que esa actividad no se ejecuta en SDD, aunque
la petición original incluyera «implementa».

Antes de editar o ejecutar una actividad, evalúa si corresponde íntegramente a
`ui-design` o `data-api`. Carga `references/agent-routing.md` bajo demanda para
criterios, precedencias y contexto copiable. Ofrece selección manual o continuidad
con SDD; no cambies de agente automáticamente ni invoques subagentes. La elección
explícita compatible evita una pregunta redundante. Conserva planificación SDD
ante ambigüedad, riesgo o cruce de dominios, sin cambiar profundidad, testing ni gates.

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

En `standard`, los artefactos nuevos declaran `Modo SDD`, `Fase`, `Estado` y
el gate pendiente o aprobado que les corresponde. La reanudación usa esos marcadores
y no infiere aprobación solo por la existencia del archivo. En `lite`, Quick Plan
genera los tres primeros archivos en una pasada y añade `verification.md` compacto
solo después de implementar; `requirements.md` declara `Modo SDD: lite`. Las specs
legacy no se migran; si una spec de tres archivos sin marcador es ambigua, pregunta
antes de reanudarla.

## Flujo con gates

> **En `standard`, no avances de fase sin aprobación explícita del usuario.**
> {{gate_instruction}}La calificación de feature no es un gate ni requiere aprobación
> separada. El preflight técnico no recomienda modelos ni añade pausas. En las
> transiciones, espera solo la aprobación del gate SDD real. `lite` usa Quick Plan
> sin Gates 1–3 y cierra sin Gate 4.

### Fase 1 — Requirements

1. Lee steering ({{steering_paths}}, `.sdd/steering/*.md`). Si existe Navigator
   aplicable, ejecuta el preflight de `references/navigator-context.md` y usa solo
   la capa mínima antes del contexto de dominio.
2. Detecta dominio y lee solo su `README.md` de contexto (`.architecture/`,
   `.design/`, `.data/`, `.security/`, `.quality/`). La ausencia de contexto no obliga
   a cambiar de agente: aplica `references/agent-routing.md` si corresponde, respeta
   la elección previa y, si el usuario continúa, captura lo imprescindible en `design.md`.
3. Analiza el impacto en el proyecto y el alcance deseado; si es una feature y el
   alcance quedó definido, el agente SDD registra/muestra la calificación única
   antes de presentar Gate 1. No la muestres si persiste una decisión esencial.
4. Descompón en historias de usuario.
5. Criterios en EARS:
   - `CUANDO <condición> EL SISTEMA DEBERÁ <comportamiento>`
   - `SI <error> ENTONCES EL SISTEMA DEBERÁ <manejo>`
   - `MIENTRAS <estado> EL SISTEMA DEBERÁ <comportamiento>`
   - `EL SISTEMA DEBERÁ <siempre activo>`
6. Cubre edge cases y errores; declara supuestos.
7. **GATE 1**: "¿Apruebas los requisitos o quieres iterarlos?"

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
3. Para TDD focalizado, cada tarea de comportamiento explicita el orden
   interno RED → GREEN → REFACTOR, sin crear tareas ceremoniales por cada paso.
4. Incluye grafo de waves. Consulta `references/templates.md` para formato.
5. **GATE 3**: "¿Apruebas el plan y empiezo a implementar?"

### Implementación

- Para una tarea especializada acotada, aplica `references/agent-routing.md` antes
  de ejecutarla: conserva vínculo a requisitos/tareas, autorización y gates pendientes.
  La selección de ejecutor no aprueba gates ni amplía alcance.
- Una tarea a la vez o en waves. Estados: `[ ]` → 🔵 → `[x]`.
- No emitas niveles por tarea/fase ni recomendaciones de modelo durante Implementación.
- Antes de `[x]`: `references/integrity-gate.md`.
- Ejecuta el ciclo elegido en `references/testing.md`; no declares TDD sin haber
  observado un RED que falle por la razón esperada.
- Waves UI/datos: revisar `references/quality-bar.md`.
- Si existe carpeta canónica del dominio y creas algo reutilizable, documéntalo con la skill del especialista.

### Fase 4 — Verificación y cierre

Prerrequisito: `[x]` con artefacto real (o `[omitido: razón]`).
1. Presenta el resumen de Implementación y continúa con Verification sin pausa por
   modelo; no emitas nivel de tarea/fase. Conserva los controles de integridad.
2. `references/integrity-gate.md`: validar cada `[x]` ↔ disco/evidencia.
3. Suite de tests + spot-check `quality-bar` y 3–5 RNF del spec.
4. `verification.md` con columna Evidencia (`templates.md`). No cerrar con huérfanos.
5. **GATE 4**: "¿Cierro la spec o cubrimos los huecos?" Después de Verification,
   no repitas la calificación de feature.

## Variante Bugfix

`bugfix.md` con tres bloques EARS:
- Actual: `CUANDO <...> EL SISTEMA <incorrecto>`
- Esperado: `CUANDO <...> EL SISTEMA DEBERÁ <correcto>`
- Inalterado: `EL SISTEMA DEBERÁ SEGUIR <...>`

Usa el flujo y gates normales, salvo bug trivial `direct`. Diseño con causa raíz +
invariantes si aplican. Primero crea una regresión que falle por el defecto; usa
caracterización para comportamiento legado que deba preservarse. Si no puede
reproducirse, registra la limitación y no inventes un RED.

## Modo lite y Quick Plan

Quick Plan es obligatorio y exclusivo de `lite`. Genera requirements, design y
tasks en una pasada, con preguntas aclaratorias esenciales por adelantado y sin
Gates 1–3. El preflight técnico identifica `Modo SDD: lite` y Quick Plan, sin
recomendar modelos ni pausar. Al concluir el análisis y definir el alcance deseado,
el agente SDD publica la calificación única de la feature en el resumen de Quick Plan.

Si la intención es solo planificación, termina después de `tasks.md` y no
implementar código. Si la solicitud original incluye implementación, aplica
integrity-gate y testing adaptativo después del plan. Al terminar, crea un
`verification.md` compacto con RED o baseline, GREEN, suite, excepciones y matriz
de evidencia; cierra sin Gate 4.

Si aparece una exclusión, detente en un punto seguro y propón `standard`. La
reclasificación requiere aprobación por el cambio de flujo. Quick Plan no es
compatible con `direct` ni `standard`.

## Reglas de calidad

- **Proporcionalidad:** aplica los criterios verificables de `direct`; no confundas
  cambio pequeño con riesgo bajo.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Implementación → `design.md`, no `requirements.md`.
- Cada requisito ≥1 tarea. Respeta steering. Sin cumplimiento inventado.
- Consulta `references/ears-reference.md` para patrones EARS.
