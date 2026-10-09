# Requisitos — Rúbrica de esfuerzo SDD anclada a ReserveLab

- **Modo SDD:** standard
- **Tipo de trabajo:** feature
- **Intención:** planificación e implementación
- **Fase:** Requirements
- **Estado:** iteración de compactación cerrada
- **Iteración vigente:** eficiencia de contexto SDD; R01–R22 conservados, R23–R28 nuevos
- **Gate 0 de esta iteración:** preflight presentado; continuación autorizada («continúa»)
- **Gate 1 de esta iteración:** aprobado por el usuario («procede»)
- **Gate 2 de esta iteración:** aprobado por el usuario («procede»)
- **Gate 3 de esta iteración:** aprobado por el usuario («procede»)
- **Gate 4 de compactación:** aprobado por el usuario («procede»); Gate 4 inicial no aplica a esta iteración
- **Gates históricos 1–3:** aprobados por «procede» para la implementación inicial
- **Próxima operación:** ninguna; iteración cerrada

## 1. Objetivo

Como usuario de SDD, quiero una calificación ordinal del esfuerzo previsto del LLM
para implementar y verificar la feature solicitada, usando ReserveLab como referencia,
para comparar alcances y explicitar supuestos sin confundir esfuerzo con riesgo,
profundidad SDD, elegibilidad de lite, nivel de LLM ni resultado funcional.

La escala no predice exactamente tokens, tiempo, pasos o costo; no constituye una
fórmula validada ni una frontera universal de capacidad. F01 es el ancla 1 y X13
el ancla 10. Los rangos históricos del laboratorio no son puntuaciones de la nueva
rúbrica: `difficulty_rank=10` de F10 y el nivel histórico 13 de X13 se conservan.

## 2. Comportamiento actual y fuentes verificadas

No existen `AGENTS.md` en la raíz ni `.sdd/steering/`. Se leyó el contexto de
`.architecture/README.md` y las instrucciones del pipeline en `docs/desarrollo.md`.
Se localizó `.navigator/config.yaml`, pero no se usan afirmaciones de sus índices
ni se declara su frescura; las conclusiones siguientes provienen de fuentes directas.

La calificación ya está implementada como instrucciones Markdown, no como motor
numérico de scoring:

- `canonical/skills/sdd-spec/references/feature-level.md`: rúbrica ordinal genérica
  1–10 y formato `Nivel de feature: <n> <emoji>`; no admite actualmente `10+`.
- `canonical/skills/sdd-spec/SKILL.md` y `canonical/agents/sdd.md`: consumen esa
  referencia y limitan la emisión al agente SDD después de definir alcance.
- `canonical/skills/sdd-spec/references/templates.md`: registro en Requirements
  standard y lite con el formato anterior.
- `tools/test_sdd_contract.py` y `tools/test_model_recommendations.py`: checks
  de contrato, presentación, separación de conceptos y distribución.
- `tools/render.py`: copia las referencias de la skill y adapta skill/agente;
  `tools/validate.py` valida el pipeline. `canonical/manifest.json` declara seis
  plataformas: Copilot, OpenCode, Kiro, Claude, Pi y Antigravity.
- `adapters/*/agents/sdd.json`: diferencias de host; no se encontraron rúbricas
  alternativas ni overrides `adapters/*/skills/sdd-spec.json` versionados.

Todas las diez referencias solicitadas están disponibles y fueron leídas:

1. `.agent-lab/sdd-escalation/runner/src/lab_runner/catalog.py`.
2. `.agent-lab/sdd-escalation/catalog/contracts.md`.
3. `.agent-lab/sdd-escalation/catalog/contracts-f05-f07.md`.
4. `.agent-lab/sdd-escalation/catalog/contracts-f08-f09.md`.
5. `.agent-lab/sdd-escalation/catalog/contracts-f10.md`.
6. `.agent-lab/sdd-escalation/catalog/contracts-x13.md`.
7. `.sdd/specs/laboratorio-evaluacion-sdd/x13-offline-multiusuario/requirements.md`.
8. `.sdd/specs/laboratorio-evaluacion-sdd/x13-offline-multiusuario/design.md`.
9. `.agent-lab/sdd-escalation/results/x13-level13-verdict.md`.
10. `.agent-lab/sdd-escalation/results/x13-level13-verdict.json`.

