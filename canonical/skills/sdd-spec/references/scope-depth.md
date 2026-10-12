# Alcance, atención y selección de profundidad

Política normativa de SDD; no es un clasificador runtime. Usa la rúbrica numérica
de `feature-level.md`, sin inventar notas por archivos ni sumar riesgos.

## Definición común

Antes de elegir profundidad, acordar objetivo, resultados, límites, exclusiones,
criterios verificables, errores, casos límite y supuestos. Preguntar solo lo
esencial; reutilizar lo indicado. Consultar código mínimo; no introducir algoritmos
en requisitos.

Esta etapa no exige archivo propio ni gate numerado nuevo. Presentar y validar
alcance completo según la sección siguiente; conservar rigor testable en todos los modos.
Para features, publicar nota tras alcance e impacto, antes de recomendar profundidad;
no repetirla por fase.

## Alcance completo y validación

Mostrar `Alcance definido` con:
- Objetivo y resultado esperado.
- Todos los comportamientos acordados, reglas y condiciones.
- Criterios de aceptación verificables por comportamiento.
- Errores, casos límite y estados relevantes identificados.
- Exclusiones, restricciones y supuestos; distinguir confirmado de supuesto.

Sin recortar información funcional por brevedad. No inventar requisitos ni detalles
de implementación; aclarar decisiones esenciales antes de calificar. Completo no
significa documentación exhaustiva del proyecto.

Esperar validación explícita antes de generar artefactos o implementar. Combinar
validación y elección pendientes en una pregunta. Elegir solo modo no valida el
alcance; elegir solo ejecutor tampoco. La nota no requiere aprobación propia.

Ante ajustes, presentar alcance completo actualizado y volver a validar, no solo el delta.
Reutilizar aprobación explícita previa de la misma versión completa si sigue vigente;
no repetir presentación/pregunta. Un resumen breve previo no acredita esa aprobación.
Nueva entrega necesita alcance propio; cambio material exige reevaluar esfuerzo,
elegibilidad y autorización. La aprobación anterior no cubre contenido nuevo.

Calificar features después de mostrar su alcance completo, incluidas 10 y 10+.
Bugfix conserva tratamiento sin nota; consulta informativa sin artefactos ni
implementación no añade aprobación ceremonial.

Validar alcance no equivale a Gate 1: standard formaliza requisitos y conserva gates;
lite genera Quick Plan en una pasada sin otra aprobación rutinaria de requirements.
Direct sigue sin spec. Exponer diferencias funcionales de formalización antes de ejecutar.
Planificación aceptada no autoriza implementación. Reanudar sin cambios conserva decisiones.

## Respuestas de validación

| Respuesta/contexto | Acción |
|---|---|
| aceptación conjunta | Continuar según modo, autorización y gates. |
| solo modo | Resolver validación pendiente. |
| solo alcance | Resolver elección pendiente. |
| ajuste | Mostrar completo actualizado y validar. |
| validación vigente | No repetir; reutilizar solo misma versión completa. |

## Recomendación base

| Caso | Profundidad | Condición |
|---|---|---|
| 1–3 trivial | direct | Localizado, reversible, verificable y sin exclusiones de direct. |
| 1–3 no trivial | lite | No forzar direct por una nota baja. |
| 4–9 | lite | Alcance definido, acotado, patrones y verificación viable. |
| 1–9 no trivial | lite | Siempre elegible; adapta controles al riesgo y ofrece división si es muy amplio. |
| 10 / 10+ | Ofrecer división | `standard` legacy no es fallback; solo continuar con él ante solicitud explícita. |

`standard` es legacy/deprecado: `direct` y `lite` son los únicos modos recomendados.
`lite` siempre es elegible. No selecciones `standard` por puntuación, complejidad
ni LLM local. Solo el usuario puede pedirlo; entonces se aplica el flujo de 4 fases.

La nota orienta, no autoriza. Direct exige ausencia de contrato público, migración,
decisión arquitectónica, cruce de capas y riesgos relevantes de seguridad,
concurrencia o integridad. No produce spec formal ni Quick Plan, pero sí criterios,
pruebas/checks pertinentes y evidencia breve en la conversación.

Lite exige decisiones funcionales esenciales resueltas, alcance acotado, patrones
existentes y reversibilidad sin migración compleja. Produce Quick Plan obligatorio
y verification compacto si implementa. La atención no reemplaza elegibilidad.

## Complicaciones controlables

Concurrencia, persistencia e integridad no excluyen lite por sí solas. Admitir lite
con atención naranja solo si se cumplen todas estas condiciones:

1. Invariante o garantía concreta definida con criterios testables.
2. Mecanismo adecuado existente o patrón establecido: transacción, unicidad, lock,
   idempotencia u otro pertinente, sin decisión arquitectónica nueva.
