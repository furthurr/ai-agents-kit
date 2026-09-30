# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.design/`, plataformas, nombres y conteos. No
recorras todos los componentes, escribas ni extraigas el sistema visual antes de
clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta o ajuste puntual de token/componente | `BAJO` | Si |
| Revision incremental de varios componentes | `MEDIO` | Si |
| Extraccion inicial/completa o rediseño de varias pantallas | `MEDIO` | Si |
| Multiples design systems, accesibilidad transversal o cruce de dominios | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; termina el turno
antes de trabajar. Espera `listo`, `continua` o `continua con el actual`, sin confirmar el modelo.
No repitas el aviso por componente o bloque.
Recalcula solo ante cambios materiales de alcance o complejidad.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
