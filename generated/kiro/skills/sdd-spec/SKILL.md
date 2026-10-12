---
name: sdd-spec
description: >-
  Aplica Spec-Driven Development (SDD) proporcional: direct, SDD-Tiny con un spec.md,
  SDD-Lite con Quick Plan o standard legacy opt-in. Úsala para planificar o implementar
  features y bugfixes con aceptación, gates vigentes, pruebas y evidencia; no para
  explicar arquitectura sin diseñar una feature.
---

# Skill: SDD Spec

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Flujo SDD proporcional con gates, EARS y trazabilidad. La calificación de feature
solo puede emitirla el agente `sdd`; cargar esta skill desde otro agente
no autoriza a mostrarla.

> **Precedencia:** si el agente `sdd` y esta skill divergen, manda esta skill.

## Modos de profundidad

| Modo técnico | Nombre visible | Cuándo | Qué produce |
|--------------|---------------|--------|-------------|
| `direct` | Direct | Cambio trivial verificable y elegible | Sin spec formal |
| `tiny` | SDD-Tiny | Feature acotada; recomendación base para nota 4–8 | Un `spec.md` breve y vivo |
| `lite` | SDD-Lite | Alcance verificable; recomendación base para nota 9–10/10+ | Quick Plan; verificación compacta si implementa |
| `standard` | Standard (legacy) | Solo ante solicitud explícita | 4 fases y Gates 1–4 |

Se conservan cuatro modos documentados: `direct`, `tiny`, `lite` y `standard`.
La recomendación automática se limita a Direct, SDD-Tiny y SDD-Lite; `standard`
queda deprecado/legacy y se activa únicamente cuando el usuario lo solicita
explícitamente. La complejidad, una nota alta o el uso de un LLM local no activan
`standard` por inferencia. SDD-Tiny solo se recomienda si el alcance cabe en una
entrega cohesiva, sus garantías se pueden probar con mecanismos adecuados y el flujo
conserva sus gates; el score por sí solo no demuestra elegibilidad. `lite` conserva
Quick Plan y sus reglas vigentes.
Tipo de trabajo (feature, bugfix o exploración), profundidad, intención
(solo planificación o implementación) y estrategia de pruebas son ejes separados.

Si el usuario solicita explícitamente `standard`, conserva esa elección y aplica
su flujo legacy, sin rebajarlo automáticamente. Sus límites son design ~≤250 líneas,
máx. 5 invariantes y 1 flowchart + 1 sequence. Un glosario o un diagrama adicional
solo se añade si el requisito lo necesita o el usuario lo pide; no crea una
profundidad nueva.

`direct` exige alcance claro, localizado y reversible, sin contrato público,
migración, decisión arquitectónica, cruce de capas ni riesgo relevante de seguridad,
concurrencia o integridad.

Recomienda profundidad después de definir alcance e impacto: 1–3 `direct`, 4–8
`tiny` (SDD-Tiny), 9–10 y 10+ `lite` (SDD-Lite), siempre como recomendación y no
selección automática. Para 10+ ofrece entregas seguras conforme a
`references/scope-depth.md`. No rebajes la nota para forzar `direct`; si el cambio
no cumple sus guardas, explica el conflicto y aplica el manejo seguro vigente.
Concurrencia/persistencia/integridad acotadas requieren mecanismos adecuados y
pruebas reales, no solo una advertencia. Los bugfixes no triviales conservan `lite`;
bugs, consultas y exploraciones no reciben calificación de feature.

Quick Plan es obligatorio y exclusivo de `lite` (SDD-Lite). Rechaza `direct` + Quick
Plan, `tiny` + Quick Plan y `standard` + Quick Plan; una petición de Quick Plan pide
evaluar SDD-Lite, pero no evita sus límites ni invalida una elección explícita previa.
Si Quick Plan contradice un modo elegido explícitamente, explica la incompatibilidad
y pide resolver esa elección; no cambies el modo en silencio.
Un bugfix trivial puede ser `direct`; los demás conservan el flujo bugfix con `lite`,
salvo que el usuario elija explícitamente otro modo elegible. `standard` solo se
activa por solicitud explícita.

Profundidad y testing son ejes independientes: sin cambio observable → sin test
nuevo; bug o legado → regresión/caracterización; comportamiento nuevo o modificado
→ TDD focalizado. `direct` puede incluir un microciclo TDD, pero no significa «sin
pruebas». TDD estricto no es una estrategia disponible. Detalle en
`references/testing.md`.

## Opciones retiradas y specs históricas

