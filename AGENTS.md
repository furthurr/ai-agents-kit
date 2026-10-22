<!-- ai-agents-kit:documentation:start -->
## Guía documental del repositorio

Este bloque orienta la consulta y el mantenimiento de documentación; no activa
un perfil de autonomía ni concede permisos técnicos o de implementación.

### Entradas y fuentes de verdad

- Entrada general: [README.md](README.md). Índice de guías: [docs/README.md](docs/README.md).
- El catálogo y el contenido compartido del MAS se definen en
  [canonical/manifest.json](canonical/manifest.json) y `canonical/`; las diferencias
  de plataforma están en `adapters/`. Los archivos de `generated/` son derivados,
  no una segunda fuente editable. Consulta [desarrollo](docs/desarrollo.md).
- Permisos y límites: [docs/permisos-hosts.md](docs/permisos-hosts.md).
  Autonomía: [docs/extra-tools/modo-autonomo.md](docs/extra-tools/modo-autonomo.md).
  Contrasta estas guías con la implementación y su ayuda antes de aplicar cambios
  a un perfil; escribir configuración no prueba su aceptación por el host.

### Documentación e índices presentes

| Carpeta / entrada | Propósito | Responsable del mantenimiento |
|---|---|---|
| [docs/](docs/README.md) | Guías de uso, instalación y desarrollo del kit. | Orquestación documental, dentro del alcance aprobado. |
| [.architecture/](.architecture/README.md) | Arquitectura, decisiones y flujos. | Especialidad de arquitectura. |
| [.navigator/](.navigator/ai-context.md) | Contexto y mapas para localizar código; no sustituyen las fuentes directas. | Especialidad de navegación. |
| [.quality/](.quality/README.md) | Registros de calidad y evidencia de sus revisiones. | Especialidad de calidad / rol de revisión. |
| [.security/](.security/README.md) | Registros de seguridad, hallazgos y límites de cobertura. | Especialidad de seguridad / rol de revisión. |

Consulta fechas, alcance y marcas de cada índice antes de asumir vigencia.
Este bloque no acredita una sincronización global ni amplía las auditorías
históricas. Si un índice contradice código o configuración actual, verifica las
fuentes directas y comunica la discrepancia sin regenerar documentación ajena al
alcance solicitado.

`.sdd/` y `.release/` pertenecen a workflows externos a la orquestación documental;
su presencia no autoriza crearlos, modificarlos ni sincronizarlos desde este flujo.
<!-- ai-agents-kit:documentation:end -->