El veredicto de Luna/MAX es **10/11 familias funcionales aprobadas, C12 válido**;
falló `admin_create` de C08. Es aceptación suplementaria acotada post-hoc, no éxito
completo ni comparación experimental directa con F10. El estado original
`invalid_infrastructure` permanece en la evidencia histórica.

La versión instalada que gobierna esta sesión conserva recomendaciones LLM y
pausas de preflight; las fuentes del repositorio ya las retiraron. Esta feature
no restaura esa política ni modifica gates, routing, profundidad o testing vigentes.

## 3. Historias y criterios EARS

### H1 — Puntuar el trabajo solicitado con evidencia

- **R01:** CUANDO SDD califique una feature de alcance definido EL SISTEMA DEBERÁ
  evaluar el esfuerzo previsto conjunto de implementación y verificación del alcance
  solicitado, no el tamaño total del proyecto ni sus dependencias históricas.
- **R02:** CUANDO SDD compare la feature con ReserveLab EL SISTEMA DEBERÁ considerar
  alcance funcional/regresión; reglas y casos límite; estados/transiciones/integridad;
  capas/módulos/entradas; persistencia/integraciones; concurrencia/idempotencia;
  fallos/compensación/recuperación; migración/legado; aislamiento/autorización cuando
  formen parte del trabajo; y construcción/ejecución de pruebas significativas.
- **R03:** CUANDO exista infraestructura reutilizable EL SISTEMA DEBERÁ distinguir
  las garantías ya implementadas de las que la feature debe construir e integrar,
  y justificar cualquier reducción del esfuerzo por reutilización con evidencia.
- **R04:** EL SISTEMA DEBERÁ tratar la escala como ordinal anclada al laboratorio,
  sin conversión matemática del rango histórico, suma automática de factores,
  predicción exacta de recursos ni puntuación basada solo en archivos, líneas,
  longitud de requisitos o etiquetas como «seguridad», «bancario» o «concurrencia».
- **R05:** SI faltan datos esenciales de alcance o infraestructura ENTONCES EL SISTEMA
  DEBERÁ investigarlos o preguntar antes de puntuar; las incertidumbres no esenciales
  deberán figurar como supuestos que podrían cambiar la nota.

### H2 — Calibrar las anclas y los valores intermedios

- **R06:** CUANDO el alcance evaluado sea el contrato F01 con su scaffold publicado
  EL SISTEMA DEBERÁ asignar `1 🟢`.
- **R07:** CUANDO el alcance evaluado sea el contrato X13 con su scaffold publicado
  EL SISTEMA DEBERÁ asignar `10 🔴`, independientemente del resultado de una entrega.
- **R08:** EL SISTEMA DEBERÁ definir descriptores reproducibles para cada valor 2–9,
  vinculados a contratos y factores reales de ReserveLab y a las garantías pendientes
  de implementación/verificación, sin exigir identidad de dominio con el laboratorio.
- **R09:** CUANDO se evalúe F10 limitado a `Saga.submit`, `Saga.step` y `Saga.get`
  sobre el scaffold correcto publicado EL SISTEMA DEBERÁ situarlo alrededor de 8;
  cualquier desviación deberá justificar diferencias materiales de alcance o soporte.
- **R10:** CUANDO una feature supere claramente la dificultad y el alcance de X13
  EL SISTEMA DEBERÁ asignar `10+ 🔴` y explicar las dimensiones y garantías adicionales
  que exceden el referente, descontando infraestructura ya resuelta.
- **R11:** EL SISTEMA DEBERÁ reservar `10+` para superioridad material demostrada,
  sin calcular un puntaje arbitrario ni inferirlo de una palabra de riesgo aislada.

