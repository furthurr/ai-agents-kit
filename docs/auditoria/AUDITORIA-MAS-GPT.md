# Auditoría del MAS — hallazgos y posibles soluciones

- **Fecha:** 9 de octubre de 2026.
- **Proyecto:** `ai-agents-kit` — MAS (Multi-Agent System).
- **Repositorio revisado:** `/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit`.
- **Guía de auditoría:** `/Users/pedrogomezvasquez/Desktop/agent-doctor.md`.
- **Tipo de revisión:** auditoría estática, complementada con evidencia histórica documentada.
- **Estado:** diagnóstico y recomendaciones; las soluciones no se han aplicado.

## Descripción del documento

Este informe reúne los diez hallazgos de la auditoría de las instrucciones, skills, agentes y adaptadores del MAS. Su propósito es identificar contradicciones, activaciones ambiguas, cargas innecesarias de contexto y problemas en los contratos de interacción, y proponer el cambio mínimo que preserve los requisitos del proyecto.

Cada hallazgo incluye descripción, ubicación de la evidencia, impacto, posible solución y verificación recomendada. Las rutas de evidencia son relativas al repositorio; los números de línea corresponden al contenido inspeccionado durante la auditoría y pueden cambiar con ediciones posteriores.

La prioridad expresa el orden recomendado de atención dentro de esta auditoría; no es una severidad Sonar u OWASP ni una puntuación global de salud del MAS.

## Diagnóstico

**El MAS tiene una base coherente, pero necesita ajustar sus contratos de interacción y carga de contexto antes de ampliar su complejidad.** La principal oportunidad de mejora está en cómo se activan los procedimientos, qué instrucciones prevalecen y cómo se conserva el alcance al combinar agentes y skills.

La separación de responsabilidades y el pipeline `canonical/` → adaptadores → `generated/` son fortalezas. Los problemas identificados pueden abordarse con cambios localizados, conservando los controles y responsabilidades existentes.

### Alcance revisado

- Definiciones canónicas de **6 agentes y 10 skills**.
- Adaptadores de las **6 plataformas**, con revisión detallada de configuraciones relevantes.
- Referencias de routing SDD, handoffs, workflows y documentación interactiva.
- Renderer, validador, pruebas de contratos y evidencia histórica de laboratorio y smoke tests.

### Límites del diagnóstico

- No se ejecutaron agentes, instaladores ni experimentos durante la auditoría.
- Los resultados históricos citados no acreditan el comportamiento de la fuente actual.
- La paridad de archivos no certifica funcionamiento runtime ni cumplimiento conversacional.
- No se cuantificaron mejoras de precisión, coste, tiempo o tokens para las soluciones propuestas.
- No se validaron exhaustivamente todos los metadatos y comportamientos de todos los hosts.

## Resumen de hallazgos

| ID | Prioridad | Hallazgo | Acción recomendada |
|---|---|---|---|
| H01 | Alta | El handoff de inspección exige evidencia documental que puede no existir | Simplificar el contrato de evidencia |
| H02 | Alta | La generación de Scalar puede salir del alcance autorizado | Cargar bajo demanda y explicitar alcance |
| H03 | Alta | UI y datos no separan suficientemente consulta, implementación y mantenimiento | Simplificar la selección de intención |
| H04 | Alta | Contradicción en la política de secretos del flujo Git | Eliminar la excepción contradictoria |
| H05 | Media | Claude precarga dos skills pese a la selección bajo demanda | Cargar solo la skill aplicable |
| H06 | Media | Reglas canónicas repetidas en varias capas | Simplificar y asignar una fuente responsable |
| H07 | Media | Descripciones con activación demasiado amplia | Precisar operación, objeto y resultado |
| H08 | Media | Límites y pausas no proporcionales a la operación | Usar presupuestos ampliables y continuar ramas independientes autorizadas |
| H09 | Media | Seguridad mezcla el estándar móvil con el contrato general de hallazgos | Usar referencias del estándar aplicable |
| H10 | Media | Refuerzos recientes de routing sin verificación conductual concluyente | Verificar antes de añadir reglas |

## Hallazgos detallados

### H01 — El handoff de inspección exige evidencia documental que puede no existir

- **Prioridad:** alta.
- **Acción:** simplificar.
- **Evidencia:** texto comprobado.
- **Ubicación:** `canonical/skills/documentation-orchestrator/references/handoff.md:74–77, 95–103`.

