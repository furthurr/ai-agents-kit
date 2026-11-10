# Experimento: Proyecto Real Android CRM — GPT 6 Luna

> Evidencia histórica anonimizada. Véase [privacidad y límites](../../PRIVACIDAD-MOVIL.md); el ZIP original no se distribuye.

**Fecha:** 2026-11-08  
**Proyecto Base:** referencia Android anonimizada; usar un fixture sintético para nuevas ejecuciones.
**Modelo:** `openai/gpt-6-luna` (Proveedor OpenAI OAuth)  
**Herramienta de Orquestación:** [`tools/real_android_multimodel_benchmark.py`](../../../tools/real_android_multimodel_benchmark.py)  
**Datos Empíricos Completos:** [`resultados.json`](resultados.json)

---

## 1. Resumen de Aceptación Funcional

| Perfil / Brazo | T1: Media-Baja (`GBA-SEARCH-PROSPECTS`) | T2: Media-Alta (`GBA-BUZON-RETRY-UI`) | Tasa Global (T1+T2) | Total Tokens (T1+T2) |
|---|:---:|:---:|:---:|---:|
| `v2_reforzado` | ✅ PASS (82.8s, 95k tok) | ❌ FAIL (167.3s, 529k tok) | 1/2 (50%) | 625,099 |
| `developer_actual` | ✅ PASS (118.3s, 195k tok) | ❌ FAIL (165.9s, 730k tok) | 1/2 (50%) | 926,556 |
| `v2` | ✅ PASS (84.1s, 106k tok) | ❌ FAIL (155.5s, 520k tok) | 1/2 (50%) | 627,264 |
| `build_mas` | ✅ PASS (82.5s, 111k tok) | ❌ FAIL (144.2s, 312k tok) | 1/2 (50%) | 423,743 |
| `build_sin_mas` | ✅ PASS (82.4s, 94k tok) | ❌ FAIL (130.1s, 201k tok) | 1/2 (50%) | 295,481 |

**Hallazgos Clave:**
1. **Récord Absoluto de Eficiencia de Tokens:** Consumió solo **2,898,143 tokens** en las 10 ejecuciones (T1: 602k, T2: 2.29M), siendo el modelo más económico y austero de todos los evaluados.
2. **Tarea 1 (100% éxito):** Tiempos muy estables (~82-84s) en casi todos los brazos y soluciones limpias en `:core:domain`.
3. **Tarea 2 (0% éxito en oráculo externo):** Al igual que GPT 6.1 Terra y MAI-Code, implementó `reintentarAltaEnConflicto` reutilizando `cola.corregir(...)` sin modificar el constructor de `BuzonSalidaViewModel`, provocando fallo de compilación con el oráculo externo. La suite original de pruebas unitarias pasó al 100%.
