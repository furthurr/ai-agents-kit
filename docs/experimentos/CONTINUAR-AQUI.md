# Punto de continuidad — decisiones Developer, SDD y ODD

**Leer primero en la siguiente sesión.** Este archivo conserva contexto, no
autoriza implementación, instalación, commits, publicación o más inferencia.
Fecha de consolidación: **2026-11-08** (acumulado de cohortes 2026-11-04 a 2026-11-08).
Repositorio: `ai-agents-kit`, baseline Git observado
`f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.

---

## 1. Dónde quedamos exactamente

El usuario solicitó formalmente: **registrar y consolidar todos los datos de los experimentos terminados**.

Durante la secuencia de evaluaciones entre el 4 y el 8 de noviembre, se completaron benchmarks sistemáticos en tres frentes fundamentales:
1. **Comparación multi-modelo y metodológica:** Evaluaciones de Developer actual, variantes compactas/v2, SDD proporcional y ODD experimental en tres familias de modelos (Gemini 3.8 Flash, GPT-6 Luna max y MAI-Code 1.1 Flash).
2. **Validación en proyectos reales:** Pruebas complejas sobre LocalLibrary (Django/SQLite con concurrencia e idempotencia) y el proyecto real de producción `Proyecto Real Android CRM` (Kotlin multi-módulo, Jetpack Compose, Room y SQLCipher).
3. **El dilema de los Estándares de Dominio (`data-api` y `ui-design`):**
   - **Evaluación empírica:** En la cohorte balanceada final con Gemini 3.8 Flash (`odd-standards-gemini38-v3-20261108`), aplicar obligatoriamente los estándares de dominio antes de escribir código logró **100 % de aceptación funcional (4/4 celdas)** y **0 errores de herramientas**, con un sobrecoste de solo **+17,42 % tokens** y **+4,54 % tiempo** (+42,5 s).
   - **Veredicto de ingeniería:** Omitir `data-api` y `ui-design` es **MALO**. Aunque simula un ahorro de tokens a corto plazo en tareas sintéticas, genera **falso ahorro por degradación**: produce contratos JSON inconsistentes, omisión de códigos de estado HTTP semánticos, pérdida de transaccionalidad/idempotencia, ruptura del sistema visual y ausencia total de accesibilidad (a11y).

**Sobre la decisión de catálogo (Developer vs. ODD):**
La evidencia acumulada (especialmente en Proyecto Real Android CRM, donde `v2_reforzado` y `v2` lograron 100 % funcional y ahorros de hasta 65 % de tokens, mientras que Developer actual falló 0/3) confirma la **Estrategia 1**:
> **Evolucionar Developer incorporando los principios rigurosos de ODD (Developer v2 / reforzado)**, manteniendo el nombre, las responsabilidades integrales del MAS y la compatibilidad de plataformas, evitando duplicar un agente general en el catálogo. SDD se mantiene como flujo formal de especificación para proyectos que lo requieran explícitamente.

*Nota:* Esta estrategia cuenta con respaldo empírico amplio, pero su integración definitiva al árbol canónico (`canonical/manifest.json`) requiere la aprobación explícita del usuario.

---

## 2. Lectura mínima para recuperar el contexto

1. Este documento completo (`docs/experimentos/CONTINUAR-AQUI.md`).
2. [Índice cronológico completo de experimentos](README.md).
3. [Cohorte definitiva ODD con Estándares en Gemini 3.8 Flash (v3)](odd-estandares-gemini-38-v3-2026-11-08/README.md).
4. [Análisis de ingeniería: Desventajas de omitir estándares](odd-estandares-gemini-38-2026-11-08/analisis-estandares.md).
5. [Experimento en proyecto real Proyecto Real Android CRM](real-android-gemini-2026-11-08/README.md).
6. [Evaluación de Developer v2 candidato2 con dominios y build nativo](developer-v2-dominios-build-gemini-2026-11-05/README.md).

---

## 3. Síntesis de resultados consolidados (2026-11-04 a 2026-11-08)

### 3.1 Ponytail — No integración (2026-11-04)
[Registro](ponytail-2026-11-04/README.md). Baseline f3b58d…, GPT/OpenCode, 60 celdas: ambos brazos 30/30 funcionales. B registró +2,74 % tokens y +1,22 % duración. Beneficio incremental inconcluso; decisión: conservar evidencia, no integrar B.

### 3.2 ODD adaptado vs SDD — GPT (2026-11-04)
[Registro](odd-vs-sdd-2026-11-04/README.md). 40 celdas comparables (R1+R2). ODD adaptado B mostró −72,34 % tokens y −46,23 % tiempo vs SDD A. Señal de ahorro descriptiva en tareas directas; el lote original fue parcial por cuota 429; no se forzó promoción.

### 3.3 Primer Gemini exploratorio — Rectificado (2026-11-04)
[Rectificación](odd-vs-sdd-2026-11-04/gemini-flash.md). El informe preliminar (−36,05 % tokens) no era un ensayo A/B válido (reutilizó éxitos y mezcló configuraciones). Queda como antecedente histórico rectificado.

### 3.4 Developer / SDD / ODD — 90 celdas en Gemini 3.8 Flash (2026-11-04)
[Resultados](developer-sdd-odd-gemini-2026-11-04/resultados.md). Diez escenarios, tres repeticiones, 30 celdas por brazo; 100 % aceptación funcional en todos.
- ODD vs Developer: **−18,34 % tokens**, **+1,55 % tiempo** (sin ventaja en velocidad).
- SDD: +112,26 % tokens y +43,60 % tiempo vs Developer (incluyendo turnos interactivos simulados).

### 3.5 Developer actual vs Compacto v1 (2026-11-04)
[Resultados](developer-compacto-gemini-2026-11-04/resultados.md). 90 celdas. La compresión de instrucciones de Developer causó **+6,84 % tokens y +16,39 % tiempo** (más pasos intermedios y `todowrite`). Decisión: **no adoptar compacto v1**.

### 3.6 Developer v2 (Candidato 1 y Candidato 2) con Build nativo (2026-11-05)
- [Candidato 1](developer-v2-alta-gemini-2026-11-05/README.md): 9 celdas en TASK-2 Alta. V2 frente a Developer: **−22,34 % tokens**, +5,13 % tiempo. 3/3 funcional.
- [Candidato 2](developer-v2-dominios-build-gemini-2026-11-05/README.md): 12 celdas en TASK-2 Alta + 5 pruebas de selectividad.
  - V2 cargó `data-api` y `ui-design` **3/3 veces** antes del primer cambio de código, únicamente cuando correspondía por contexto.
  - V2 vs Developer actual: **−19,48 % tokens**, −0,34 % tiempo, **0 errores de herramienta**.
  - Cierre documental: detectó documentación obsoleta y propuso `documentation-orchestrator` sin editar ilegalmente fuera de su rol.
  - Comparativa con `build` nativo: V2 consumió −27,26 % tokens que Build.

### 3.7 Validación en proyectos reales (2026-11-05 y 2026-11-08)
- [LocalLibrary TASK-3 Muy Alta](real-project-gemini-2026-11-05/README.md): 27 celdas. Todos los agentes pasaron tareas Media-Alta y Alta (6/6), pero fallaron 0/3 en Muy Alta por filtrar préstamos entre sucursales. Conclusión: *preservar tests preexistentes no demuestra cobertura del nuevo contrato*.
- [Proyecto Real Android CRM](real-android-gemini-2026-11-08/README.md): 15 ejecuciones en repo Kotlin real con Compose y SQLCipher.
  - `v2_reforzado`: **100 % PASS (3/3)**, con ahorros de hasta **−65,1 % tokens** vs base.
  - `v2 (candidato2)`: **100 % PASS (3/3)**.
  - `developer_actual`: **0/3 FAIL** (incapaz de resolver la modularidad y dependencias Android).

### 3.8 Variantes exploratorias de ODD en GPT-6 Luna max (2026-11-05)
- [Batching de operaciones](odd-batching-luna-max/README.md): 4 celdas. Redujo tokens brutos (−28,78 %), pero falló en suite conjunta (1/2 aceptación). Descartado.
- [Ruta selectiva con `.navigator` y `.architecture`](odd-navigator-architecture-luna-max/README.md): 2 celdas. +55,77 % tokens y +47,14 % tiempo. Descartado.
- [Núcleo breve y partición de skills](odd-domain-core-luna-max/README.md): 2 celdas. +165,57 % tokens por relecturas de fragmentos. Descartado.

### 3.9 Batería multi-modelo (2026-11-06)
- [GPT-6 Luna Copilot](gpt-6-luna-task2-high-2026-11-06/README.md) y [MAI-Code Flash](mai-code-flash-2026-11-06/README.md): Confirmaron que SDD respeta las decisiones de modo sin inventar aprobaciones de usuario.

### 3.10 ODD con Estándares en Gemini 3.8 Flash (Cohortes 2026-11-08)
- [Diagnóstico Cohorte v1](odd-estandares-gemini-38-2026-11-08/README.md): ODD original cortado a los 600,18 s (falso negativo por timeout rígido de 600 s); ODD ajustado cortado por límite de contexto de Copilot (>100k tokens por micro-logs repetitivos con `todowrite`).
- [Cohorte v3 Definitiva](odd-estandares-gemini-38-v3-2026-11-08/README.md): Timeout operacional de 1.200 s y regla anti-micrologs redundantes.
  - **4/4 celdas balanceadas aprobadas al 100 %** (43 tests originales + 9 oráculos externos).
  - ODD Ajustado cargó `data-api` y `ui-design` antes de código (2/2) y registró **0 errores de herramienta**.
  - Sobrecoste de estándares: **+17,42 % tokens** y **+4,54 % tiempo** (+42,5 s).
  - Veredicto de [análisis arquitectónico](odd-estandares-gemini-38-2026-11-08/analisis-estandares.md): Este modesto sobrecoste es plenamente justificado para evitar la generación masiva de deuda técnica.

### 3.12 Batería Multi-Modelo en Proyecto Real Android CRM (2026-11-08)
Evaluación exhaustiva de 45 ejecuciones sobre la app real Android (Kotlin, Jetpack Compose, Room, SQLCipher):
- **Gemini 3.8 Flash (Copilot):** 15/15 corridas (3 tareas × 5 brazos). `v2_reforzado` y `v2` 100 % funcional con −65,1 % tokens en T1 y −53,4 % en T3; `developer_actual` alcanzó 100 % al desbloquear su modo autónomo (300, 163 y 507 LOC).
- **MAI-Code-1.1-Flash (Copilot):** 10 corridas (T1 y T2). 100 % en T1, 3,80M tokens totales. En T2 resolvió con `cola.corregir()` (suite original 100 % OK).
- **GPT 6.1 Terra (OpenAI):** 10 corridas (T1 y T2). 100 % en T1 con el gasto más bajo (~100k tokens por ejecución); 3,88M tokens totales.
- **GPT 6 Luna (OpenAI):** 10 corridas (T1 y T2). Récord absoluto de eficiencia de tokens en todo el proyecto: **2,89M tokens acumulados** y 100 % funcional en T1.

### 3.13 Proyecto Real iOS CRM — Benchmark Nativo Antigravity (2026-11-09)
Evaluación sistemática de 15 ejecuciones sobre la app real iOS (`mobile-ios.zip`, Swift 6, Xcode 26.1, iOS Simulator 26.1):
- **Modelo y Proveedor:** `Gemini 3.8 Flash` ejecutado directamente sobre el arnés nativo de Google Antigravity (`agentapi` / Language Server de Google DeepMind) sin intermediación de GitHub Copilot.
- **Resultados:**
  - **Tarea 1 (Media-Baja):** 1/5 aprobado (`build_sin_mas` con 101 pasos y 361k tokens).
  - **Tarea 2 (Media-Alta):** **100 % aprobado (5/5 brazos)**; `v2_reforzado`, `developer_actual`, `v2`, `build_mas` y `build_sin_mas` pasaron oráculos y suite original con cero regresión.
  - **Tarea 3 (Alta):** **`developer_actual` fue el único ganador (1/5)**, resolviendo deduplicación atómica, concurrencia multihilo segura y cifrado AES-GCM con CryptoKit (186 LOC de producción y 346 LOC de pruebas propias).
- **Gasto Global:** 2,886,697 tokens totales en 83.0 minutos de ejecución autónoma.

---

## 4. Límites de infraestructura descubiertos y reglas operativas

1. **Desmantelamiento del CLI de Gemini:** El binario `/opt/homebrew/bin/gemini` fue desactivado por Google para cuentas individuales (`IneligibleTierError`). El proveedor directo en OpenCode presenta HTTP 403. El canal operativo y validado para Gemini 3.8 Flash es `github-copilot/gemini-3.8-flash`.
2. **Ventana de contexto en GitHub Copilot:** El endpoint de Gemini 3.8 Flash en Copilot rechaza peticiones que superen ~96k–100k tokens en el acumulado del prompt con `APIError: statusCode 400`. En tareas complejas (Django, Compose), deben evitarse bucles de edición de logs markdown innecesarios.
3. **Timeout operacional:** Tareas full-stack reales requieren entre 200 y 750 segundos. Cualquier arnés de evaluación debe configurar `limit=1200` s para no incurrir en falsos negativos por milisegundos.
4. **Métricas estrictas:** No mezclar contadores entre modelos ni sumar tokens cacheados y no cacheados como si tuvieran el mismo coste monetario.

---

## 5. Acuerdos de diseño consolidados

1. **Trabajo pequeño/mediano sin micro-logs persistentes:** No crear archivos en `.odd/tasks/` si la tarea y el diff bastan para reanudar.
2. **Carga selectiva de estándares de dominio:** Si la tarea involucra API/datos, cargar `data-api`; si involucra UI/estilos, cargar `ui-design`; si involucra ambas, cargar ambas antes de modificar código; si no aplica ninguna, no cargar ninguna.
3. **Cierre documental responsable:** Detectar documentación impactada y proponer `documentation-orchestrator` esperando respuesta del usuario, sin editar documentación fuera del alcance técnico.
4. **Respeto de límites MAS:** No realizar commits, pushes, tags, releases ni publicación de paquetes sin autorización explícita previa.

---

## 6. Próximo paso funcional

Con toda la evidencia empírica completada y registrada:
- **Opción recomendada (Evolución Developer v2):** Actualizar `canonical/agents/developer.json` y su skill `canonical/skills/developer/SKILL.md` para incorporar las reglas de Developer v2 / reforzado (selectividad de dominios, disciplina RED-GREEN, prevención de micro-logs redundantes y cierre documental).
- **Opción alternativa:** Crear un nuevo agente ODD independiente en el catálogo y someterlo a periodo de transición.

*Requerimiento:* Esperar la decisión explícita del usuario sobre cuál de las dos vías implementar.

---

## 7. Estado del repositorio preservado

- HEAD: `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
- El catálogo canónico permanece intacto (5 agentes, 11 skills, 6 plataformas).
- Todos los reportes, protocolos, runners y JSONs de resultados en `docs/experimentos/` y `tools/` se encuentran preservados en disco local sin versionar.

---

## 8. Texto para retomar en una siguiente sesión

> Lee `docs/experimentos/CONTINUAR-AQUI.md` y su índice en `docs/experimentos/README.md`. Todo el histórico de experimentos hasta el 2026-11-08 está consolidado. Quiero tomar la decisión final sobre la evolución de Developer v2 frente a ODD. Resume únicamente las dos opciones de catálogo y la recomendación técnica antes de realizar cualquier cambio en el repositorio.
