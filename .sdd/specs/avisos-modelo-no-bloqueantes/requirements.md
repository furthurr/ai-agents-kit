# Avisos de modelo sin pausas redundantes

- Modo SDD: standard
- Tipo: feature (ajuste del contrato conversacional del MAS)
- Intención: implementación
- Fase: Requirements
- Estado: aprobado
- Gate aprobado: Gate 1 — usuario: «procede»

## Problema y objetivo

El usuario solicita eliminar interacciones en las que el agente anuncia el proceso
y recomienda cambiar de modelo, pero no realiza el trabajo hasta recibir
«continúa». El ejemplo aportado es una consulta visual puntual de solo lectura.
El contrato actual extiende esa espera a especialistas, SDD, Navigator y
Documentation Orchestrator. Una recomendación descrita como informativa termina
actuando como un bloqueo operativo.

Objetivo: continuar el trabajo ya solicitado y autorizado sin esperar respuestas
por avisos de proceso o modelo, conservando intervenciones con una decisión,
autorización o aclaración real pendiente.

El inventario de fuentes y controles está en `inventory.md`. Este cambio sustituye
la política vigente; no reescribe decisiones ni evidencias de specs históricas.

## Historias y criterios de aceptación

### R1 — Continuidad después de avisos informativos

Como usuario, quiero que el agente atienda mi petición sin obligarme a responder
solo para superar un anuncio de proceso o una recomendación de modelo.

- CUANDO una operación esté solicitada y autorizada y no exista una decisión
  pendiente EL SISTEMA DEBERÁ continuar su ejecución en el mismo turno sin
  terminarlo exclusivamente para anunciar el proceso o recomendar un modelo.
- CUANDO comunique una recomendación de modelo EL SISTEMA DEBERÁ tratarla como
  informativa sin exigir «continúa», «listo» ni confirmación del modelo elegido.
- EL SISTEMA DEBERÁ mantener el cambio de modelo como decisión manual del usuario
  sin seleccionar ni modificar el modelo del host.

### R2 — Preflight y cambios de nivel no bloqueantes

- CUANDO clasifique la próxima operación EL SISTEMA DEBERÁ conservar un preflight
  proporcional y barato sin convertirlo en una autorización adicional.
- CUANDO cambie únicamente el nivel recomendado EL SISTEMA DEBERÁ comunicar la
  actualización sin detener el trabajo autorizado por ese motivo.
- CUANDO anuncie un proceso o nivel ya comunicado para el mismo alcance
  EL SISTEMA DEBERÁ evitar avisos duplicados sin exigir una confirmación previa
  del usuario para reconocer esa comunicación.
- CUANDO una operación exceda el alcance autorizado o requiera una decisión real
  EL SISTEMA DEBERÁ detenerse explicando la decisión pendiente, no atribuir la
  pausa al nivel de modelo.

### R3 — SDD conserva gates reales, no pausas por modelo

- CUANDO inicie `direct`, Quick Plan `lite` o Requirements `standard`
  EL SISTEMA DEBERÁ continuar después del preflight si no falta una aclaración
  esencial, sin esperar exclusivamente para permitir un cambio de modelo.
- MIENTRAS un gate real de `standard` esté pendiente EL SISTEMA DEBERÁ esperar su
  aprobación explícita antes de cruzarlo y conservar Gates 1, 2, 3 y 4.
- CUANDO se apruebe el gate actual EL SISTEMA DEBERÁ iniciar la siguiente fase sin
  una nueva espera por recomendación de modelo.
- CUANDO termine Implementación dentro del alcance aprobado EL SISTEMA DEBERÁ
  continuar con Verification sin una pausa informativa intermedia y presentar
  Gate 4 solo después de obtener y registrar la evidencia requerida.
- CUANDO la intención sea solo planificación EL SISTEMA DEBERÁ respetarla sin
  interpretar la eliminación de pausas como autorización para implementar.
- SI `lite` deja de ser elegible ENTONCES EL SISTEMA DEBERÁ solicitar aprobación
  de la reclasificación a `standard`, aunque no cambie el nivel recomendado.

