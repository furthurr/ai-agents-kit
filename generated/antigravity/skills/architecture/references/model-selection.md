# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.architecture/`, nombres, metadatos y conteos. No
leas todo el repositorio, escribas ni generes diagramas antes de clasificar.

| Operacion | Nivel |
| --- | --- |
| Consulta, ADR o ajuste puntual localizado | `BAJO` |
| Sincronizacion incremental o documentacion de un modulo | `MEDIO` |
| Inicializacion, modo `full` o auditoria completa | `MEDIO` |
| Monorepo, arquitectura ambigua, mas de 100 archivos o varios proyectos | `ALTO` |

Muestra operacion, alcance, nivel y 1-3 motivos; continúa el trabajo autorizado en el mismo turno
sin exigir confirmación del modelo. No repitas el aviso por bloque. Ante cambios
materiales de alcance o riesgo, recalcula; cambiar solo el nivel se comunica sin pausa.
Detente únicamente ante decisiones, autorizaciones o gates reales pendientes; conserva integridad.

Si Documentation Orchestrator ya comunicó el nivel para el mismo alcance, no repitas el aviso.
Nunca selecciones ni cambies el modelo del host.
