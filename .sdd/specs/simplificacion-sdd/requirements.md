# Requisitos — Simplificación del agente SDD

- Modo SDD: standard
- Fase: 1 — Requirements
- Estado: aprobado
- Gate 1: aprobado por el usuario mediante «procede» tras presentar los requisitos
- Tipo de trabajo: feature
- Intención: implementación, después de aprobar los gates correspondientes
- Estrategia de pruebas prevista: regresión del contrato; sin ciclo TDD productivo nuevo por cambios exclusivamente documentales. La selección definitiva corresponde a Design.

## Objetivo y motivación

Reducir las opciones y la carga operativa del MAS retirando la profundidad `deep`
y la estrategia diferenciada TDD estricto. El usuario confirma que ambas se
eliminan incluso como opciones bajo petición explícita. Conservar SDD proporcional,
TDD focalizado y verificación con evidencia.

La motivación es la ausencia de mejoras observadas por el usuario con estas
opciones. No se establece que un nivel alto de LLM sustituya pruebas, trazabilidad
o revisión, ni se condiciona el contrato a un modelo o proveedor concreto.

## Contexto confirmado

- El contrato actual reconoce `direct`, `lite`, `standard` y `deep`.
- Actualmente `deep` y TDD estricto ya son opt-in; no basta con desactivarlos por defecto.
- Las fuentes compartidas están en `canonical/`, la adaptación por host en
  `adapters/` y las salidas regenerables en `generated/`.
- El repositorio contiene cambios locales ajenos que deben preservarse.
- Evidencia de alcance: `canonical/agents/sdd.md`,
  `canonical/skills/sdd-spec/SKILL.md`, sus referencias y adapters SDD de las cinco
  plataformas; documentación pública y `tools/test_sdd_contract.py`.

## Historias y criterios de aceptación

### R1 — Tres profundidades disponibles

Como usuario, quiero elegir una profundidad proporcional sin una variante documental más pesada.

- R1.1: EL SISTEMA DEBERÁ reconocer exactamente `direct`, `lite` y `standard` como profundidades SDD disponibles para trabajo nuevo.
- R1.2: CUANDO el usuario solicite `deep` EL SISTEMA DEBERÁ informar que se retiró, proponer `standard` y esperar aceptación antes de iniciar ese flujo, sin convertir la solicitud silenciosamente.
- R1.3: EL SISTEMA DEBERÁ conservar los criterios vigentes de elegibilidad de `direct` y `lite`, y usar `standard` cuando no pueda demostrarse esa elegibilidad.
- R1.4: EL SISTEMA DEBERÁ conservar Quick Plan como operación obligatoria y exclusiva de `lite`.

### R2 — Testing adaptativo sin TDD estricto

Como usuario, quiero pruebas relevantes sin exigir un ciclo por cada incremento interno de producción.

- R2.1: EL SISTEMA DEBERÁ conservar las estrategias sin test nuevo justificado, caracterización/regresión y TDD focalizado, sin ofrecer TDD estricto como estrategia diferenciada.
- R2.2: CUANDO el usuario solicite TDD estricto EL SISTEMA DEBERÁ informar que se retiró, proponer TDD focalizado y esperar aceptación antes de aplicar esa sustitución.
- R2.3: CUANDO cambie comportamiento observable EL SISTEMA DEBERÁ seleccionar TDD focalizado por comportamiento o criterio relevante, salvo la estrategia de regresión/caracterización o una excepción de pruebas documentada que corresponda al caso.
- R2.4: CUANDO se declare evidencia TDD EL SISTEMA DEBERÁ exigir un RED observado por la razón esperada, GREEN y evidencia de la suite, sin presentar tests retroactivos como TDD.
- R2.5: EL SISTEMA DEBERÁ mantener profundidad SDD y estrategia de pruebas como ejes independientes, sin desactivar pruebas por elegir `direct` o `lite`.

### R3 — Calidad y proporcionalidad conservadas

Como usuario, quiero simplificar el proceso sin perder sus controles de calidad.

- R3.1: EL SISTEMA DEBERÁ conservar Gate 0 y las recomendaciones informativas por próxima operación, los Gates 1–4 de `standard` y el flujo reducido vigente de `lite`.
- R3.2: EL SISTEMA DEBERÁ conservar EARS, trazabilidad, quality-bar e integrity-gate, sin marcar tareas completas ni cerrar cobertura sin evidencia real.
- R3.3: CUANDO la intención sea solo planificación EL SISTEMA DEBERÁ detenerse sin implementar.
- R3.4: CUANDO un comportamiento justifique pruebas basadas en propiedades EL SISTEMA DEBERÁ permitirlas por esa necesidad, sin depender de `deep` ni exigir una estrategia estricta.
- R3.5: EL SISTEMA DEBERÁ conservar los límites documentales vigentes de `standard`, sin trasladar automáticamente la carga adicional de `deep` al flujo normal.

### R4 — Compatibilidad con specs históricas

Como usuario, quiero retomar trabajo existente sin migraciones o aprobaciones inventadas.

- R4.1: CUANDO una spec histórica declare `deep` o TDD estricto EL SISTEMA DEBERÁ identificar la opción retirada y solicitar aceptación para continuar con `standard` o TDD focalizado, respectivamente, antes de modificar la spec o continuar su ejecución.
- R4.2: EL SISTEMA DEBERÁ preservar los artefactos históricos, sus evidencias y decisiones, sin migrarlos en lote, borrar pruebas ni inventar aprobaciones o resultados pasados.
- R4.3: SI los marcadores de fase, modo, estado o aprobación son ambiguos ENTONCES EL SISTEMA DEBERÁ pedir aclaración antes de reanudar, sin inferir aprobación por existencia de archivos.
- R4.4: EL SISTEMA DEBERÁ conservar soporte de rutas planas y agrupadas y la identidad por ruta relativa completa.

### R5 — Contrato consistente en la distribución

Como mantenedor, quiero que todas las plataformas expongan las mismas opciones admitidas.

- R5.1: EL SISTEMA DEBERÁ publicar el contrato de tres profundidades y testing adaptativo actualizado de forma consistente en agente, skill, referencias, adapters, documentación de uso y salidas de las cinco plataformas soportadas.
- R5.2: EL SISTEMA DEBERÁ permitir menciones de `deep` o TDD estricto solo cuando expliquen su retirada, compatibilidad histórica o casos de rechazo, sin presentarlos como opciones vigentes.
- R5.3: EL SISTEMA DEBERÁ disponer de comprobaciones del contrato para las opciones admitidas, solicitudes de opciones retiradas y controles que permanecen vigentes.
- R5.4: EL SISTEMA DEBERÁ preservar cambios locales ajenos y producir salidas reproducibles a partir de sus fuentes, sin editar manualmente artefactos generados.

## Fuera de alcance

- Cambiar el modelo del host o basar garantías en un proveedor concreto.
- Retirar TDD focalizado, PBT pertinente, gates o verificación.
- Alterar otros agentes o estrategias de revisión del MAS.
- Migrar specs históricas o snapshots legacy de forma automática.
- Instalar el kit en configuraciones globales, hacer commits, push o releases.

## Decisiones que Gate 1 ratifica

Las solicitudes de opciones retiradas y la reanudación de specs que las declaren
requieren aceptar la alternativa; no habrá conversión silenciosa. Las menciones
históricas explicativas siguen siendo válidas. La implementación actualizará las
fuentes y distribución del repositorio, no la configuración cargada por esta sesión.

## Estado de verificación

Solo se investigó el contrato y se redactaron requisitos. No se ejecutaron pruebas,
no se modificó el agente y no se declara implementado ningún criterio.
