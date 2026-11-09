# Reproducción y lectura de evidencia

No ejecutar para «actualizar» los resultados anteriores ni reutilizar una raíz ya
usada. Son llamadas reales al proveedor y consumen cuota. No existe factura
monetaria inferida del coste cero que puede exponer el host.

## Entradas y comandos

Requiere OpenCode con la integración Antigravity habitual y acceso efectivo a
`google/antigravity-gemini-3.8-flash`, Python y Git. El evaluador no lee/copia
credenciales. Se conserva el plugin del host sin `--pure` o cambio de XDG.

Desde el repositorio, elegir `<ROOT>` externa y nueva:

```text
python3 tools/test_developer_compact_benchmark.py
python3 tools/developer_compact_benchmark.py <ROOT> prepare
python3 tools/developer_compact_benchmark.py <ROOT> probe
python3 tools/developer_compact_benchmark.py <ROOT> freeze
python3 tools/developer_compact_benchmark.py <ROOT> filter
python3 tools/developer_compact_benchmark.py <ROOT> replicate
python3 tools/developer_compact_report.py <ROOT>
```

`prepare` valida oráculos y la equivalencia A/B de skill/referencias, configuración
normalizada y estados iniciales. `probe` verifica prompt resuelto, skill por cuerpo
íntegro, lectura, edición real y ejecución unittest. `freeze` registra entradas
antes de las tareas. No modificar prompts, código o reglas durante las celdas.

`launch-filter`/`launch-replicate` lanzan en background con PID y log. Esperar su
finalización y revisar el filtro antes de replicar: un lanzamiento exitoso no es
un experimento terminado. No se reejecuta una celda para corregir su resultado.
El analizador permite `--export <DESTINO-NUEVO>`; nunca exportar encima de archivos
ya conservados. Si cambia una entrada, crear otra versión de experimento.

El wrapper adapta funciones del runner anterior en memoria. No modifica el
archivo importado ni sus resultados. Se congelan hashes del wrapper, el runner
reutilizado, tests, perfiles y corpus. A/B tienen el mismo nombre público de
agente/skill en procesos separados, sin un homónimo instalado por el experimento;
la configuración de cada proceso monta una sola ruta de perfil.

## Semántica de resultados

- `functional_pass`: aceptación del fixture mediante oráculo, suite y controles
  de intención observables, no ausencia de todo defecto.
- `successful_delivery`/`conforming_delivery`: además pasan procesos, carga y
  controles mecánicos; no equivalencia semántica exhaustiva del contrato.
- Errores de herramientas, comandos denegados, PLAN con efectos de bytecode y
  otras alertas se informan aparte. No eliminar una celda por ser desfavorable.
- Tokens comparables = input + cache-read + cache-write + output; reasoning
  separado y `tokens.total` del SDK como contraste. Contadores no son contenido
  de razonamiento privado. Una métrica ausente es desconocida, no cero.
- Duración: conversación CLI, no tiempo humano. La suma de celdas concurrentes
  no equivale al wall-clock del lote. Los checks externos posteriores quedan fuera.
- Medir bytes/palabras del prompt no equivale a medir tokens ni demuestra que el
  comportamiento vaya a mantenerse al retirar una repetición.

## Conservación

El exportador conserva ledger, perfil de cada brazo, casos y oráculos, igualdad
A/B, preflight normalizado, comandos, snapshots finales, métricas y hashes de
trazas. Los datos completos de transporte API y razonamiento privado no se guardan.
Las trazas sanitizadas quedan externamente y su permanencia no está garantizada.
Un hash permite contrastar una copia recuperada, no reconstruir un archivo perdido.

El contexto global, plugin y caché del proveedor no son herméticos. Las herramientas
personalizadas heredadas deben declararse; la configuración del ensayo no es un
sandbox de sistema operativo. No usar fixtures con datos de producto ni tomar
el resultado como permiso para instalar la variante o desactivar guardas.
