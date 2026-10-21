# Agente SDD — Spec-Driven Development

## Resumen

| Campo | Información |
|---|---|
| ID | `sdd` |
| Skill | [`sdd-spec`](../../canonical/skills/sdd-spec/SKILL.md) |
| Propósito | Convertir features y bugfixes en trabajo trazable antes de implementarlos |
| Artefactos | `.sdd/specs/<ruta-spec>/`, plana o agrupada por módulo |
| Particularidad | Puede implementar código de producto según la profundidad y sus confirmaciones |

SDD separa el **qué y porqué** del **cómo** y deja decisiones trazables.

## Cuándo usarlo

- Para una feature nueva o un cambio de comportamiento.
- Para un bugfix que necesita regresión y causa raíz.
- Para una decisión con impacto entre capas.
- Para planificar una feature con un único spec breve mediante SDD-Tiny o Quick Plan
  mediante SDD-Lite.
- Para continuar la implementación de tareas ya aprobadas.

Primero define y presenta el alcance funcional completo, consulta contexto técnico
mínimo y califica features. Recomienda profundidad y espera validación del alcance
y elección pendientes en una interacción; reutiliza decisiones vigentes.
Para features de alcance definido, recomienda 1–3 `direct`, 4–8 SDD-Tiny (`tiny`) y
9–10/10+ SDD-Lite (`lite`). La nota no basta: se comprueba elegibilidad y no
selecciona un modo contra una elección explícita. `direct` mantiene todas sus guardas;
una nota baja no las elimina. SDD-Tiny usa un único `spec.md` breve, Gate 3 antes de
implementar y Gate 4 al cerrar, con pruebas proporcionales. SDD-Lite conserva Quick
Plan obligatorio y su verificación compacta. Para 10+ recomienda SDD-Lite y ofrece
entregas seguras. `standard` queda deprecado/legacy y solo se usa si el usuario lo
solicita explícitamente; no es fallback ante alcance amplio ni riesgo. No existe una
profundidad `deep`; pide elegir Direct, SDD-Tiny, SDD-Lite o solicitar `standard`
legacy, sin conversión silenciosa.

## Esfuerzo previsto del LLM

Al terminar alcance e impacto, antes de recomendar profundidad, SDD publica una
sola vez `Esfuerzo previsto del LLM: <nota e icono>`. Referente, factores y supuestos
se registran en la spec, no en mensajes rutinarios. La
[rúbrica ReserveLab](../../canonical/skills/sdd-spec/references/feature-level.md)
define anclas, reutilización y `10+`. La nota orienta la recomendación, pero no
demuestra elegibilidad. No puntúa antes de entender el alcance ni repite la nota en Requirements,
Design, Tasks, Implementación o Verification. No es una recomendación de modelo,
no identifica ni selecciona un LLM y nunca pausa el flujo por modelo. Si el alcance
cambia de forma sustancial, primero vuelve a analizarlo y actualiza la clasificación;
las decisiones y aprobaciones propias del flujo siguen siendo independientes.

Antes de calificar debe quedar visible el alcance completo, también para 10/10+:
objetivo/resultado, todos los comportamientos, reglas/condiciones, criterios de
aceptación, errores/estados/casos límite, exclusiones, restricciones y supuestos.
Distinguir confirmado de supuesto; no omitir detalles por brevedad ni inventar
requisitos. Esperar validación explícita antes de artefactos o implementación.
Solo elegir modo/ejecutor no valida el alcance. Ajustes requieren presentar todo
el conjunto actualizado y volver a validar. Reutilizar únicamente aprobación
explícita vigente de la misma versión completa, no un resumen breve previo.

Esfuerzo y atención son distintos: 1–7 normalmente 🟢, pero pueden mostrar 🟠
con una complicación concreta; 8–9 🟠, 10/10+ 🔴. Una reserva de nivel 6 puede
usar SDD-Tiny con atención especial si hay garantía definida, mecanismo adecuado,
pruebas concurrentes viables y recuperación acotada. Naranja no reemplaza controles.

Ejemplo ilustrativo, después de acordar estas condiciones:

