---
name: sdd-spec
description: >-
  Aplica la metodología Spec-Driven Development (SDD) estilo Kiro: genera y
  refina specs (requirements.md, design.md, tasks.md, verification.md) con modos
  proporcionales, gates de aprobación, notación EARS y trazabilidad. Úsala para
  planificar o implementar una feature/bugfix mediante spec, requisitos, tareas y
  verificación; no para explicar arquitectura sin diseñar una feature.
---

# Skill: SDD Spec

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Flujo SDD proporcional con gates, EARS y trazabilidad. La calificación de feature
solo puede emitirla el agente `/sdd`; cargar esta skill desde otro agente
no autoriza a mostrarla.

> **Precedencia:** si el agente `/sdd` y esta skill divergen, manda esta skill.

## Modos de profundidad

| Modo | Cuándo | Qué produce | Carga documental |
|------|--------|-------------|-------------------|
| `direct` | Cambio trivial verificable | Sin spec 4 fases | Mínima |
| `lite` | Alcance claro y acotado, garantías verificables | Quick Plan; verificación compacta si implementa | Ligera |
| `standard` | Fallback seguro; alcance completo 10/10+ | 4 fases, design corto, 0–5 invariantes, testing adaptativo | Moderada |

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

Recomienda profundidad después de definir alcance e impacto: 1–3 `direct` si
es trivial; 4–9 prioriza `lite` si es elegible; 10/10+ `standard` para el conjunto
y ofrece división. Un 1–3 no trivial puede usar `lite`. Carga
`references/scope-depth.md` para condiciones, atención y selección manual.
Concurrencia/persistencia/integridad acotadas permiten evaluar `lite` con mecanismos
adecuados y pruebas reales; no basta una advertencia. Si la elegibilidad de `lite`
no puede demostrarse, usa `standard`. Conserva las exclusiones de la referencia
y el tratamiento standard de bugfix no trivial.

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

`deep` no está disponible: ante una solicitud nueva propone `standard` y espera
aceptación; no conviertas la solicitud silenciosamente. En una spec histórica conserva
artefactos/evidencia y pide aceptar su sustitución antes de reanudarla. TDD estricto
se trata en `references/testing.md`.
Aceptar la sustitución no aprueba gates. Si los marcadores de modo/fase/estado/gate
faltan o se contradicen, aclara antes de continuar; no infieras aprobación por archivos.

## Preflight técnico y calificación de feature

Antes de contexto pesado, realiza un preflight técnico breve para identificar el
tipo de trabajo, la siguiente operación y decisiones esenciales pendientes. No
recomiendes ni menciones modelos/proveedores LLM, no califiques fases o tareas y no
conviertas el preflight en un gate de usuario. Continúa el trabajo autorizado en el
mismo turno; solo una decisión esencial o un gate real puede requerir respuesta.

Solo el agente `/sdd` califica features de alcance definido; cargar esta
skill desde otro agente no autoriza la emisión. Consulta
`references/feature-level.md`, fuente única de la rúbrica. Bugs, exploraciones y
consultas no reciben nota por defecto.

Publica `Esfuerzo previsto del LLM: <nota e icono>` al terminar alcance e impacto,
antes de recomendar profundidad. Referente, factores y supuestos quedan en la spec,
no en mensajes rutinarios. Separa nota y atención según la rúbrica. No muestra
notas provisionales, no repite ni pausa ni pide aprobación de la nota; reanaliza
cambios materiales. No cambia testing, ejecutor, permisos o modelo ni crea gates.

## Definición de alcance y criterios de aceptación

Antes de elegir profundidad, define objetivo, resultados, exclusiones, criterios,
errores y supuestos. Preguntas esenciales sin repetir información; consulta
contexto técnico mínimo. No crea un documento obligatorio
y no aprueba Gate 1. Conserva EARS.
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
> La calificación de feature no es un gate ni requiere aprobación
> separada. El preflight técnico no recomienda modelos ni añade pausas. En las
> transiciones, espera solo la aprobación del gate SDD real. `lite` usa Quick Plan
> sin Gates 1–3 y cierra sin Gate 4.

### Fase 1 — Requirements

1. Lee steering (`AGENTS.md`, `CLAUDE.md`, `.pi/APPEND_SYSTEM.md`, `.sdd/steering/*.md`). Si existe Navigator
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

Usa el flujo y gates normales, salvo bug trivial `direct`. Diseño con causa raíz +
invariantes si aplican. Primero crea una regresión que falle por el defecto; usa
caracterización para comportamiento legado que deba preservarse. Si no puede
reproducirse, registra la limitación y no inventes un RED.

## Modo lite y Quick Plan

Quick Plan es obligatorio y exclusivo de `lite`. Con alcance validado y selección
resuelta, genera requirements, design y tasks en una pasada,
sin Gates 1–3. Reutiliza criterios acordados y registra la nota sin volver a
publicarla. El preflight técnico no recomienda modelos ni pausa por modelo.

Si la intención es solo planificación, termina después de `tasks.md` y no
implementar código. Si la solicitud original incluye implementación, aplica
integrity-gate y testing adaptativo después del plan. Al terminar, crea un
`verification.md` compacto con RED o baseline, GREEN, suite, excepciones y matriz
de evidencia; cierra sin Gate 4.

Si aparece una exclusión, detente en un punto seguro y propón `standard`. La
reclasificación requiere aprobación por el cambio de flujo. Quick Plan no es
compatible con `direct` ni `standard`.

## Modo direct

Con alcance validado y selección resuelta, ejecuta solo lo autorizado, con el
cambio mínimo correcto y testing adaptativo. No crea archivos formales de spec
ni Quick Plan. Presenta cambios, evidencia real y límites en un cierre breve;
actualiza documentación existente solo si el cambio o steering lo exige.
Si deja de ser trivial, detente y solicita reclasificación antes de ampliar el flujo.

## Reglas de calidad

- **Proporcionalidad:** aplica los criterios verificables de `direct`; no confundas
  cambio pequeño con riesgo bajo.
- Un requisito = un comportamiento testable. Sin adjetivos vagos.
- Sujeto siempre "EL SISTEMA".
- Implementación → `design.md`, no `requirements.md`.
- Cada requisito ≥1 tarea. Respeta steering. Sin cumplimiento inventado.
- Los patrones EARS mínimos ya están en esta skill; abre `ears-reference.md` solo si hace falta una forma no cubierta.
