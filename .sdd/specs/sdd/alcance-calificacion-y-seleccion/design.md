# Diseño — Alcance, calificación y selección de profundidad SDD

Modo SDD: standard
Fase: Design
Estado: aprobado
Gate 2: aprobado por el usuario («procede»)

## Contexto y decisiones

El comportamiento se define mediante prompts y referencias canónicas, no mediante
un clasificador ejecutable. Se conserva el pipeline canonical → adapters → generated.
No se modifican adaptadores, configuraciones globales, instaladores ni runtime.
La conversación aprobada define la intención y requirements.md fija sus criterios.

## Responsabilidades y archivos

- `canonical/agents/sdd.md`: instrucciones esenciales, orden del flujo y carga
  selectiva de la política; sin duplicar la rúbrica completa.
- `canonical/skills/sdd-spec/SKILL.md`: flujo normativo común, selección explícita,
  artefactos por profundidad y preservación de gates.
- Nueva `canonical/skills/sdd-spec/references/scope-depth.md`: criterios de
  elegibilidad, atención especial, precedencias y división en entregas.
- `references/feature-level.md`: conserva las anclas numéricas ReserveLab; cambia
  momento de publicación, presentación y separación entre esfuerzo y atención.
- `references/templates.md`: registra nota y atención, recomendación, elección,
  justificación y controles en artefactos lite/standard sin repetirlos al usuario.
- Revisar `references/agent-routing.md`, `testing.md`, `integrity-gate.md` y
  `quality-bar.md` para eliminar contradicciones sin debilitar controles existentes.
- `docs/agentes/sdd.md`, `docs/sdd-smoke.md`, `docs/sdd-effort-examples.md` y otros
  textos de uso afectados: alinear ejemplos y distinguir evidencia de expectativas.
- `tools/test_sdd_contract.py` y pruebas relacionadas: sustituir aserciones del
  contrato retirado por regresiones del nuevo y conservar protecciones no afectadas.
- `generated/`: regenerar exclusivamente con `tools/render.py` para seis plataformas.

## Flujo común y precedencias

1. Preflight breve y steering; clasificar tipo e intención, no elegir modo prematuramente.
2. Resolver ejecutor antes de escrituras. Solo visual/datos claro puede recomendar
   especialista; ambiguo/mixto conserva planificación SDD. Respetar elección previa.
3. Definir objetivo, alcance, exclusiones, criterios, errores y supuestos mediante
   preguntas esenciales y evidencia técnica mínima; no crear un documento obligatorio.
4. Para features, calificar el alcance completo una vez usando las anclas existentes.
5. Evaluar elegibilidad y proponer profundidad; respetar selección previa compatible.
6. Resolver selección pendiente antes de Quick Plan, fases standard o ejecución direct.
7. Reutilizar criterios y continuar según intención; la elección no aprueba gates.

Las solicitudes de standard no se rebajan. Una nota no autoriza permisos ni elimina
restricciones. Bugfix no trivial sigue en standard sin calificación de feature.
Exploraciones y consultas no reciben nota; no se inventa una feature para puntuarlas.
Reanudaciones conservan modo, artefactos y gates; no se reclasifican silenciosamente.

## Recomendación por esfuerzo y elegibilidad

| Caso | Recomendación |
|---|---|
| 1–3 y trivial, localizado, reversible y verificable | direct |
| 1–3 no trivial pero elegible para lite | lite |
| 4–9 elegible | lite, con atención si corresponde |
| 1–9 no elegible tras aclarar incertidumbres | standard o división segura |
| 10 / 10+ | standard para el conjunto y opción de dividir |

Direct conserva límites actuales: sin contrato público, migración, arquitectura,
cruce de capas ni riesgos relevantes de seguridad, concurrencia o integridad.
Sin spec formal ni Quick Plan; criterios y evidencia breve quedan en la conversación.

Lite exige resultado definido, alcance acotado, patrones existentes, verificación
viable y reversibilidad. Concurrencia, persistencia o integridad no lo excluyen por
su mera presencia. Para admitir complicaciones, todas estas condiciones deben cumplirse:

1. Invariante o garantía concreta identificada y criterios testables.
2. Mecanismo existente o patrón establecido que resuelve la garantía, sin introducir
   una arquitectura nueva: transacción, restricción de unicidad, lock o idempotencia.
3. Pruebas viables sobre el mecanismo real o seam representativo, incluyendo
   concurrencia/reintentos/fallos pertinentes; un mock que oculta la garantía no basta.
4. Dependencias, efectos laterales y recuperación acotados; sin dejar estados
   críticos inconsistentes entre entregas y con una forma segura de revertir.
