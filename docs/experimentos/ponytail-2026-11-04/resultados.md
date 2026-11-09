# Resultados, verificaciones y procedencia

[Informe y decisión](README.md) · [Protocolo](protocolo.md)

## Calidad por escenario

| Caso | A | B | Evaluación registrada |
|---|---:|---:|---|
| S01 | 3/3 | 3/3 | Helper compatible reutilizado sin duplicación. |
| S02 | 3/3 | 3/3 | Caja conservada, sin reutilización incompatible. |
| S03 | 3/3 | 3/3 | `safe_load`, dependencia justificada, errores y rechazo de tags. |
| S04 | 3/3 | 3/3 | Contrato, consumidores y fixture coordinados; límites externos explícitos. |
| S05 | 3/3 | 3/3 | Cierre, autorización, errores y cancelación conservados. |
| S06 | 3/3 | 3/3 | Puerto, separación de dominio e inyección preservados. |
| S07 | 3/3 | 3/3 | Por salida: 1 TP, 0 FP, 0 FN; regresión conectada detectada. |
| S08 | 3/3 | 3/3 | 0 FP; defecto independiente excluido del cambio. |
| S09 | 3/3 | 3/3 | Por salida: 1 TP known; unknown condicionado; 0 FP/FN. |
| S10 | 3/3 | 3/3 | Cambio y exploración localizados. |
| **Total** | **30/30** | **30/30** | Sin diferencia de calidad según la rúbrica. |

Las 42 implementaciones pasaron suites unittest y oráculos externos, más inspección
de diffs/salidas. No se observaron tests debilitados para forzar éxito ni dependencias
injustificadas. Las 18 revisiones conservaron archivos intactos. Por brazo hubo seis
TP agregados (tres S07 y tres known S09), cero FP/FN, tres S08 sin hallazgos y tres
unknown S09 condicionados; estos últimos no son defectos confirmados.

Los oráculos no son exhaustivos: S05 comprueba cierre/error/KeyboardInterrupt, pero
no doble fallo read+close; la inspección de implementaciones/pruebas generadas cubrió
la conservación del error original. S03 sigue SafeLoader de la versión disponible de
PyYAML, sin matriz de versiones ni afirmación de compatibilidad YAML 1.2 completa.

## Tokens y repetición

| Contador `step_finish`, 30 celdas/brazo | A | B |
|---|---:|---:|
| Entrada no cacheada | 509.613 | 479.235 |
| Lectura de caché | 1.693.696 | 1.785.216 |
| Escritura de caché | 0 | 0 |
| Salida | 40.852 | 41.013 |
| Contador de razonamiento | 873 | 1.056 |
| **Total observado, incluido razonamiento** | **2.245.034** | **2.306.520** |

La caída de entrada no cacheada no es ahorro agregado: aumentó la lectura de caché.
No se conservó contenido de razonamiento privado. El coste real de facturación y
operaciones auxiliares del host, como titulado, no están íntegramente medidos.

| Repetición | Tokens A | Tokens B | Herramientas A/B | Pasos A/B |
|---|---:|---:|---:|---:|
| 1 | 768.170 | 764.477 | 105 / 102 | 70 / 70 |
| 2 | 742.837 | 765.298 | 98 / 104 | 70 / 70 |
| 3 | 734.027 | 776.745 | 101 / 99 | 68 / 73 |

| Escenario, tres repeticiones | Tokens A | Tokens B |
|---|---:|---:|
| S01 | 173.250 | 184.813 |
| S02 | 173.086 | 193.857 |
| S03 | 433.872 | 382.508 |
| S04 | 496.082 | 573.963 |
| S05 | 182.107 | 183.563 |
| S06 | 178.751 | 180.532 |
| S07 | 136.012 | 138.420 |
| S08 | 135.292 | 127.441 |
| S09 | 159.554 | 162.489 |
| S10 | 177.028 | 178.934 |

Las repeticiones 2 y 3 aportan cuarenta celdas temporalmente homogéneas:
868,158 s A frente a 878,783 s B (+1,22 %), y 1.476.864 tokens A frente a
1.542.043 B (+4,41 %). Son sumas de duraciones concurrentes. Las cuatro sesiones
recuperadas de r1 tienen duración desde timestamps de sesión, sin arranque CLI;
no se mezclaron para aceptar por eficiencia.

