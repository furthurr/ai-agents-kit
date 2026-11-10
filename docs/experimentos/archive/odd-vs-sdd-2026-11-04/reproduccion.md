# Reproducción y lectura de evidencia

Este experimento usa inferencia real de un proveedor. Reejecutarlo consume los
recursos de la cuenta del host; no hay una estimación de factura a partir del
coste cero que puede reportar OpenCode.

## Entradas y requisitos

- Baseline MAS: `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
- OpenCode 1.18.34 con acceso existente al modelo `openai/gpt-6.1-sol`.
- Python 3.12 o compatible; librería estándar, sin dependencias Python adicionales.
- [Runner, fixtures y oráculos](../../../tools/odd_vs_sdd_experiment.py).
- [Auditor/exportador](../../../tools/odd_vs_sdd_audit.py).
- [Tratamiento B](tratamiento-b.md) y [protocolo](protocolo.md).

El runner comprueba que HEAD sea el baseline antes de preparar perfiles. Si el
repositorio ya avanzó, preparar una **copia temporal independiente** en ese commit
y copiar allí, como overlay documental/experimental, ambos scripts y los tres
archivos `protocolo.md`, `investigacion.md` y `tratamiento-b.md` de este paquete.
No retroceder el checkout de trabajo ni sobrescribir cambios locales para hacerlo.
El auditor es posterior a la ejecución y no forma parte del tratamiento.

## Advertencia sobre el runner actual

El SHA-256 de `tools/odd_vs_sdd_experiment.py` registrado en la congelación v2 es
`633eb3a0e4705b7f93174aecea87ed6b08a62a6b878805a0cd2412690cba0ec3`.
El archivo presente al archivar tiene
`e80a792abbc9d68476b91fdd3375f1cdadfb50c31393febb5f0d29a79e3be9f4`:
se cambió posteriormente su helper `run` al diagnosticar la salida de Gemini
(decodificación tolerante y manejo de timeout). No es el runner congelado exacto.

Los hashes de `protocolo.md`, `tratamiento-b.md` e `investigacion.md` sí coinciden
con sus entradas v2 al archivar. No se restaura el runner ni se retocan los JSON
para ocultar la discrepancia: los resultados anteriores son evidencia histórica.
Antes de intentar reproducción exacta, recuperar una copia del runner que
coincida con el hash congelado. Si no se dispone de ella, la ejecución con el
script actual debe identificarse como un experimento nuevo con nuevas entradas.
Los comandos siguientes describen el flujo original, no una reproducción exacta
ya acreditada con el árbol actual. No reejecutar el auditor contra la evidencia
original exportándola encima para «actualizar» retroactivamente el experimento.

## Secuencia

Desde la copia preparada, elegir una raíz externa temporal vacía. Sustituir
`<ROOT>` por esa ruta; los ángulos son placeholders, no shell literal:

```text
python3 tools/odd_vs_sdd_experiment.py <ROOT> prepare
python3 tools/odd_vs_sdd_experiment.py <ROOT> probe
python3 tools/odd_vs_sdd_experiment.py <ROOT> freeze
python3 tools/odd_vs_sdd_experiment.py <ROOT> filter
python3 tools/odd_vs_sdd_experiment.py <ROOT> replicate
python3 tools/odd_vs_sdd_experiment.py <ROOT> report
python3 tools/odd_vs_sdd_audit.py <ROOT> --sanitize-errors
python3 tools/odd_vs_sdd_audit.py <ROOT>
```

`prepare` valida que los oráculos distingan baseline de referencia; `probe`
comprueba configuración resuelta y carga real de ambas skills. `freeze` registra
las entradas antes de inferencia A/B. No editar fuentes congeladas entre fases.
Si hay fallo de infraestructura, conservarlo y crear otra versión/raíz, sin
sobrescribir celdas ni seleccionar reintentos favorables.

`filter` y `replicate` bloquean hasta terminar su lote. También existen
`launch-filter` y `launch-replicate`, que escriben un log y PID y dejan el proceso
en segundo plano; no equivalen a haber completado la fase. Nunca iniciar
replicación antes de inspeccionar las veinte celdas del filtro y sus controles.

Las credenciales no se leen ni copian: OpenCode utiliza su autenticación habitual.
La configuración y skills se montan en perfiles temporales, iniciados en procesos
nuevos. La sesión habitual no necesita reiniciarse y no recibe el tratamiento B.

Sanear errores es obligatorio antes de inspeccionar o exportar trazas: el runner
congelado v2 no filtra por sí mismo los datos de transporte adjuntos a un error
API. `--sanitize-errors` conserva solo tipo, mensaje, statusCode e isRetryable;
retira headers/cuerpos/metadata y registra hashes antes/después. No cambia tokens,
duración, artefactos ni aceptación. No repetir sobre la misma raíz: conservar el
primer recibo. En este estudio se aplicó una vez tras los errores de cuota.

## Qué permiten reconstruir los archivos

- `congelacion.json`: fecha, hashes, fixtures, tareas, referencias y oráculos.
- `celdas.json`: una fila por celda, métricas, respuestas, aprobaciones simuladas,
  artefactos y archivos finales modificados.
- `metricas.json`: agregados por brazo, escenario y repetición.
- `auditoria.json`: checks post-run, comandos/resultados observados, preservación
  de assertions originales y búsqueda de accesos visibles fuera del alcance.
- `preflight.json`: configuración resuelta y hashes de instrucciones de perfiles.
- `procedencia.json`: hashes de trazas completas externas y ubicación original.
- `incidente-v1.json`: intento anterior interrumpido, excluido de los agregados v2.
- `errores-proveedor.json`: fallos tipados y recibos de saneamiento de trazas.

Las trazas completas externas incluyen las secuencias de herramientas, pero no
razonamiento privado. Los JSON conservados no sustituyen cada evento de esas
trazas ni garantizan la permanencia de su ubicación temporal. Los hashes permiten
comparar una copia recuperada, no recrear un archivo ausente.

La igualdad exacta de resultados no está garantizada: inferencia estocástica,
caché del proveedor, servicio remoto y condiciones de carga no quedan congelados.
