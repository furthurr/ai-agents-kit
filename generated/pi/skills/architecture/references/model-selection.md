# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.architecture/`, nombres, metadatos y conteos. No
leas todo el repositorio, escribas ni generes diagramas antes de clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta, ADR o ajuste puntual localizado | `BAJO` | Si |
| Sincronizacion incremental o documentacion de un modulo | `MEDIO` | Si |
| Inicializacion, modo `full` o auditoria completa | `MEDIO` | Si |
| Monorepo, arquitectura ambigua, mas de 100 archivos o varios proyectos | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; termina el turno
antes de trabajar. Espera `listo`, `continua` o `continua con el actual`, sin confirmar el modelo.
No repitas el aviso por bloque. Si cambia
el alcance, recalcula y detente de nuevo solo si cambia el nivel.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