> **Alcance definido**
>
> **Objetivo:** reservar unidades disponibles y recuperarlas al cancelar, sin sobreventa.
>
> **Comportamientos y reglas:**
> - Reservar una unidad solo si está disponible; una reserva confirmada reduce la disponibilidad en uno.
> - Cancelar una reserva activa devuelve una unidad y pasa la reserva a cancelada.
> - Repetir la cancelación no devuelve otra unidad ni cambia la disponibilidad.
>
> **Criterios de aceptación:**
> - Con una unidad disponible y dos reservas simultáneas, solo una se confirma y la disponibilidad termina en cero.
> - Al cancelar una reserva activa, su estado queda cancelado y la disponibilidad aumenta en uno.
> - Al repetir esa cancelación, la disponibilidad permanece igual.
> - Sin unidades disponibles o con reserva inexistente al cancelar, se informa el error sin modificar reservas ni disponibilidad.
>
> **Errores y estados:** reserva activa/cancelada; sin disponibilidad y reserva inexistente son errores explícitos sin cambios parciales.
>
> **Exclusiones:** vencimiento automático y funcionamiento offline.
>
> **Restricciones:** conservar los contratos existentes del catálogo y las reservas.
>
> **Contexto confirmado:** catálogo y reservas ya existen. No hay supuestos funcionales pendientes en este ejemplo.
>
> **Esfuerzo previsto del LLM: 6 🟠**
>
> **Atención especial:** reservas simultáneas; se verificarán con pruebas específicas.
>
> **Profundidad recomendada: SDD-Tiny.**
>
> ¿Este alcance refleja completamente lo que quieres y continuamos con SDD-Tiny, o necesitas corregir, agregar o eliminar algo? También puedes elegir otra profundidad elegible o solicitar explícitamente el modo legacy `standard`.

## Definición de alcance y entregas

La etapa común exige validar el contenido completo, sin imponer archivo propio
ni un gate numerado nuevo. Combina validación y elección cuando faltan ambas;
si el usuario responde solo «usa SDD-Tiny», queda validación pendiente. Consultas
informativas sin artefactos ni código no adquieren otra aprobación ceremonial.
Mantiene rigor testable y reutiliza lo definido en los artefactos del modo elegido.
Validar alcance o solicitar `standard` legacy no aprueba su Gate 1 formal. SDD-Tiny
usa Gate 3/4 en la implementación/cierre; SDD-Lite conserva Quick Plan en una pasada
sin otra pausa de requirements; direct no genera spec formal.

Para 10/10+ ofrece dividir en entregas seguras. Abordar el conjunto en `standard`
requiere solicitud explícita del usuario. Cada entrega debe tener
resultado verificable, dependencias y garantías transversales explícitas; se califica
individualmente y puede seguir en 10/10+. Si otra separación no es segura, detenerse
y explicar la opción de `standard` legacy, sin seleccionarlo automáticamente. No
prometer que todo será SDD-Lite ni cerrar el conjunto sin pruebas integradas.
Política: [alcance y profundidad](../../canonical/skills/sdd-spec/references/scope-depth.md).

## Continuidad de specs y contexto selectivo

Antes de recomendar profundidad para una modificación, SDD comprueba specs
relacionadas mediante búsqueda localizada: ruta indicada/spec activa primero,
después candidatas por módulo y comportamiento si hace falta. No audita toda `.sdd`
ni afirma ausencia global por una búsqueda limitada. La política detallada de
[continuidad](../../canonical/skills/sdd-spec/references/spec-continuity.md) se carga
solo ante relación o ambigüedad relevante.

| Situación | Tratamiento |
|---|---|
| Implementar una tarea ya especificada | Conservar modo, autorización y gates pendientes. |
| Ajuste trivial que conserva requisitos | Direct evaluable si no evita una tarea/gate; vínculo y evidencia breve. |
| Cambio de requisito, incluso con nota 2 | Mostrar actual/propuesto, mantener modo y revisar dependencias/aprobaciones afectadas. |
| Spec cerrada | Proponer revisión o spec vinculada conservando historia del cierre. |
| Evidencia de comportamiento anterior | Conservar como histórica y marcar solo lo afectado para revalidación. |
| Código y spec contradictorios | Determinar bug, documentación obsoleta o cambio funcional; aclarar si la autoridad no es evidente. |

Enmiendas mantienen IDs del mismo requisito y señalan adiciones/sustituciones.
En una spec `standard` legacy ya solicitada se revisan los gates afectados; elegir direct no permite evitarlos. En lite
se actualiza Quick Plan autorizado sin crear gates nuevos. No desmarcar todas las
tareas ni considerar un archivo presente como evidencia del requisito modificado.

Las elecciones de modo/ejecutor valen para el alcance aceptado, no para toda la
sesión. Cambios pequeños relacionados se evalúan en conjunto, sin sumar notas.
Reutilizar contexto si fuentes/alcance siguen vigentes; revalidar cuando cambien.
Leer cabecera/requisitos y ampliar según impacto, sin cargar todos los artefactos.
Las pruebas miden palabras/caracteres de instrucciones fijas y presupuestos,
no tokens reales ni ahorro porcentual; código/specs y número de candidatas son variables.

