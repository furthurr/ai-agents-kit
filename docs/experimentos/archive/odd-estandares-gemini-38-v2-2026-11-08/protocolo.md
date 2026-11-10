# Cohorte v2 de ODD con estándares — Gemini 3.8 Flash (Solución de Timeout y Contexto)

ID: odd-standards-gemini38-v2-20261108.
Autorización del usuario:
«Bien deja registro de esto por ahora me interesa terminar el experimento, porque se o terunpio el otro agente? Soluciónalo y Reintenta»

Los lotes anteriores (`odd-standards-v1-20261105`, `odd-standards-retry-v1-20261105` y `odd-standards-gemini38-v1-20261108`) permanecen intactos como evidencia histórica. Este lote v2 implementa las soluciones técnicas a las dos causas de interrupción identificadas:

## 1. Correcciones de Infraestructura y Procedimiento

1. **Ampliación de Timeout a 1200 s:**
   Se eleva el límite simétrico por invocación de 600 s a 1200 s (20 minutos), replicando la solución de `odd-standards-luna-1800` para evitar cortes por milisegundos en tareas Django completas.
2. **Alineación con el Acuerdo de Continuidad (Prevención de desbordamiento >100k tokens):**
   Se refuerza en la especificación que para esta tarea el diff de código y los oráculos bastan para reanudar, evitando que el agente cree archivos de seguimiento redundantes en `odd/tasks/` y llamadas continuas a `todowrite` que saturan la ventana de contexto de Copilot (>100k tokens).
3. **Ejecución Secuencial (`max_workers=1`):**
   Las celdas se ejecutan una a una para evitar contención de red y bloqueos de base de datos durante las pruebas concurrentes.

## 2. Invariantes

- Modelo ejecutado: `github-copilot/gemini-3.8-flash` (Gemini 3.8 Flash, vía proveedor Copilot activo en OpenCode 1.18.34).
- Agentes y skills byte a byte idénticos al lote anterior, con namespaces `oa` (histórico) y `ob` (ajustado con estándares).
- Baseline idéntico y suite de referencia (43 pruebas originales + 9 externas) pasando antes del freeze.
- Tarea TASK-2 literal de LocalLibrary (reservas UI/API, persistencia, idempotencia y concurrencia SQLite).
- Criterio de parada: ante cualquier error API/proceso o timeout se detienen nuevas repeticiones y se conserva la evidencia.
