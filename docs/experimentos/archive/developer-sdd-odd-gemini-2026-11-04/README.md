# Developer vs SDD vs ODD — Gemini 3.8 Flash

Identificador: `gemini-three-way-v1-20261104`. Modelo solicitado:
`google/antigravity-gemini-3.8-flash`, a través del plugin Antigravity de OpenCode.

**Estado: terminado, 90/90 celdas con aceptación funcional.** En esta batería,
ODD experimental consumió **18,34 % menos tokens que Developer**, con duración
agregada **1,56 % mayor**: no fue más rápido globalmente. Developer y ODD quedaron
muy próximos en varias tareas. SDD tuvo más consumo y más turnos, pero sus
beneficios de especificación formal no quedaron representativamente evaluados.

No se activa ni promueve un agente por estos resultados. No se reutilizan las
cifras del anterior ensayo Gemini, que no fue una comparación validada.

## Pregunta

¿Cómo cambian calidad, uso de herramientas, duración, tokens e intervenciones al
usar Developer, SDD o el tratamiento ODD experimental con el mismo modelo?
¿Qué observaciones ayudan a elegir un flujo según el tipo de tarea?

## Diseño

Diez escenarios sintéticos, tres brazos, tres repeticiones: 90 celdas previstas.
SDD recomienda su profundidad natural, salvo reanudación de una spec previa.
Las aprobaciones necesarias se responden con un simulador acotado y se cuentan;
no se atribuye a una máquina tiempo de decisión humana.

Se verificó en preflight la identidad del agente, contenido de skill y herramientas
efectivamente utilizadas. Se congelaron 176 entradas antes de las celdas. Los
resultados se evalúan con oráculos externos y suites originales, no solo por la
afirmación final del modelo. Se conservan errores y todos los intentos.

## Entradas

- [Protocolo](protocolo.md).
- [Tratamientos y procedencia](tratamientos.md).
- [Runner](../../../../tools/gemini_three_way.py).
- [Pruebas offline del runner](../../../../tools/test_gemini_three_way.py).
- [Analizador y exportador](../../../../tools/gemini_three_way_report.py).

Los perfiles son temporales y los procesos conservan la integración de
autenticación del host sin leer o copiar credenciales. No se editan fuentes de
agentes, adaptadores, instaladores ni defaults persistentes.

## Resultado agregado

Treinta celdas por flujo, mismas diez tareas y tres repeticiones:

| Métrica | Developer | SDD | ODD experimental |
|---|---:|---:|---:|
| Aceptación funcional | 30/30 | 30/30 | 30/30 |
| Tokens comparables observados | 3.987.598 | 8.464.007 | 3.256.158 |
| Duración sumada de conversaciones | 1.094,989 s | 1.572,366 s | 1.112,014 s |
| Herramientas llamadas | 364 | 409 | 356 |
| Errores de herramienta recuperados | 1 | 0 | 4 |
| Respuestas simuladas de usuario | 0 | 27 | 0 |

SDD respecto a Developer: **+112,26 % tokens**, **+43,60 % duración**. Se incluyó
recomendación natural de profundidad y respuesta de selección. Esa fase también
contiene exploración y definición de alcance: no es íntegramente trabajo inútil
ni debe restarse para inventar el coste de una ejecución alternativa.

Tokens comparables = input + cache-read + cache-write + output; reasoning aparte.
El tiempo suma celdas concurrentes, **no es wall-clock del lote ni tiempo humano**.
Coste monetario real desconocido. El tamaño/longitud de instrucciones y el método
varían juntos; no se separaron causalmente sus efectos.

## Qué elegir, según lo observado

- **Developer:** opción general razonable. Muy cerca de ODD en funciones pequeñas,
  features acotadas y planificación; más rápido en el bug monetario y la reanudación
  sencilla de esta batería.
- **ODD experimental:** opción prometedora cuando importa reducir tokens. Ahorro
  claro frente a Developer en documento, CLI, reglas literales, persistencia y
  consulta; no mejora grande en todas las tareas ni calidad superior demostrada.
  Se observó RED antes del código en sus 21 celdas de comportamiento.
- **SDD:** elegir por necesidad de acuerdo explícito, revisión de especificación
  y trazabilidad, no por esperar menor latencia. El modelo eligió Direct en las
  24 decisiones nuevas y conservó Tiny solo en las tres reanudaciones. No se
  probó creación nueva de Tiny/Lite, y algunas elecciones Direct requieren revisar
  sus guardas. No extrapolar a que todo SDD es más lento o menos útil.

**Aceptación funcional no equivale a fidelidad perfecta:** hubo calificación de
esfuerzo en un bug, omisiones de líneas Risk y dos py_compile en modo PLAN. Véanse
los [resultados y alertas](resultados.md). Diferencias pequeñas (<10 %) se tratan
como cercanía descriptiva, no un ganador; n=3 no prueba significancia estadística.

## Evidencia y límites

- [Resultados por tarea, herramientas y recomendaciones](resultados.md).
- [Reproducción y semántica de métricas](reproduccion.md).
- [Congelación](evidencia/freeze.json), [perfiles](evidencia/profiles.json) y
  [casos/oráculos](evidencia/cases.json).
- [Ledger de 90 celdas y snapshots finales](evidencia/records.json).
- [Métricas agregadas](evidencia/summary.json), [auditoría](evidencia/audit.json)
  y [aclaraciones de interpretación](evidencia/interpretacion.json).
- [Preflight](evidencia/preflight.json) y [procedencia de trazas](evidencia/provenance.json).

Las 176 entradas congeladas siguen intactas; las 63 suites originales ejecutadas
sobre las soluciones finales pasaron. Sin errores API, timeouts, métricas ausentes,
llamadas malformadas detectadas, cambios de tratamiento o reintentos selectivos.
Se observaron 377 lecturas/búsquedas sin accesos a otras raíces. El host exponía
también herramientas personalizadas de búsqueda/cuota: no se usaron, pero los
deny de webfetch/websearch no acreditan un bloqueo de red universal ni un sandbox.

Se conservan las entradas, perfiles, contadores, comandos y archivos finales;
las trazas completas sanitizadas son externas y su permanencia no está garantizada.
La evaluación no es ciega ni representa producción, UI/APIs distribuidas,
compactación real o todas las plataformas. No hay evidencia para retirar agentes
del MAS ni para garantizar ahorros fuera de este corpus/modelo/configuración.

## Conservación posterior para otra sesión

Las 90 trazas sanitizadas se copiaron posteriormente con sus hashes a
[un ZIP preservado en el repositorio](../continuidad-2026-11-04/README.md).
Las rutas de origen en la procedencia histórica no se reescriben; ahora existe
esa copia adicional, sin volver a ejecutar modelos ni cambiar resultados.
Leer [índice de experimentos](../../README.md) para las conclusiones posteriores
y la decisión aún pendiente sobre Developer/ODD.