## Selección explícita de metodología

La metodología se activa al seleccionar el agente SDD. SDD mantiene la planificación
y la implementación de solicitudes visuales, de datos/APIs, negocio o multicapa bajo
sus propios gates; no hace routing automático a Developer ni a agentes retirados.
Puede cargar `data-api` y `ui-design` bajo demanda como referencias técnicas sin
cambiar el ejecutor.

Developer tiene un flujo independiente, con modo PLAN conversacional y sin creación
de specs. Para usar SDD, selecciona explícitamente el agente y acepta sus gates; para
implementar sin esa metodología, selecciona Developer. Un cambio de agente que pida
el usuario conserva la evidencia y decisiones, pero no transfiere autorización ni
marca tareas como completadas.

Contrato: [selección de metodología](../../canonical/skills/sdd-spec/references/agent-routing.md).

## Modos

| Modo | Uso | Resultado |
|---|---|---|
| `direct` | Recomendación 1–3; solo si es trivial, localizado y reversible | Sin spec; pruebas/checks y evidencia breve |
| SDD-Tiny (`tiny`) | Recomendación 4–8 si es una entrega cohesiva y verificable | Un `spec.md` vivo; Gate 3 antes de implementar y Gate 4 al cerrar |
| SDD-Lite (`lite`) | Recomendación 9–10/10+; alcance acotado y garantías verificables | Quick Plan compacto; artefactos según intención |
| `standard` (legacy) | Solo ante solicitud explícita del usuario | Requirements, design, tasks y verification; Gates 1-4 |

`standard` está deprecado/legacy y nunca se recomienda ni activa automáticamente.
Se conserva una elección explícita previa compatible. Quick Plan es obligatorio y
exclusivo de SDD-Lite; combinarlo con Direct, SDD-Tiny o Standard es inválido.

La profundidad y la verificación son decisiones independientes. Una feature normal
usa pruebas o checks focalizados en sus criterios y riesgos, sin imponer que los
tests se escriban antes del código. Los bugfixes usan regresión y el legado usa
caracterización. Se conservan comandos, resultados y limitaciones reales.

`deep` puede aparecer en specs históricas, pero no es una opción vigente.
SDD conserva esos artefactos y evidencias; para `deep`, pide elegir
Direct/SDD-Tiny/SDD-Lite o solicitar explícitamente `standard` legacy. No convierte la
solicitud silenciosamente ni confunde la elección de modo con la aprobación de un gate.

## Flujo y gates

0. **Alcance y elección:** presentar contenido completo, revisar contexto mínimo,
   calificar features y recomendar profundidad. Resolver validación y elección pendientes.
   `direct` ejecuta lo autorizado, verifica y resume sin crear spec ni Quick Plan.
1. **Requirements:** historias, criterios EARS, errores, edge cases y supuestos.
     Gate 1: aprobar requisitos en `standard` legacy solicitado explícitamente.
2. **Design:** arquitectura, modelos, errores, pruebas y estrategia de testing.
     Gate 2: aprobar diseño en `standard` legacy solicitado explícitamente.
3. **Tasks:** tareas trazadas a requisitos, dependencias y waves.
     Gate 3: aprobar el plan y empezar a implementar en `standard` legacy solicitado explícitamente.
4. **Implementación:** ejecutar una tarea o wave, con integrity gate antes de marcarla.
5. **Verification:** tras Implementación, ejecutar pruebas,
   registrar evidencia y revisar requisitos y RNF. Gate 4: cerrar la spec o corregir
   huecos en `standard` legacy solicitado explícitamente; Tiny también espera Gate 4
   al cerrar el único spec después de verificación.

En SDD-Tiny se crea un único `spec.md` inicial antes de cambiar código; Gate 3
aprueba el plan antes de implementar y el mismo documento se actualiza con pruebas,
comandos/resultados y cierre antes de Gate 4. No requiere Quick Plan, EARS completa
ni matriz de trazabilidad. Solo planificación deja el documento Planificado y no
implementa ni afirma resultados.

En SDD-Lite, Quick Plan genera `requirements.md`, `design.md` y `tasks.md` en una
pasada después de validar alcance y resolver elección, sin repetir la nota. No existen Gates 1-3
ni Gate 4. Si el alcance es solo planificar, termina con esos tres archivos; si también se
implementa, añade un `verification.md` compacto con la evidencia.

## Contexto opcional de Project Navigator

