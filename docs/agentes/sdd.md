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
- Para crear un plan rápido de trabajo acotado, claro y de bajo riesgo mediante
  `lite` y Quick Plan.
- Para continuar la implementación de tareas ya aprobadas.

Un cambio trivial, localizado y reversible puede usar `direct`. Tras descartarlo,
SDD selecciona `lite` automáticamente para trabajo acotado, claro y de bajo riesgo.
Si hay dudas, riesgo, contrato público, migración, cruce de capas o un bugfix no
trivial, usa `standard` como modo por defecto y fallback seguro. No existe una
profundidad `deep`; las solicitudes históricas o explícitas de ese modo requieren
aceptar su sustitución por `standard`.

## Esfuerzo previsto del LLM

Tras definir alcance, SDD publica una sola vez el bloque `Esfuerzo previsto del LLM`
con referente, justificación y supuestos. La
[rúbrica ReserveLab](../../canonical/skills/sdd-spec/references/feature-level.md)
define anclas, rangos, reutilización y `10+`; es independiente de profundidad y
elegibilidad de lite. No puntúa antes de entender el alcance ni repite la nota en Requirements,
Design, Tasks, Implementación o Verification. No es una recomendación de modelo,
no identifica ni selecciona un LLM y nunca pausa el flujo por modelo. Si el alcance
cambia de forma sustancial, primero vuelve a analizarlo y actualiza la clasificación;
las decisiones y aprobaciones propias del flujo siguen siendo independientes.

## Recomendación de agente por dominio

SDD evalúa quién puede ejecutar el alcance antes de editarlo. La política inicial
cubre dos especialistas, sin invocarlos automáticamente:

| Actividad | Ruta |
|---|---|
| Solo apariencia/componentes visuales, clara y acotada | Recomendar `ui-design`. |
| Solo datos/APIs, clara y dentro de límites | Recomendar `data-api`. |
| Ambigua, varios dominios o planificación pendiente por riesgo/contratos/migraciones | Mantener planificación SDD. |
| Tarea especializada autorizada de una spec aprobada | Puede recomendar al especialista para esa tarea, conservando la spec. |

La recomendación justifica el candidato y pregunta si quieres **seleccionarlo
manualmente o continuar con SDD**. Si decides seguir aquí, no repite la recomendación
mientras no cambien alcance, riesgo o decisión. Una selección explícita compatible
ya dada se respeta; si contradice límites, se aclara antes de actuar.

SDD no clasifica por palabras aisladas como «pantalla» o «JSON», ni ofrece un agente
de UI para lógica de negocio o uno de datos para UI. La falta de `.design/` o `.data/`
no obliga a cambiar de agente. Tampoco recomienda candidatos cuyo alcance no pueda
verificar ni afirma conocer su instalación en tu host.

Si eliges al especialista, entrega **Contexto para selección manual**: objetivo,
alcance autorizado, exclusiones, rutas verificadas, requisitos/tareas y decisiones
aprobadas si existen, fase/gates pendientes y preguntas abiertas. Copia ese contexto
al agente seleccionado en la interfaz del host. `@` es notación del kit, no un
comando universal. SDD no cambia la interfaz, llama subagentes ni ejecuta en paralelo
la actividad transferida; el contexto no acredita entrega o finalización.

La elección de ejecutor **no aprueba gates**, no modifica permisos ni amplía alcance.
SDD mantiene planificación para rediseños ambiguos/multipantalla y cambios de datos
con contratos, esquemas, migraciones o compatibilidad afectados. Una tarea aprobada
puede ejecutarse después con el especialista sin reabrir requisitos por el mero
cambio de ejecutor, pero el receptor conserva sus propias comprobaciones y gates.

