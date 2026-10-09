# Seguridad — Tablero de hallazgos

Alcance actual: revisión puntual del runner/evaluador F07, no del repositorio completo.

| ID | Severidad | Hallazgo | Referencia | Ubicación | Estado |
|---|---|---|---|---|---|
| SEC-0001 | 🟠 Alta | Confianza en declaraciones y writers/evidencia no separados | ASVS 5.0.0, CWE-284, CWE-693 | Prototipo `storage_rpc.py`; remediación supervisor/inspector/proxy observado | Resuelto: alcance F07 revisado |
| SEC-0002 | 🟡 Media | TOCTOU en apertura confiable de SQLite | CWE-367 | Prototipo `storage_rpc.py`; remediación `own_store`/quiescencia/captura | Resuelto: alcance F07 revisado |

Decisión y límites: `reviews/f07-2026-10-07.md`. No equivalen a revisión del proyecto completo.
