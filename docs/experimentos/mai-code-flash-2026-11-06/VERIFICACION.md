# Verificación de la repetición MAI

## Ejecutado

- `python3 -B -m unittest discover -s tools -p 'test_mai_flash_benchmark.py' -v`:
  4/4 antes de preparar y congelar.
- `python3 -B tools/mai_flash_benchmark.py prepare all`: cuatro cohortes nuevas.
- `python3 -B tools/mai_flash_benchmark.py offline all`: tres cohortes completadas;
  timeout del operador durante el probe sintético de la cuarta. Recuperación
  exclusivamente offline de sdd-high documentada en el protocolo; cuatro freezes.
- `python3 -B -m unittest discover -s tools -p 'test_six_agent*.py' -v`: 30/30.
  5/5.
  todas correctas antes de cerrar las ejecuciones.
- `python3 -B tools/mai_flash_benchmark.py run all`: 12 invocaciones iniciales,
  evaluaciones y cuatro exportaciones terminadas. Cada exportación verificó
  todos sus miembros por SHA256.
- `python3 -B tools/mai_flash_report.py`: revisión posterior sin inferencia;
  seis evaluaciones aisladas de los mismos 13 oráculos de búsqueda y nueva
  verificación íntegra de los cuatro archivos (2.361 miembros).
- `python3 -B -m unittest discover -s tools -p 'test_mai_flash*.py' -v`: 8/8 al
  cierre, incluyendo clasificación de pausas, límites y error de setUpClass.
- `python3 -B tools/mai_flash_benchmark.py check all`: PASS al cierre.

## Límite de la última comprobación adicional

Un comando adicional del operador para releer el manifiesto suplementario,
reconciliar totales y comparar de nuevo las entregas recibió
`permission.rejected` antes de ejecutarse. No se presenta esa comprobación
adicional como realizada ni se eludió la denegación. No afecta a los checks
de freeze, a los tests ni a las verificaciones SHA256 ya ejecutadas por los
exportadores y el informe posterior.

## Alcance

Archivos nuevos de implementación del experimento: `tools/mai_flash_benchmark.py`,
`tools/test_mai_flash_benchmark.py`, `tools/mai_flash_report.py` y
`tools/test_mai_flash_report.py`. Evidencia/documentación nueva solo bajo
`docs/experimentos/mai-code-flash-2026-11-06/` y la raíz temporal MAI declarada.
Sin edición de soluciones por el operador, reintentos de modelo, commits, push,
instalación global ni cambios a las cohortes previas.