#### Descripción

La acción `inspect` permite una revisión puntual de solo lectura. Sin embargo, el contrato de respuesta exige archivos existentes dentro del `scope` documental, limitado a `.data/`, `.design/`, `.quality/` o `.security/`.

Un especialista puede inspeccionar correctamente el código de un proyecto que no tenga esa documentación y no disponer de una forma válida de acreditar el resultado. Incluso cuando la carpeta existe, la fuente real de un hallazgo puede estar en código o configuración fuera de ella.

#### Impacto

- Puede bloquear la entrega de una inspección válida.
- Dificulta citar la fuente real del diagnóstico.
- Confunde el alcance de escritura con el conjunto de fuentes admisibles para lectura y evidencia.

#### Posible solución mínima

Diferenciar el contrato de evidencia según la acción:

- **`inspect`:** admitir fuentes existentes dentro del proyecto y pertinentes al dominio, aunque estén fuera de la carpeta documental.
- **Acciones de escritura:** exigir evidencia de artefactos dentro del `write_scope` autorizado.

Conservar la comprobación de rutas, raíces y symlinks, así como los límites efectivos del receptor. Ajustar también el validador del contrato si reproduce la restricción actual.

#### Verificación recomendada

- Inspeccionar un proyecto sin la carpeta documental del dominio y devolver evidencia de código sin crear archivos.
- Inspeccionar un proyecto documentado y citar una fuente real fuera de la carpeta documental.
- Comprobar que una acción de escritura no puede acreditarse mediante un archivo fuera del `write_scope`.
- Mantener el rechazo de evidencia que escape del proyecto.

### H02 — La generación de Scalar puede salir del alcance autorizado de una operación documental

- **Prioridad:** alta.
- **Acción:** cargar bajo demanda.
- **Evidencia:** texto comprobado.
- **Ubicaciones:**
  - `canonical/skills/data-api/SKILL.md:185–200`.
  - `canonical/skills/data-api/references/api-docs.md:35–47`.
  - `canonical/skills/documentation-orchestrator/references/handoff.md:54–58, 83–86`.

#### Descripción

El flujo de datos exige crear un lanzador al documentar una API REST y propone la ubicación `scripts/api-docs.<extensión>`. Un handoff de datos, en cambio, autoriza escritura únicamente en `.data/`.

El receptor debe elegir entre incumplir el entregable de su skill o escribir fuera del alcance recibido. La ejecución local desde el orquestador también encuentra tensión con su límite de documentación e índices canónicos.

#### Impacto

- Contrato de escritura incompatible con un entregable obligatorio.
- Posible ampliación no autorizada del conjunto de archivos modificados.
- Generación de herramientas auxiliares que pueden no ser necesarias para la petición.

#### Posible solución mínima

Exigir que el lanzador esté incluido expresamente en el plan autorizado. Para handoffs restringidos a `.data/`, permitir alojarlo allí o informar que su generación externa requiere ampliar el alcance.

Conservar las comprobaciones del contrato, la ejecución manual y la prohibición de instalar o iniciar servidores durante la sesión documental. El problema es la obligatoriedad y ubicación del artefacto, no esos controles.

#### Verificación recomendada

- Confirmar que una operación limitada a `.data/` no escribe en `scripts/`.
- Documentar una API sin autorización para añadir herramientas locales y finalizar con un resultado válido.
- Generar el lanzador cuando su creación y ruta estén expresamente autorizadas.
- Comprobar que un lanzador sin OpenAPI válido no instala dependencias ni inicia servidores.

### H03 — UI y datos no separan suficientemente consulta, implementación y mantenimiento documental

- **Prioridad:** alta.
- **Acción:** simplificar.
- **Evidencia:** texto comprobado.
- **Ubicaciones:**
  - `canonical/skills/ui-design/SKILL.md:41–46, 105–147`.
  - `canonical/skills/data-api/SKILL.md:66–71, 143–183`.
  - Contraste: `canonical/skills/architecture/SKILL.md:57–67`.

#### Descripción

UI y datos incluyen instrucciones generales como «si no existe, créala» y flujos de extracción, deuda y sincronización. Arquitectura, calidad y seguridad ya distinguen explícitamente las consultas de solo lectura.