## Verificaciones e incidentes

| Comando/check | A | B externo |
|---|---|---|
| `python3 tools/validate.py` | Correcto: 11 skills, 5 agentes, 6 plataformas | Ídem |
| `python3 tools/check_links.py` | 94 Markdown correctos | 94 correctos con overlay descrito abajo |
| `python3 tools/test_context_efficiency.py` | 12 correctas | 13 correctas |
| `python3 tools/test_code_review_contract.py` | 7 correctas | 7 correctas |
| Render oficial | Reproducibilidad comprobada por validate | `python3 tools/render.py`, reproducibilidad comprobada |
| Estado final original | `git status --short` vacío; `git diff --check` correcto | B solo externa |

Medición estática de las dos fuentes candidatas: A 12.189 bytes, B 13.632:
**+1.443 bytes, +174 palabras, +18 líneas**. No mide el prompt completo ni tokens.

Incidentes conservados en el registro original:

1. El supervisor shell con timeout de 120 s se interrumpió durante el filtro.
   S04-A-r1, S05-A-r1, S05-B-r1 y S06-B-r1 terminaron normalmente; se recuperaron
   desde sus IDs originales, sin repetir llamadas. Sus códigos de proceso no se conocen.
2. Exportaciones/debug masivos por pipe se truncaron alrededor de 64 KiB. Se contrastó
   inventario con manifiestos y cargas reales; se recuperaron las cuatro sesiones vía
   PTY, filtrando en memoria antes de guardar y sin bloques de razonamiento.
3. Enlaces B fallaron inicialmente por seis destinos de A no montados en el snapshot:
   MAS.png y cinco referencias históricas .sdd. Se corrigió el evaluador con overlay
   de existencia, sin copiar ni modificar .sdd ni fuentes. No atribuir el fallo a B.
4. `measure_context.py` rechazó rutas absolutas; se repitió con rutas relativas a cada
   snapshot. La medición posterior no transforma volumen estático en uso real.
5. Un intento de delegación adicional fue rechazado por profundidad máxima 1;
   el coordinador ejecutó directamente el experimento, sin alterar el host.

Se registraron 60 celdas únicas, un intento por celda, sin timeouts del agente ni
errores de herramientas en las celdas. Auditoría de 408 llamadas read/glob/grep:
ninguna lectura fuera del fixture/configuración de su brazo ni de oráculos por esas
herramientas. No equivale a sandbox de sistema operativo.

## Procedencia de este registro

Esta selección procede de `resultado-final-v1.md`, `protocolo-v1.md`,
`metricas-final-v1.json`, `evaluacion-final-v1.md`, `estado-final-v1.json`,
`preregistro-v1.json` y una muestra del ledger `ejecuciones-v1.jsonl`.
Los agregados se transcriben de las métricas finales; aquí no se importan las
sesenta filas originales ni las transcripciones o configuraciones del host.

Directorio externo original (no es requisito de carga ni ruta portable):
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/mas-ponytail-evaluacion-20261103/`.

Hashes SHA-256 registrados en los artefactos originales:

| Artefacto original | SHA-256 |
|---|---|
| resultado-final-v1.md | `5b0ea5c8f8138bdea570e236ca3b63d29b069661e9fa7b8b85de4bd55098b9ac` |
| protocolo-v1.md | `fb864cb8e06f0cf4ac67b1c3fd8ccf768e05b812983996059a218797057d114f` |
| build_cases.py | `027f4abe0a41bc69105d892da21ca973146950e7b07a493f71344a8bf5bb09b5` |
| runner.py | `60f736cd223d1fec67ce284685ca5670f728a56c759b6cd6643553e557fc1ea8` |
| variante-b.patch | `6ae6c4bafebc6d461f9d70107af9bbe5b165fcd43dec2723b92bd8f165402378` |

Son identificadores de procedencia, no los hashes de estas síntesis Markdown.
El archivo original de estado final registra 162 hashes congelados intactos,
42 implementaciones verificadas, 18 revisiones sin cambios y cero trabajadores
activos al cierre. Los artefactos completos externos son necesarios para repetir
la agregación o reconstruir cada resultado; esta selección no los sustituye.