3. Pruebas viables que comprueban la garantía con el mecanismo real o un seam
   representativo, incluyendo fallos, reintentos y concurrencia pertinentes. Un
   mock que oculta el comportamiento crítico no demuestra la garantía.
4. Efectos, dependencias, recuperación y reversibilidad acotados; no dejar estados
   críticos inconsistentes ni separar una operación de su protección obligatoria.
5. Controles trazados en diseño/tareas y evidencia exigida antes del cierre.

No fuerces lite ante contrato público/API, migraciones, arquitectura nueva,
integración externa significativa, cruce relevante de capas, cambios de seguridad
o legado riesgoso. Reutilizar una API/autorización existente sin cambiarla no
modifica ese contrato. Evaluar responsabilidades, no palabras clave. Si lite deja de ser
elegible, detente y explica la exclusión: ofrece reducir/dividir o espera
solicitud explícita de `standard`.

## Selección y continuidad

- Antes de recomendar modo, comprobar specs relacionadas con búsqueda localizada;
  aplicar `spec-continuity.md` bajo demanda. Una enmienda conserva modo/gates:
  nota baja no autoriza direct para sustituir un acuerdo o tarea pendiente.
- Recomendar `direct` o `lite` y esperar validación/elección explícita. `standard`
  solo ante solicitud explícita; no se rebaja cuando el usuario lo pide.
- Si se pide un modo no elegible, explicar el límite y ofrecer uno elegible o
  reducir/dividir alcance. `standard` nunca es recomendación automática.
- La elección no aprueba gates ni amplía permisos, alcance o intención. La
  conversación común no aprueba Gate 1: standard formaliza requisitos y lo conserva.
- La nota no crea un gate ni requiere aprobación propia. La selección es una
  decisión esencial pendiente, no Gates 1–3 adicionales para lite.
- Solo planificación nunca implementa. Testing es independiente de profundidad.
  Direct no significa sin pruebas; lite reduce ceremonia, no evidencia.
- Bugfix no trivial usa lite (siempre elegible). Bugs, consultas y exploraciones
  no reciben notas de feature. Trivial bugfix puede ser direct con regresión proporcional.
- Specs históricas conservan modo, evidencia y gates; no migrar ni inferir aprobación.
  Reanalizar solo cambios materiales, y no repitas selección/calificación por fase.
- Elecciones previas se limitan al alcance aceptado, no a toda la sesión. Cambios
  relacionados requieren evaluación conjunta sin sumar notas.
- SDD se usa porque el usuario seleccionó explícitamente ese agente. No hagas routing
  automático por dominio a Developer; carga skills visuales o de datos bajo demanda
  como apoyo técnico sin cambiar el ejecutor ni los gates SDD.

## Entregas incrementales

Para 10 o 10+ ofrecer división aunque alguna entrega siga en 10/10+. Si no existe
división segura, detenerse; el conjunto solo sigue en `standard` si el usuario lo
solicita explícitamente.

Mapa ligero: resultados verificables, límites, dependencias y garantías
transversales. No confundir entregas con fases SDD. Evaluar cada entrega de forma
independiente; la división no garantiza nota menor ni que todas sean lite.

Si una entrega sigue en 10/10+, evaluar otra separación. Sin división segura,
detenerse. No fragmentar para bajar la nota ni entregar sin protección.

Conservar requisitos transversales y verificar integración entre entregas. No
cerrar el conjunto por cierres parciales. Las entregas lite y las specs standard
legacy explícitas pueden vincularse por módulo; direct no crea carpeta forzada.
No mover specs existentes automáticamente.

## Casos de decisión

Ejemplos ilustrativos; no son resultados nuevos de laboratorio ni un scorer.

| Caso | Presentación | Decisión y supuesto |
|---|---|---|
| 1 | 1 🟢 | direct: trim de función pura localizada, con límites definidos. |
| 2 | 2 🟢 | direct: predicados locales y orden estable, sin otros efectos. |
| 3 | 3 🟢 | direct: cálculo puro de ejemplo, redondeo definido, sin pagos reales. |
| 4 | 4 🟢 | lite: normalización y conflictos acotados, patrones existentes. |
| 6-controlado | 6 🟠 | lite: reserva acotada con mecanismo adecuado y pruebas concurrentes. |
| 6-sin-garantías | 6 🟠 | Pausar: no hay verificación viable; reducir/dividir o esperar solicitud explícita de standard. |
| 10 | 10 🔴 | Ofrecer entregas verificables; standard solo a petición explícita. |
| 10+-entrega | 10+ 🔴 | Evaluar otra división útil; si no es segura, detenerse hasta petición explícita de standard. |

Pruebas lite descritas por el usuario motivan la preferencia 4–9, pero no certifican
todos los alcances ni reemplazan evidencia de cada caso.
