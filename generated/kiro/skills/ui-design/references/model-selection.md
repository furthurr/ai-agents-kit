# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.design/`, plataformas, nombres y conteos. No
recorras todos los componentes, escribas ni extraigas el sistema visual antes de
clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta o ajuste puntual de token/componente | `BAJO` | No |
| Revision incremental de varios componentes | `MEDIO` | No |
| Extraccion inicial/completa o rediseño de varias pantallas | `MEDIO` | Si |
| Multiples design systems, accesibilidad transversal o cruce de dominios | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; espera `listo`,
`continua` o `continua con el actual`. No repitas el aviso por componente o bloque.
Recalcula solo ante cambios materiales de alcance o complejidad.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