5. Controles registrados en diseño/tareas y comprobados antes del cierre.

Se conserva standard para cambios de contrato público/API, migraciones,
decisiones arquitectónicas nuevas, integraciones significativas, cruces relevantes
de capas/módulos, cambios de seguridad/autorización/privacidad/compliance, legado
riesgoso o garantías no demostrables. No se excluye por palabras aisladas: reutilizar
una API o autorización existente sin cambiarla no equivale a modificar su contrato.
La nota no garantiza que estas condiciones se cumplan; si lite deja de ser elegible,
detenerse en un punto seguro y solicitar reclasificación.

## Atención y presentación

La nota sigue siendo ordinal 1–10 o 10+; no se cambian anclas ni datos históricos.
Registrar esfuerzo y atención como conceptos separados, sin añadir un score de riesgo.

- 1–7: verde normalmente; naranja cuando existan complicaciones concretas controlables.
- 8–9: mantener naranja como atención reforzada.
- 10 y 10+: rojo; siempre ofrecer evaluación de entregas incrementales.

Mensaje rutinario: nota/icono, advertencia concreta si aplica, profundidad recomendada
y elección concisa. Sin referente de laboratorio, explicación de rangos ni prefacio.
Justificaciones extendidas solo si el usuario las pide o necesita entender un límite.
La atención naranja no altera nota ni aprueba modo. Incertidumbre esencial se aclara
antes de calificar; no se disfraza mediante una advertencia genérica.
En specs guardar referente, factores, supuestos, atención y controles. Direct no crea
un archivo solo para ese registro; se conserva la explicación mínima en conversación.
No repetir calificación por fase; actualizar únicamente ante cambio material.

## Entregas incrementales

División opcional, no un cuarto modo ni una fase de aprobación adicional.
Definir un mapa ligero del alcance completo: entregas, resultados, dependencias y
garantías transversales. Cada entrega definida se califica y selecciona por separado.
No calificar provisionalmente entregas aún ambiguas ni prometer que todas serán lite.
Una entrega 10/10+ ofrece otra división útil; si no existe, recomendar standard y
explicar el límite. No fragmentar repetidamente para bajar la nota artificialmente.
Registrar criterios transversales y tarea de verificación integrada en la entrega
que complete la garantía; no declarar cerrado el conjunto por cierres parciales.
Crear specs por entrega solo tras seleccionar lite/standard, respetando rutas del
módulo y conservando vínculos; direct no se fuerza a producir carpeta de spec.

## Errores y límites de selección

- Solicitar modo no elegible: explicar motivo concreto y ofrecer modos elegibles
  o reducción del alcance; no aceptar silenciosamente ni repetir todos los límites.
- Elección ambigua: aclarar solo la decisión pendiente.
- Elegir especialista: contexto manual y detener actividad; sin subagente automático.
- Solo planificación: nunca implementar; seleccionar modo no amplía autorización.
- Specs históricas: preservar evidencia y aprobaciones; no migración automática.

## Estrategia de pruebas

TDD focalizado para contrato textual nuevo: añadir regresiones y observar RED por
ausencia de reglas nuevas, aplicar cambios y observar GREEN. Actualizar aserciones
antiguas solo donde el comportamiento aprobado las sustituya; no borrar cobertura
de gates, especialistas, formatos históricos o límites de testing.
Comprobar casos 1/2/3 direct, 4 lite, 6 naranja con garantías lite, 6 sin garantías
standard, 10/10+ con división, entrega que sigue en 10, elección previa y routing.
Comandos previstos: test_sdd_contract.py, test_model_recommendations.py,
test_handoff_contract.py, render.py, validate.py, check_links.py y git diff --check.
Usar smoke manual documentado para conducta del agente; resultados textuales no
acreditan ejecución LLM real. No añadir dependencias de testing ni PBT ceremonial.

## Invariantes y RNF

- RNF-1: las seis distribuciones contienen el mismo contrato tras render reproducible.
- RNF-2: ninguna recomendación salta permisos, selección de ejecutor o Gates 1–4.
- RNF-3: nota numérica, atención, profundidad e intención permanecen distinguibles.
- RNF-4: cierre lite/direct conserva evidencia proporcional de criterios y controles.
- RNF-5: no quedan instrucciones activas del momento de calificación retirado ni
  selección automática incompatible con la nueva elección manual.

Quality bar: separación entre agente, política y renderer; sin lógica duplicada en
adaptadores. DI, loop UI y encapsulación de BD no aplican a este cambio documental.
No se introducen servicios, persistencia o capas anticipadas. Evidencia, errores y
testing se verifican con suites existentes y revisión de textos.