`deep` no está disponible: informa que fue retirado y pide elegir `direct`, SDD-Tiny
(`tiny`) o SDD-Lite (`lite`), o solicitar explícitamente `standard` legacy; no
conviertas la solicitud en `standard` silenciosamente. En una spec histórica conserva artefactos/evidencia y aclara el modo
antes de reanudarla si la elección no está vigente. TDD estricto se trata en
`references/testing.md`.
Aceptar la sustitución no aprueba gates. Si los marcadores de modo/fase/estado/gate
faltan o se contradicen, aclara antes de continuar; no infieras aprobación por archivos.

## Preflight técnico y calificación de feature

Antes de contexto pesado, realiza un preflight técnico breve para identificar el
tipo de trabajo, la siguiente operación y decisiones esenciales pendientes. No
recomiendes ni menciones modelos/proveedores LLM, no califiques fases o tareas y no
conviertas el preflight en un gate de usuario. Continúa el trabajo autorizado en el
mismo turno; solo una decisión esencial o un gate real puede requerir respuesta.

Solo el agente `sdd` califica features de alcance definido; cargar esta
skill desde otro agente no autoriza la emisión. Consulta
`references/feature-level.md`, fuente única de la rúbrica. Bugs, exploraciones y
consultas no reciben nota por defecto.

Publica `Esfuerzo previsto del LLM: <nota e icono>` al terminar alcance e impacto,
antes de recomendar profundidad. Referente, factores y supuestos quedan en la spec,
no en mensajes rutinarios. Separa nota y atención según la rúbrica; `10+` conserva
nota 10 más `exceeds_x13=true`, nunca nota 11. No califiques bugs, consultas ni
exploraciones. No muestra notas provisionales, no repite ni pausa ni pide aprobación
de la nota; reanaliza cambios materiales. La recomendación no selecciona un modo
contra una elección explícita, no aprueba alcance ni gates y no crea otro gate. No
cambia testing, ejecutor, permisos o modelo.

## Definición de alcance y criterios de aceptación

Antes de elegir profundidad, define objetivo, resultados, exclusiones, criterios,
errores y supuestos. Preguntas esenciales sin repetir información; consulta
contexto técnico mínimo. Esta etapa común no crea un documento obligatorio ni
aprueba Gate 1.
Usa EARS donde lo exija el modo; Tiny conserva comportamientos y aceptación
verificables sin exigir una matriz EARS.
Antes de recomendar, busca specs relacionadas localmente; carga
`references/spec-continuity.md` solo ante relación o ambigüedad relevante.
Aplica `references/scope-depth.md`: presenta alcance, califica features y recomienda modo;
valida alcance completo y elección explícita antes de artefactos/código;
respeta la previa compatible. Solo planificación nunca implementa.

## Contexto selectivo

Carga únicamente la referencia necesaria para la decisión/fase actual. Lee el
fragmento pertinente y reutilízalo durante la tarea; no vuelvas a cargar el mismo
archivo en cada fase si alcance y fuente no cambiaron. No cargues todas las
referencias por defecto.

Antes de consumir `.navigator/`, carga
`references/navigator-context.md`. Aplica su preflight y orden de fuentes en
exploración y en cada fase que necesite contexto nuevo. Navigator es auxiliar: su
ausencia o desfase no bloquea SDD y nunca autoriza escribir sus índices sin
aprobación explícita.

## Selección explícita de metodología

El usuario activa esta metodología al seleccionar el agente `sdd`. No vuelvas a
clasificar el agente ejecutor por dominio; SDD no deriva automáticamente a `developer`.
Mantén planificación e implementación bajo los gates SDD, incluso si la tarea toca
UI, datos/APIs, negocio o varias capas. Carga `data-api` y/o `ui-design` bajo demanda
como referencias técnicas; esas skills no alteran intención, gates ni ownership de
la ejecución. Si el usuario pide cambiar de agente, conserva decisiones y estado,
prepara un resumen portable y detén la actividad actual hasta que elija cómo seguir.
Consulta `references/agent-routing.md` solo cuando se solicite ese cambio; no crea
un flujo de delegación automática.

## Artefactos

Destino: `.sdd/specs/<ruta-spec>/`

`<ruta-spec>` admite uno o más segmentos. Conserva la ruta plana
`<nombre-feature>/` y permite agrupar por módulo, por ejemplo
`modo-invitado/android-contactos/`. La ruta relativa completa identifica la spec;
el nombre de la carpeta final por sí solo no es suficiente.

