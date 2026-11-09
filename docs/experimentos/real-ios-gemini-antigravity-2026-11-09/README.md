# Experimento: Proyecto Real iOS CRM — Gemini 3.8 Flash (Google Antigravity Nativo)

> **Evidencia anonimizada:** identificadores y fragmentos originales han sido sustituidos u omitidos. Las métricas son históricas; no acreditan una ejecución nueva sobre los fixtures. Véase [alcance y límites](../PRIVACIDAD-MOVIL.md).

> **Fecha:** 2026-11-09  
> **Proyecto:** referencia histórica iOS anonimizada; el ZIP original no se distribuye. Los datos agregados del entorno original no describen un fixture nuevo.
> **Modelo:** `google/gemini-3.8-flash`  
> **Proveedor / Runtime:** **Google Antigravity Nativo** (`agentapi` / Language Server de Google DeepMind). Sin intermediarios de terceros ni GitHub Copilot.  
> **Diseño Experimental:** 3 Tareas de calibración equivalente a Android × 5 Brazos metodológicos = **15 ejecuciones completas**.

---

## 1. Resumen Ejecutivo

Este benchmark evalúa la eficacia, disciplina arquitectónica (Clean Architecture + MVVM + Coordinator), costo en tokens y calidad de código generado por el modelo **Gemini 3.8 Flash** en el proyecto productivo real **Proyecto Real iOS CRM**, ejecutado a través del arnés nativo de Antigravity.

### Resultados Globales

- **Tasa Global de Aceptación Funcional:** **7 / 15 (46.7%)**
- **Tokens Totales Consumidos (15 ejecuciones):** **2,886,697 tokens** (~2.89M tokens)
- **Duración Total Acumulada de Inferencia y Compilación:** **83.03 minutos**
- **Brazo Ganador en Tareas Complejas (Media-Alta + Alta):** **`developer_actual` (2/3, 66.7%)**, siendo el **único brazo en resolver exitosamente la Tarea 3 (Alta - Concurrencia y Cifrado CryptoKit)**.
- **Brazo de Mayor Consistencia en Tareas 1 y 2:** **`build_sin_mas` (2/3, 66.7%)**.
- **Comportamiento en Tarea 2 (Media-Alta):** **100% de éxito (5/5 brazos aprobados)**, demostrando una excelente adherencia del modelo a los patrones de presentación y gestión de estado en Swift / SwiftUI.

---

## 2. Matriz de Resultados (15 Ejecuciones)

| Tarea / Nivel | Brazo Metodológico | Oráculo Externo | Suite Original (No Regresión) | Aceptación Funcional | LOC Prod | LOC Test | Tokens Totales | Pasos (Steps) | Duración |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **T1: Media-Baja** (`GIOS-SEARCH-PROSPECTS`) | `v2_reforzado` | ❌ Fallo |  Pasa | ❌ No | 197 | 360 | 132,768 | 30 | 145.5s |
| | `developer_actual` | ❌ Fallo |  Pasa | ❌ No | 101 | 296 | 272,178 | 73 | 491.1s |
| | `v2` | ❌ Fallo | ❌ Fallo | ❌ No | 111 | 370 | 99,112 | 17 | 75.3s |
| | `build_mas` | ❌ Fallo | ❌ Fallo | ❌ No | 181 | 344 | 100,297 | 21 | 105.3s |
| | `build_sin_mas` |  **Pasa** |  **Pasa** |  **Aprobado** | 107 | 306 | 361,936 | 101 | 1127.3s |
| **T2: Media-Alta** (`GIOS-BUZON-RETRY-UI`) | `v2_reforzado` |  **Pasa** |  **Pasa** |  **Aprobado** | 85 | 255 | 224,074 | 55 | 340.8s |
| | `developer_actual` |  **Pasa** |  **Pasa** |  **Aprobado** | 93 | 252 | 224,104 | 60 | 405.9s |
| | `v2` |  **Pasa** |  **Pasa** |  **Aprobado** | 269 | 253 | 386,745 | 111 | 676.4s |
| | `build_mas` |  **Pasa** |  **Pasa** |  **Aprobado** | 87 | 287 | 228,442 | 58 | 410.9s |
| | `build_sin_mas` |  **Pasa** |  **Pasa** |  **Aprobado** | 89 | 162 | 183,152 | 46 | 320.8s |
| **T3: Alta** (`GIOS-QUEUE-CONCURRENCY-CIPHER`) | `v2_reforzado` | ❌ Fallo |  Pasa | ❌ No | 145 | 385 | 100,333 | 18 | 140.4s |
| | `developer_actual` |  **Pasa** |  **Pasa** |  **Aprobado** | 186 | 346 | 375,695 | 56 | 571.4s |
| | `v2` | ❌ Fallo |  Pasa | ❌ No | 262 | 296 | 62,847 | 11 | 55.3s |
| | `build_mas` | ❌ Fallo |  Pasa | ❌ No | 0 | 11 | 59,902 | 12 | 80.3s |
| | `build_sin_mas` | ❌ Fallo |  Pasa | ❌ No | 0 | 0 | 75,112 | 6 | 35.2s |