Esta diferencia deja ambiguo si explicar un DTO o hacer un cambio visual localizado exige iniciar mantenimiento documental.

#### Impacto

- Creación de carpetas o artefactos no solicitados.
- Propuestas y pausas documentales en tareas puntuales.
- Comportamiento desigual entre dominios ante intenciones equivalentes.

#### Posible solución mínima

Añadir al inicio de UI y datos una selección breve de intención:

1. **Consulta o inspección:** lectura y respuesta, sin persistencia.
2. **Implementación puntual:** fuentes afectadas y verificación proporcional; documentación cuando el cambio o las instrucciones del proyecto lo exijan.
3. **Documentación o sincronización:** flujo documental autorizado.

No hace falta crear otro router. Basta con precisar cuándo corresponde el flujo existente y condicionar la creación de carpetas a una operación documental autorizada.

#### Verificación recomendada

- Explicar un DTO sin crear `.data/`.
- Explicar estilos de un componente sin crear `.design/`.
- Realizar un cambio puntual autorizado sin activar extracción global.
- Inicializar documentación explícitamente solicitada conservando las decisiones y controles pertinentes.

### H04 — Contradicción en la política de secretos del flujo Git

- **Prioridad:** alta.
- **Acción:** eliminar la excepción contradictoria.
- **Evidencia:** texto comprobado; deuda ya reconocida en el proyecto.
- **Ubicaciones:**
  - `canonical/skills/git-commit/SKILL.md:34, 83–106`.
  - `README.md:174`.
  - `docs/mejoras.md:138–147`.

#### Descripción

La skill permite incluir archivos sensibles mediante autorización y pide no bloquear el commit. El README establece «Nunca commits de secretos». El backlog reconoce pendiente la unificación de esa política.

El flujo no diferencia con suficiente claridad una configuración legítima con nombre sospechoso de un archivo que contiene un secreto real.

#### Impacto

- Interpretaciones incompatibles sobre qué puede incluirse en un commit.
- Posibilidad de tratar una autorización conversacional como excepción a la prohibición del proyecto.
- Avisos basados en nombres que no distinguen configuración pública, placeholders y credenciales reales.

#### Posible solución mínima

Conservar la decisión del usuario para **archivos potencialmente sensibles**, pero excluir secretos reales conforme al contrato del proyecto. Informar su ubicación sin mostrar valores.

Unificar esa distinción en la skill y sus documentos consumidores. No crear otro registro paralelo para una deuda que ya está reconocida.

#### Verificación recomendada

- Usar un fixture sintético de credencial y comprobar que no se incluye aunque se solicite su inclusión.
- Confirmar que una configuración pública o con placeholders no se clasifica automáticamente como secreto real.
- Comprobar que los mensajes no reproducen valores sensibles.

### H05 — Claude precarga dos skills donde el agente exige seleccionar solo la aplicable

- **Prioridad:** media.
- **Acción:** cargar bajo demanda.
- **Evidencia:** configuración comprobada y documentación oficial.
- **Ubicaciones:**
  - `adapters/claude/agents/git-release-manager.json:18–21`.
  - `canonical/agents/git-release-manager.md:35–36`.

#### Descripción

El adaptador declara `git-commit` y `release-management` en el campo `skills`. Claude Code documenta que ese campo inyecta el contenido completo al iniciar el subagente. El agente, en cambio, pide cargar únicamente la skill aplicable.

#### Impacto

- Una consulta Git o un commit recibe también el procedimiento completo de releases.
- Existe una divergencia entre la carga selectiva declarada y la configuración real.
- Se añade contexto ajeno a la operación actual. Su efecto sobre coste o precisión no fue medido.

#### Posible solución mínima

Retirar la precarga conjunta y seleccionar la skill durante la ejecución, manteniendo disponible la herramienta `Skill`. Cuando una release incluya commit, cargar ambos procedimientos en el momento pertinente.

#### Verificación recomendada

- Invocar el agente para un commit y comprobar que no precarga el procedimiento de release.
- Invocarlo para una release con commit y verificar disponibilidad de ambas skills cuando corresponda.
- Confirmar que las aprobaciones de commit, tag y push se mantienen.

### H06 — Reglas canónicas repetidas en varias capas

