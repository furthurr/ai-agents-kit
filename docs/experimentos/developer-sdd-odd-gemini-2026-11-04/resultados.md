# Reporte — Developer, SDD y ODD con Gemini 3.8 Flash

[Resumen](README.md) · [Protocolo](protocolo.md) · [Tratamientos](tratamientos.md)

## 1. Cobertura y procedencia

Se completaron **90 intentos únicos**: diez escenarios, tres flujos y tres
repeticiones, con `google/antigravity-gemini-3.8-flash` y OpenCode 1.18.34.
El transporte fue el plugin Antigravity habitual del host, no la aplicación
Antigravity standalone. No hubo errores API, timeouts ni métricas ausentes.

Se congelaron 176 entradas antes de las celdas; sus hashes permanecen iguales.
Los tres agentes se seleccionaron explícitamente y las skills se verificaron
por contenido íntegro en las noventa celdas. No se reutilizaron solo éxitos ni
se reejecutaron celdas para mejorar la tabla. El intento técnico de preflight
anterior, con patrones de permisos incorrectos, quedó fuera del lote de tareas.

Fixtures y oráculos provienen de declaraciones del ensayo anterior, fijadas de
nuevo por hash. Se usan nuevas raíces, sesiones y registros. No se mezclan estos
resultados con la exploración Gemini anterior rectificada ni con el estudio GPT.

## 2. Resultado agregado

| Métrica, 30 celdas por flujo | Developer | SDD | ODD experimental |
|---|---:|---:|---:|
| Aceptación funcional externa | 30/30 | 30/30 | 30/30 |
| Checks mecánicos de entrega | 30/30 | 30/30 | 30/30 |
| Skill primaria correcta por contenido | 30/30 | 30/30 | 30/30 |
| Tokens input + caché + output | 3.987.598 | 8.464.007 | 3.256.158 |
| Duración sumada de celdas | 1.094,989 s | 1.572,366 s | 1.112,014 s |
| Mediana de duración por celda del corpus | 35,127 s | 55,026 s | 36,001 s |
| Herramientas | 364 | 409 | 356 |
| Steps con métricas | 366 | 437 | 347 |
| Invocaciones CLI | 30 | 57 | 30 |
| Respuestas simuladas de usuario | 0 | 27 | 0 |
| Errores de herramienta recuperados | 1 | 0 | 4 |

Respecto a Developer, ODD registró **−18,343 % tokens y +1,555 % duración**;
SDD **+112,258 % tokens y +43,597 % duración**. Son descripciones de esta carga
equilibrada, no estimaciones de todos los proyectos. ODD no ganó globalmente
en velocidad. No hubo mejora funcional demostrada: todos alcanzaron el techo
de la rúbrica, que no es exhaustiva.

El tiempo incluye conversación CLI, contexto y comprobaciones del agente, sin
esperas humanas reales. Excluye preparación de fixtures y evaluación externa
posterior. Sumar celdas concurrentes no equivale a tiempo de reloj del lote.

## 3. Medianas por tarea

**n=3 por casilla.** Se conservan todos los intentos. No se usa una ejecución
favorita por escenario; diferencias inferiores al 10 % se consideran pequeñas.

### Consumo observado

| Caso | Developer | SDD | ODD |
|---|---:|---:|---:|
| S01 errata documental | 73.990 | 205.186 | 58.558 |
| S02 función pura pequeña | 114.118 | 319.214 | 109.435 |
| S03 validación y seis reglas | 132.193 | 330.503 | 123.365 |
| S04 bug monetario | 114.679 | 326.140 | 109.029 |
| S05 CLI compartida | 225.170 | 362.062 | 165.356 |
| S06 doce reglas literales | 209.278 | 362.910 | 159.483 |
| S07 persistencia y fallos | 143.194 | 344.610 | 111.721 |
| S08 reanudación desde documento | 150.637 | 400.653 | 143.163 |
| S09 solo planificación | 67.434 | 208.762 | 71.818 |
| S10 consulta de solo lectura | 44.955 | 55.820 | 21.710 |

### Duración observada, segundos

| Caso | Developer | SDD | ODD |
|---|---:|---:|---:|
| S01 | 21,467 | 36,056 | 19,911 |
| S02 | 31,289 | 56,495 | 32,953 |
| S03 | 35,522 | 58,075 | 33,535 |
| S04 | 29,909 | 53,557 | 34,250 |
| S05 | 51,200 | 58,574 | 46,489 |
| S06 | 52,479 | 61,931 | 49,434 |
| S07 | 41,692 | 68,301 | 39,377 |
| S08 | 37,329 | 66,662 | 54,617 |
| S09 | 31,556 | 45,501 | 34,123 |
| S10 | 22,878 | 19,347 | 16,301 |

### Lectura práctica de esas medianas

