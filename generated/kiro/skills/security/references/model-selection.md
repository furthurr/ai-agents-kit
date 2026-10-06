# Seleccion de nivel de modelo

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de modelos,
proveedores ni equivalencias comerciales.

## Preflight

Usa la solicitud, estado de `.security/`, superficie indicada, nombres y conteos.
No recorras todo el codigo, ejecutes auditorias ni expongas valores antes de
clasificar.

| Operacion | Nivel |
| --- | --- |
| Consulta de estado o finding conocido | `BAJO` |
| Revision o micro-remediacion localizada de riesgo no critico | `MEDIO` |
| Auditoria inicial/completa o analisis de dependencias amplio | `ALTO` |
| Auth, criptografia, PII, confianza de red, varios proyectos o riesgo critico | `ALTO` |

Muestra operacion, alcance, nivel y 1-3 motivos; continúa el trabajo autorizado en el mismo turno
sin exigir confirmación del modelo. No repitas el aviso por finding o micro-paso.
Recalcula ante cambios materiales de alcance o riesgo; cambiar solo el nivel se comunica sin pausa.
Conserva decisiones, autorizaciones, gates, aprobaciones por micro-paso e integridad.

Si Code Review o Documentation Orchestrator ya comunicó el nivel para el mismo
alcance y dominios, no repitas el aviso. Nunca selecciones ni cambies el modelo del host.