### H3 — Presentar una evaluación compacta y uniforme

- **R12:** CUANDO emita una evaluación EL SISTEMA DEBERÁ usar estas cuatro líneas:
  `Esfuerzo previsto del LLM: <nota e icono>`,
  `Referente del laboratorio: <prueba o rango comparable>`,
  `Justificación: <2–4 factores concretos>` y
  `Supuestos relevantes: <infraestructura existente o incertidumbres que cambian la nota>`.
- **R13:** CUANDO la nota sea 1–7 EL SISTEMA DEBERÁ mostrar el entero asignado y 🟢;
  para 8–9 el entero y 🟠; para 10, `10 🔴`; y para un alcance claramente superior
  a X13, exactamente `10+ 🔴` como nota, sin mostrar 11, 12, 13 u otro entero mayor
  de 10 como calificación SDD, ni decimales, cero o rangos como nota.
- **R14:** EL SISTEMA DEBERÁ conservar la emisión exclusiva del agente SDD tras
  analizar el alcance, sin puntuar tareas/fases ni repetir la nota en transiciones;
  un cambio material de alcance requiere reanálisis antes de actualizar el registro.
- **R15:** SI se requiere una representación estructurada ENTONCES EL SISTEMA
  DEBERÁ conservar compatibilidad y separar el entero 1–10 del indicador de superar
  X13, sin sustituir el campo numérico por la cadena `10+` ni un entero mayor de 10.

### H4 — Separar esfuerzo, política operativa y resultados

- **R16:** EL SISTEMA DEBERÁ mantener independientes la nota de esfuerzo, profundidad
  direct/lite/standard, elegibilidad de lite, nivel de LLM, riesgo, resultado funcional,
  testing, routing, gates y permisos; esta feature no modifica sus políticas.
- **R17:** MIENTRAS existan exclusiones vigentes de lite por seguridad, concurrencia,
  migración o integridad EL SISTEMA DEBERÁ conservarlas aunque la nota sea verde.
- **R18:** CUANDO describa la evidencia observada de X13 EL SISTEMA DEBERÁ distinguir
  10/11 familias funcionales de C12 válido y mencionar el fallo de creación
  administrativa, sin presentar éxito completo ni una frontera universal de capacidad.

### H5 — Distribuir y verificar sin alterar el laboratorio

- **R19:** EL SISTEMA DEBERÁ mantener una definición canónica compartida por skill,
  agente, plantillas y consumidores generados de las seis plataformas, actualizando
  la documentación de uso activa que describa la salida anterior.
- **R20:** CUANDO distribuya el cambio EL SISTEMA DEBERÁ usar el pipeline de generación,
  sin editar `generated/` manualmente, modificar configuraciones globales, publicar
  `.agent-lab` cambiando `.gitignore` ni alterar contratos/resultados/specs históricos
  o cambios locales ajenos.
- **R21:** EL SISTEMA DEBERÁ poder usar la rúbrica distribuida sin exigir acceso al
  laboratorio local ignorado; las referencias locales fundamentan sus descriptores,
  no se convierten en una dependencia obligatoria de los consumidores.
- **R22:** EL SISTEMA DEBERÁ aportar pruebas significativas de F01=1, X13=10, F10≈8,
  las presentaciones 1–7/8–9/10/10+, un caso superior a X13 con dimensiones explícitas,
  reducción razonada al reutilizar infraestructura, independencia de lite y paridad
  canónica/generada. Los checks deterministas no deberán presentarse como medición
  empírica de capacidad o garantía de que cualquier LLM aplicará siempre la rúbrica.

## 4. Comprobaciones de consistencia propuestas para Design

Estos referentes son perfiles comparables, no una conversión del catálogo ni una
fórmula de asignación; Design concretará los descriptores y casos discriminantes.

