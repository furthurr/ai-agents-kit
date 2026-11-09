# Experimentos del MAS — índice y continuidad

**Para retomar la conversación en otra sesión, empezar por
[CONTINUAR-AQUI.md](CONTINUAR-AQUI.md).** No hace falta volver a ejecutar las
baterías ni depender del historial de chat para conocer resultados y pendientes.

## Catálogo cronológico de experimentos

### 1. Batería inicial y comparaciones directas (2026-11-04)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [Ponytail](ponytail-2026-11-04/README.md) | GPT, variante de instrucciones del MAS, 60 celdas | Beneficio incremental inconcluso; no integrar B ni reglas parciales. |
| [ODD vs SDD](odd-vs-sdd-2026-11-04/README.md) | GPT, 60 intentos y suplemento separado de 6 celdas | Señal de ahorro para ODD adaptado; lote original parcial por cuota, no promoción. |
| [Gemini exploratorio anterior](odd-vs-sdd-2026-11-04/gemini-flash.md) | 12 resultados finales seleccionados | No es A/B validado; porcentajes rectificados, no usar para decidir adopción. |
| [Developer / SDD / ODD](developer-sdd-odd-gemini-2026-11-04/README.md) | Gemini 3.8 Flash, 90 celdas | Todos pasan oráculos; ODD ahorra tokens vs Developer, sin ventaja global de tiempo en esa cohorte. |
| [Developer actual / compacto / ODD](developer-compacto-gemini-2026-11-04/README.md) | Gemini 3.8 Flash, 90 celdas, skill A/B idéntica | No adoptar compacto v1: más tokens/tiempo y más alertas PLAN. |

### 2. Evolución de Developer y proyectos reales (2026-11-05)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [Developer v2 candidato 1](developer-v2-alta-gemini-2026-11-05/README.md) | Gemini 3.8 Flash, 9 celdas, TASK-2 Alta en LocalLibrary | V2 frente a Developer: −22,34 % tokens, +5,13 % tiempo. 100 % funcional (3/3). |
| [Developer v2 candidato 2 + Build](developer-v2-dominios-build-gemini-2026-11-05/README.md) | Gemini 3.8 Flash, 12 celdas + 5 focalizadas | V2 carga selectivamente `data-api` y `ui-design` (3/3) antes de código; −19,48 % tokens vs Developer actual; cierre documental sin escrituras ilegales. |
| [Real Project LocalLibrary](real-project-gemini-2026-11-05/README.md) | Gemini 3.8 Flash, 27 celdas (tareas Media-Alta, Alta, Muy Alta) | 18/27 funcionales (6/9 por brazo); la Tarea Muy Alta expuso fugas de sucursal en todos los flujos; demuestra que mantener tests previos no garantiza cubrir contratos nuevos. |

### 3. ODD con estándares y variantes exploratorias (2026-11-05)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [ODD estándares Gemini](odd-estandares-gemini-2026-11-05/README.md) / [Reintento](odd-estandares-reintento-gemini-2026-11-05/README.md) | Gemini 3.8 Flash, perfiles aislados | R1 completo; bloqueado en R2/R3 por HTTP 403 y deshabilitación del CLI de Gemini. |
| [ODD estándares GPT-6 Luna max 1800s](odd-estandares-gpt6-luna-max-1800/README.md) | GPT-6 Luna max, 6 celdas, timeout 1.800 s | ODD ajustado 3/3 funcional (+36,78 % tokens, +23,25 % tiempo por carga exhaustiva de estándares de dominio). |
| [ODD batching de operaciones](odd-batching-luna-max/README.md) | GPT-6 Luna max, 4 celdas | Aceptación 1/2 por brazo; −28,78 % tokens brutos pero fallo en suite conjunta; descartado como variante eficiente. |
| [ODD mapas `.navigator` y `.architecture`](odd-navigator-architecture-luna-max/README.md) | GPT-6 Luna max, 2 celdas | Ambos funcionales, pero +55,77 % tokens y +47,14 % tiempo; no produjo ahorro. |
| [ODD núcleo breve + referencias](odd-domain-core-luna-max/README.md) | GPT-6 Luna max, 2 celdas | Ambos funcionales, pero +165,57 % tokens por relecturas de particiones; no adoptar. |

### 4. Batería multi-modelo y rigor procedural (2026-11-06)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [MAI-Code-1.1-Flash](mai-code-flash-2026-11-06/README.md) | MAI-Code Flash vía Copilot, 12 invocaciones (Low y High) | 2/6 en Low, 0/6 en High; Developer y SDD respetaron pausas y gates ante fricción de workspace/permisos. |
| [GPT-6 Luna Copilot — Alta](gpt-6-luna-task2-high-2026-11-06/README.md) y [Media-Baja](gpt-6-luna-ll-search-2026-11-06/README.md) | GPT-6 Luna vía Copilot, 12 invocaciones | SDD pausa correctamente para elección de modo; 3/5 aceptación primaria en Alta. |

