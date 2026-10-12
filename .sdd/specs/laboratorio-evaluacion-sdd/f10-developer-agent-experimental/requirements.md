# Requisitos — F10 Developer Agent Experimental

- Modo SDD: lite
- Tipo de trabajo: extensión acotada del harness experimental
- Intención: implementar y verificar el soporte; no lanzar un modelo
- Alcance validado por la solicitud explícita del usuario
- Spec relacionada: `.sdd/specs/laboratorio-evaluacion-sdd/f10-no-sdd/`
- Candidato: `developer-agent-experimental`, solo F10; no usa SDD

## Objetivo

Añadir una condición independiente que pruebe F10 con las instrucciones actuales
del agente Developer y su método propio. Preservar contrato, snapshot público,
scaffold, evaluación F10 y resultados históricos. La construcción del harness no
autoriza autenticación real, llamadas a modelos, gasto ni launch.

## Criterios de aceptación

### R1 — Condición y contexto del candidato

- CUANDO se solicite `developer-agent-experimental` ENTONCES EL SISTEMA DEBERÁ
  aceptar únicamente F10 y crear una ejecución desde un snapshot público nuevo.
- CUANDO se prepare el contexto del candidato ENTONCES EL SISTEMA DEBERÁ incluir
  únicamente contrato, scaffold, pruebas públicas y los artefactos de perfil
  Developer expresamente empaquetados.
- EL SISTEMA DEBERÁ resolver los tokens compartidos de las fuentes canónicas con
  las sustituciones y el adaptador OpenCode vigentes, sin escribir ni regenerar
  `generated/`.
- EL SISTEMA DEBERÁ registrar hashes de Developer, skills Developer/data-api,
  adaptador, fuentes de sustitución y perfil renderizado.
- MIENTRAS se ejecute la condición EL SISTEMA DEBERÁ mantener exactamente las
  cuatro herramientas sandbox existentes y no conceder acceso al host, repositorio,
  ejecuciones anteriores, `generated/`, `.sdd/` del host, shell del host, red,
  credenciales ni herramientas adicionales.

### R2 — Método Developer y resultado de la sesión

- CUANDO se invoque al candidato EL SISTEMA DEBERÁ proporcionarle el agente Developer,
  su skill y acceso consultable a la skill `data-api` para el estado durable de F10,
  sin cargar UI u otras skills.
- EL SISTEMA DEBERÁ permitir que Developer presente un plan y solicite aprobación;
  EL SISTEMA no deberá simular ni concederla, invocar otra sesión ni reparar la
  primera entrega.
- CUANDO la respuesta final solicite claramente aprobación y no haya implementación
  ENTONCES EL SISTEMA DEBERÁ clasificar `plan_only`, conservar la respuesta y omitir
  la evaluación funcional.
- CUANDO no exista implementación y no pueda confirmarse una solicitud de aprobación
  ENTONCES EL SISTEMA DEBERÁ clasificar `no_delivery`, conservar el texto disponible
  y omitir la evaluación funcional.
- CUANDO exista implementación ENTONCES EL SISTEMA DEBERÁ congelar y conservar su
  primera entrega antes de evaluarla; no deberá exponer resultados al candidato.

### R3 — Integridad, evaluación y evidencia

- CUANDO se procese una entrega F10 ENTONCES EL SISTEMA DEBERÁ permitir únicamente
  cambios en los cuerpos de `Saga.submit`, `Saga.step` y `Saga.get`, usando el guard
  AST existente y sin importar ni ejecutar código candidato en el host.
- CUANDO se evalúe una primera entrega implementada ENTONCES EL SISTEMA DEBERÁ usar
  un contenedor separado y el evaluador F10 existente para F10-01–F10-06.
- EL SISTEMA DEBERÁ registrar condición, modelo/variante efectivos, versión OpenCode,
  hashes de perfil/snapshot/contrato/entrega, límites, telemetría disponible y
  evidencia de cada criterio.
- CUANDO se ejecute el dry-run EL SISTEMA DEBERÁ usar un actor falso, Docker y cero
  llamadas a modelos; EL SISTEMA DEBERÁ etiquetarlo como fixture y no como resultado
  del LLM.
- EL SISTEMA DEBERÁ preservar íntegros los resultados existentes `lite-experimental`,
  `no-sdd` y `lite2-experimental`.

## Exclusiones y límites

- No se cambia el contrato, los snapshots ni el evaluador F10.
- El candidato no recibe `.sdd/` ni se le impone Quick Plan, EARS, etapas, matrices
  de trazabilidad o documentos de requisitos.
- No se inicia modelo, autenticación real, consumo de presupuesto ni launch.
- No se atribuyen diferencias causales a una sola condición con un intento.
- Esta spec pertenece a la construcción del harness; no forma parte del paquete
  candidato.