| Nota | Referente y dificultad observable |
|---|---|
| 1 | F01: formato exacto, validación estricta, ausencia de I/O y mutación. |
| 2 | F02: predicados combinados, límites inclusivos y orden estable. |
| 3 | F03: orden de descuento/impuesto, redondeo entero y límites. |
| 4 | F04: agrupación, conflictos, normalización y propiedad de idempotencia. |
| 5 | F05–F06: efectos transaccionales durables, rollback/reinicio e identidad de reintentos sobre baseline correcto. |
| 6 | F07: escasez entre procesos, reserve/cancel y restitución exactamente una vez. |
| 7 | F08–F09: recuperación de claim/delivery/ack o convergencia de eventos/tombstones; escenarios acotados, infraestructura proporcionada. |
| 8 | F10: saga durable multirrecurso, fallos y compensación en intent/effect/ack; participantes, locks, esquema y validadores proporcionados. |
| 9 | Perfil entre F10 y X13: mayor integración y superficie de regresión por construir, pero menos garantías/interacciones pendientes que X13 completo. No existe una prueba independiente de nivel 9 acordada. |
| 10 | X13: integración offline/local/remota, sesiones, autorización, workers/fencing, migración y recuperación combinadas sobre legado. |
| 10+ | Superioridad material frente a X13, por ejemplo integrar además una saga multirrecurso de efectos externos y compensaciones no proporcionadas, manteniendo las garantías de X13 y probando sus interacciones. |

F10 no exige implementar desde cero participantes ni locks; F08 tiene un único
dispatcher sin leases, y F09 solo sincroniza note/tags, no stock/pagos. X13 tiene
interfaces/IPC/reloj/fixtures proporcionados, pero su coordinación y lógica remota
forman parte del trabajo. Esas diferencias deben conservarse en la rúbrica.

## 5. Alcance físico candidato, supuestos y verificación

Fuentes a modificar tras gates: `canonical/skills/sdd-spec/references/feature-level.md`,
`canonical/skills/sdd-spec/SKILL.md`, `canonical/agents/sdd.md`,
`canonical/skills/sdd-spec/references/templates.md`, `tools/test_sdd_contract.py`,
`tools/test_model_recommendations.py`; pruebas específicas adicionales solo si aportan
comportamiento discriminante, sin crear un motor de scoring artificial para testearlo.

Documentación activa candidata: `docs/catalogo.md`, `docs/uso.md`,
`docs/agentes/sdd.md`, `docs/agentes/README.md`, `docs/sdd-smoke.md` y
`docs/model-recommendations-smoke.md`. No se reescriben specs anteriores.

Los adaptadores inspeccionados no contienen una escala propia: no se prevén cambios
en `adapters/`, manifest, renderer o instaladores salvo necesidad demostrada en Design.
El render actualizará skill, referencia, plantillas y agente SDD en `generated/`
para las seis plataformas sin edición manual.

Se reutilizarán renderer, validadores y harness Python existentes. Estrategia prevista:
TDD focalizado de los contratos modificados, más regresión de políticas que deben
permanecer inalteradas y validación de reproducibilidad/enlaces. No se ha ejecutado
RED, GREEN ni ninguna suite durante Requirements.

Supuestos: el alcance es documental/de contratos del MAS, no UI ni una API de producto;
permanece en SDD. No se requieren inferencias nuevas, Docker, reevaluar entregas,
instalar agentes ni importar todo el laboratorio al catálogo canónico. La calificación
de este cambio bajo la nueva rúbrica se pospone hasta acordar su definición, para no
presentar como vigente una regla aún pendiente de aprobación.

## 6. Iteración de eficiencia de contexto — propuesta

Como usuario, quiero consumir menos contexto obligatorio de SDD sin perder las
reglas de calificación acordadas, para evitar tokens de instrucciones duplicadas,
ejemplos exhaustivos o respaldo documental que no ayudan a decidir una nota.

Esta iteración no amplía la optimización a todo el kit. Solo afecta al agente SDD,
su skill, rúbrica, plantillas/consumidores y pruebas/docs pertinentes. R01–R22 siguen
vigentes. La implementación inicial y sus resultados en `implementation-evidence-inicial.md`
y `verification-inicial.md` se conservan como baseline, no como prueba del cambio siguiente.
Los diseños/tareas con aprobación anterior corresponden a esa implementación;
no autorizan cruzar los gates pendientes de esta iteración.