- La carpeta final es la raíz de la spec y contiene `requirements.md` o
  `bugfix.md`, o `spec.md` en SDD-Tiny. Las carpetas intermedias solo agrupan y no
  son specs.
- Al crear sin ruta explícita, revisa las rutas de specs existentes. Si varias
  pertenecen claramente al mismo módulo, reutiliza `<módulo>/<nombre-feature>`;
  para specs aisladas conserva una ruta plana. No muevas specs existentes
  automáticamente ni añadas profundidad extra sin una necesidad real.
- Dentro de un módulo evita repetir su prefijo: usa
  `modo-invitado/android-contactos/`, no
  `modo-invitado/modo-invitado-android-contactos/`.
- Si el usuario proporciona una ruta, úsala exactamente tras comprobar que es
  relativa, no contiene `..` y permanece bajo `.sdd/specs/`.
- Para continuar sin ruta explícita, busca recursivamente `requirements.md`,
  `bugfix.md` y `spec.md`. Si hay varias candidatas plausibles, muestra sus rutas
  relativas y pregunta; nunca elijas solo por el nombre de la carpeta final.

| Archivo | Modo | Contenido |
|---------|------|-----------|
| `spec.md` | `tiny` | Documento único inicial/final: alcance, enfoque/pruebas, checklist, verificación/cierre |
| `requirements.md` (o `bugfix.md`) | `lite` / `standard` | Historias + criterios EARS |
| `design.md` | `lite` / `standard` | Arquitectura, modelos, pruebas y diagramas cuando correspondan |
| `tasks.md` | `lite` / `standard` | Quick Plan (`lite`) o tareas trazadas (`standard`) |
| `verification.md` | `lite` implementado / `standard` | Evidencia compacta (`lite`) o matriz y cierre (`standard`) |

En `standard` legacy, usado solo por solicitud explícita, los artefactos nuevos
declaran `Modo SDD`, `Fase`, `Estado` y el gate pendiente o aprobado que les
corresponde. La reanudación usa esos marcadores y no infiere aprobación solo por la
existencia del archivo. En `lite`, Quick Plan genera los tres primeros archivos en
una pasada y añade `verification.md` compacto solo después de implementar;
`requirements.md` declara `Modo SDD: lite`. En `tiny`, `spec.md` declara `Modo SDD:
tiny`, se crea antes de cambiar código y se actualiza en el mismo path al cerrar; no
se crean los otros archivos. Las specs legacy no se migran; si una spec sin marcador
es ambigua, pregunta antes de reanudarla.

## Flujo con gates

> **En `standard` legacy, solicitado explícitamente, no avances de fase sin aprobación explícita del usuario.**
> La calificación de feature no es un gate ni requiere aprobación
> separada. El preflight técnico no recomienda modelos ni añade pausas. En las
> transiciones, espera solo la aprobación del gate SDD real. `lite` usa Quick Plan
> sin Gates 1–3 y cierra sin Gate 4. `tiny` conserva Gate 3 antes de implementar
> y Gate 4 tras documentar la verificación; la recomendación de score no añade otro
> gate. `standard` conserva sus cuatro gates.

### Fase 1 — Requirements

1. Lee steering (`.kiro/steering/*.md`, `AGENTS.md`, `.sdd/steering/*.md`). Si existe Navigator
   aplicable, ejecuta el preflight de `references/navigator-context.md` y usa solo
   la capa mínima antes del contexto de dominio.
2. Detecta dominio y lee solo su `README.md` de contexto (`.architecture/`,
   `.design/`, `.data/`, `.security/`, `.quality/`). La ausencia de contexto no obliga
   a cambiar de agente: usa fuentes directas, respeta la selección SDD y captura en
   `design.md` lo imprescindible para las decisiones aprobadas.
3. Reutiliza el alcance y los criterios acordados; registra la calificación ya
   emitida si aplica y la profundidad elegida, sin repetirla ni inferir Gate 1 aprobado.
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
4. Incluye grafo de waves. Consulta solo la sección `tasks.md` de `references/templates.md`.
5. **GATE 3**: "¿Apruebas el plan y empiezo a implementar?"

### Implementación

- Mantén la ejecución dentro de SDD y conserva vínculo a requisitos/tareas,
  autorización y gates pendientes. Carga skills de dominio bajo demanda cuando
  aporten estándares técnicos para el trabajo.
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
4. Usa la sección `verification.md` de `templates.md` y la matriz de evidencia. No cerrar con huérfanos.
5. **GATE 4**: "¿Cierro la spec o cubrimos los huecos?" Después de Verification,
   no repitas la calificación de feature.

