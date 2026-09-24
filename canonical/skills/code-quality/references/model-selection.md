# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.quality/`, lenguajes, nombres y conteos. No recorras
todo el codigo, ejecutes auditorias ni escribas findings antes de clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta de metricas o finding conocido | `BAJO` | Si |
| Revision incremental o micro-remediacion localizada | `MEDIO` | Si |
| Auditoria inicial/completa o sin baseline util | `ALTO` | Si |
| Mas de 100 archivos, varios proyectos o analisis transversal complejo | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; termina el turno
antes de trabajar. Espera `listo`, `continua` o `continua con el actual`, sin confirmar el modelo.
No repitas el aviso en cada finding o
micro-paso. Recalcula solo ante cambios materiales de alcance o complejidad.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
