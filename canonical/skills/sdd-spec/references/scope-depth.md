# Alcance, atención y selección de profundidad

Política normativa de SDD; no es un clasificador runtime. Usa la rúbrica numérica
de `feature-level.md`, sin inventar notas por archivos ni sumar riesgos.

## Definición común

Antes de elegir profundidad, acordar objetivo, resultados, límites, exclusiones,
criterios verificables, errores, casos límite y supuestos pertinentes. Preguntar
solo decisiones esenciales pendientes; reutilizar lo ya indicado por el usuario.
Consultar código y contratos mínimos: una capacidad existente y otra por construir
no tienen el mismo esfuerzo. No introducir algoritmos ni arquitectura en requisitos.

Esta etapa no exige archivo propio ni gate nuevo. Alcance claro puede resumirse
brevemente; un alcance ambiguo requiere interacción antes de puntuar. Conservar
el mismo rigor testable en lite y standard, con documentación proporcional.
Para features, publicar nota una vez al terminar alcance e impacto, antes de
recomendar profundidad. No repetirla al producir Quick Plan o Requirements.

## Recomendación base

| Caso | Profundidad | Condición |
|---|---|---|
| 1–3 trivial | direct | Localizado, reversible, verificable y sin exclusiones de direct. |
| 1–3 no trivial elegible | lite | No forzar direct por una nota baja. |
| 4–9 elegible | lite | Alcance definido, acotado, patrones y verificación viable. |
| 1–9 no elegible | standard | Aclarar incertidumbres o evaluar división segura. |
| 10 / 10+ | standard | Para el conjunto; ofrecer dividir en entregas. |

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

Mantener standard para cambios de contrato público/API, migraciones, arquitectura
nueva, integración externa significativa, cruce relevante de capas/módulos,
cambios de seguridad/autorización/privacidad/compliance, legado riesgoso o garantías
no demostrables. Reutilizar una API/autorización existente sin cambiarla no equivale
a modificar ese contrato. Evaluar responsabilidades, no palabras clave aisladas.
Incertidumbres esenciales se aclaran antes de calificar: no esconderlas en una
advertencia genérica. Si lite deja de ser elegible, detenerse en un punto seguro
y pedir aprobación para reclasificar a standard.

## Selección y continuidad

- Antes de recomendar modo, comprobar specs relacionadas con búsqueda localizada;
  aplicar `spec-continuity.md` bajo demanda. Una enmienda conserva modo/gates:
  nota baja no autoriza direct para sustituir un acuerdo o tarea pendiente.
- Ofrecer aceptación de la recomendación o elección de otra profundidad elegible.
  Esperar elección explícita pendiente antes de ejecutar el flujo; no repetir si
  ya existe una elección compatible. Standard explícito no se rebaja.
- Si se pide una profundidad no elegible, explicar el límite concreto y ofrecer
  modos elegibles o reducción de alcance. No presentar opciones incompatibles
  como si pudieran seleccionarse sin condiciones.
- La elección no aprueba gates ni amplía permisos, alcance o intención. La
  conversación común no aprueba Gate 1: standard formaliza requisitos y lo conserva.
- La nota no crea un gate ni requiere aprobación propia. La selección es una
  decisión esencial pendiente, no Gates 1–3 adicionales para lite.
- Solo planificación nunca implementa. Testing es independiente de profundidad.
  Direct no significa sin pruebas; lite reduce ceremonia, no evidencia.
- Bugfix no trivial conserva standard; bugs, consultas y exploraciones no reciben
  notas de feature. Trivial bugfix puede ser direct con regresión proporcional.
- Specs históricas conservan modo, evidencia y gates; no migrar ni inferir aprobación.
  Reanalizar solo cambios materiales, y no repitas selección/calificación por fase.
- Elecciones previas se limitan al alcance aceptado, no a toda la sesión. Cambios
  relacionados requieren evaluación conjunta sin sumar notas.
- Resolver especialista con `agent-routing.md`: solo visual/datos ejecutable claro
  puede recomendar ui-design/data-api. Mixto/ambiguo mantiene planificación SDD.
  Elegir especialista entrega contexto manual y detiene la actividad en SDD.

## Entregas incrementales

Para 10 o 10+ ofrecer división aunque alguna entrega vuelva a obtener 10 o 10+.
También puede proponerse en otros alcances cuando aporte valor, sin obligarla.

Definir mapa ligero: resultados útiles y verificables, límites, dependencias y
garantías transversales. No confundir entregas con fases SDD ni crear un cuarto modo.
Evaluar cada entrega con alcance definido de forma independiente: la división
no garantiza una nota menor ni que todas sean lite. No puntuar entregas ambiguas.

Si una entrega sigue en 10/10+, evaluar otra separación útil; si no existe división
segura, mantener standard y explicar el límite. No fragmentar indefinidamente
para bajar la nota ni entregar reservas sin protección contra sobreventa.

Conservar requisitos transversales y prever verificación de integración entre
entregas. No cerrar el conjunto por cierres parciales sin comprobar esas garantías.
Las entregas lite/standard pueden tener specs vinculadas por módulo; direct no
se fuerza a crear carpeta. No mover automáticamente specs ya existentes.

## Casos de decisión

Ejemplos ilustrativos; no son resultados nuevos de laboratorio ni un scorer.

| Caso | Presentación | Decisión y supuesto |
|---|---|---|
| 1 | 1 🟢 | direct: trim de función pura localizada, con límites definidos. |
| 2 | 2 🟢 | direct: predicados locales y orden estable, sin otros efectos. |
| 3 | 3 🟢 | direct: cálculo puro de ejemplo, redondeo definido, sin pagos reales. |
| 4 | 4 🟢 | lite: normalización y conflictos acotados, patrones existentes. |
| 6-controlado | 6 🟠 | lite: reserva acotada con mecanismo adecuado y pruebas concurrentes. |
| 6-sin-garantías | 6 🟠 | standard: no hay verificación viable de la garantía crítica; no forzar lite. |
| 10 | 10 🔴 | standard para el conjunto; ofrecer entregas verificables. |
| 10+-entrega | 10+ 🔴 | Evaluar otra división útil o standard si no es segura. |

Pruebas lite descritas por el usuario motivan la preferencia 4–9, pero no certifican
todos los alcances ni reemplazan evidencia de cada caso.
