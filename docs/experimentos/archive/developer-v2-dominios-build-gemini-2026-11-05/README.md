# V2 candidato2: consultas selectivas, cierre documental y build nativo

**Terminado: doce celdas nuevas de tarea Alta, todas funcionales, más cinco
comprobaciones focalizadas de V2.** Modelo solicitado único:
`google/antigravity-gemini-3.8-flash`, OpenCode 1.18.34. ID: `v2-domains-build-v1-20261105`.
No se instalaron ni sustituyeron agentes del MAS.

## 1. Respuesta a la preocupación sobre las skills

| Tarea Alta, tres repeticiones | Developer actual | ODD histórico | V2 candidato2 | Build nativo |
|---|---:|---:|---:|---:|
| Aceptación funcional | 3/3 | 3/3 | **3/3** | 3/3 |
| `data-api` cargada por contenido | 3/3 | 1/3 | **3/3** | 2/3 |
| `ui-design` cargada por contenido | 3/3 | 1/3 | **3/3** | 0/3 |
| Ambas skills en la misma ejecución | 3/3 | 1/3 | **3/3** | 0/3 |

V2 cargó cada skill **una sola vez por ejecución y antes del primer cambio de código**.
No se aceptó una mera mención: se contrastó el contenido devuelto por la herramienta
con la skill esperada. En esta tarea había endpoints/modelo/persistencia y formulario
UI: ambas eran pertinentes. No se modificaron sus estándares ni se les añadió una
versión recortada específica del escenario.

La corrección del candidato es una regla breve de selección explícita: API/datos
carga data-api; pantalla/formulario/estilos carga ui-design; ambos carga ambas;
ninguno no carga ninguna. Referencias adicionales solo cuando ayuden, sin bootstrap.
[Agente](candidato/agent.md) y [skill candidato2](candidato/SKILL.md).
Agente+skill primaria runtime de V2: **3.926 bytes**; Developer13.399, ODD5.041.
Bytes no son una estimación de tokens. Build tiene instrucciones nativas no medidas
por el tamaño de un prompt personalizado; no se le atribuye un prompt de cero tokens.

## 2. Selectividad y documentación: cinco casos adicionales

Sesiones independientes, excluidas del coste comparativo de la tarea Alta:

| Comprobación de V2 | Esperado | Observado |
|---|---|---|
| PLAN endpoint JSON/backend | Solo data-api; cero escrituras | Correcto |
| PLAN CSS/barra lateral | Solo ui-design; cero escrituras | Correcto |
| PLAN función pura | Ninguna skill de dominio; cero escrituras | Correcto |
| Cambio de saludo con contrato de uso que queda obsoleto | Implementar/probar, indicar ruta+motivo, proponer documentation-orchestrator sin editar documentación | Correcto |
| Añadir test sin cambio funcional ni documental | No cargar dominios ni recomendar actualización innecesaria | Correcto |

Los cinco procesos fueron saludables. No hubo intentos de escritura en PLAN ni
bootstrap, carpetas canónicas o seguimiento nuevos. En el caso positivo solo cambió
`core.py` y su test; una comprobación externa confirmó el saludo nuevo y unittest pasó.
El cierre identificó `docs/usage.md`, explicó el literal obsoleto y propuso el agente
documental esperando respuesta. En el negativo solo se añadió un test, la función y
documentación conservaron sus bytes y no se propuso el orquestador.

**Esto demuestra en estas fixtures que el cierre documental no depende de cargar
data-api/ui-design.** No ejecuta ni certifica la actualización posterior por el
orquestador: el usuario debe seleccionar ese agente y autorizar el alcance correspondiente.

Límite de proporcionalidad: el plan visual, aunque no produjo artefactos, ofreció
opciones opcionales de `padding`/`min-height` además del color solicitado. No fueron
implementadas y no son autorización para ampliar el cambio. La selección correcta
de skills y ausencia de bootstrap **no certifican concisión ni mínima solución perfectas**.
Los cinco checks automáticos pasaron; esta observación semántica se conserva aparte.

