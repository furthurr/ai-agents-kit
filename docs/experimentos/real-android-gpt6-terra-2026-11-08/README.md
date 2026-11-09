# Experimento: Proyecto Real Android CRM — GPT 6.1 Terra

**Fecha:** 2026-11-08  
**Proyecto Base:** `mobile-android.zip` (CRM móvil Empresa Financiera Enterprise)  
**Modelo:** `openai/gpt-6.1-terra` (Proveedor OpenAI OAuth)  
**Herramienta de Orquestación:** [`tools/real_android_multimodel_benchmark.py`](../../../tools/real_android_multimodel_benchmark.py)  
**Datos Empíricos Completos:** [`resultados.json`](resultados.json)

---

## 1. Resumen de Aceptación Funcional

| Perfil / Brazo | T1: Media-Baja (`GBA-SEARCH-PROSPECTS`) | T2: Media-Alta (`GBA-BUZON-RETRY-UI`) | Tasa Global (T1+T2) |
|---|:---:|:---:|:---:|
| `v2_reforzado` | ✅ PASS (79.9s, 100k tok) | ❌ FAIL (164.3s, 405k tok) | 1/2 (50%) |
| `developer_actual` | ✅ PASS (77.9s, 142k tok) | ❌ FAIL (209.7s, 1.01M tok) | 1/2 (50%) |
| `v2` | ✅ PASS (72.6s, 99k tok) | ❌ FAIL (161.6s, 378k tok) | 1/2 (50%) |
| `build_mas` | ✅ PASS (84.6s, 114k tok) | ❌ FAIL (213.6s, 636k tok) | 1/2 (50%) |
| `build_sin_mas` | ✅ PASS (79.4s, 140k tok) | ❌ FAIL (199.1s, 847k tok) | 1/2 (50%) |

**Hallazgos Clave:**
1. **Tarea 1 (100% éxito):** Consumo de tokens extremadamente bajo (~100k tokens por ejecución en Tarea 1, el menor observado entre todos los modelos).
2. **Tarea 2 (0% éxito en oráculo externo):** Mismo comportamiento que MAI-Code: delegó a través de `cola.corregir()` sin inyectar `almacen` en el constructor de `BuzonSalidaViewModel`. La suite original de pruebas unitarias pasó al 100%.
