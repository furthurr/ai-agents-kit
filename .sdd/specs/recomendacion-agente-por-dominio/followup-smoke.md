# Smoke de seguimiento — OpenCode aislado

Modo SDD: standard
Fase: Verification
Estado: parcial — hallazgos históricos R04/R10; reintentos post-corrección bloqueados
Fecha: 2026-10-07
Host: OpenCode 1.18.34

## Método

Fixtures independientes en el directorio temporal aprobado, con HOME/XDG propios,
sin credenciales copiadas, sin modelo seleccionado, sin cambios al perfil global.
`edit`, `bash`, `task`, `webfetch` y acceso externo están denegados. Un comando
rechazado o timeout no se cuenta como respuesta correcta. Los casos R01/R02/R03/
R05/R08/R09/R10 y R12 están descritos en `runtime-smoke.md`,
`correction-evidence.md` y las trazas sanitizadas de los fixtures temporales.

## Resultados nuevos

| Caso | Resultado | Evidencia observada |
|---|---|---|
| R04 ambiguo | **FAIL** | Pide cinco aclaraciones y no escribe, pero enumera `security`, `code-quality` y `architecture` como dominios/agentes candidatos, aunque esta versión solo permite recomendar `ui-design` y `data-api`. Traza: `routing-short-fuw6jzu6/R04/artifacts/R04.summary.json`. |
| R05 multipantalla | PASS | Recomienda planificar en SDD por tres pantallas, nuevos flujos/estados y decisiones ambiguas; no usa herramientas de escritura. |
| R06 migración/contrato | BLOQUEADO | Dos intentos de 90–125 s terminan sin texto final después de cargar skill/referencias y explorar contexto. No se infiere PASS/FAIL funcional. |
| R07 Gate 3 pendiente | BLOQUEADO | Dos intentos detectan `.sdd`, pero solicitan `bash ls`; el permiso se rechaza y el CLI termina sin decisión textual. No se infiere que el gate se conservaría en la respuesta. |
| R08 decisión explícita previa | PASS de control | Fixture suministró historial controlado de recomendación y respuesta «prefiero seguir aquí en SDD». El agente dice que respeta la decisión y no repite recomendación; no usa herramientas. No acredita memoria entre sesiones reales. |
| R09 selección de UI | PASS | Produce `Contexto para selección manual` con objetivo, alcance, exclusiones, ruta, ausencia de spec/gates y aceptación; no ejecuta ni invoca. |
| R10 preferencia incompatible UI/API | PASS | Explica límite de `ui-design`, propone `data-api` solo si el endpoint es el alcance real y pregunta cómo continuar por ambigüedad; no escribe. |
| R10 selección explícita de data-api | PASS condicionado | Al pedir explícitamente contexto copiable y prohibir edición, genera `Contexto para selección manual` para `data-api`, cita `user_dto.py`, no edita ni ejecuta. En una prueba anterior, el prompt «Quiero que @data-api actualice el DTO» sí produjo intento de `edit` desde SDD (bloqueado). Por eso el caso general de transferencia manual permanece como riesgo/ambigüedad y no queda plenamente demostrado. |
| R11 candidato ausente | BLOQUEADO | Fixture eliminó agente y skill `ui-design`; el modelo intenta `bash ls` para inspeccionar el entorno. Bash es rechazado y no hay respuesta final. No afirmar que reconoció ausencia ni que inventó disponibilidad. |
| R12 distribución | PASS parcial | Debug confirma carga en OpenCode 1.18.34 del agente, skill y referencia. No se ejecutó runtime en los otros cinco hosts. |

Resumen de fixtures temporales: `routing-followup-5ttidcu5`,
`routing-remainder-oswf7skh`, `routing-final-z0y0lm9_`, `routing-short-fuw6jzu6` y
`routing-r10-explicit-k6bvqvp9` bajo el directorio temporal preaprobado. Los prompts,
resúmenes JSON y eventos relevantes se conservaron allí; no se copiaron perfiles,
credenciales ni HOME. Las notas de evidencia conservan las conclusiones necesarias.

## Interpretación / decisiones pendientes

- La barrera R01 se comportó correctamente en su repetición. R02, R03, R05, R08,
  R09 y R10 incompatible también dieron la ruta esperada bajo sus prompts de control.
- **R04 contradice REQ-002** al enumerar agentes fuera del conjunto v1. No corregir
  sin autorización: la solicitud original de corrección cubría el fallo R01, no esta
  brecha distinta.
- R06, R07 y R11 son bloqueos por falta de respuesta final, no resultados favorables.
- El intento de edición del R10 compatible demuestra riesgo de que una selección de
  agente expresada dentro de una instrucción de implementación no siempre detenga
  la ejecución local de SDD; el prompt de contexto manual explícito sí se detuvo.
- R12 es estático/dinámico de carga solo para OpenCode; no certifica otros hosts.

Gate 4 queda pendiente. La whitelist y el stop/package se reforzaron después de
estos hallazgos; ver [correction-evidence.md](correction-evidence.md). La repetición
con el fixture sin shell se bloqueó antes de respuesta por HTTP 403 del proveedor CLI.
No cambió modelo/proveedor, no se copiaron credenciales y no se eludió el error. Por
ello no hay evidencia conversacional de eficacia del último refuerzo; R04/R10
post-corrección y R06/R07/R11 siguen no verificados.
