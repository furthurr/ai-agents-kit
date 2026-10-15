# SEC-0004: Las instalaciones pueden conservar agentes obsoletos

- Estado: Resuelto para la política de retirada explícita; instalaciones no migradas conservan riesgo residual
- Severidad: 🟢 Baja
- Referencia: OWASP LLM06:2025 (Excessive Agency / funcionalidad obsoleta) · CWE-250 si el artefacto conserva permisos ya no requeridos
- Ubicación: `scripts/install/opencode.sh:101-110,133-144`; patrón equivalente en otros instaladores; `tools/install_preflight.py:119-135`
- Fecha de detección: 2026-10-05

## Descripción del riesgo

Los instaladores copian y fusionan el contenido actual, pero no eliminan
artefactos que dejaron de estar declarados. El preflight solo los anuncia como
no declarados y no bloquea la finalización. Por tanto, un agente retirado de una
versión del kit puede seguir disponible en el directorio del host con sus
instrucciones o capacidades anteriores. No se inspeccionaron instalaciones
locales de los hosts; la exposición concreta depende de que existan artefactos
obsoletos y de sus permisos.

## Impacto, esfuerzo y recomendación

- Impacto potencial: persistencia de instrucciones o herramientas antiguas,
  posiblemente con privilegios superiores a los que el usuario espera tras una
  actualización.
- Esfuerzo estimado: Medio; la eliminación debe preservar contenido de usuario.
- Recomendación: definir una política de retiro/migración auditable para
  artefactos administrados, distinguiéndolos del contenido ajeno; no borrar
  directorios completos de forma implícita.

## Plan de remediación (no ejecutado)

- [x] Definir cómo identificar con seguridad los artefactos instalados por el
  kit y cómo notificar los obsoletos.
- [x] Añadir una retirada explícita, reversible y verificada, preservando
  contenido ajeno y confirmando el alcance antes de eliminar.

## Bitácora

- 2026-10-14: revalidada la solución ya presente en MAS 3.2.0, conforme a la política
  aprobada de no retirar automáticamente. Catálogo/procedencia y SHA de bytes
  desconocidos, opt-in, respaldo verificado fuera de árboles activos, conservación
  de archivos personales y avisos diferenciados de instalación/migración.
  `python3 -B tools/test_retired_agents.py`: 26 tests OK, incluidos wrappers reales
  Bash de seis plataformas en perfiles temporales. No se ejecutó PowerShell nativo
  ni se migraron instalaciones del usuario. No fue necesario modificar instaladores.
  La descripción original es histórica: existe migración explícita y documentada
  (`docs/migracion-agentes.md`), aunque la instalación normal sigue conservando restos.

- 2026-10-05: hallazgo estático registrado; no se ejecutaron instaladores.