## 3. Eficiencia de la tarea Alta

Todos los brazos parten del mismo LocalLibrary documentado y TASK-2 literal, con
referencia revalidada, nueve oráculos externos y los43 tests originales restaurados
en una copia de evaluación. Son doce ejecuciones nuevas, no controles históricos reutilizados.

| Agregado de tres ejecuciones | Developer | ODD | V2 candidato2 | Build |
|---|---:|---:|---:|---:|
| Tokens comparables | 4.663.627 | **3.702.904** | 3.754.925 | 5.162.426 |
| Duración sumada de conversaciones (s) | 719,342 | 758,734 | **716,905** | 822,920 |
| Herramientas | 123 | 124 | **112** | 135 |
| Eventos de pasos con métricas | 126 | 127 | **112** | 138 |
| Lecturas directas completadas | 48 | 37 | 43 | 55 |
| Errores de herramienta | 1 | 3 | **0** | 1 |
| Respuestas de aprobación simuladas | 0 | 0 | 0 | 0 |

V2 frente a Developer: **−19,48 % tokens**, **−0,34 % duración** (tiempo prácticamente igual).
V2 frente a ODD: **+1,40 % tokens**, **−5,51 % duración** (cercanía/trade-off, no ganador robusto).
V2 frente a Build: **−27,26 % tokens**, **−12,88 % duración**.

V2 cumple el umbral de eficiencia de esta tarea frente a Developer y Build, **no frente
a ODD**: este último es ligeramente más barato, pero cargó ambas skills solo en1/3.
Con Developer sí hubo igual frecuencia de consulta de estándares y menor consumo de V2.
Cargar una skill no prueba por sí solo aplicar cada estándar, y la aceptación funcional
no certifica equivalencia integral ni seguridad visual/API exhaustiva.

| Repetición | Developer tokens | ODD tokens | V2 tokens | Build tokens |
|---|---:|---:|---:|---:|
| R1 | 1.837.805 | **725.666** | 1.325.529 | 1.591.172 |
| R2 | **1.292.830** | 1.944.264 | 1.309.366 | 1.315.830 |
| R3 | 1.532.992 | **1.032.974** | 1.120.030 | 2.255.424 |

V2 ahorra tokens en2/3 repeticiones frente a Developer,1/3 frente a ODD y3/3 frente a
Build. No eliminar la repetición desfavorable ni retocar el candidato después de verla.
No se mezclan estos datos con los del candidato1 ni se atribuye causalmente toda
variación entre cohortes a las dos reglas nuevas.

Tokens comparables=input+cache_read+cache_write+output; reasoning separado en JSON.
No se calcula factura ni ahorro monetario. Las duraciones sumadas no son wall-clock
ni espera humana. Lote principal wall-clock **964,273 s**, incluyendo coordinación y
checks externos. Las cinco llamadas focalizadas suman133,912s y se informan separadas.

## 4. Qué significa el control Build

Se invocó el **agente nativo `build` real**, no un alias con un prompt nuestro. Se
verificó `native:true` y ausencia de prompt personalizado, antes y con la configuración
experimental. Solo se igualaron modelo, temperatura, pasos y permisos. No se le ordenó
cargar Developer, ODD ni V2 y no se fingió una skill primaria inexistente: ese campo
es `null` en sus registros, con identidad nativa comprobada por separado.

Build tuvo acceso opcional a las mismas skills de dominio y no a metodologías MAS.
Permanecen instrucciones del proveedor/host/OpenCode y del laboratorio: no es un LLM
sin instrucciones ni una instalación virgen. Esta comparación aísla el procedimiento
especializado con herramientas equivalentes, no mide todos los defaults irrestrictos.

Build pasó3/3, pero no fue más eficiente aquí. Cargó data-api en2/3 y nunca ui-design;
consumió más herramientas, lecturas y tokens en agregado. La ausencia de un prompt
personalizado largo no garantizó menos consumo. No extrapolar a que build siempre
sea peor o incapaz: una tarea/un proyecto/tres repeticiones no acreditan eso.

