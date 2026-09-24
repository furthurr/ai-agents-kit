# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.data/`, contratos, nombres y conteos. No recorras
toda la capa de datos, escribas ni reconstruyas contratos antes de clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta o documentacion puntual de endpoint/DTO | `BAJO` | Si |
| Cambio localizado que preserva contratos y esquemas | `MEDIO` | Si |
| Inicializacion, catalogo o sincronizacion completa | `MEDIO` | Si |
| Migracion, contrato publico, varias fuentes/servicios o riesgo de integridad | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; termina el turno
antes de trabajar. Espera `listo`, `continua` o `continua con el actual`, sin confirmar el modelo.
No repitas el aviso por endpoint o tarea.
Recalcula solo ante cambios materiales de alcance o riesgo.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