### 5. Proyectos móviles reales y benchmark definitivo Gemini 3.8 Flash (2026-11-08)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [Proyecto Real Android CRM — Gemini 3.8 Flash](real-android-gemini-2026-11-08/README.md) | Gemini 3.8 Flash, 15 ejecuciones (3 tareas × 5 brazos) en app Kotlin multi-módulo real | `v2_reforzado`, `v2`, `build_sin_mas` y `developer_actual` (desbloqueado) logran 100 % aceptación (3/3); `v2_reforzado` ahorra hasta −65,1 % tokens vs base. |
| [Proyecto Real Android CRM — MAI-Code-1.1-Flash](real-android-mai-flash-2026-11-08/README.md) | MAI-Code Flash vía Copilot, 10 ejecuciones (T1 y T2 × 5 brazos) | 100 % en T1; 0 % en T2 por oráculo de inyección `almacen` en ViewModel; 3,80M tokens totales. |
| [Proyecto Real Android CRM — GPT 6.1 Terra](real-android-gpt6-terra-2026-11-08/README.md) | GPT 6.1 Terra vía OpenAI OAuth, 10 ejecuciones (T1 y T2 × 5 brazos) | 100 % en T1 con ~100k tokens por corrida; 0 % en T2 por oráculo de constructor; 3,88M tokens totales. |
| [Proyecto Real Android CRM — GPT 6 Luna](real-android-gpt6-luna-2026-11-08/README.md) | GPT 6 Luna vía OpenAI OAuth, 10 ejecuciones (T1 y T2 × 5 brazos) | Récord absoluto de eficiencia de tokens (2,89M tokens totales); 100 % en T1. |
| [ODD estándares Gemini 3.8 Flash (Cohorte v1)](odd-estandares-gemini-38-2026-11-08/README.md) | Gemini 3.8 Flash vía Copilot | Diagnóstico de paradas: corte a los 600,18 s e interrupción por límite Copilot (>100k tokens por micro-logs `todowrite`). |
| [Análisis: Desventajas de omitir estándares](odd-estandares-gemini-38-2026-11-08/analisis-estandares.md) | Informe de ingeniería de software | Demuestra por qué omitir `data-api` y `ui-design` degrada contratos, a11y y crea deuda técnica (falso ahorro). |
| [ODD estándares Gemini 3.8 Flash (Cohorte v3)](odd-estandares-gemini-38-v3-2026-11-08/README.md) | Gemini 3.8 Flash vía Copilot, 4 celdas balanceadas (R1+R2) | **100 % funcional (4/4 celdas)**; 2/2 cargas de `data-api` y `ui-design` antes de código; solo **+17,42 % tokens** y **+4,54 % tiempo** por estándares; 0 errores de herramientas. |

### 6. Proyecto Real iOS CRM — Benchmark Nativo Antigravity (2026-11-09)

| Registro | Modelo / alcance | Estado y decisión |
|---|---|---|
| [Proyecto Real iOS CRM — Gemini 3.8 Flash Nativo](real-ios-gemini-antigravity-2026-11-09/README.md) | Gemini 3.8 Flash vía Google Antigravity Nativo (`agentapi`), 15 ejecuciones (3 tareas × 5 brazos) en app Swift 6 / Xcode 26.1 real | **100 % de éxito en Tarea 2** (5/5 brazos); **`developer_actual` único ganador en Tarea 3 Alta (CryptoKit + Concurrencia)**; 2,89M tokens invertidos; cero intermediarios de terceros. |

Cada carpeta conserva resumen, protocolo, resultados y sus anexos. Las cifras no
se agregan entre cohortes, modelos o tratamientos. Pasar fixtures no acredita
equivalencia completa de agentes ni certificación de producción.

## Conservación para siguientes sesiones

[Paquete de continuidad](continuidad-2026-11-04/README.md): trazas recuperadas y
otros originales comprimidos, hashes, herramientas actuales y copia exacta del
plan ODD del Escritorio. Son copias posteriores: no modifican los ledgers,
congelaciones, fallos o decisiones de los experimentos.

El kit sigue con cinco agentes y once skills en seis plataformas. No hay agente
ODD instalado ni un Developer convertido a ODD. No se hizo commit/push: abrir el
mismo checkout para continuar; una sesión en otro worktree o máquina no recibe
automáticamente los archivos locales sin versionar.