## Variante Bugfix

`bugfix.md` con tres bloques EARS:
- Actual: `CUANDO <...> EL SISTEMA <incorrecto>`
- Esperado: `CUANDO <...> EL SISTEMA DEBERÁ <correcto>`
- Inalterado: `EL SISTEMA DEBERÁ SEGUIR <...>`

Usa regresión y causa raíz; elige `direct` solo si el bug es trivial, o `lite` para
bugfix no trivial según la política vigente. No puntúes bugs como features. Tiny no
se recomienda a bugs por score; solo aplícalo si el usuario lo elige explícitamente
y el bug queda cubierto por su spec breve y gates. `standard` solo si el usuario lo
solicita explícitamente. Primero crea una regresión que falle por el defecto; usa
caracterización para comportamiento legado que deba preservarse. Si no puede
reproducirse, registra la limitación y no inventes un RED.

## Modo tiny (SDD-Tiny)

Al seleccionar `tiny`, carga `references/tiny.md`. Tras validar alcance y elección,
crea un solo `.sdd/specs/<ruta-spec>/spec.md` con las cuatro secciones breves de la
plantilla. Escribe el estado inicial antes de cambiar código y actualiza ese mismo
documento tras implementar. Registra alcance, comportamientos, criterios, errores e
invariantes; enfoque y pruebas proporcionales; checklist; y comandos, resultados
realmente observados y cierre. Conserva fallos locales y reparaciones en el registro
de verificación. No exijas Quick Plan, cuatro documentos, EARS completa ni una matriz
completa de trazabilidad. Tiny no significa sin pruebas.

Si la intención incluye implementación, Gate 3 aprueba el spec/plan breve antes de
escribir código; tras verificar, Gate 4 decide cierre o huecos. Si es solo
planificación, deja estado `Planificado`, no implementes y no simules verificación.
Aplica integrity-gate, la estrategia de `testing.md`, permisos efectivos y el
quality-bar proporcional. La creación o recomendación de Tiny no aprueba esos gates.

## Modo lite (SDD-Lite) y Quick Plan

Quick Plan es obligatorio y exclusivo de `lite` (nombre visible SDD-Lite). Con
alcance validado y selección resuelta, genera requirements, design y tasks en una pasada,
sin Gates 1–3. Reutiliza criterios acordados y registra la nota sin volver a
publicarla. El preflight técnico no recomienda modelos ni pausa por modelo.

Si la intención es solo planificación, termina después de `tasks.md` y no
implementar código. Si la solicitud original incluye implementación, aplica
integrity-gate y testing adaptativo después del plan. Al terminar, crea un
`verification.md` compacto con RED o baseline, GREEN, suite, excepciones y matriz
de evidencia; cierra sin Gate 4.

Si aparece una exclusión, detente en un punto seguro; no cambies automáticamente a
`tiny` o `standard`. Explica cómo reducir/dividir el alcance o elegir Tiny solo si es
seguro; continúa con `standard` únicamente si el usuario lo solicita explícitamente.
Quick Plan no es compatible con `direct`, `tiny` ni `standard`.

## Modo direct

Con alcance validado y selección resuelta, ejecuta solo lo autorizado, con el
cambio mínimo correcto y testing adaptativo. Solo usa `direct` si el cambio es
pequeño, claro, localizado y reversible, sin contrato público, migración, decisión
arquitectónica, cruce de capas ni riesgo relevante de seguridad, concurrencia o
integridad. Una nota 1–3 no omite estas guardas. Si el alcance no es elegible,
explica el conflicto sin alterar la nota y aplica el manejo seguro de
`references/scope-depth.md`. No crea archivos formales de spec ni Quick Plan.
Presenta cambios, evidencia real y límites en un cierre breve;
actualiza documentación existente solo si el cambio o steering lo exige.
Si deja de ser trivial, detente y solicita reclasificación antes de ampliar el flujo.

## Reglas de calidad

- **Proporcionalidad:** aplica los criterios verificables de `direct`; no confundas
  cambio pequeño con riesgo bajo.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Lite/Standard: implementación y diseño → `design.md`, no `requirements.md`; Tiny
  registra el enfoque técnico en `spec.md`.
- En Lite/Standard, cada requisito ≥1 tarea; en Tiny la checklist conserva vínculos
  verificables sin exigir una matriz completa. Respeta steering. Sin cumplimiento inventado.
- Los patrones EARS mínimos ya están en esta skill; abre `ears-reference.md` solo si hace falta una forma no cubierta.