---

## 3. Resumen Consolidado por Brazo

| Brazo Metodológico | Aceptación (3 Tareas) | Tasa de Éxito | Tokens Totales | Duración Acumulada | Pasos Promedio | LOC Prod Prom. |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`developer_actual`** | **2 / 3** | **66.7%** | 871,977 | 24.5 min | 63.0 | 126.7 |
| **`build_sin_mas`** | **2 / 3** | **66.7%** | 620,200 | 24.7 min | 51.0 | 65.3 |
| **`v2_reforzado`** | **1 / 3** | **33.3%** | 457,175 | 10.4 min | 34.3 | 142.3 |
| **`v2`** | **1 / 3** | **33.3%** | 548,704 | 13.5 min | 46.3 | 214.0 |
| **`build_mas`** | **1 / 3** | **33.3%** | 388,641 | 9.9 min | 30.3 | 89.3 |

---

## 4. Análisis Detallado por Tarea y Arquitectura

### Tarea 1: Media-Baja (`GIOS-SEARCH-PROSPECTS`)
- **Objetivo:** Implementar en `Domain/` la entidad `ProspectoItem` y el caso de uso `SearchProspectsUseCase` con normalización de diacríticos Unicode (NFD/regex), filtrado multi-campo (nombre, apellidos, RFC, teléfono) y ordenamiento determinista alfabético compuesto.
- **Hallazgo Clave:**
  - `build_sin_mas` fue el único brazo en aprobar el 100% de los criterios del oráculo (`OracleSearchProspectsTests.swift`). Al carecer de abstracciones o convenciones intermedias, operó 101 pasos explorando la compilación directamente hasta calibrar con exactitud matemática el ordenamiento y el filtrado insensible a mayúsculas/acentos.
  - `developer_actual` implementó toda la arquitectura Clean completa (`ProspectoItem.swift` y `SearchProspectsUseCase.swift`) y 296 líneas de pruebas unitarias en 73 pasos. Sin embargo, presentó una discrepancia en la política de ordenamiento secundario (retornó 3 prospectos filtrados en lugar de 4 en uno de los asertos de frontera), fallando el oráculo estricto.
  - `v2_reforzado` definió contratos alternativos no coincidentes exactamente con el protocolo `DefaultSearchProspectsUseCase`.
  - `v2` y `build_mas` sufrieron un bloqueo de base de datos intermedia de Xcode (`build.db locked`) durante la concurrencia de builds que impidió la finalización del oráculo.

### Tarea 2: Media-Alta (`GIOS-BUZON-RETRY-UI`)
- **Objetivo:** Remediación del hallazgo de calidad `QLT-0017` en la capa de Presentación SwiftUI. Visibilidad del estado de la cola offline, reintentos de acciones en conflicto (`FAILED`) y transiciones de estado en `FixtureComponent1`.
- **Hallazgo Clave:**
  - **Éxito unánime: 5/5 brazos aprobaron al 100%** tanto el oráculo (`OracleBuzonRetryUiTests.swift`) como la suite original de no-regresión.
  - **Sobregeniería vs Sobriedad:**
    - `v2_reforzado` y `developer_actual` mostraron la implementación más sobria y quirúrgica: ~85-93 LOC de producción, modificando `FixtureComponent1.swift` e introduciendo `BuzonSalidaViewModel.swift` y `EstadoAccesoBuzon.swift`.
    - `v2` incurrió en **sobreingeniería sustancial (269 LOC de producción)**, creando una vista completa `BuzonSalidaView.swift` con componentes SwiftUI auxiliares no solicitados en el spec.
    - `build_sin_mas` resolvió la tarea en 46 pasos y 183k tokens, siendo el brazo más rápido y económico en esta tarea.