### R4 — Intervenciones necesarias y privilegios intactos

- CUANDO falte una decisión esencial de alcance, proyecto, ruta, contrato o flujo
  EL SISTEMA DEBERÁ solicitar la aclaración antes de actuar sobre esa decisión.
- CUANDO una escritura, remediación, publicación o acción destructiva requiera
  autorización EL SISTEMA DEBERÁ conservar la intervención correspondiente.
- CUANDO exista autorización efectiva para la misma operación y alcance en la
  sesión EL SISTEMA DEBERÁ reutilizarla conforme al contrato vigente sin confundir
  una recomendación de modelo o metadatos de handoff con autorización.
- EL SISTEMA DEBERÁ conservar las aprobaciones por micro-paso de Quality/Security,
  los controles de Git/release y las dobles confirmaciones destructivas vigentes.
- EL SISTEMA DEBERÁ mantener los permisos `ask`/`deny` del host sin ampliarlos para
  reducir interacciones.
- SI un control técnico detecta falta de evidencia o integridad ENTONCES
  EL SISTEMA DEBERÁ bloquear la declaración de éxito o cierre sin inventar una
  confirmación humana para comprobaciones puramente técnicas.

### R5 — Consistencia entre fuentes y distribución

- CUANDO se actualice la política EL SISTEMA DEBERÁ reflejarla en agentes, skills,
  referencias, descripciones de adapters, documentación y pruebas activas que
  actualmente exigen pausas exclusivamente por modelo.
- EL SISTEMA DEBERÁ producir los derivados para Copilot, OpenCode, Kiro, Claude y
  Pi mediante el renderer, sin editar `generated/` manualmente.
- EL SISTEMA DEBERÁ preservar specs y registros históricos, snapshots legados
  fuera del pipeline y cambios locales ajenos al ajuste.

## Escenarios mínimos de aceptación

1. Consulta UI puntual como la captura: inspección y respuesta en el mismo turno;
   no respuesta compuesta únicamente por nivel recomendado y «continúa».
2. Consulta Architecture, Data o Code Review de solo lectura: continuidad sin
   confirmación de modelo ni autorización de remediación implícita.
3. Orchestrator `status`/`release-check`: inspección e informe sin pausa por modelo.
4. Orchestrator con escrituras pendientes: conserva aprobación del plan global;
   especialistas no añaden otra espera por modelo al recibir el handoff.
5. Navigator pesado solicitado: sin espera exclusivamente por modelo; creación o
   sobrescritura de índices sigue requiriendo autorización efectiva.
6. Quick Plan: ejecución tras preflight; planificación sola no implementa.
7. SDD standard: pausa en Gates 1–4, no al inicio ni entre implementación y suite.
8. Cambio de nivel sin cambio de autorización: aviso y continuidad; cambio de
   alcance/flujo con decisión pendiente: pregunta concreta y pausa legítima.
9. Quality/Security: auditoría no autoriza remediación; conserva micro-pasos.
10. Git/release/destructivos y permisos del host: sin reducción de salvaguardas.

## Verificación prevista y límites

Cambio observable del contrato conversacional: TDD focalizado sobre las pruebas
contractuales modificadas, preservando pruebas de controles reales y de paridad.
La estrategia detallada y los comandos se definirán en Design.
Las comprobaciones textuales no demuestran por sí solas conducta real de un LLM:
los smokes conversacionales deberán distinguir ejecución observada de escenario
documentado y de prueba no ejecutada.

Fuera de alcance: retirar todos los avisos, automatizar la selección de modelo,
suprimir gates SDD reales, modificar permisos, instalar globalmente el kit, ejecutar
commits/releases, cambiar el laboratorio o migrar specs antiguas.

## Supuesto explícito

Se conserva la recomendación breve cuando corresponda; se elimina su carácter
bloqueante. La petición se interpreta como eliminación de interacciones
innecesarias, no como prohibición absoluta de comunicar niveles de modelo.
