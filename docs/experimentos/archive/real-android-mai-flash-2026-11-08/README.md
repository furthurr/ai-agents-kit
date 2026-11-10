# Experimento: Proyecto Real Android CRM — MAI-Code-1.1-Flash

> Evidencia histórica anonimizada. Véase [privacidad y límites](../../PRIVACIDAD-MOVIL.md); el ZIP original no se distribuye.

**Fecha:** 2026-11-08  
**Proyecto Base:** referencia Android anonimizada; usar un fixture sintético para nuevas ejecuciones.
**Modelo:** `github-copilot/mai-code-1.1-flash` (Proveedor GitHub Copilot)  
**Herramienta de Orquestación:** [`tools/real_android_multimodel_benchmark.py`](../../../../tools/real_android_multimodel_benchmark.py)
**Datos Empíricos Completos:** [`resultados.json`](resultados.json)

---

## 1. Resumen de Aceptación Funcional

| Perfil / Brazo | T1: Media-Baja (`GBA-SEARCH-PROSPECTS`) | T2: Media-Alta (`GBA-BUZON-RETRY-UI`) | Tasa Global (T1+T2) |
|---|:---:|:---:|:---:|
| `v2_reforzado` | ✅ PASS (82.0s, 186k tok) | ❌ FAIL (140.1s, 465k tok) | 1/2 (50%) |
| `developer_actual` | ✅ PASS (46.4s, 154k tok) | ❌ FAIL (166.3s, 595k tok) | 1/2 (50%) |
| `v2` | ✅ PASS (51.5s, 156k tok) | ❌ FAIL (133.2s, 437k tok) | 1/2 (50%) |
| `build_mas` | ✅ PASS (75.0s, 218k tok) | ❌ FAIL (136.7s, 451k tok) | 1/2 (50%) |
| `build_sin_mas` | ✅ PASS (45.8s, 168k tok) | ❌ FAIL (268.7s, 969k tok) | 1/2 (50%) |

**Hallazgos Clave:**
1. **Tarea 1 (100% éxito):** Excelente rapidez y bajo consumo de tokens en tareas directas de `:core:domain`.
2. **Tarea 2 (0% éxito por divergencia de diseño en ViewModel):** Resolvió la lógica delegando en `cola.corregir()` en vez de agregar el parámetro `almacen` en el constructor de `BuzonSalidaViewModel`, provocando fallo de compilación con el oráculo externo (`No parameter with name 'almacen' found`). La suite original del proyecto pasó al 100%.
