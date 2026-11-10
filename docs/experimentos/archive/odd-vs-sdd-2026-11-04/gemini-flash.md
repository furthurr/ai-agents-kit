# Evaluación con Antigravity Gemini 3.8 Flash

**Estado: exploración histórica, no comparación A/B validada.** Este anexo
rectifica el reporte inicial: no permite atribuir a ODD un ahorro de 36,05 % ni
una mejora de fiabilidad de herramientas frente a SDD. No se usa para promover
un agente ni se agrega a las métricas GPT o del suplemento.

Se utilizó `google/antigravity-gemini-3.8-flash` a través del plugin de Antigravity
en OpenCode; esto no prueba el comportamiento del host Antigravity standalone.
La etiqueta «más ligero» fue una intención de selección, no una medición de
capacidad, tamaño, parámetros ni rendimiento intrínseco del modelo.

Fecha: **2026-11-04**.

## Objetivo original

Contrastar si la menor sobrecarga de ODD adaptado frente a SDD se mantiene en un modelo con menor capacidad/peso que `gpt-6.1-sol`, evaluando específicamente la fiabilidad en el uso de herramientas (`skill`, `read`, `edit`, `bash`), el seguimiento de contratos y el consumo de recursos.

## Batería explorada

Se evaluaron 12 celdas emparejadas (A: SDD vs B: ODD adaptado) en 6 escenarios representativos:
- **S01:** Corrección documental pasiva.
- **S02:** Función pura con colapso de whitespace y Unicode (`direct`).
- **S03:** Feature con validación y límites (`tiny`).
- **S04:** Corrección numérica monetaria con Decimal (`lite`).
- **S08:** Reanudación de trabajo inconcluso desde documento previo.
- **S10:** Consulta y diagnóstico en solo lectura sin mutaciones.

## Agregados del resumen final seleccionado — no inferenciales

Se conservan los números del reporte previo para no borrar el antecedente.
Reflejan los registros finales que sobrevivieron a reejecuciones y selección de
éxitos; no representan todos los intentos ni un lote congelado comparable.
«6/6» es aceptación funcional reportada de esa selección, no éxito al primer
intento ni fidelidad acreditada a dos tratamientos distintos.

| Métrica | A: SDD | B: ODD adaptado | Diferencia |
|---|---:|---:|---:|
| Aceptación funcional | 6/6 (100 %) | 6/6 (100 %) | 0 |
| Tokens observados (input + caché + output) | 1.595.982 | 1.020.596 | **−36,05 %** |
| Duración agregada de celdas | 351,98 s | 232,78 s | **−33,86 %** |
| Llamadas a herramientas | 74 | 68 | −8,11 % |

### Detalle por escenario

| Escenario | Tokens A | Tokens B | Delta Tokens | Tiempo A | Tiempo B | Herramientas A/B |
|---|---:|---:|---:|---:|---:|---:|
| **S01 (Documental)** | 124.932 | 114.669 | −8,2 % | 20,7 s | 22,4 s | 6 / 7 |
| **S02 (Función pura)** | 290.743 | 123.989 | **−57,4 %** | 58,9 s | 28,3 s | 16 / 11 |
| **S03 (Feature con validación)** | 413.009 | 205.707 | **−50,2 %** | 115,3 s | 59,6 s | 15 / 13 |
| **S04 (Monetario/Decimal)** | 235.624 | 221.319 | −6,1 % | 46,6 s | 50,7 s | 12 / 15 |
| **S08 (Reanudación)** | 345.841 | 218.900 | **−36,7 %** | 60,8 s | 44,9 s | 16 / 14 |
| **S10 (Consulta solo lectura)** | 185.833 | 136.012 | **−26,8 %** | 49,7 s | 27,0 s | 9 / 8 |

## Por qué no es una comparación válida

La revisión del código actual de [gemini_benchmark.py](../../../../tools/gemini_benchmark.py)
y del historial de ejecución de esta sesión identifica estos problemas:

1. Se cambió la configuración durante los intentos: `--pure` no cargaba la
   integración de autenticación; después se cambió el aislamiento de perfiles y
   se retiraron overrides de permisos. No se congeló una configuración final
   con preflight A/B suficiente antes de las celdas usadas en el reporte.
2. El comando final no selecciona `--agent sdd` ni un agente experimental propio:
   usa el agente por defecto del host. Se añadió una ruta a una skill homónima
   `sdd-spec`, mientras continuaba el descubrimiento de la instalación habitual.
   El indicador `skill_loaded` solo comprueba el nombre, no el contenido cargado.
   No se acreditó que A y B recibieran efectivamente instrucciones distintas.
3. El runner elimina un workspace si ya existe y sobrescribe su registro. Al
   reanudar reutiliza solo registros con `functional_pass` y herramientas; los
   restantes se ejecutan de nuevo. Los primeros intentos con llamadas malformadas
   y las repeticiones no sobreviven como un ledger completo e inmutable.
4. Las trazas se procesaron en memoria pero no se guardaron completas. El registro
   final retiene nombres de herramientas, contadores, flags y respuesta truncada,
   no entradas/salidas necesarias para auditar secuencia RED/GREEN, assertions
   originales, comandos concretos o ausencia de accesos fuera de alcance.
5. Hubo una sola selección final de seis escenarios, sin tres repeticiones
   controladas ni orden aleatorizado. Cambiaron integración, caché y contexto;
   tampoco corresponde comparar sus porcentajes con los del lote GPT.

Por ello se retiran las afirmaciones anteriores de precisión general de tool
calling, test-first probado, suites originales intactas y causalidad del ahorro.
S02 estaba en Direct, que no exige una spec formal: su diferencia de consumo no
se puede explicar automáticamente por documentación o gates obligatorios.

## Qué sí queda registrado

- El modelo respondió a través de la integración habitual y hubo ejecuciones
  con herramientas, además de intentos con errores o llamadas malformadas.
- El resumen final conservado reporta aceptación funcional de doce resultados.
  Eso no valida la comparación ni demuestra que no existieran fallos previos.
- Es un antecedente para diseñar pruebas mejores, no una certificación de ODD,
  SDD, Gemini ni la seguridad del host. No se ejecutaron nuevos tests al archivar.

## Procedencia y conservación

Resumen externo original (temporal, no portable):
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/mas-gemini38-eval/gemini_benchmark_summary.json`.
SHA-256 comprobado al archivar:
`a644410118d3b23a599ec9d43ed66f9d8fd1b2de65cf71e1aae1e318c0bd3ee9`.
Runner actual SHA-256:
`ef4e1d45687a0e6c4bd13243bbb3cf7e15ac69c8c62164748d05875c55f22c33`.
Ese hash identifica el script revisado, no prueba que fuera idéntico en todos los
intentos. El resumen y sus registros finales no reconstruyen las trazas ni los
intentos sobrescritos. La permanencia de la carpeta temporal no está garantizada.
