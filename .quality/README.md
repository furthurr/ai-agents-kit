# Calidad de código — AI Agents Kit

Estado canónico de calidad del repositorio. Léelo antes de continuar auditorías
o iniciar una remediación.

## Estado de sincronización

- Lenguajes auditados: Python 3, Bash y PowerShell.
- Alcance auditado: `tools/*.py` y `scripts/install/`, `scripts/backup/`.
- Snapshot: working tree local observado el 2026-10-05, incluidos sus cambios
  locales; no se declara `HEAD` como baseline ni como fuente de esos cambios.
- Última actualización: 2026-10-05.
- Revalidación puntual QLT-0001: 2026-10-14 sobre MAS 3.2.0 y cambios locales;
  remediado y verificado. No equivale a una nueva auditoría completa.
- Estado: auditoría inicial; no hay marca basada en commit.

## Contexto para IA

- **Stack y pruebas:** utilidades Python basadas en la biblioteca estándar,
  pruebas de contrato/integridad e instaladores Bash y PowerShell.
- **Quality gate:** no configurado ni medido; no se encontró configuración o
  reporte de SonarQube.
- **Métricas:** sin reporte de cobertura, duplicación o complejidad; ver
  [`metrics.md`](metrics.md).
- **Hallazgos abiertos registrados:** 0; [`QLT-0001`](findings/QLT-0001-expresiones-duplicadas-en-integridad.md)
  resuelto. La suite general mantiene un fallo de enlace local documentado en el finding.
- **Reglas Sonar de referencia:** Python, regla `python:S1764`, cacheada en
  [`standards/python.md`](standards/python.md).
- **Límite de evidencia:** las pruebas y comprobaciones describen el snapshot
  local de esta auditoría. No validan ejecución de PowerShell en Windows ni
  equivalen a un análisis Sonar.

## Índice

- Tablero de hallazgos: [`quality-tech-debt.md`](quality-tech-debt.md)
- Detalle por hallazgo: [`findings/`](findings/)
- Métricas: [`metrics.md`](metrics.md)
- Reglas cacheadas: [`standards/`](standards/)