| Necesidad | Qué sugiere este corpus | Qué no permite afirmar |
|---|---|---|
| Función pequeña o validación local | Developer y ODD cercanos: en S02/S03 las diferencias entre ambos son <10 % en tokens y tiempo. | Que siempre convenga cambiar de Developer a ODD. |
| Errata, CLI, reglas literales o persistencia | ODD ahorra >10 % de tokens frente a Developer; en varios casos la velocidad queda cercana. | Que ese ahorro pruebe mayor seguridad o calidad. |
| Bug monetario | Developer fue más rápido; diferencia de tokens con ODD pequeña. | Que ODD sea más lento en todos los bugs. |
| Reanudación sencilla | Developer terminó antes; ODD mantuvo el registro y SDD el cierre Tiny. | Beneficio de meses de historial, compactación o una segunda reanudación, no medidos aquí. |
| Solo planificar | Developer y ODD cercanos; SDD incluye elección de profundidad. | Calidad de planificación de un sistema complejo real. |
| Consulta | ODD tuvo menor mediana de tokens y tiempo en S10. | Resistencia general a inyecciones o superioridad en cualquier investigación. |
| Especificación contractual revisable | SDD mantiene ese propósito de producto. | Ventaja empírica de crear specs Tiny/Lite: no fue ejercitada en esta muestra natural. |

No se calculan p-values ni se promete significancia con tres repeticiones
sintéticas. Las preferencias son descriptivas y condicionadas a aceptación.

## 4. Por qué el resultado SDD necesita contexto

El modelo eligió **Direct en las 24 decisiones nuevas**, conservó Tiny en las
tres reanudaciones históricas y realizó tres consultas sin elección de modo.
No hubo creación nueva de Tiny ni uso de Lite o Standard. No se puede extrapolar
esta tabla a todo el ciclo formal SDD ni atribuir el sobrecoste de Direct a
documentos/gates que no produjo.

El simulador realizó 24 selecciones de modo y tres aprobaciones Gate 4, frente
a cero respuestas adicionales en Developer/ODD. La propuesta inicial de alcance
y profundidad de SDD consumió **3.100.118 tokens y 606,854 s en 24 invocaciones**.
Esa etapa contiene exploración y definición de criterios, no solo una pregunta
ceremonial. No restarla para inventar qué habría costado una ejecución distinta.
Si el usuario ya seleccionó un modo compatible y validó el alcance, esa transición
adicional no representa necesariamente su experiencia real.

Además, en S05 (CLI compartida) y S07 (garantía de persistencia) se marcaron las
seis elecciones Direct para revisar su elegibilidad frente a las guardas de la
skill. No se deben usar sin revisión como prueba de clasificación impecable del
modelo. Los criterios funcionales sí pasaron. Si necesitas SDD por riesgo o
trazabilidad, **revisa el modo y la spec; no delegues ciegamente esa decisión al LLM**.

## 5. Herramientas, pruebas y fidelidad

Las 90 celdas completaron sus conversaciones; no se detectaron llamadas
malformadas como en el exploratorio anterior. Los cuerpos de las skills primarias
se contrastaron con perfiles congelados, no solo con el nombre `skill_loaded`.
Las 63 suites originales de comportamiento, ejecutadas sin modificar su código
contra cada solución final, pasaron, junto con las suites finales y oráculos.

### Test-first observado

- ODD: RED antes de modificar producto en **21/21** celdas de comportamiento,
  con GREEN posterior. Esto comprueba secuencia observada, no cobertura exhaustiva
  de cada regla ni causalidad sobre calidad.
- Developer: RED antes de producto en 9 celdas; SDD en 5. No era una obligación
  universal de sus contratos, por lo que no se cuenta su ausencia como defecto.

### Errores de herramientas recuperados

- Developer: un intento `rm -rf __pycache__` denegado en planificación.
- ODD: dos intentos `mkdir -p odd/tasks` y uno de limpieza de caché denegados;
  un `edit` con fragmento original que no coincidía, corregido después.
- SDD: cero tools con estado de error en estas trazas.

Estos son errores observados de uso/higiene de herramientas, no fallos finales
de los oráculos. Un exit no cero de un test RED esperado no se equipara a un
fallo de transporte de la herramienta. No hay evidencia para afirmar que ODD
domine a los demás en fiabilidad de tool calling por consumir menos tokens.

### Alertas semánticas que el checker mecánico no certifica

1. SDD emitió calificación numérica de esfuerzo en las tres ejecuciones del bug
   S04, aunque su contrato reserva esa calificación a features.
2. Las seis elecciones Direct de S05/S07 requieren la revisión ya descrita.
3. Cinco respuestas finales ODD no incluyeron la línea literal `Risk:` prescrita.
   Son omisiones del formato de cierre, no cinco bugs confirmados; no se interpreta
   que ningún riesgo se analizara solo por faltar una línea en la respuesta.
4. Developer invocó py_compile en dos ejecuciones de solo planificación. Aunque
   no cambió fuentes de producto, genera bytecode: es una alerta respecto a su
   contrato PLAN de solo lectura, no una prueba de implementación inexistente.

Por eso `successful_delivery`/`conforming_delivery` del JSON significa **checks
mecánicos aprobados**, no cumplimiento semántico perfecto. Las notas de auditoría
y [aclaraciones](evidencia/interpretacion.json) deben acompañar esas cifras.

