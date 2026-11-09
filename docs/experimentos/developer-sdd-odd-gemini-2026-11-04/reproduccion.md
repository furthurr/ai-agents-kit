# Reproducción y lectura de la evidencia

Este ensayo es independiente del anterior Gemini exploratorio. No modifica ni
recalcula los resultados históricos de ODD vs SDD.

## Requisitos

- OpenCode con el modelo `google/antigravity-gemini-3.8-flash` accesible por su
  integración Antigravity habitual; aparecer en el selector no acredita acceso.
- Python con librería estándar, Git y permisos para una raíz temporal externa.
- Fuentes del MAS, tratamiento B histórico y scripts con los hashes de la nueva
  congelación. Si cambiaron, usar otro identificador y no sobrescribir este lote.
- Cuota/coste de inferencia disponible: estos comandos hacen llamadas reales.

No se copia configuración global ni se lee autenticación. El host conserva su
plugin, que puede actualizar sus estadísticas/sesiones normales. La configuración
experimental es efímera por proceso; la sesión habitual no necesita reiniciarse
porque no se cambia su configuración persistente ni se instala un agente.

## Secuencia

Sustituir `<ROOT>` por una raíz temporal externa **nueva**, no por una carpeta con
resultados de otra ejecución. Desde la raíz del repositorio:

```text
python3 tools/test_gemini_three_way.py
python3 tools/gemini_three_way.py <ROOT> prepare
python3 tools/gemini_three_way.py <ROOT> probe
python3 tools/gemini_three_way.py <ROOT> freeze
python3 tools/gemini_three_way.py <ROOT> filter
python3 tools/gemini_three_way.py <ROOT> replicate
python3 tools/gemini_three_way_report.py <ROOT>
```

`prepare` valida oráculos contra baseline/referencias y monta namespaces.
`probe` contrasta el agente resuelto y el cuerpo completo de la skill primaria,
edición/lectura y unittest reales por brazo. `freeze` registra entradas y casos
antes de inferencia de tareas. No modificar esas entradas durante el lote.

El filtro tiene 30 celdas. Inspeccionarlo antes de replicar: errores de API,
contaminación, acceso externo o cambios de hash impiden continuar. Los fallos
funcionales ordinarios se conservan para evaluar fiabilidad. No cambiar permisos
durante celdas ni repetir únicamente fallos hasta completar una tabla verde.

`launch-filter` y `launch-replicate` son equivalentes de lanzamiento en background:
guardan PID/log, no un resultado exitoso. Esperar fin de proceso y comprobar todos
los registros. No lanzar dos veces una fase sobre la misma raíz.

El exportador acepta `--export <DESTINO-NUEVO>`. Conserva snapshots, perfiles,
mensajes y comandos, con referencias a trazas externas. Los archivos de destino
se crean exclusivamente; no exportar encima de evidencia ya publicada para
actualizarla retroactivamente. Usar otra carpeta si se necesita otro análisis.

## Semántica de la evaluación

- `functional_pass`: pasa el oráculo/suite y controles estructurales de intención.
- `successful_delivery` y `conforming_delivery`: pasan también carga por contenido,
  procesos y checks mecánicos del runner. **No prueban todo el contrato semántico**.
  Las notas de cualificación del auditor requieren revisión, por ejemplo la
  elegibilidad de Direct ante un contrato compartido o datos persistidos.
- `tool_errors`: herramientas con estado de error, incluidos comandos denegados;
  no equivale automáticamente a un bug final ni incluye todo exit no cero.
- `user_turns`: mensajes simulados de elección/aprobación, no trabajo humano real.
- Tokens comparables: input + cache-read + cache-write + output; reasoning separado.
- `seconds_sum`: suma de duraciones de celdas concurrentes, no wall-clock del lote.

Las medianas y sumas incluyen todos los intentos disponibles; un error no se borra
para mejorar la eficiencia. Revisar cobertura y aceptación antes de comparar coste.
El coste cero del host no es una factura, y una suite vacía no cuenta como test.

## Cobertura y límites del host

El plugin habitual expone también herramientas personalizadas. El preflight
conserva la tabla real de herramientas; los deny de webfetch/websearch no se
presentan como bloqueo universal de todos los plugins. El auditor informa llamadas
a `google_search` o `antigravity_quota` si las hubiera. Las instrucciones del
experimento no autorizan usarlas. La disponibilidad común de esas herramientas
y del contexto global se declara, no se oculta ni se confunde con un sandbox.

Los directorios y secretos tienen reglas del host; ejecutar código Python de un
agente no queda aislado a nivel de sistema operativo por esas reglas. Usar solo
fixtures sintéticos y no ejecutar el harness contra datos reales de producto.

## Persistencia

Las trazas sanitizadas no guardan razonamiento privado ni transporte de errores
del proveedor. En el repo se conservan ledger, snapshots finales, perfiles,
comandos observados, hashes y análisis. Las trazas completas quedan fuera y su
permanencia temporal no está garantizada. Un hash no recrea un archivo perdido.

El analizador es posterior al lote; los oráculos y la política del simulador sí
estaban congelados. No mezclarlo con una revisión ciega independiente ni con una
certificación de funcionamiento de otras plataformas/modelos.
