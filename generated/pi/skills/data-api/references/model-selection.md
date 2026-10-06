# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.data/`, contratos, nombres y conteos. No recorras
toda la capa de datos, escribas ni reconstruyas contratos antes de clasificar.

| Operacion | Nivel |
| --- | --- |
| Consulta o documentacion puntual de endpoint/DTO | `BAJO` |
| Cambio localizado que preserva contratos y esquemas | `MEDIO` |
| Inicializacion, catalogo o sincronizacion completa | `MEDIO` |
| Migracion, contrato publico, varias fuentes/servicios o riesgo de integridad | `ALTO` |

Muestra operacion, alcance, nivel y 1-3 motivos; continúa el trabajo autorizado en el mismo turno
sin exigir confirmación del modelo. No repitas el aviso por endpoint o tarea.
Recalcula ante cambios materiales de alcance o riesgo; cambiar solo el nivel se comunica sin pausa.
Detente únicamente ante decisiones, autorizaciones o gates reales pendientes; conserva integridad.

Si Documentation Orchestrator ya comunicó el nivel para el mismo alcance, no repitas el aviso.
Nunca selecciones ni cambies el modelo del host.
