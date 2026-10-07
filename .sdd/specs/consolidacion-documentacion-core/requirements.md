# Consolidación de documentación core

- Modo SDD: standard
- Trabajo: exploración de una propuesta de cambio del MAS
- Intención: solo planificación; implementación no autorizada
- Fase: 1 — Requirements
- Estado: aprobado
- Gate aprobado: Gate 1 — usuario indicó «procede» el 2026-10-07
- Enmienda R5 aprobada: usuario indicó «procede» a la política de migración segura el 2026-10-07

## Objetivo y motivación

Simplificar los puntos de entrada del MAS retirando los agentes independientes
`architecture` y `project-navigator`, sin retirar sus skills ni perder sus
capacidades. `documentation-orchestrator` asume su responsabilidad documental y
de investigación; los demás agentes descubren y consumen el contexto del proyecto
directamente, sin depender de un handoff para leerlo.

Esta es una propuesta para aprobación, no una decisión ya implementada.

## Evidencia del estado actual

- `canonical/manifest.json` declara agentes y skills en listas separadas.
- `canonical/agents/documentation-orchestrator.md:21-22,38-40` ya permite
  ejecutar skills localmente o derivar a un agente real.
- `canonical/skills/documentation-orchestrator/SKILL.md:31-38,54-67` reconoce
  ambas carpetas como core, pero sus modos actuales priorizan mantenimiento.
- `canonical/skills/documentation-orchestrator/references/handoff.md:35-65`
  y `tools/handoff_contract.py:26-32` incluyen los agentes como targets.
- `canonical/skills/sdd-spec/references/navigator-context.md:8-47,49-86`
  proporciona consumo selectivo, frescura y degradación para SDD.
- `tools/validate.py:167-183` comprueba agentes canónicos huérfanos;
  `tools/render.py:74-108` genera agentes y skills por separado.
- `tools/install_preflight.py:99-146` detecta agentes instalados no declarados,
  sin eliminarlos automáticamente.
- `.architecture/README.md` orienta sobre el pipeline, pero no declara un
  baseline Git verificable; no se usa como prueba de vigencia.

La revisión fue de lectura; no se ejecutaron pruebas ni instaladores.

## Historias y criterios de aceptación

### R1 — Conservar especialización con menos agentes

Como usuario del kit, quiero una única entrada documental sin perder capacidades.

- R1.1: CUANDO se consulte el catálogo vigente EL SISTEMA DEBERÁ ofrecer
  `documentation-orchestrator` como agente responsable de arquitectura y navegación,
  sin ofrecer `architecture` o `project-navigator` como agentes independientes.
- R1.2: CUANDO se distribuyan las capacidades core EL SISTEMA DEBERÁ conservar las
  skills `architecture` y `project-navigator` separadas y utilizables.
- R1.3: EL SISTEMA DEBERÁ conservar `.architecture/` y `.navigator/` como destinos
  canónicos distintos, sin duplicarlos en una carpeta documental nueva.

### R2 — Absorber las entradas de trabajo

Como usuario, quiero solicitar mantenimiento o consultas core a documentación.

- R2.1: CUANDO se solicite documentar, auditar o sincronizar arquitectura
  EL SISTEMA DEBERÁ atender la solicitud desde documentación aplicando la skill
  `architecture` y sus límites.
- R2.2: CUANDO se solicite navegar o investigar el proyecto EL SISTEMA DEBERÁ
  permitir una respuesta de solo lectura desde documentación mediante la skill
  `project-navigator`, sin exigir crear o actualizar índices.
- R2.3: CUANDO se solicite bootstrap o actualización de índices EL SISTEMA DEBERÁ
  obtener la autorización de escritura aplicable y respetar el alcance aprobado.
- R2.4: EL SISTEMA DEBERÁ cargar las skills especialistas bajo demanda, sin exigir
  cargar todas las skills documentales para cada consulta.

### R3 — Descubrimiento y consumo por otros agentes

Como agente del MAS, quiero conocer el contexto disponible sin un intermediario.

- R3.1: CUANDO un agente necesite contexto del proyecto EL SISTEMA DEBERÁ indicar
  qué aportan `.architecture/` y `.navigator/`, sus puntos de entrada y cómo
  solicitar su mantenimiento a documentación.
- R3.2: CUANDO el contexto sea relevante EL SISTEMA DEBERÁ permitir su consulta
  directa, selectiva y de solo lectura sin un handoff obligatorio.
- R3.3: SI el contexto está ausente, es ambiguo, incompleto o no tiene frescura
  verificable ENTONCES EL SISTEMA DEBERÁ continuar con fuentes directas y comunicar
  la limitación pertinente, sin generar documentación ni índices automáticamente.
- R3.4: CUANDO un índice aporte una afirmación relevante EL SISTEMA DEBERÁ tratar
  código, steering y contratos canónicos como autoridad y validar esa afirmación
  según el trabajo; un índice desfasado solo podrá aportar pistas.

### R4 — Preservar límites y autorizaciones

Como usuario, quiero que la consolidación no amplíe permisos de forma implícita.

