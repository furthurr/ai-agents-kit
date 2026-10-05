# Métricas de calidad

- Snapshot evaluado: working tree local, 2026-10-05. No se usa `HEAD` como
  baseline.
- Archivos incluidos: 16 archivos Python bajo `tools/`; 20 scripts bajo
  `scripts/` (10 Bash y 10 PowerShell).
- Cobertura de pruebas: N/D; no hay reporte de cobertura y no se ejecutó una
  herramienta de cobertura.
- Duplicación: N/D; no se ejecutó SonarQube ni otra medición de duplicación.
- Complejidad: N/D; no se ejecutó un analizador que mida complejidad.
- Deuda técnica estimada: aproximadamente 10 minutos para QLT-0001; estimación
  manual, no derivada de Sonar.
- Quality gate: no configurado/no medido; no se declara `passed` ni `failed`.

## Verificaciones ejecutadas

- Pasaron con código de salida 0: `test_code_review_contract.py`,
  `test_handoff_contract.py`, `test_install.py`, `test_sdd_contract.py` y
  `test_integrity.py`. Esta última suite también ejecutó las pruebas de
  validación, enlaces, recomendaciones de modelo e identidad MAS.
- Parseo AST correcto en los 16 archivos Python de `tools/`.
- `bash -n` correcto en los 10 scripts Bash.
- `pwsh` y `shellcheck` no estaban disponibles: no se pudo ejecutar la suite
  PowerShell ni ShellCheck. `test_install.py` comprueba estáticamente parte de
  la paridad de los instaladores.
