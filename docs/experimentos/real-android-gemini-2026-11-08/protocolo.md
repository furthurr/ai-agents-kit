# Protocolo Experimental: Proyecto Real Android CRM con Gemini 3.8

**Fecha de congelación:** 2026-11-08  
**Proyecto base:** referencia histórica Android anonimizada; el ZIP privado original no se distribuye.
**Entorno técnico:** macOS (Apple Silicon), OpenCode 1.18.34, Gradle Wrapper 9.8.0, OpenJDK 21.0.12, Android SDK 37 (API 37).  
**Modelo único:** `github-copilot/gemini-3.8-flash` (Gemini 3.8 Flash, endpoint verificado con tool calling y razonamiento nativo).

---

## 1. Objetivo y Pregunta de Investigación

Evaluar el rendimiento comparativo, la calidad de entrega y la fidelidad metodológica de cinco configuraciones del Multi-Agent System (MAS) en un proyecto real de producción Android (`App CRM Móvil Empresarial`).

El objetivo es contrastar si los candidatos evolucionados (`Developer v2` y `Developer v2 reforzado`) y el contexto MAS aportan mejoras mensurables frente al agente `Developer instalado` y al baseline nativo (`Main agent`), manteniendo:
1. Cero regresiones en la suite original de pruebas unitarias.
2. Cumplimiento determinista de oráculos externos independientes.
3. Eficiencia en el consumo de tokens comparables y tiempo de resolución.
4. Respeto estricto del sandbox de permisos y seguridad.

---

## 2. Los Cinco Tratamientos / Perfiles Comparativos

| Brazo | Identificador | Tipo de Agente | Prompt / Procedimiento | Contexto MAS disponible |
|---|---|---|---|---|
| **1** | `v2_reforzado` | Agente Developer reforzado | Candidato Developer v2 + Refuerzos ODD (Delta A: regresión de comportamiento compartido; Delta B: reanudación reconciliada). | Sí: `AGENTS.md` + `.architecture/`, `.data/`, `.design/`, `.quality/`, `.security/`, `.navigator/` |
| **2** | `v2` | Developer v2 candidato2 | Candidato 2 ligero con carga selectiva modular de dominios (`data-api` y `ui-design`). | Sí: `AGENTS.md` + documentación MAS completa |
| **3** | `developer_actual` | Developer actual instalado | Procedimiento canónico Developer v1 (PLAN, ejecución integral UI/datos/negocio, cierre documental). | Sí: `AGENTS.md` + documentación MAS completa |
| **4** | `build_sin_mas` | Main agent sin MAS | Prompt nativo/base de OpenCode (`build`), sin instrucciones MAS. | **No:** Se eliminan `AGENTS.md` y todas las carpetas `.architecture/`, `.data/`, `.design/`, etc. |
| **5** | `build_mas` | Main agent con MAS | Prompt nativo/base de OpenCode (`build`), sin skill de Developer. | **Sí:** Conserva `AGENTS.md` y toda la documentación MAS como contexto de consulta. |

---

## 3. Estratificación de Tareas

Las tareas han sido diseñadas para abordar tres niveles de complejidad real en la arquitectura limpia del CRM:

1. **Tarea 1 — Media-Baja (`GBA-SEARCH-PROSPECTS`):**
   - Módulo: `:core:domain`
   - Dominio: Lógica de negocio pura, filtrado multi-criterio, sanitización, normalización de acentos y ordenamiento en memoria.
   - Restricción: Cero modificaciones a esquemas de base de datos o endpoints de red.
2. **Tarea 2 — Media-Alta (`GBA-BUZON-RETRY-UI`):**
   - Módulos: `:app` (`features/offline/buzon`) y `:core:domain` (`queue`).
   - Dominio: Remediación del hallazgo de fiabilidad `QLT-0017` en `AccesoBuzonViewModel`, modelado de StateFlow fidedigno (error vs vacío) y UI Compose interactiva para reintentar altas en `CONFLICTO`.
   - Restricción: Coordinación UI + Dominio sin alterar el flujo normal de sincronización.
3. **Tarea 3 — Alta (`GBA-QUEUE-CONCURRENCY-CIPHER`):**
   - Módulos: `:core:data` (`local/offline`), `:core:security` (`crypto`) y `:core:domain`.
   - Dominio: Persistencia en Room + SQLCipher, deduplicación atómica bajo concurrencia real (multi-corutina con barreras), cifrado obligatorio de PII con `WrappedKeyCipher` y recuperación segura de candados en `ENVIANDO` sin corromper `AMBIGUO`.
   - Restricción: Ningún dato personal en claro en SQLite; rollback atómico obligatorio ante excepciones criptográficas.

---

## 4. Condiciones de Aislamiento y Entorno

- **Copia fresca por celda:** Cada ejecución se realiza en un directorio aislado `/tmp/real-android-benchmark/runs/<task>/<arm>`, descomprimido directamente desde el zip original.
- **Configuración de variables de entorno:**
  - `JAVA_HOME=/opt/homebrew/opt/openjdk@21`
  - `ANDROID_HOME=[LOCAL_MOBILE_WORKSPACE]`
  - `local.properties` inyecta automáticamente la ruta local correcta del SDK.
- **Políticas de permisos (`permission.json`):**
  - Permitido: lectura y edición dentro del workspace; ejecución de comandos Gradle de test unitario (`./gradlew :core:domain:test*`, `./gradlew :app:testDebugUnitTest*`, `./gradlew :core:data:test*`), `git status`, `git diff`.
  - Denegado: `git commit`, `git push`, comandos de red externa, lectura de secretos/keystores (`*.jks`, `*.keystore`, `*.key`, `auth.json`, etc.).
- **Límites de ejecución (Presupuesto):**
  - Pasos máximos: 60 por conversación.
  - Timeout: 1.800 s (30 min) por celda.
  - Umbral de tokens: 5.000.000 tokens comparables por conversación.
  - Sin reintentos interactivos ni corrección guiada por el evaluador.

---

## 5. Criterios de Evaluación y Parada

1. **Aceptación Funcional Primaria:**
   - La suite original de pruebas unitarias del módulo correspondiente debe pasar al 100% (cero regresiones).
   - La suite de oráculos externos de la tarea debe pasar al 100%.
   - El código debe compilar limpiamente con Gradle 9.8.0 y JDK 21.
2. **Entrega de Pruebas Propias:**
   - Se cuantifica y valida si el participante añadió pruebas unitarias persistidas para respaldar su entrega.
3. **Métricas Comparables:**
   - Tokens totales = `input + output + cache_read + cache_write + reasoning`.
   - Tiempo de conversación (s) y llamadas a herramientas.