- R4.1: MIENTRAS documentación ejecuta capacidades core EL SISTEMA DEBERÁ conservar
  la prohibición de modificar código de producto o ejecutar refactors.
- R4.2: CUANDO una operación requiera un gate de una skill EL SISTEMA DEBERÁ
  conservar ese gate, sin considerar una recomendación de modelo como autorización.
- R4.3: CUANDO se proponga exportar contexto a instrucciones del proyecto
  EL SISTEMA DEBERÁ solicitar la confirmación específica exigida por Navigator.
- R4.4: EL SISTEMA DEBERÁ conservar los agentes y contratos de otros dominios,
  salvo los ajustes de consumo de contexto y referencias necesarios para esta propuesta.

### R5 — Catálogo, contratos y actualización coherentes

Como mantenedor, quiero evitar referencias activas a receptores inexistentes.

- R5.1: CUANDO se retire un agente core EL SISTEMA DEBERÁ mantener coherentes
  catálogo, fuentes, adaptadores, distribuciones, contratos, pruebas y guías activas
  en todas las plataformas soportadas.
- R5.2: SI una solicitud o handoff usa un identificador retirado ENTONCES
  EL SISTEMA DEBERÁ informar que ya no es un receptor vigente e indicar documentación
  como nueva entrada, sin ejecutar una escritura ni inferir autorización.
- R5.3: CUANDO se autorice una actualización con migración de agentes retirados
  EL SISTEMA DEBERÁ retirar del directorio activo los agentes antiguos
  verificablemente administrados por el kit y sin modificaciones, después de
  crear y verificar un respaldo fuera de las rutas que escanea el host.
- R5.4: EL SISTEMA DEBERÁ preservar specs y evidencia históricas que mencionen los
  agentes anteriores, distinguiéndolas de instrucciones operativas vigentes.
- R5.5: SI un candidato está personalizado o su procedencia no es verificable
  ENTONCES EL SISTEMA DEBERÁ conservarlo hasta obtener confirmación específica
  sobre ese archivo y respaldarlo antes de una retirada autorizada.
- R5.6: SI el respaldo o la validación del destino falla ENTONCES EL SISTEMA
  DEBERÁ conservar el candidato activo y no declarar la migración completada.
- R5.7: CUANDO se ejecute un dry-run EL SISTEMA DEBERÁ mostrar clasificación,
  respaldo y acciones previstas sin modificar archivos ni metadatos instalados.
- R5.8: EL SISTEMA DEBERÁ distinguir instalación vigente de migración completa,
  preservar archivos ajenos no seleccionados y permitir restaurar los respaldos.

## Fuera de alcance

- Implementar cambios, retirar archivos o actualizar instalaciones en esta fase.
- Renombrar `documentation-orchestrator` a `documentation`.
- Fusionar las skills core o alterar sus formatos persistidos.
- Consolidar agentes de UI, datos, calidad/seguridad, SDD o releases.
- Cambiar la política de avisos de modelo del kit.
- Bootstrap/sync de la documentación de dominio de este repositorio.
- Reescribir specs históricas o modificar la spec activa
  `recomendacion-agente-por-dominio`.

## Supuestos y decisiones para Gate 1

1. Se propone que documentación absorba también consultas puntuales de navegación
   y arquitectura, no solo mantenimiento. Requiere aprobación de R2.
2. Se propone conservar el identificador `documentation-orchestrator`.
3. Se propone una retirada sin aliases ejecutables de los agentes anteriores:
   orientación de migración y diagnóstico, no delegación silenciosa.
4. El contrato compartido no obliga a leer carpetas completas en cada petición.

## Riesgos y coordinación

- La spec `recomendacion-agente-por-dominio` tiene implementación en progreso y
  puede tocar SDD, sus tests, documentación y `generated/`. Antes de una futura
  implementación se debe revisar el estado real y coordinar cambios; esta spec no
  amplía ni hereda sus autorizaciones.
- El working tree tenía cambios ajenos en esa spec,
  `.sdd/specs/laboratorio-evaluacion-sdd/tasks.md` y
  `.opencode/commands/lab-pilot.md`; se preservan.
- La frontera por carpeta es contractual; no debe describirse como sandbox si
  los permisos de la plataforma no lo garantizan.
- Las instalaciones existentes pueden seguir mostrando agentes retirados hasta
  que se complete la migración autorizada; una instalación con candidatos
  pendientes no debe presentarse como migración completada.

## Estrategia preliminar de verificación

Solo planificación: no hay comportamiento implementado ni RED/GREEN declarado.
El diseño deberá concretar pruebas de catálogo y contratos, consumo mínimo,
fallos/degradación, render por plataforma e instalación con residuos. Si se
autoriza implementación, los comportamientos modificados usarán TDD focalizado;
los comportamientos que deben preservarse usarán regresión/caracterización.

## Gate 1

Aprobado por el usuario mediante «procede» el 2026-10-07. Permite pasar a
Design; no autoriza implementar ni retirar agentes. Los supuestos propuestos
forman parte del alcance aprobado.

Enmienda posterior aprobada: la retirada con respaldo sustituye la política inicial
de solo advertir. La aprobación autoriza diseñar esa migración, no ejecutarla en
la instalación del usuario.