- **Prioridad:** media.
- **Acción:** simplificar.
- **Evidencia:** texto comprobado.
- **Ubicaciones:**
  - Bloques de identidad del MAS en los seis agentes y diez skills.
  - Bloques de contexto compartido en los seis agentes.
  - `canonical/agents/sdd.md:43–90`.
  - `canonical/skills/sdd-spec/SKILL.md:27–144`.
  - Referencias `scope-depth.md` y `agent-routing.md` de `sdd-spec`.

#### Descripción

Se reiteran decisiones sobre profundidad, opciones retiradas, selección de ejecutor, aprobaciones y contexto, además de existir referencias responsables de esas reglas.

La repetición no es un defecto por longitud en sí misma: el problema es mantener una misma regla normativa en varios lugares sin una necesidad diferenciada.

#### Impacto

- Una modificación exige actualizar múltiples archivos.
- Mayor probabilidad de divergencias entre agente, skill y referencias.
- Parte del contenido se duplica al cargar agente y skill.

#### Posible solución mínima

Mantener una fuente responsable por regla:

- **Agente:** responsabilidad, límites, selección de skill y finalización.
- **Skill o referencia responsable:** procedimiento normativo.
- **Consumidores:** resumen mínimo necesario y referencia directa.

Conservar en los documentos principales los controles esenciales. No sustituir la repetición por una cadena profunda de referencias ni extraer cada frase a un archivo distinto.

#### Verificación recomendada

- Comparar los contratos antes y después para confirmar que se conservan requisitos y límites.
- Revisar que las referencias directas existan en las distribuciones.
- Ajustar pruebas que exijan frases duplicadas para que comprueben la regla en su fuente responsable.
- Evaluar casos representativos sin asumir que reducir texto mejora automáticamente el comportamiento.

### H07 — Descripciones con activación demasiado amplia

- **Prioridad:** media.
- **Acción:** simplificar.
- **Evidencia:** ambigüedad comprobada en el texto; frecuencia de activaciones incorrectas pendiente de evaluación.
- **Ubicaciones:**
  - `canonical/skills/ui-design/SKILL.md:4–10`: «cualquier aspecto visual».
  - `canonical/skills/data-api/SKILL.md:4–13`: «TODO», «modelos» y «repositorios».
  - `canonical/skills/security/SKILL.md:11–13`: «auditoría» y «buenas prácticas».
  - `canonical/skills/sdd-spec/SKILL.md:7–9`: «diseñar arquitectura» y lista de palabras clave.

#### Descripción

Las descripciones contienen términos compartidos por otros dominios y por consultas generales. Por ejemplo, auditar instrucciones de agentes no implica auditar seguridad de aplicaciones, y explicar arquitectura no implica diseñar una feature mediante SDD.

#### Impacto

- Ambigüedad de selección entre skills.
- Posible carga de procedimientos ajenos a la intención de la tarea.
- Dificultad para distinguir consultas cercanas que no requieren activar el workflow.

#### Posible solución mínima

Expresar **operación, objeto y resultado esperado**, sustituyendo términos genéricos por condiciones específicas. Añadir una exclusión breve solo cuando resuelva un solapamiento concreto.

No cargar todas las skills de un dominio por defecto ni añadir un nuevo router antes de comprobar que hace falta.

#### Verificación recomendada

Evaluar sesiones independientes con:

- Casos donde cada skill deba activarse.
- Casos próximos donde no deba hacerlo.
- Peticiones con términos ambiguos como «modelo», «auditoría» o «arquitectura».

Registrar selección correcta, falsos positivos y skills necesarias omitidas. No presentar la ambigüedad textual como una tasa de fallos medida.

### H08 — Límites y pausas no proporcionales a la operación

- **Prioridad:** media.
- **Acción:** simplificar.
- **Evidencia:** texto comprobado.
- **Ubicaciones:**
  - `canonical/skills/project-navigator/SKILL.md:85–86`.
  - `canonical/skills/documentation-orchestrator/SKILL.md:130–131`.
  - `canonical/skills/documentation-orchestrator/references/workflows.md:176–177`.

#### Descripción

Navigator establece máximos de capas y archivos por pregunta sin excepción explícita para investigaciones que necesiten más fuentes. El orquestador exige preguntar antes de continuar con ramas independientes cuando una se bloquea.

#### Impacto

