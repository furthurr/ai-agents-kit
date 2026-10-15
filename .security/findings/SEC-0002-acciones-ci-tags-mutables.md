# SEC-0002: Acciones de CI referenciadas por tags mutables

- Estado: Resuelto en los workflows versionados; ejecución remota pendiente
- Severidad: 🟢 Baja
- Referencia: GitHub Actions Security Hardening · CWE-829
- Ubicación: `.github/workflows/ci.yml:7-8,14-16`
- Fecha de detección: 2026-10-05

## Descripción del riesgo

El workflow consume `actions/checkout@v4` y `actions/setup-python@v5` por tags,
que no fijan de forma inmutable el código de la acción. Si una referencia
upstream se retargetea o compromete, el código de la acción podría ejecutarse en
el runner. El workflow limita `GITHUB_TOKEN` a `contents: read`; no se observó
un job de despliegue. No se inspeccionaron los secretos ni las reglas de
protección configurados en GitHub.

## Impacto, esfuerzo y recomendación

- Impacto potencial: ejecución de código externo durante CI, con alcance
  limitado por el token de solo lectura y la configuración del runner.
- Esfuerzo estimado: Bajo.
- Recomendación: fijar las acciones a SHA completos verificados y mantener un
  proceso de actualización/revisión de esas referencias.

## Plan de remediación (no ejecutado)

- [x] Revisar y fijar `checkout` y `setup-python` a SHA completos de sus
  repositorios oficiales.
- [x] Añadir una rutina de actualización y revisión de acciones.

## Bitácora

- 2026-10-14: los cuatro usos en los dos jobs de CI quedan fijados a SHA completos.
  `git ls-remote` contra los repositorios oficiales verifica checkout v4.4.0
  (`11d5960a326750d5838078e36cf38b85af677262`) y setup-python v5.6.0
  (`a26af69be951a213d495a4c3e4e4022e16d87065`), coincidentes con los majors previos
  en el momento de revisión. Se conservan majors y permisos `contents: read`.
  Dependabot propone actualizaciones mensuales, sin automerge; revisar procedencia,
  diff y CI antes de aprobar. No se ejecutó GitHub Actions remotamente.

- 2026-10-05: hallazgo estático registrado; no se modificó el workflow.
