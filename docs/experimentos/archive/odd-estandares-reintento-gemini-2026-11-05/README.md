# Reintento ODD original / con estándares — bloqueado por HTTP403

**Estado: nuevo lote PARCIAL. No fue posible completar las seis celdas porque el
proveedor de inferencia respondió403 en ambos perfiles durante R2.** No hay un
proceso de pruebas en segundo plano pendiente de terminar; el runner se detuvo.

ID: `odd-standards-retry-v1-20261105`. Modelo solicitado único:
`google/antigravity-gemini-3.8-flash`, OpenCode1.18.34.

## Qué se hizo

Tras autorización del usuario para reintentar, se preparó una raíz nueva con seis
ejecuciones NUEVAS (tres por brazo), no un reemplazo aislado del intento fallido.
Se verificó igualdad de baseline, oráculos, tarea, perfiles y configuración con el
[lote parcial anterior](../odd-estandares-gemini-2026-11-05/README.md), normalizando
solo rutas. No cambió el ajuste ni se aumentó el timeout600s.

Ambos preflights reales y la referencia original43+externos9 pasaron de nuevo. Los
cinco casos focalizados previos no se repitieron ni se sumaron al coste de este lote;
su copia se etiqueta expresamente como evidencia heredada.

## Resultado de cada intento

| Intento nuevo | Conversación | Snapshot final | Tokens observados | Duración conversación (s) |
|---|---|---|---:|---:|
| Original R1 | Completa/saludable | Aceptación funcional aprobada | 659.590 | 164,944 |
| Ajustado R1 | Completa/saludable | Aceptación funcional aprobada | 2.950.878 | 298,337 |
| Original R2 | **APIError403, exit1** | Incompleto; no pasa aceptación | 1.097.327* | 167,874* |
| Ajustado R2 | **APIError403, exit1** | Incompleto; no pasa aceptación | 1.229.115* | 161,748* |
| Original/Ajustado R3 | **No iniciados por regla de parada** | No aplicable | Desconocido | Desconocido |

*Contadores hasta la interrupción, no equivalentes a una entrega terminada.*

Las dos interrupciones nuevas no fueron timeouts: `timeout:false`, `returncode:1`,
evento de error de la API de inferencia con `name:APIError`, `statusCode:403`.
No confundirlo con respuestas403 del endpoint de la aplicación de biblioteca.

La consulta de estado/cuota de Antigravity también falló: `fetchAvailableModels
failed (403)`. No se pudo obtener cuota ni acreditar si se trata de cuota, permisos,
estado de cuenta o verificación del proveedor. No se leyeron credenciales ni se
cambiaron cuentas, proveedor, modelo o políticas para eludirlo.

El lote tardó501,488s de reloj con coordinación/checks externos. Inputs nuevos y
anteriores siguen intactos. Se conservaron cuatro intentos; no hubo reintentos
selectivos, aumento de límites ni continuación automática de R3.

## Qué sí y qué no acredita

- En R1 el ajustado pasa la aceptación y carga ambas skills antes de escribir.
- En R2 el ajustado también había cargado ambas antes del código, pero su entrega
  quedó interrumpida; no se cuenta como una ejecución funcional completa.
- El control original no cargó estas skills en los dos intentos observados.
- No se observaron lecturas directas de documentación del proyecto en el ajustado,
  fuera de su propio registro ODD; tampoco recomendación documental en su cierre R1.
  El mecanismo se validó previamente en fixtures claras, no de forma general en la app.
- Los snapshots interrumpidos no permiten atribuir su fallo de aceptación a la
  metodología: el proceso dejó de recibir respuestas del LLM antes de terminar.
- **La comparación agregada de eficiencia queda sin conclusión.** La única pareja
  completa muestra mayor consumo del ajustado, pero n=1 no estima un efecto típico.
  No usar las interrupciones para proclamar ventajas de velocidad/coste.

Tokens comparables=input+cache_read+cache_write+output, reasoning aparte. No son
factura. La suma de conversaciones no es wall-clock; preflights y referencia separados.

## Historial completo, sin selección de éxitos

El ensayo anterior conserva4 intentos:3 conversaciones completas y1 timeout del
original con snapshot funcional. Este reintento conserva4 intentos:2 completas y2
errores403. En total hay8 intentos comparativos preservados entre ambos lotes, no
una batería de seis sin fallos. **No se agregan sus tokens/tiempos ni se completan
retrospectivamente las cohortes.**

Hay tres entregas completas y funcionales del ajustado entre los dos lotes y una
cuarta interrumpida por403. Es una observación del historial, no tres repeticiones
de una cohorte comparativa terminada ni certificación de riesgo acumulativo eliminado.

## Bloqueo y siguiente paso

Es necesario restablecer acceso de Gemini/Antigravity antes de otro intento. El
usuario debe revisar el estado/acceso en el proveedor o la interfaz del host;
no enviar tokens, contraseñas ni archivos de autenticación al asistente.

Una vez disponible, acordar una nueva ejecución identificada y conservar ambos
lotes parciales. No seguir reintentando en bucle ni cambiar silenciosamente de
modelo para obtener resultados. Este informe no autoriza más inferencia.

El ODD histórico, el ajuste, los agentes instalados, el Developer canónico y el plan
del Escritorio no se modificaron. Sin commits/push ni cambios de configuración global.

## Evidencia

- [Protocolo de reintento](protocolo.md), [copia congelada](evidencia/protocol.md).
- [Procedencia del reintento](evidencia/retry-plan.json).
- [Resultados y conducta](evidencia/summary-audit.json), [parada](evidencia/batch-result.json).
- [Freeze](evidencia/freeze.json), [preflights nuevos](evidencia/preflight.json).
- [Referencia revalidada](evidencia/reference-proof.json), [contratos](evidencia/cases.json).
- [Checks focalizados PREVIOS, no repetidos](evidencia/prior-consultation-summary.json).
- [Skill ajustada idéntica](evidencia/adjusted-SKILL.md), [verificaciones](verificaciones.json).
- [Laboratorio completo y trazas saneadas](laboratorio.tar.gz), [hashes](preservacion.json).

Wrapper nuevo: `tools/odd_standards_retry.py`, pruebas `tools/test_odd_standards_retry.py`.
Se reutilizaron sin alterar `odd_standards_benchmark.py` y su analizador. Se preservan
snapshots, llamadas y errores tipados sin razonamiento privado ni credenciales.
Reproducir requiere revisar rutas y entorno; los permisos no constituyen sandbox OS.
