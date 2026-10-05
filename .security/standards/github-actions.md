# Estándar cacheado — GitHub Actions

Consulta: 2026-10-05. Alcance: workflow `.github/workflows/ci.yml` y referencias
de acciones externas.

## Controles relevantes

- Fijar cada acción a un SHA completo e inmutable; un tag puede moverse aunque
  pertenezca a una acción conocida.
- Asignar a `GITHUB_TOKEN` los permisos mínimos y ampliarlos solo en el job que
  los requiere. Mantener `contents: read` cuando basta para validar.
- Tratar el contenido de pull requests como no confiable y evitar disparadores
  privilegiados que procesen código no confiable sin aislamiento.
- Revisar actualizaciones de acciones y advisories; pinning inmutable y
  actualización regular son controles complementarios.

## Uso en esta auditoría

SEC-0002 registra tags mutables en `checkout` y `setup-python`. El workflow
observado configura `contents: read`, lo que reduce el impacto potencial; la
configuración del repositorio y sus secretos no se inspeccionaron.

## Fuente

- GitHub, Security hardening for GitHub Actions:
  <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
- CWE-829: <https://cwe.mitre.org/data/definitions/829.html>
