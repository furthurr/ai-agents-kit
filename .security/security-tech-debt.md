# Seguridad — Tablero de hallazgos

Alcance: hallazgos históricos del kit y revisión puntual del runner/evaluador F07.
Revalidación/remediación del kit: 2026-10-14, MAS 3.2.0 más cambios locales.
No es una auditoría completa del repositorio ni de las instalaciones del usuario.

## Kit MAS

Los IDs SEC-0001/SEC-0002 colisionan históricamente con los de F07. Se preservan
para trazabilidad y se desambiguan por alcance y archivo; citar siempre ambos.

| ID | Severidad | Hallazgo | Evidencia/seguimiento | Estado |
|---|---|---|---|---|
| SEC-0005 (kit) | 🟡 Media | Instrucciones del workspace en SDD | [Finding](findings/SEC-0005-inyeccion-contexto-sdd.md) | Política implementada; validación LLM/otros hosts pendiente |
| SEC-0001 (kit) | 🟡 Media | Capacidades de Code Review | [Finding](findings/SEC-0001-capacidades-amplias-code-review.md) | Mitigación implementada; validación LLM/otros hosts pendiente |
| SEC-0003 (kit) | 🟢 Baja | Importador sigue enlaces | [Finding](findings/SEC-0003-importador-sigue-enlaces.md) | Fix multiplataforma; 10 tests locales OK; CI Windows pendiente |
| SEC-0002 (kit) | 🟢 Baja | Tags mutables de CI | [Finding](findings/SEC-0002-acciones-ci-tags-mutables.md) | Resuelto en workflows; ejecución remota pendiente |
| SEC-0004 (kit) | 🟢 Baja | Persistencia de agentes obsoletos | [Finding](findings/SEC-0004-agentes-obsoletos-en-instalaciones.md) | Política opt-in verificada; 26 tests OK; instalaciones reales no migradas |

Evidencia consolidada y límites: [remediación MAS 3.2.0](reviews/remediacion-mas-3.2.0.md).

## Laboratorio F07

| ID | Severidad | Hallazgo | Referencia | Ubicación | Estado |
|---|---|---|---|---|---|
| SEC-0001 | 🟠 Alta | Confianza en declaraciones y writers/evidencia no separados | ASVS 5.0.0, CWE-284, CWE-693 | Prototipo `storage_rpc.py`; remediación supervisor/inspector/proxy observado | Resuelto: alcance F07 revisado |
| SEC-0002 | 🟡 Media | TOCTOU en apertura confiable de SQLite | CWE-367 | Prototipo `storage_rpc.py`; remediación `own_store`/quiescencia/captura | Resuelto: alcance F07 revisado |

Decisión y límites: `reviews/f07-2026-10-07.md`. No equivalen a revisión del proyecto completo.
