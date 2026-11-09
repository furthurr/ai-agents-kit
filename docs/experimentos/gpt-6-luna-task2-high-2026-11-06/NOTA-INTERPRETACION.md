# Nota de interpretación — TASK-2 Alta

## Resultado en una línea

Ninguna de las cinco implementaciones alcanza la aceptación **completa** definida
por el arnés, pero la causa dominante es un contrato extendido (`edges5`) que
—funcionalidad, conjunta, check, migraciones y tests nuevos— la logran 3 de 5.

## Calibración del contrato extendido

pruebas:

- `test_anonymous_api_401_json_with_real_csrf`: devuelve 403, no 401.
- `test_anonymous_ui_cannot_reserve`: devuelve 500, no 302.

Por tanto, `edges5` no está calibrado como contrato alcanzable ni como criterio
de entrega. Se conserva como diagnóstico y **no** debe usarse para declarar que
Luna falló donde la referencia acierta. La definición de `complete_acceptance`
del arnés incluye `edges5`; por eso el marcador automático es 0/6.

## Detalle por configuración

| Configuración | Primaria | Causa si no primaria | Extendido |
|---|---|---|---|
| Build sin MAS | No | Su propio test de UI falla en conjunta | 2 fallos de borde |
| Build con MAS | Sí | — | 2 fallos de borde |
| Developer instalado | Sí | — | 1 fallo de borde |
| Candidato2 + refuerzos | No | 4 errores propios: base de datos cerrada en tests | 1 fallo de borde |
| Developer v2 candidato2 | Sí | — | 1 fallo de borde |
| SDD instalado | No | Pausa real; sin cambios | No evaluable sin implementación |

Las cinco implementaciones que existen devuelven **403** donde la tarea exige
**401** para API anónima. Build sin MAS y Build con MAS tampoco generan el campo
oculto de idempotencia ni la confirmación visible exigidos en la UI.

## SDD Alta

Pausa real tras 6 pasos y 118.389 tokens: definió el alcance, recomendó
**SDD-Lite** y pidió confirmación antes de escribir artefactos o código. No se
reanudó ni se fabricó aprobación. Ese coste es de pausa, no de entrega.

## Límites

- n=1; no hay conclusión causal ni superioridad universal.
- El total de 7.065.071 tokens incluye la pausa SDD y no es un coste de seis
  entregas terminadas.
- Fidelidad procedural no certificada; sin commits ni push.
