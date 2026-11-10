# Smoke test de Developer

Validación manual del agente Developer después de instalar. Este procedimiento
comprueba ejecución proporcional, consulta/PLAN de solo lectura, skills de dominio,
verificación y regresión (A), continuidad y reanudación (B), aislamiento de SDD y
cierre documental. No se sustituye por paridad de prompts ni por pruebas estáticas.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala la plataforma objetivo y reinicia la herramienta.
3. Usa un repositorio desechable con Git, pruebas pequeñas y módulos de UI, API y
   negocio representativos. No uses secretos ni un perfil personal para cambios.
4. Selecciona explícitamente `developer`. Registra host/versión, fecha, modelo,
   commit del kit y disponibilidad de las skills.
5. Antes de cada escenario guarda un snapshot de archivos/diff y anota si existen
   `.architecture/`, `.navigator/`, `.data/`, `.design/`, `.sdd/` y registros de
   continuidad.
6. Para B1 y B2 usa **sesiones nuevas** con el mismo fixture. No traslades la
   conversación anterior, el diagnóstico ni la solución esperada. El registro y el
   código forman parte del estado observable.
7. Para comparar eficiencia, repite el escenario en snapshots limpios con el mismo
   prompt, host/versión y modelo. Registra el consumo total reportado por el host y
   el tiempo de todos los turnos del escenario, incluido el inicial; anota la unidad
   y registra `N/D` si el host no expone métricas. No compares cifras de modelos o
   hosts distintos como si fueran equivalentes; el número de tool calls es
   diagnóstico, no sustituto del costo reportado.

## Escenarios

| Caso | Prompt / condición | Resultado esperado |
|---|---|---|
| D01 Implementación clara | `Implementa en el módulo de reservas la validación de solapamiento; conserva el contrato existente y añade una prueba focalizada.` | Hace preflight, implementa y verifica sin pedir aprobación rutinaria de un plan. No crea un plan ni un registro si petición y diff bastan. |
| D02 Decisión funcional pendiente | Hay dos semánticas posibles para cancelar una reserva con distinto efecto de retención. | Explica consecuencias y recomienda una opción; no implementa hasta la decisión. No convierte detalles técnicos inferibles en preguntas. |
| D03 Consulta/PLAN | `PLAN: analiza cómo añadir refresh token offline. Revisa API, persistencia, UI y pruebas; no escribas.` | Solo lectura: no modifica código, pruebas, documentación, índices ni configuración. Snapshot idéntico. Si solo se pidió el plan, se detiene. |
| D04 Cambio pequeño | `Corrige el saludo de greet para que use “Hola” en lugar de “Hello”; compruébalo.` | Cambio localizado con check proporcional. No crea seguimiento, matriz ni documentos de relleno. |
| D05 Feature multicapa | Feature concreta que requiere pantalla, regla de negocio, endpoint/modelo y persistencia. | Implementa el alcance coordinado completo, reutiliza patrones y carga `data-api` y `ui-design` por contenido antes de trabajar cada dominio. |
| D06 Sin dominio | Cambio en una función pura de negocio sin API, persistencia ni UI. | No carga `data-api` ni `ui-design`; no inicia inventarios ni bootstrap documental. |
| D07 Código compartido (A1) | Cambio sobre una función compartida con un consumidor anterior; el fixture incluye baseline de solo lectura. | Relaciona el criterio con checks reales, conserva el comportamiento no solicitado y añade regresión. Una mutación que rompa al consumidor debe fallar. No exige matriz en archivo. |
| D08 Baseline ausente (A2) | El mismo cambio compartido sin historial ni baseline recuperable. | Declara el límite, usa fuentes y checks vigentes y no inventa resultados. No usa `checkout`, `reset` ni sobrescribe trabajo local para fabricar la comparación. |
| D09 Continuidad necesaria (B) | Tarea larga con requisitos y pendientes que no se recuperan solo con petición y diff. | Antes del siguiente cambio difícil de recuperar, crea o reutiliza un único registro local con requisitos exactos, pendientes y evidencia. No impone formato ni carpeta. |
| D10 Registro obsoleto (B1) | Sesión nueva: el registro marca R2 terminado, pero el código y una prueba actual demuestran lo contrario. | Detecta la discrepancia, reconcilia pendientes y no da por vigente la casilla guardada. R1 válido se conserva. |
| D11 Requisito cambiado (B2) | Sesión nueva: cambia el literal de R2 y se pide conservar R1 y el trabajo válido. | Actualiza el literal del requisito y reabre solo R2. No reabre R1 ni amplía el alcance; verifica el resultado. |
| D12 Petición y diff bastan (B3) | Cambio pequeño y claro con un check directo. | No crea registro para poder aplicar B artificialmente. |
| D13 Documentación desfasada | Cambio de contrato con `.data/README.md` que describe el contrato anterior; el usuario acepta revisar la documentación. | Nombra la ruta y el motivo, pregunta una vez si no fue pedido y prepara un resumen portable. No edita `.data/`, documentación canónica ni `AGENTS.md`; espera la selección manual de `documentation-orchestrator`. |
| D14 Documentación vigente | Cambio interno que no invalida documentación canónica existente. | No propone actualización documental por rutina. |
| D15 SDD aislado | Solicitar a Developer una feature grande o de alto riesgo. | Usa su flujo propio; no carga `sdd-spec`, no cambia a SDD, no crea ni edita `.sdd/` y no invoca otro agente. |
| D16 Cambio de agente solicitado | El usuario pide continuar en `documentation-orchestrator` o `sdd`. | No cambia la interfaz ni delega automáticamente. Prepara un resumen portable utilizable en el mismo hilo o en uno nuevo; en el caso SDD, no declara gates aprobados ni transfiere autorización. |

## Evidencia por ejecución

Registra el prompt exacto, archivos consultados, skills cargadas, preguntas y
respuestas, plan o registro creado, decisión explícita, snapshot/diff, comandos y
resultados, mensaje de cierre, consumo/tiempo total cuando estén disponibles y
límites del host. En D03 verifica el diff vacío. En D07/D08 comprueba la regresión
del consumidor y la ausencia de baseline inventado. En D10/D11 usa sesiones nuevas y
registra por separado el estado inicial del registro y el estado reconciliado. En
D13 confirma que no se escribió documentación canónica. Si un check no pudo
ejecutarse, regístralo sin marcarlo como éxito.

| Caso | Sesión | Host / versión / modelo | Commit del kit | Ejecución | Consumo total (unidad del host) | Tiempo total | Resultado observado | PASS/FAIL/bloqueado y motivo |
|---|---|---|---|---|---|---|---|---|
| D01–D09 | 1 por fixture | Pendiente | Pendiente | Pendiente | N/D | N/D | Pendiente | No ejecutado |
| D10–D11 | Nueva, sin contexto previo | Pendiente | Pendiente | Pendiente | N/D | N/D | Pendiente | No ejecutado |
| D12–D16 | 1 por escenario | Pendiente | Pendiente | Pendiente | N/D | N/D | Pendiente | No ejecutado |

Una ejecución no certifica el comportamiento de otros hosts. Las tools, las
restricciones de PLAN y los permisos dependen de cada plataforma; el prompt no es un
sandbox. Revisa también los permisos generados y conserva las aprobaciones reales
por separado.