- Una consulta de impacto transversal puede quedar limitada artificialmente.
- Una sincronización de varios dominios ya autorizados puede detenerse aunque el trabajo restante sea independiente.
- Se añaden intervenciones humanas que no necesariamente cambian una decisión relevante.

#### Posible solución mínima

- Tratar el número de archivos como presupuesto inicial ampliable con justificación, manteniendo lectura selectiva.
- Continuar dominios independientes ya autorizados, informando el bloqueo y sin declarar éxito global.
- Pedir decisión cuando cambien dependencias, alcance, coste relevante o autorización.

Las aprobaciones SDD y por micro-paso de remediación son requisitos explícitos del MAS. Esta propuesta no implica retirarlas indiscriminadamente.

#### Verificación recomendada

- Resolver una consulta transversal que necesite más de tres archivos, sin volcar el repositorio completo.
- Simular el bloqueo de un dominio y comprobar que los independientes autorizados pueden completarse.
- Confirmar que una dependencia bloqueada impide ejecutar trabajos que dependan de ella.
- Mantener un informe final que identifique resultados parciales y pendientes.

### H09 — Seguridad mezcla el estándar móvil con el contrato general de hallazgos

- **Prioridad:** media.
- **Acción:** simplificar.
- **Evidencia:** texto comprobado.
- **Ubicaciones:**
  - `canonical/skills/security/SKILL.md:45–55, 118–130`.
  - `canonical/skills/security/references/templates.md:32–38`.

#### Descripción

La skill permite aplicar ASVS y otros estándares en tecnologías no móviles, pero declara que cada hallazgo se referencia con MASVS + MASWE + CWE. La plantilla mantiene ese formato móvil.

#### Impacto

- Una auditoría backend o web puede forzar referencias móviles que no corresponden.
- Riesgo de mapeos artificiales o referencias inventadas para completar la plantilla.
- Inconsistencia entre la tecnología detectada y el contrato de salida.

#### Posible solución mínima

Exigir el **estándar aplicable y su identificador**, añadiendo CWE cuando exista un mapeo verificable. Conservar MASVS/MASWE para los casos móviles pertinentes.

La plantilla debe aceptar referencias del estándar seleccionado y permitir declarar que un mapeo adicional no está disponible.

#### Verificación recomendada

- Registrar un hallazgo móvil con referencias móviles pertinentes.
- Registrar un hallazgo backend o web sin exigir MASVS/MASWE.
- Confirmar que no se inventan identificadores cuando no existe un mapeo verificable.

### H10 — Refuerzos recientes de routing sin verificación conductual concluyente

- **Prioridad:** media.
- **Acción:** conservar controles y verificar antes de añadir reglas.
- **Evidencia:** resultados históricos documentados e inspección de pruebas; eficacia actual pendiente de evaluación.
- **Ubicaciones:**
  - `.sdd/specs/recomendacion-agente-por-dominio/followup-smoke.md:22–31, 43–57`.
  - `docs/sdd-smoke.md:49–64`.
  - `docs/code-review-smoke.md:3–5`.
  - `tools/test_sdd_contract.py:43–76, 128–167`.

#### Descripción

La evidencia histórica registra que:

- R04 enumeró candidatos fuera del conjunto permitido.
- Una variante de R10 intentó editar desde SDD pese a la selección del especialista.
- Los refuerzos posteriores no tienen repetición conversacional concluyente.
- Las pruebas de contratos revisadas comprueban texto y propagación, no decisiones reales del modelo.

El propio proyecto distingue correctamente estos límites. Los fallos históricos no deben presentarse como fallos confirmados de la última versión ni los bloqueos como resultados favorables.

#### Impacto

Conservar una regla en todos los artefactos no demuestra que se cumpla durante la ejecución. Añadir instrucciones sin verificar el resultado puede aumentar complejidad sin resolver la causa.

#### Posible solución mínima

Repetir los casos afectados con la fuente actual, host y modelo registrados, incluyendo variantes naturales y contextos independientes. Antes de reforzar nuevamente el prompt, distinguir si el fallo proviene de instrucciones, herramientas, permisos o diseño del caso.

#### Verificación recomendada

