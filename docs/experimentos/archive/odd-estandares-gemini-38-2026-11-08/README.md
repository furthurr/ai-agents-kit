# ODD con estándares — Cohorte limpia Gemini 3.8 Flash

**Estado: Lote PARCIAL detenido por regla de parada en R1.**
ID: `odd-standards-gemini38-v1-20261108`. Fecha: 2026-11-08.
Modelo ejecutado: `github-copilot/gemini-3.8-flash` (Gemini 3.8 Flash, vía proveedor Copilot activo en OpenCode 1.18.34).

## 1. Resumen de ejecución

Se preparó una cohorte independiente y limpia para evaluar ODD Original frente a ODD Ajustado con Estándares en la tarea Alta (TASK-2 de LocalLibrary: reservas persistidas, idempotencia, concurrencia SQLite y UI).

| Métrica | ODD Histórico (R1) | ODD Ajustado con Estándares (R1) |
|---|---:|---:|
| **Aceptación funcional (oráculos externos 9/9)** | **Aprobada (1/1)** | Incompleta (0/1) |
| **Preservación suite original (43/43)** | **Aprobada (1/1)** | Incompleta (0/1) |
| **Carga de `data-api` por contenido** | 0/1 | **1/1 (Antes de código)** |
| **Carga de `ui-design` por contenido** | 0/1 | **1/1 (Antes de código)** |
| **Tokens comparables** | 2.778.347 | 3.914.147 |
| **Tiempo de conversación** | 600,183 s | 570,916 s |
| **Herramientas utilizadas** | 50 | 65 |
| **Pasos ejecutados** | 50 | 59 |
| **Razón de interrupción / parada** | Timeout de proceso a los 600 s (+0,18 s) | APIError HTTP 400 (límite de contexto Copilot >100k) |

## 2. Hallazgos técnicos observados

1. **ODD Original:**
   - Logró implementar toda la funcionalidad requerida de forma impecable: pasaron las 43 pruebas originales de LocalLibrary y los 9 oráculos externos.
   - No consultó ni cargó ninguna de las skills de dominio (`data-api` ni `ui-design`).
   - El proceso excedió el límite estricto de timeout de 600 s por tan solo 183 ms (600,183 s), lo que resultó en `timeout: true` (`returncode: -15`).

2. **ODD Ajustado:**
   - Cumplió con rigor metodológico la selección y carga por contenido de ambas skills de dominio (`data-api` y `ui-design`) antes de realizar el primer cambio de producto.
   - El procedimiento generó mayor exploración, lectura de criterios y pasos de edición (65 herramientas frente a 50).
   - En el paso 125, la longitud acumulada del contexto en la conversación alcanzó 100.312 tokens en una sola petición (`cache_read: 95.756`), excediendo el límite de ventana por solicitud del endpoint de Copilot y provocando un error terminal `HTTP 400`.

3. **Parada reglamentaria:**
   - Siguiendo el protocolo establecido para evitar bucles de reintentos o sesgos de selección, la cohorte detuvo nuevas repeticiones (R2 y R3) al fallar R1.

## 3. Evidencia preservada

- Protocolo: [`protocolo.md`](protocolo.md)
- Resumen estructurado: [`summary-audit.json`](summary-audit.json)
- Runner utilizado: [`tools/odd_standards_gemini38.py`](../../../../tools/odd_standards_gemini38.py)
- Pruebas unitarias de integridad: [`tools/test_odd_standards_gemini38.py`](../../../../tools/test_odd_standards_gemini38.py)
- Trazas completas y registros de ejecución: `/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/odd-standards-gemini38-20261108/`
