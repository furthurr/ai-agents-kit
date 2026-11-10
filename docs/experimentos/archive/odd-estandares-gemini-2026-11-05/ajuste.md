## Ajuste experimental: estándares y contexto del proyecto

Estas reglas complementan el procedimiento ODD anterior; no sustituyen sus pruebas,
seguimiento proporcional ni límites. Aplican también a planificación.

- **Dominio pertinente.** Si la petición afecta endpoints, modelos/DTOs, serialización,
  persistencia o integraciones, carga `data-api`; si afecta pantallas, formularios,
  componentes, estilos o accesibilidad visual, carga `ui-design`. Si afecta ambos,
  carga ambas antes de trabajar esos dominios. Si no toca ninguno, no las cargues.
  Usa su contenido, no solo sus nombres; carga una vez mientras siga disponible y
  consulta solo referencias necesarias. No inicies bootstrap, inventarios ni sync.
- **Fuentes del proyecto.** Antes de cambiar, localiza una entrada documental pertinente
  (README o índice del área) si todavía no conoces sus fuentes. Consulta solo contratos,
  componentes y decisiones afectados; reutiliza contexto vigente. Contrasta con código
  y pruebas. Si faltan fuentes o están desfasadas, declara el límite y sigue con evidencia
  directa; pregunta solo si queda una decisión funcional esencial sin resolver.
- **Cumplimiento.** Comprueba las reglas de dominio y los consumidores pertinentes,
  no solo que funcione el caso nuevo. No conviertas cada cambio en auditoría completa
  ni generes documentos o seguimiento por haber consultado estándares.
- **Cierre documental independiente.** Aunque no hayas cargado skills de dominio,
  contrasta cambios y documentación pertinente al cerrar. Si quedó documentación
  canónica desfasada, indica rutas y motivo, propone `documentation-orchestrator` y
  pregunta una vez por su actualización si no fue pedida. Su mantenimiento y `AGENTS.md`
  corresponden a ese agente: prepara contexto portable y espera selección manual,
  sin editar canónicos ni cambiar de agente automáticamente. Si sigue vigente, no
  propongas actualización por rutina. Una nota ODD no sustituye documentación canónica.