- Repetir R04 y las variantes de R10 con la fuente actual.
- Completar R06, R07 y R11 cuando el entorno permita obtener una respuesta concluyente.
- Registrar prompt, contexto, host, versión, modelo, fuente probada, herramientas intentadas y respuesta sanitizada.
- Clasificar resultados como PASS, FAIL o bloqueado sin inferir éxito de una ejecución incompleta.
- Comparar modificaciones en contextos independientes y con repetición suficiente para observar variabilidad.

## Elementos que conviene conservar

| Elemento | Justificación |
|---|---|
| `canonical/` + adaptadores + `generated/` | Evita mantener procedimientos separados por plataforma. |
| Especialistas con fronteras de dominio | Hace identificable la responsabilidad y limita ampliaciones accidentales. |
| Separación de consulta y mantenimiento ya presente en arquitectura, calidad y seguridad | Es una buena base para homogeneizar UI y datos. |
| Contexto selectivo y degradación a fuentes directas | Permite continuar cuando los índices faltan o no son fiables. |
| Handoff sin duplicar la ejecución | Evita realizar la misma operación en origen y destino. |
| Distinción entre `gate_state` y autorización efectiva | Evita atribuir permisos a metadatos copiados. |
| Modos SDD proporcionales y cierre con evidencia | Mantiene trazabilidad sin exigir siempre el flujo completo. |
| Separación de pruebas estáticas y runtime en la documentación | Comunica correctamente el alcance de la evidencia disponible. |

## Verificación de la auditoría

### Comprobaciones realizadas

- Se confirmó el inventario de **6 agentes, 10 skills y 6 plataformas**.
- Se comprobaron nombres y descripciones canónicos contra las restricciones relevantes de Agent Skills: **sin incumplimientos detectados**.
- Se realizaron **270 comparaciones de contenido** entre fuentes y distribuciones:
  - Skills con sustituciones.
  - Recursos distribuidos.
  - Cuerpos de agentes con sustituciones y sufijos.
  - **Resultado: ninguna discrepancia.**
- Se consultó documentación oficial actual de Agent Skills, Claude Code, OpenCode y Kiro para contrastar formato, precarga y permisos.

Estas comprobaciones no equivalen a validar exhaustivamente todos los metadatos de los hosts ni a certificar comportamiento runtime. La comparación de cuerpos de agentes no es una validación completa de su frontmatter.

### Verificaciones pendientes

- Evaluación conversacional de activación y routing con la fuente actual.
- Verificación de permisos efectivos y límites de escritura en cada host pertinente.
- Pruebas de los contratos de inspección y Scalar una vez corregidos.
- Comparación de comportamiento antes y después de simplificar instrucciones.
- Medición de coste, tiempo o tokens solo si se pretende afirmar mejoras en esas dimensiones.

## Orden mínimo recomendado de corrección

1. Resolver los contratos incompatibles de **evidencia de inspección, Scalar y secretos**: H01, H02 y H04.
2. Homogeneizar la separación entre **consulta, implementación y mantenimiento**: H03.
3. Corregir la **precarga de Claude** y reducir duplicación normativa: H05 y H06.
4. Afinar descripciones, presupuestos proporcionales y referencias de seguridad: H07, H08 y H09.
5. Repetir los casos conductuales afectados y evaluar los cambios frente a una referencia: H10.

Este orden orienta una futura remediación; no autoriza por sí mismo cambios de código, instalación, commit, push o release.

## Referencias oficiales consultadas

Consultadas durante la auditoría del 9 de octubre de 2026:

- [Agent Skills — Specification](https://agentskills.io/specification).
- [Claude Code — Create custom subagents](https://code.claude.com/docs/en/sub-agents): el campo `skills` precarga contenido completo; formato y herramientas de subagentes.
- [OpenCode — Permissions](https://opencode.ai/docs/permissions/): permisos, patrones y configuración por agente.
- [Kiro — Agent configuration reference](https://kiro.dev/docs/custom-agents/configuration-reference/): formato de agentes, herramientas, recursos y permisos.

Las reglas del documento adjunto se utilizaron como criterios de análisis. No se ejecutaron instrucciones ni scripts de los documentos auditados por el mero hecho de leerlos.

## Conclusión

Conviene mejorar la coherencia del MAS existente antes de añadir agentes, routers o memoria adicional. Los diez hallazgos pueden abordarse con cambios localizados, conservando sus controles y responsabilidades. Las mejoras conductuales deberán demostrarse mediante evaluaciones pertinentes, sin confundir validez de formato con utilidad real.
