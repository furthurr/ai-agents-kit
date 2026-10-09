# Requisitos — Continuidad de specs y contexto selectivo

Modo SDD: standard
Fase: Requirements
Estado: aprobado
Gate 1: aprobado por el usuario («procede»)
Intención: implementación tras aprobar los gates correspondientes

## Relación y estado previo

Amplía `.sdd/specs/sdd/alcance-calificacion-y-seleccion/`, cuya implementación y
verificación estática están completas y cuyo Gate 4 sigue pendiente. No sobrescribe
su evidencia ni interpreta la autorización de esta ampliación como cierre anterior.
La sesión utiliza instrucciones instaladas anteriores; se modifican fuentes del
kit, sin instalar ni sustituir automáticamente el contrato cargado.

## Objetivo

Evitar contradicciones entre solicitudes nuevas, specs existentes, código y evidencia
mediante detección localizada, enmiendas trazables y revalidación proporcional,
sin imponer auditoría completa de `.sdd` ni documentación adicional a todo cambio.

## Calificación de esta ampliación

- Esfuerzo previsto del LLM: 4 🟢
- Referente del laboratorio: F04, comparación ordinal de normalización y conflictos.
- Justificación: resuelve conflictos entre cambios y acuerdos previos; coordina
  estados/aprobaciones/evidencia; reutiliza navegación y renderer existentes;
  requiere regresiones de continuidad y presupuestos de contexto.
- Supuestos relevantes: contrato de instrucciones, no motor ejecutable de estados;
  pruebas estáticas y escenarios manuales, sin certificar conducta runtime.

## Historia 1 — Detectar y clasificar relaciones

- Req 1.1: CUANDO se solicite una modificación, EL SISTEMA DEBERÁ comprobar si
  afecta specs relevantes antes de recomendar profundidad.
- Req 1.2: CUANDO exista una ruta explícita o una spec activa conocida, EL SISTEMA
  DEBERÁ comenzar por esa referencia sin búsqueda global rutinaria.
- Req 1.3: CUANDO la solicitud no identifique una spec, EL SISTEMA DEBERÁ buscar
  candidatas por módulo/comportamiento y ampliar la búsqueda solo si es necesario.
- Req 1.4: SI hay varias specs candidatas sin autoridad distinguible, ENTONCES EL
  SISTEMA DEBERÁ pedir aclaración antes de modificar acuerdos incompatibles.
- Req 1.5: CUANDO exista una relación relevante, EL SISTEMA DEBERÁ distinguir
  implementación de requisito, cambio de requisito, bugfix o discrepancia documental.
- Req 1.6: SI no se encuentra una relación en las fuentes consultadas, ENTONCES EL
  SISTEMA DEBERÁ continuar sin afirmar que auditó todas las specs del proyecto.

## Historia 2 — Enmiendas y aprobaciones

- Req 2.1: CUANDO una petición cambie un requisito existente, EL SISTEMA DEBERÁ
  presentar el comportamiento actual y el propuesto con spec e ID afectados.
- Req 2.2: CUANDO modifique acuerdos previos, EL SISTEMA DEBERÁ respetar el modo y
  gates de la spec, sin usar una nota baja o direct para evitarlos.
- Req 2.3: CUANDO actualice requisitos, EL SISTEMA DEBERÁ conservar IDs para el
  mismo requisito e identificar adiciones/sustituciones sin perder trazabilidad.
- Req 2.4: CUANDO una enmienda afecte diseño, tareas o pruebas, EL SISTEMA DEBERÁ
  revisar esas dependencias y actualizar solo los artefactos afectados.
- Req 2.5: CUANDO una enmienda invalide aprobaciones standard, EL SISTEMA DEBERÁ
  solicitar los gates afectados sin repetir aprobaciones que siguen siendo válidas.
- Req 2.6: CUANDO haya alcance nuevo no aprobado, EL SISTEMA DEBERÁ abstenerse de
  implementarlo hasta resolver autorización y gates pertinentes.

