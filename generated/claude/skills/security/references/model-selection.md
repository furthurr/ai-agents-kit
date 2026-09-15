# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.security/`, superficie indicada, nombres y conteos.
No recorras todo el codigo, ejecutes auditorias ni expongas valores antes de
clasificar.

| Operacion | Nivel | Hard stop |
| --- | --- | --- |
| Consulta de estado o finding conocido | `BAJO` | No |
| Revision o micro-remediacion localizada de riesgo no critico | `MEDIO` | No |
| Auditoria inicial/completa o analisis de dependencias amplio | `ALTO` | Si |
| Auth, criptografia, PII, confianza de red, varios proyectos o riesgo critico | `ALTO` | Si |

Para un hard stop, muestra operacion, alcance, nivel y 1-3 motivos; espera `listo`,
`continua` o `continua con el actual`. No repitas el aviso en cada finding o
micro-paso. Recalcula solo ante cambios materiales de alcance o riesgo.

Si Documentation Orchestrator ya recomendo explicitamente el nivel para este
alcance y el usuario lo confirmo, no repitas el aviso. Nunca selecciones ni
cambies el modelo del host.
