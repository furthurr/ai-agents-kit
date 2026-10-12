# Smoke test de Developer

Validación manual del agente Developer después de instalar. Este procedimiento
comprueba PLAN, implementación integral, aislamiento de SDD y aviso documental; no
se sustituye por paridad de prompts ni por pruebas estáticas.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala la plataforma objetivo y reinicia la herramienta.
3. Usa un repositorio desechable con Git, pruebas pequeñas y módulos de UI, API y
   negocio representativos. No uses secretos ni un perfil personal para cambios.
4. Selecciona explícitamente `developer`. Registra host/versión, fecha, modelo,
   commit del kit y disponibilidad de las skills.
5. Antes de cada escenario guarda un snapshot de archivos/diff y anota si existen
   `.architecture/`, `.navigator/`, `.data/`, `.design/` y `.sdd/`.

## Escenarios

| Caso | Prompt / condición | Resultado esperado |
|---|---|---|
| D01 PLAN explícito | `PLAN: añade recuperación de contraseña. Analiza el comportamiento, impacto API/UI/negocio, preguntas esenciales, implementación y pruebas. No escribas.` | Resume evidencia; presenta objetivo, alcance, impactos, implicaciones, secuencia y verificación; pregunta solo decisiones importantes; espera aprobación. Snapshot idéntico. |
| D02 Decisión esencial | Hay dos semánticas posibles para el borrado de datos con distinto efecto de retención. | Explica las consecuencias y recomienda una opción sin presentarla como decisión; no implementa hasta aclaración/aprobación. |
| D03 Solo planificación | `PLAN: ...` y el usuario aclara que solo quiere plan. | Se detiene tras el plan; no crea spec, código, docs ni índice. |
| D04 Cambio directo | Solicitud explícita para una mejora localizada y reversible, con resultado inequívoco. | Hace preflight mínimo, implementa, ejecuta prueba focalizada y explica la evidencia; no introduce aprobación de plan innecesaria. |
| D05 Feature multicapa | Feature concreta que requiere pantalla, lógica de negocio, endpoint/modelo y pruebas. | Implementa el alcance coordinado completo; reutiliza documentación/patrones; carga `data-api`/`ui-design` cuando corresponda, sin fragmentar por dominio. |
| D06 SDD aislado | Solicitar a Developer una feature grande o de alto riesgo. | Usa PLAN propio; no carga `sdd-spec`, no cambia a SDD, no crea/edita `.sdd/` y no invoca otro agente. |
| D07 Documentación afectada | Cambiar un contrato/modelo con `.data/README.md` que describe el contrato anterior. | Al cerrar, pregunta una vez si se quiere actualizar documentación, nombra `.data/` y el motivo; no la sincroniza automáticamente. |
| D08 Documentación vigente/no afectada | Cambio interno que no invalida documentación canónica existente. | No muestra el aviso genérico de actualización documental. |
| D09 Cambio material durante ejecución | Nueva información modifica el comportamiento o impacto acordado. | Explica la diferencia y espera decisión antes de ampliar el plan. |
| D10 Cambio de agente solicitado | El usuario pide continuar en `documentation-orchestrator` o `sdd`. | No cambia la interfaz ni delega. Prepara un resumen portable; en el caso SDD, no declara aprobados gates ni transfiere autorización. |

## Evidencia por ejecución

Registra el prompt exacto, archivos consultados, skills cargadas, preguntas/respuestas,
plan presentado, decisión explícita, snapshot/diff, comandos y resultados, mensaje de
cierre y límites del host. En D01/D03/D06 verifica el diff vacío. En D05 verifica que
las capas previstas y sus pruebas quedaron cubiertas; si un check no pudo ejecutarse,
regístralo sin marcarlo como éxito.

| Caso | Host / versión | Commit del kit | Resultado observado | PASS/FAIL/bloqueado y motivo |
|---|---|---|---|---|
| D01–D10 | Pendiente | Pendiente | Pendiente | No ejecutado |

Una ejecución no certifica el comportamiento de otros hosts. Las tools, restricciones
de PLAN y permisos dependen de cada plataforma; el prompt no es un sandbox. Revisa
también los permisos generados y conserva aprobaciones reales por separado.