## Historia 3 — Estados y evidencia

- Req 3.1: CUANDO cambie un requisito, EL SISTEMA DEBERÁ identificar tareas y
  evidencias que necesitan revalidación sin reutilizar cumplimiento obsoleto.
- Req 3.2: CUANDO una evidencia pierda vigencia, EL SISTEMA DEBERÁ conservarla como
  histórica e indicar el estado actual sin desmarcar indiscriminadamente tareas no afectadas.
- Req 3.3: CUANDO una petición afecte una spec cerrada, EL SISTEMA DEBERÁ proponer
  revisión o spec vinculada según alcance sin reescribir silenciosamente el cierre.
- Req 3.4: CUANDO utilice specs previas, EL SISTEMA DEBERÁ distinguir requisitos
  vigentes, sustituidos y documentos históricos mediante evidencia disponible.
- Req 3.5: SI modo, estado, vigencia o gate son ambiguos, ENTONCES EL SISTEMA
  DEBERÁ aclararlos sin inferir aprobación o caducidad por antigüedad del archivo.

## Historia 4 — Discrepancias e impacto conjunto

- Req 4.1: SI código y spec difieren, ENTONCES EL SISTEMA DEBERÁ aclarar si corresponde
  corregir implementación, actualizar documentación o cambiar el acuerdo funcional.
- Req 4.2: CUANDO solicitudes pequeñas estén relacionadas, EL SISTEMA DEBERÁ evaluar
  su impacto conjunto y dependencias sin sumar matemáticamente sus notas.
- Req 4.3: CUANDO cambie materialmente el alcance, EL SISTEMA DEBERÁ reevaluar la
  compatibilidad de modo/ejecutor y la autorización del alcance nuevo.
- Req 4.4: CUANDO reutilice una elección previa, EL SISTEMA DEBERÁ limitarla al
  alcance aceptado sin considerarla autorización general de la sesión.

## Historia 5 — Contexto y costo proporcional

- Req 5.1: CUANDO no exista relación relevante con una spec, EL SISTEMA DEBERÁ
  evitar cargar el procedimiento detallado de continuidad.
- Req 5.2: CUANDO consulte una spec relacionada, EL SISTEMA DEBERÁ leer primero
  modo/estado/gates y requisitos pertinentes, ampliando a dependencias según impacto.
- Req 5.3: MIENTRAS alcance y archivos relevantes no cambien, EL SISTEMA DEBERÁ
  reutilizar contexto ya leído sin búsquedas, lecturas o preguntas repetidas.
- Req 5.4: SI cambia el contexto relevante o no puede verificarse su vigencia,
  ENTONCES EL SISTEMA DEBERÁ revalidar lo necesario sin asumir una caché fiable.
- Req 5.5: CUANDO implemente la política, EL SISTEMA DEBERÁ mantener los presupuestos
  existentes del agente/skill y limitar separadamente la referencia bajo demanda.
- Req 5.6: CUANDO informe costo de contexto, EL SISTEMA DEBERÁ distinguir mediciones
  estáticas de palabras/caracteres de tokens reales, sin prometer porcentajes no medidos.

## Verificación prevista y exclusiones

- Regresiones de cambio pequeño que modifica requisito, continuación sin enmienda,
  spec cerrada, evidencia obsoleta, discrepancia código/spec, peticiones relacionadas,
  varias candidatas y elección previa limitada al alcance.
- Checks de fuentes canónicas, carga selectiva, presupuestos, paridad y render.
- Escenarios manuales para cambio aislado, spec conocida, enmienda y candidatas
  múltiples; registrar runtime como pendiente si no se ejecuta.
- No crear índices ni caché persistente, ni bootstrap/sync automático.
- No obligar a direct a crear spec para modificaciones que conservan requisitos;
  no permitir que direct evite el proceso de una enmienda.
- Mantener routing manual de especialistas, testing y permisos existentes.
- Sin instalación global, commit, push, release o migración automática de specs.