### Baseline observado antes de compactar

Conteos del texto canónico, palabras separadas por whitespace y caracteres Unicode:

| Fuente | Palabras | Caracteres |
|---|---:|---:|
| `canonical/agents/sdd.md` | 1.066 | 7.580 |
| `canonical/skills/sdd-spec/SKILL.md` | 2.357 | 16.378 |
| `canonical/skills/sdd-spec/references/feature-level.md` | 1.774 | 12.303 |
| `canonical/skills/sdd-spec/references/templates.md` | 863 | 5.722 |

Agente + skill + rúbrica: **5.197 palabras / 36.261 caracteres**. Esta referencia
es bajo demanda, pero se consulta para puntuar una feature: mover texto a otro
archivo leído obligatoriamente no representa ahorro. Las seis distribuciones son
alternativas, no seis cargas simultáneas. No se dispone de tokenizer específico;
los conteos anteriores no son tokens facturados ni telemetría del host.

### H6 — Menos contexto obligatorio, mismo contrato

- **R23:** CUANDO se aplique la compactación EL SISTEMA DEBERÁ reducir palabras y
  caracteres del agente SDD, del cuerpo de su skill y de la referencia operativa
  de esfuerzo respecto al baseline anterior, conservando R01–R22; el ahorro no
  deberá proceder de borrar garantías ni empeorar legibilidad con abreviaturas opacas.
- **R24:** CUANDO agente, skill y referencia consuman la rúbrica EL SISTEMA DEBERÁ
  delegar sus detalles en una definición canónica única, manteniendo en cada
  consumidor solo las instrucciones de entrada, alcance y emisión que necesita,
  sin repetir innecesariamente escala, ejemplos o justificaciones completas.
- **R25:** CUANDO los ejemplos exhaustivos o la procedencia detallada no sean
  necesarios para decidir una nota EL SISTEMA DEBERÁ conservarlos como respaldo
  o fixtures fuera de la lectura rutinaria, sin añadir una lectura obligatoria
  equivalente; la rúbrica instalada deberá seguir siendo autosuficiente para
  anclas, descriptores, formato, reutilización, 10+, independencia y matiz de X13.
- **R26:** CUANDO se verifique la versión compacta EL SISTEMA DEBERÁ conservar
  pruebas discriminantes de R01–R22, adaptando las que dependan de ejemplos
  trasladados o prosa redundante; no deberá mantener texto innecesario solo para
  satisfacer búsquedas literales ni declarar validación empírica del razonamiento.
- **R27:** CUANDO se presente el ahorro EL SISTEMA DEBERÁ comparar antes/después
  por fuente y por escenario de carga, incluyendo cualquier nueva lectura requerida,
  distinguir conteos exactos de estimaciones y no afirmar tokens/costo real sin
  tokenizer o instrumentación del host; plantillas no deberán compensar el ahorro
  aumentando el contexto obligatorio del mismo escenario.
- **R28:** CUANDO se distribuya la compactación EL SISTEMA DEBERÁ regenerar y
  verificar los seis consumidores mediante el pipeline, preservando políticas
  operativas, historial, cambios locales ajenos y configuraciones globales.

No se exige una cuota mínima porcentual: el objetivo es una reducción comprobable
y útil, no optimizar artificialmente un contador. Una referencia de 1.000–1.200
palabras es una orientación del análisis, no un requisito que autorice omisiones.

### Verificación prevista de la iteración

Regresión/caracterización del contrato ya implementado, más TDD focalizado donde
se añadan checks nuevos de organización/eficiencia. Medición textual antes/después,
auditoría de lecturas requeridas, anclas/casos discriminantes, paridad y suites del
pipeline. No se afirma RED de esta iteración ni implementación de compactación.
No se requiere ejecutar modelos, instalar agentes, modificar tooling de medición
del kit ni tocar otros dominios para completar esta optimización.
