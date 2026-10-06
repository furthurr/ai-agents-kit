# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.quality/`, lenguajes, nombres y conteos. No recorras
todo el codigo, ejecutes auditorias ni escribas findings antes de clasificar.

| Operacion | Nivel |
| --- | --- |
| Consulta de metricas o finding conocido | `BAJO` |
| Revision incremental o micro-remediacion localizada | `MEDIO` |
| Auditoria inicial/completa o sin baseline util | `ALTO` |
| Mas de 100 archivos, varios proyectos o analisis transversal complejo | `ALTO` |

Muestra operacion, alcance, nivel y 1-3 motivos; continúa el trabajo autorizado en el mismo turno
sin exigir confirmación del modelo. No repitas el aviso por finding o micro-paso.
Recalcula ante cambios materiales de alcance o complejidad; cambiar solo el nivel se comunica sin pausa.
Conserva decisiones, autorizaciones, gates, aprobaciones por micro-paso e integridad.

Si Code Review o Documentation Orchestrator ya comunicó el nivel para el mismo
alcance y dominios, no repitas el aviso. Nunca selecciones ni cambies el modelo del host.