## 5. Lo que sigue sin demostrarse del cierre documental real

En las doce celdas principales **ningún perfil leyó directamente README o
`docs/lab-context.md` ni propuso actualización documental en el texto final**. ODD
creó una nota en `odd/tasks/reservation.md` en una ejecución; los otros perfiles no
crearon seguimiento. Ninguno creó `.data/`, `.design/` ni otros registros canónicos.

Las fixtures pequeñas hicieron localizable el contrato de uso desde README; la tarea
Alta mantuvo el baseline/entrada anterior sin una nueva guía documental. Los casos
focalizados validan el mecanismo cuando encuentra una fuente clara; **no demuestran
que descubra y revise siempre la documentación de un proyecto existente**. No se
puede concluir solo por el silencio del cierre que ninguna documentación necesitaba
actualización, ni afirmar que el ciclo documental productivo quedó resuelto.

## 6. Integridad, alcance y lectura del resultado

Cuatro preflights reales pasaron (resolución, lectura/edición/unittest y contenido
primario o identidad nativa). Se congelaron candidato, perfiles, corpus, scripts y
oráculos antes de las cinco comprobaciones y las doce celdas. Inputs intactos al cierre.
Sin errores API, timeouts comparativos, skills ajenas, accesos externos o herramientas
prohibidas detectadas. Los tests originales pasan en12/12, además de los nueve externos.

Se configuraron60 pasos y600s por llamada, máximo6 llamadas por celda; configuración
igual no acredita un hard cap SDK. Permisos del host no son sandbox OS; código Python
generado no queda aislado universalmente. SQLite real en disco con hilos/conexiones
independientes no certifica sistemas distribuidos o todos los escenarios multi-proceso.
Caché y host no herméticos. Procedimiento/longitud cambian juntos, evaluación no ciega.

**Recomendación:** candidato2 es una base más convincente que omitir consultas para
ahorrar: conserva la ventaja frente a Developer con la misma frecuencia de skills,
queda cerca de ODD en consumo y mejora al build nativo en este ensayo. Mantenerlo
experimental, sin afirmar equivalencia completa o cierre documental generalizado.
La preocupación de selección de skills quedó atendida en esta muestra; descubrimiento
documental y proporcionalidad de propuestas aún requieren evidencia adicional.

## Evidencia

- [Protocolo previo](protocolo.md), [copia congelada](evidencia/protocol.md).
- [Métricas, consultas por contenido y comportamiento](evidencia/summary-audit.json).
- [Cinco comprobaciones y respuestas completas](evidencia/consultation-summary.json).
- [Definición de casos focalizados](evidencia/probe-cases.json).
- [Identidad Build](evidencia/native-base.json), [preflights](evidencia/preflight.json).
- [Contratos](evidencia/cases.json), [referencia revalidada](evidencia/reference-proof.json).
- [Congelación](evidencia/freeze.json), [tratamientos](evidencia/treatments.json).
- [Lote](evidencia/batch-result.json), [dependencias](evidencia/dependencies.lock.txt).
- [Verificaciones](verificaciones.json), [laboratorio completo](laboratorio.tar.gz),
  [manifest y SHA256](preservacion.json).

Scripts nuevos: `tools/developer_v2_domains_build.py`, `tools/developer_v2_domains_report.py`
y sus tests. Reutilización explícita del arnés anterior en una instancia privada:
`shared_runner.py` difiere solo en quitar la orden de skill primaria al brazo Build.
Se preservan código/metadata dependientes, corpus, trazas saneadas, árboles finales y
pruebas sin credenciales, venv, `.git`, estáticos derivados ni bases SQLite.

No se modificaron agentes canónicos/instalados, adaptadores ni configuración global;
sin commits/push. La reproducción requiere revisar rutas absolutas y reconstruir
dependencias/estáticos; inferencia nueva exige nueva raíz y congelación, nunca
sobrescribir estas ejecuciones ni prometer respuestas idénticas del proveedor.