Si existe una instancia aplicable de `.navigator/`, SDD comprueba su configuración,
capas y frescura antes de usarla. El orden de lectura es:

1. steering de la plataforma y `.sdd/steering/`;
2. preflight y capa mínima de Navigator;
3. README del dominio y documentación estrictamente necesaria;
4. código y pruebas puntuales según la fase.

Un Navigator `vigente` orienta la exploración inicial. Si está `desfasado` o
`no_verificable`, solo aporta pistas de ubicación y SDD confirma las afirmaciones
en documentación y código reales. Si está `ausente` o resulta `ambiguo`, se omite
y el flujo continúa: Navigator nunca es un requisito para usar SDD.

SDD no crea ni actualiza `.navigator/` automáticamente. Puede recomendar bootstrap
o update, pero el usuario debe decidir si continúa con `documentation-orchestrator`,
que ejecuta la skill Project Navigator con sus propios gates. El código, el steering
y los contratos canónicos siguen siendo las fuentes de verdad.

## Qué produce

```text
.sdd/specs/
├── <nombre-feature>/              # ruta plana, continúa siendo válida
│   ├── spec.md                     # SDD-Tiny: documento único
│   ├── requirements.md            # o bugfix.md (SDD-Lite / Standard)
│   ├── design.md
│   ├── tasks.md
│   └── verification.md
└── <modulo>/<nombre-feature>/     # agrupación recomendada si hay varias specs
    ├── spec.md                     # SDD-Tiny: documento único
    ├── requirements.md            # o bugfix.md (SDD-Lite / Standard)
    ├── design.md
    ├── tasks.md
    └── verification.md
```

La ruta relativa completa identifica la spec. Una carpeta intermedia es solo un
agrupador: la raíz de una spec contiene `spec.md`, `requirements.md` o `bugfix.md`.
Al reanudar sin ruta explícita, SDD busca esos marcadores de forma
recursiva y pregunta si encuentra varias candidatas plausibles.

La estructura completa corresponde a un `standard` legacy solicitado explícitamente
o a un SDD-Lite implementado. SDD-Tiny conserva solo `spec.md`; SDD-Lite solo de
planificación omite `verification.md`; `direct` no crea esta carpeta.

No marca una tarea `[x]` sin artefacto real o evidencia. El design debe registrar
la estrategia de pruebas y respetar la barra de calidad de la skill.

## Ejemplos de uso

```text
@sdd Diseña y planifica el bloqueo de cuenta después de tres intentos fallidos.
Usa modo standard y detente en cada gate.
```

```text
@sdd Corrige este bug reproducible con una regresión antes del fix y deja evidencia
de la suite ejecutada.
```

```text
@sdd Quick Plan para una pantalla de ajustes bien definida; registra la estrategia
de testing y no implementes todavía.
```

Esta petición solicita evaluar SDD-Lite (`lite`) y Quick Plan; no evita sus
condiciones. `Quick Plan standard`, `Quick Plan direct` y `Quick Plan SDD-Tiny` son
combinaciones inválidas.

## Límites y confirmaciones

- No cruza los Gates 1-4 de `standard` legacy sin aprobación explícita.
- La clasificación del esfuerzo se emite una sola vez tras analizar el alcance
  definido, con el formato `Esfuerzo previsto del LLM: <nota e icono>` (1–7 🟢 o
  🟠 con atención especial, 8–9 🟠, 10 🔴, superior a X13: `10+ 🔴`);
  no recomienda niveles ni selecciona LLM.
- Ninguna fase repite esa clasificación ni espera por modelo; SDD-Lite inicia Quick
  Plan sin pausa por modelo, sin crear Gates 1-3 ni Gate 4.
- La intención de solo planificación no autoriza implementar. Cambiar de SDD-Lite
  a `standard` requiere que el usuario lo solicite explícitamente, aunque la clasificación
  de feature no cambie.
- Quick Plan solo existe en SDD-Lite (`lite`) y no se combina con otra profundidad.
- No recomienda, identifica ni selecciona modelo, proveedor o nivel de LLM.
- No inventa requisitos, cumplimiento, resultados de tests ni evidencia.
- No añade dependencias de testing sin un test que las use en la misma entrega.
- No presenta un Navigator desfasado o sin baseline verificable como vigente.
- No escribe `.navigator/` ni cambia automáticamente a `documentation-orchestrator`.
- Respeta `.architecture/`, `.design/`, `.data/`, `.security/` y `.quality/` cuando
  existen; si falta contexto, documenta solo lo imprescindible dentro de la spec.
- Confirma acciones destructivas y nunca expone secretos.
