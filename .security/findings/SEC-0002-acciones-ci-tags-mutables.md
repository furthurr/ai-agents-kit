# SEC-0002: Acciones de CI referenciadas por tags mutables

- Estado: Pendiente
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

- [ ] Revisar y fijar `checkout` y `setup-python` a SHA completos de sus
  repositorios oficiales.
- [ ] Añadir una rutina de actualización y revisión de acciones.

## Bitácora

- 2026-10-05: hallazgo estático registrado; no se modificó el workflow.