## 6. Contabilidad de tokens y coste

| Contador | Developer | SDD | ODD |
|---|---:|---:|---:|
| Input | 3.794.941 | 2.337.119 | 3.011.367 |
| Cache-read | 138.349 | 6.052.193 | 192.582 |
| Cache-write | 0 | 0 | 0 |
| Output | 54.308 | 74.695 | 52.209 |
| Reasoning, separado | 1.221 | 0 | 1.539 |

La fórmula predefinida input+caché+output suma **15.707.763** entre los brazos.
El campo SDK `tokens.total` suma **15.710.523** en 1.150 steps; la diferencia
agregada de **2.760** coincide con los contadores reasoning separados. Hay 17
steps donde esos totales difieren. Se conserva esa aclaración sin cambiar la
fórmula congelada ni almacenar razonamiento privado.

La caché no se reinició y su distribución es muy distinta. Más lectura de caché
sigue siendo contexto observado, pero no equivale al mismo precio de input
no cacheado. El coste reportado de los pasos es cero: **no permite calcular una
factura, declarar gratuidad ni convertir el ahorro de tokens en ahorro monetario**.

## 7. Controles, alcance y límites

- 176 hashes intactos, 90 IDs únicos y hashes de trazas contrastados.
- 377 llamadas de lectura/búsqueda sin rutas de otros escenarios/perfiles.
- Sin llamadas observadas a task/webfetch/websearch ni herramientas heredadas
  google_search/antigravity_quota. Estas dos últimas estaban expuestas por el
  host común: no afirmar bloqueo universal de red a partir de otros deny.
- El evaluador no leyó/copió credenciales ni cambió defaults o instaló el agente.
  El host conserva su plugin y puede actualizar estadísticas/sesiones habituales.
- No es sandbox OS ni auditoría de seguridad. Se ejecuta Python sintético en
  directorios temporales, no contra datos reales de un producto.
- Un modelo/host y diez tareas pequeñas. No hay cobertura de UI, APIs distribuidas,
  equipos, decisiones arquitectónicas amplias, pérdida de memoria real o meses
  de evolución. La segunda reanudación desde lo entregado no se midió.
- Mismo contexto global del host y nombres experimentales prefijados; no son una
  reproducción hermética de todas las instalaciones reales del kit.
- Longitud de instrucciones, selección de modo y metodología varían juntos. No se
  atribuye una diferencia a una sola regla ni se comparan estos números con GPT.
- Evaluación no ciega. La aceptación es relativa a oráculos y fixtures conocidos,
  no demostración de ausencia de todo defecto ni equivalencia universal.

## 8. Recomendación final

**Developer como opción general; ODD experimental si priorizas consumo y quieres
su disciplina de prueba/registro; SDD cuando necesitas especificación y revisión
explícitas, verificando su profundidad.**

La evidencia no justifica retirar Developer o SDD ni convertir ODD en default.
Justifica considerar ODD como alternativa opt-in, especialmente por tokens,
sin anunciar que acelera todas las tareas o produce código mejor. En esta muestra,
Developer y ODD empatan funcionalmente y sus tiempos agregados difieren solo 1,56 %.
El valor de revisión formal de SDD requiere escenarios que realmente lo ejerzan.

## 9. Evidencia conservada y verificaciones

El [ledger](evidencia/records.json) incluye las noventa filas, respuestas,
aprobaciones, etapas, hashes y archivos finales. Se preservan
[perfiles](evidencia/profiles.json), [casos](evidencia/cases.json),
[preflight](evidencia/preflight.json), [summary](evidencia/summary.json),
[audit](evidencia/audit.json) y [procedencia](evidencia/provenance.json).
Las trazas completas sanitizadas son externas; no se garantiza persistencia
de esa ubicación temporal. Un hash no sustituye el contenido de una traza perdida.

Las pruebas offline del runner pasaron 7/7, el kit validó 11 skills/5 agentes/6
plataformas, y se comprobaron sintaxis Python, enlaces y whitespace. Esos checks
no certifican el runtime de otras plataformas. No se modificaron `canonical/`,
`adapters/` o `generated/`, ni se hicieron commits o publicaciones.

| Verificación de entrega | Resultado |
|---|---|
| `python3 tools/test_gemini_three_way.py` | 7/7 correctas, sin llamadas a proveedores. |
| `python3 tools/validate.py` | 11 skills, 5 agentes, 6 plataformas correctos. |
| `python3 tools/check_links.py` | 110 Markdown correctos. |
| `python3 -m py_compile tools/gemini_three_way.py tools/gemini_three_way_report.py tools/test_gemini_three_way.py` | Correcto. |
| `git diff --check` | Correcto. |
| Auditoría | 176 entradas intactas, 90 trazas con hash coincidente, 63 suites originales correctas. |
| Procesos de filtro/replicación | Finalizados; PIDs ausentes al cierre. |

Se preservaron los cambios locales previos, incluidos el registro anterior y
sus scripts. Este trabajo añadió el experimento, sus tres herramientas de
ejecución/pruebas/análisis y una entrada en `docs/README.md`; no instaló ODD.
