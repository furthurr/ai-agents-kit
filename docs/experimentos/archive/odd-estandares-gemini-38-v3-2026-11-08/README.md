# ODD con estándares — Cohorte v3 Gemini 3.8 Flash

**Estado: Lote PARCIAL de 5 intentos preservados. Repeticiones R1 y R2 completas, saludables y 100% funcionales (4/4 celdas balanceadas). Parada en R3 por límite de contexto de Copilot.**
ID: `odd-standards-gemini38-v3-20261108`. Fecha: 2026-11-08.
Modelo ejecutado: `github-copilot/gemini-3.8-flash` (Gemini 3.8 Flash, vía proveedor Copilot activo en OpenCode 1.18.34).

## 1. Resumen de Resultados Comparables (R1 + R2)

Las repeticiones R1 y R2 ofrecen una comparación simétrica, completa y saludable de 2 celdas por brazo (4 celdas en total) sobre la tarea Alta (`TASK-2` de LocalLibrary):

| Métrica (Cohorte Balanceada R1 + R2) | ODD Histórico (2 celdas) | ODD Ajustado con Estándares (2 celdas) | Delta (Ajustado vs. ODD) |
|---|---:|---:|---:|
| **Aceptación funcional (oráculos externos 9/9)** | **2/2 (100 %)** | **2/2 (100 %)** | Idéntica (0 fallos) |
| **Preservación suite original (43/43 tests)** | **2/2 (100 %)** | **2/2 (100 %)** | Idéntica (0 fallos) |
| **Carga de `data-api` por contenido** | 0/2 | **2/2 (100 %)** | +2 cargas |
| **Carga de `ui-design` por contenido** | 0/2 | **2/2 (100 %)** | +2 cargas |
| **Ambas skills cargadas antes de código** | 0/2 | **2/2 (100 %)** | +2 cargas |
| **Tokens comparables acumulados** | 5.527.753 | 6.490.862 | **+17,42 % tokens** |
| **Duración sumada de conversaciones** | 937,856 s | 980,403 s | **+4,54 % tiempo** (+42,5 s) |
| **Errores de herramientas** | 1 | **0** | Mejor estabilidad |

---

## 2. Detalle Celda por Celda

### Repetición 1 (R1)
- **`TASK-2-ODD-r1`:** 3.699.814 tokens | 731,207 s | **Funcional 100%** | Sin skills de dominio.
- **`TASK-2-ADJUSTED-r1`:** 4.001.422 tokens | 690,142 s | **Funcional 100%** | Cargó `data-api` y `ui-design` antes de código.
- *Nota R1:* ODD Ajustado fue **41 segundos más rápido** que el original (-5,62 % tiempo) con un sobrecoste de tokens de solo +8,15 %.

### Repetición 2 (R2)
- **`TASK-2-ADJUSTED-r2`:** 2.489.440 tokens | 290,261 s | **Funcional 100%** | Cargó `data-api` y `ui-design` antes de código.
- **`TASK-2-ODD-r2`:** 1.827.939 tokens | 206,649 s | **Funcional 100%** | Sin skills de dominio.
- *Nota R2:* Ambas celdas ejecutaron con extrema rapidez y pasaron todos los oráculos externos y pruebas de regresión.

### Repetición 3 (R3) y Causa de Parada
- **`TASK-2-ODD-r3`:** Implementó y pasó el 100% de las pruebas funcionales (`functional_pass: True`, 43 originales + 9 externas aprobadas en 457,149 s). Sin embargo, al ir a generar su resumen final, la conversación acumuló 101.067 tokens en el prompt, alcanzando el límite duro de ~100k tokens por petición de GitHub Copilot para Gemini (`APIError: statusCode 400`).
- **Parada:** Siguiendo la regla de parada estricta del protocolo congelado, no se realizaron reintentos en bucle y se detuvo la ejecución preservando los 5 intentos observados.

---

## 3. Conclusiones Metodológicas y de Coste

1. **El coste real de aplicar estándares en Gemini 3.8 Flash:**
   - Cargar y aplicar fielmente los estándares de API (`data-api`) y de interfaz gráfica (`ui-design`) representó un sobrecoste de solo **+17,42 % en tokens** y **+4,54 % en tiempo** en la cohorte balanceada.
   - Es un incremento notablemente inferior al observado en otros modelos (como GPT-6 Luna, donde alcanzó +36,78 %), demostrando que Gemini 3.8 Flash sintetiza y aplica las directrices de dominio con gran eficiencia cuando no se pierde en micro-logs redundantes.
2. **Cero errores de herramientas en el Ajustado:**
   - ODD Ajustado tuvo 0 errores de herramientas en sus celdas completadas, frente a 1 error en el original, indicando que el contexto de las skills orienta al agente a no intentar operaciones prohibidas o mal formateadas.
3. **Límite de infraestructura identificado:**
   - La ventana de contexto de GitHub Copilot para Gemini (~100k tokens por petición) impone un techo duro: cuando una conversación excede los 50 pasos complejos con salidas extensas de herramientas, la API responde HTTP 400. La solución aplicada (evitar micro-logs repetitivos) permitió que las tareas se resolvieran holgadamente dentro del margen.