Contrato: [recomendación de agente](../../canonical/skills/sdd-spec/references/agent-routing.md).
Evaluación: [escenarios manuales](../sdd-smoke.md#recomendación-de-agente-por-dominio).

## Modos

| Modo | Uso | Resultado |
|---|---|---|
| `direct` | Cambio trivial, localizado y reversible | Sin spec; verificación mínima |
| `lite` | Selección automática para trabajo acotado, claro y de bajo riesgo | Quick Plan compacto; artefactos según se planifique o implemente |
| `standard` | Modo por defecto y fallback seguro; obligatorio para bugfixes no triviales | Requirements, design, tasks y verification; Gates 1-4 |

Estas son las tres profundidades válidas: `direct`, `lite` y `standard`.
Quick Plan es obligatorio y exclusivo de `lite`; combinarlo con cualquier otra
profundidad es inválido.

La profundidad y el testing son decisiones independientes. Una feature normal usa
TDD focalizado; TDD estricto está retirado. Si se solicita, propone TDD focalizado
y espera aceptación. Los bugfixes usan regresión y el legado usa caracterización.

`deep` y TDD estricto pueden aparecer en specs históricas, pero no son opciones
vigentes. SDD conserva esos artefactos y evidencias, informa la retirada y espera
aceptación antes de continuar con `standard` o TDD focalizado; no convierte la
solicitud silenciosamente ni confunde esa aceptación con la aprobación de un gate.

## Flujo y gates

0. **Clasificación de feature:** tras analizar el alcance definido, emite una sola
   vez el bloque `Esfuerzo previsto del LLM: <nota e icono>` con referente,
   justificación y supuestos; no recomienda modelos ni pausa por modelo.
   `direct` no crea spec.
1. **Requirements:** historias, criterios EARS, errores, edge cases y supuestos.
    Gate 1: aprobar requisitos en `standard`.
2. **Design:** arquitectura, modelos, errores, pruebas y estrategia de testing.
    Gate 2: aprobar diseño en `standard`.
3. **Tasks:** tareas trazadas a requisitos, dependencias y waves.
    Gate 3: aprobar el plan y empezar a implementar en `standard`.
4. **Implementación:** ejecutar una tarea o wave, con integrity gate antes de marcarla.
5. **Verification:** tras Implementación, ejecutar pruebas,
   registrar evidencia y revisar requisitos y RNF. Gate 4: cerrar la spec o corregir
   huecos en `standard`; después termina el flujo.

En `lite`, Quick Plan genera `requirements.md`, `design.md` y `tasks.md` en una
pasada después de analizar el alcance, sin pausa por modelo. No existen Gates 1-3
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
│   ├── requirements.md            # o bugfix.md
│   ├── design.md
│   ├── tasks.md
│   └── verification.md
└── <modulo>/<nombre-feature>/     # agrupación recomendada si hay varias specs
    ├── requirements.md            # o bugfix.md
    ├── design.md
    ├── tasks.md
    └── verification.md
```

La ruta relativa completa identifica la spec. Una carpeta intermedia es solo un
agrupador: la raíz de una spec es la carpeta que contiene `requirements.md` o
`bugfix.md`. Al reanudar sin ruta explícita, SDD busca esos marcadores de forma
recursiva y pregunta si encuentra varias candidatas plausibles.

La estructura completa corresponde a `standard` o a un `lite` implementado.
Un `lite` solo de planificación omite `verification.md`; `direct` no crea esta
carpeta.

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

Esta petición usa `lite` automáticamente. `Quick Plan standard` y
`Quick Plan direct` son combinaciones inválidas.

## Límites y confirmaciones

- No cruza los Gates 1-4 de `standard` sin aprobación explícita.
- La clasificación del esfuerzo se emite una sola vez tras analizar el alcance
  definido, con el formato `Esfuerzo previsto del LLM: <nota e icono>` (1–7 🟢,
  8–9 🟠, 10 🔴, superior a X13: `10+ 🔴`) y referente/justificación/supuestos;
  no recomienda niveles ni selecciona LLM.
- Ninguna fase repite esa clasificación ni espera por modelo; `lite` inicia Quick
  Plan sin pausa por modelo, sin crear Gates 1-3 ni Gate 4.
- La intención de solo planificación no autoriza implementar. Cambiar de `lite`
  a `standard` requiere aprobación por el cambio de flujo, aunque la clasificación
  de feature no cambie.
- Quick Plan solo existe en `lite` y no se combina con otra profundidad.
- No recomienda, identifica ni selecciona modelo, proveedor o nivel de LLM.
- No inventa requisitos, cumplimiento, resultados de tests ni evidencia.
- No añade dependencias de testing sin un test que las use en la misma entrega.
- No presenta un Navigator desfasado o sin baseline verificable como vigente.
- No escribe `.navigator/` ni cambia automáticamente a `documentation-orchestrator`.
- Respeta `.architecture/`, `.design/`, `.data/`, `.security/` y `.quality/` cuando
  existen; si falta contexto, documenta solo lo imprescindible dentro de la spec.
- Confirma acciones destructivas y nunca expone secretos.
