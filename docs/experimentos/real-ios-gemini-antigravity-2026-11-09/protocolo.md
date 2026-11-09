# Protocolo: Proyecto Real iOS CRM — Gemini 3.8 Flash (Antigravity Nativo)

**Fecha:** 2026-11-09  
**Proyecto Base:** referencia histórica iOS anonimizada; el ZIP privado original no se distribuye.
**Entorno de Compilación:** Xcode 26.1 (Build 17B55), iOS Simulator 26.1  
**Modelo:** `Gemini 3.8 Flash`  
**Proveedor:** **Google Antigravity Nativo** (`agentapi` / runtime oficial Google DeepMind), sin intermediación de GitHub Copilot ni envoltorios de terceros.  
**Herramienta de Orquestación:** [`tools/real_ios_antigravity_benchmark.py`](../../../tools/real_ios_antigravity_benchmark.py)

---

## 1. Justificación y Objetivos

Evaluar de forma rigurosa y autónoma los 5 perfiles metodológicos del MAS sobre la base de código real de producción iOS de Empresa Financiera Enterprise (`CRM Empresarial`), implementada en Swift 6, SwiftUI, Clean Architecture, MVVM + Coordinators y Swift Testing / XCTest.

Se garantiza paridad de complejidad estricta contra las 3 tareas del benchmark previo de Android:
1. **Tarea 1 (Media-Baja):** `GIOS-SEARCH-PROSPECTS` (Capa `Domain/`). Búsqueda reactiva, normalización de cadenas (trim, acentos, mayúsculas) y filtrado de prospectos.
2. **Tarea 2 (Media-Alta):** `GIOS-BUZON-RETRY-UI` (Capa `Presentacion/`). Remediación arquitectónica de buzón offline, retención de visibilidad ante errores y reintento de altas en conflicto.
3. **Tarea 3 (Alta):** `GIOS-QUEUE-CONCURRENCY-CIPHER` (Capa `Data/`). Deduplicación atómica por `(idEjecutivo, rfc, tipoDeAlta)`, exclusión mutua concurrente con `actor` de Swift / `NSLock` y cifrado CryptoKit AES-GCM.

---

## 2. Los 5 Brazos Metodológicos

1. **`build_sin_mas`:** Agente genérico sin contexto documental ni AGENTS.md (Control negativo).
2. **`build_mas`:** Agente genérico con acceso a la documentación `.architecture/`, `.data/`, `.quality/`, etc.
3. **`developer_actual`:** Agente Developer v1 canónico instalado, evaluado en ejecución autónoma con directiva de aprobación previa.
4. **`v2`:** Agente Developer v2 modular candidato 2 (con dominios `data-api` y `ui-design`).
5. **`v2_reforzado`:** Agente Developer v2 enriquecido con los dos refuerzos ODD (Delta A: Comprobación y Regresión; Delta B: Continuidad reconciliada).

---

## 3. Condiciones de Control y Aislamiento

- Cada celda se ejecuta en un workspace limpio extraído de `mobile-ios.zip` en `/tmp/real-ios-benchmark/`.
- Protección estricta de credenciales, secretos (`*.p12`, `*.mobileprovision`, tokens, llaves de firma) y `AGENTS.md`.
- Verificación funcional doble:
  1. **Oráculo Externo:** Suite XCTest inyectada temporalmente para verificar los contratos requeridos.
  2. **Suite Original:** Verificación de no-regresión sobre las pruebas unitarias existentes del proyecto (`xcodebuild test`).