### Tarea 3: Alta (`GIOS-QUEUE-CONCURRENCY-CIPHER`)
- **Objetivo:** Implementación de deduplicación atómica (`enqueueIdempotente`), concurrencia multihilo segura mediante primitivas de sincronización (`NSLock` / Actor / colas concurrentes) y cifrado transparente AES-GCM con `CryptoKit` para el payload sensible en almacenamiento offline.
- **Hallazgo Clave:**
  - **`developer_actual` fue el GANADOR ABSOLUTO y ÚNICO aprobador de la tarea.**
    - Ejecutó 56 pasos, 375,695 tokens, y produjo **186 líneas de código Swift de producción impecables**.
    - Importó `CryptoKit` y `Security`, implementó `SymmetricKey`, cifrado y descifrado AES-GCM con nonce determinista para idempotencia, y protegió el acceso a la cola contra condiciones de carrera concurrentes (`concurrency-safe`).
    - Añadió además su propia suite de pruebas `FixtureComponent2ConcurrencyTests.swift` (346 LOC) con `DispatchQueue.concurrentPerform` para probar saturación de 50 hilos concurrentes.
    - Aprobó el oráculo externo (`OracleQueueConcurrencyCipherTests.swift`) y la suite original con cero fallos.
  - Los otros 4 brazos (`v2_reforzado`, `v2`, `build_mas`, `build_sin_mas`) **sub-iteraron y se detuvieron prematuramente** (entre 6 y 18 pasos), concluyendo el turno sin haber implementado el método `enqueueIdempotente` ni la integración con CryptoKit.

---

## 5. Comparativa Multi-Plataforma: Android vs iOS

Al comparar estos resultados con los obtenidos previamente en **Android CRM** (`app-crm-android-enterprise`):

| Dimensión Analizada | Android CRM (Kotlin / Coroutines) | iOS CRM (Swift / Xcode) | Observación Comparativa |
|---|---|---|---|
| **Rendimiento de `developer_actual`** | 3/3 (100% Aprobado) | 2/3 (66.7% Aprobado) | En ambas plataformas demostró ser el perfil más robusto para tareas de alta complejidad técnica (concurrencia, cifrado y estado). |
| **Comportamiento en Tarea 2 (Media-Alta)** | 1/5 brazos en modelos alternativos por divergencia de constructor | **5/5 brazos (100% Aprobado)** en iOS | En Swift, el manejo de dependencias opcionales y extensiones en `FixtureComponent1` facilitó que todos los perfiles alcanzaran la compatibilidad exacta con el oráculo. |
| **Resistencia a la Complejidad (Tarea 3)** | Resuelto consistentemente con Kotlin Mutex / Room | Solo resuelto por `developer_actual` (Swift / CryptoKit) | En iOS, la combinación de `CryptoKit`, `NSLock` y `DispatchQueue` requirió mayor capacidad de razonamiento iterativo; los perfiles no especializados se rindieron tras pocos pasos. |
| **Gasto de Tokens Promedio por Tarea** | ~180k - 250k tokens | ~192k tokens | Similar eficiencia de contexto en ambos ecosistemas. |
| **Estabilidad de Herramientas** | Gradle daemon requirió aislamiento de lock | Xcode build database (`build.db`) requiere compilación secuencial estricta | En ambas plataformas se confirmó que ejecuciones concurrentes en el mismo DerivedData/Gradle cache provocan bloqueos a nivel de sistema operativo. |

---

## 6. Conclusiones y Recomendaciones de Gobernanza

1. **Eficiencia del Proveedor Antigravity Nativo:**
   La ejecución a través de `agentapi` de Antigravity demostró una fiabilidad del 100% en invocación de herramientas nativas (`write_file`, `edit_file`, `read_file`, `run_command` con `xcodebuild`), sin necesidad de depender de pasarelas de terceros como GitHub Copilot para modelos Gemini.
2. **Superioridad de `developer_actual` en Tareas Críticas:**
   Al igual que en Android, el agente `developer_actual` demuestra que contar con instrucciones explícitas de implementación directa (sin pausas interactivas y con enfoque exhaustivo en pruebas de regresión) es el único mecanismo que logra resolver con éxito features de nivel **Alta (High)** que involucran criptografía y concurrencia.
3. **Control de Sobregeniería:**
   El perfil `v2` tiende a generar vistas auxiliares no solicitadas en SwiftUI (269 LOC vs 85-93 LOC en los demás). Se recomienda mantener los lineamientos de sobriedad de `developer_actual` para desarrollos productivos en la aplicación empresarial.
