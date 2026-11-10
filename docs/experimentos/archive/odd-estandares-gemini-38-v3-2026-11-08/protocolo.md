# Cohorte v3 de ODD con estándares — Gemini 3.8 Flash (Timeout 1200s Forzado y Context Guard)

ID: odd-standards-gemini38-v3-20261108.
Autorización del usuario:
«Bien deja registro de esto por ahora me interesa terminar el experimento, porque se o terunpio el otro agente? Soluciónalo y Reintenta»

## Diagnóstico del Lote Anterior (v2) y Corrección Definitiva

En el lote v2 se resolvieron con éxito los problemas de contexto:
- `TASK-2-ODD-r1`: Completado con éxito en 257,513 s (2.324.553 tokens), 100% pruebas aprobadas.
- `TASK-2-ADJUSTED-r1`: Completado con éxito en 316,514 s (2.719.641 tokens), cargando ambas skills antes de código y 100% pruebas aprobadas.
- `TASK-2-ADJUSTED-r2`: Pasó el 100% de las pruebas funcionales (`functional_pass: True`), pero tardó 600,136 s. Aunque `invoke` tenía default `limit=1200`, el llamador interno `runner.py` línea 568 pasaba `limit=600` como argumento explícito, provocando un corte por SIGTERM a los 600 segundos.

## Solución en v3

1. **Forzado estricto de `timeout=1200` en `invoke`**: Se ignora el argumento `limit=600` heredado del runner base y se aplica `actual_limit = TIMEOUT` (1200 s / 20 min) en `child.communicate`, dando tiempo suficiente para que todas las celdas de Django terminen.
2. **Context Guard**: Se mantiene la especificación que evita la creación de micro-logs redundantes en `odd/tasks/` para conservar el contexto por debajo de 100k tokens.
3. **Ejecución secuencial (`max_workers=1`)**: Orden simétrico (R1: odd/adj, R2: adj/odd, R3: odd/adj) con aislamiento total.
