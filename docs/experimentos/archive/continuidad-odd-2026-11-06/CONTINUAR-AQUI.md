# Continuidad — ODD con estándares y eficiencia

**Entrada prioritaria para una sesión NUEVA.** Fecha de cierre:2026-11-06 UTC.
Este es un artefacto de continuidad experimental, no una sincronización de los
índices canónicos ni una autorización para programar/instalar/ejecutar modelos.
El usuario pidió detener las pruebas por ahora y continuar en otra sesión.

## 1. Objetivo actual del usuario

> Crear una versión de ODD que consulte correctamente los dominios ya definidos
> y no consuma tantos tokens, sin ahorrar mediante omisión de estándares.

Dominio pertinente → cargar y usar criterios de data-api/ui-design; ambos → ambas;
ninguno → ninguna por rutina. También consultar fuentes concretas del proyecto y
detectar documentación desactualizada, sin bootstrap ni actualización canónica automática.
Se busca consumo TOTAL de la tarea, no solo un prompt pequeño o una respuesta breve.

La versión eficiente de ODD **sigue pendiente**. Dos optimizaciones exploratorias
recientes no dieron ahorro y no están aprobadas para producción. No declarar
equivalencia, eliminar estándares o inventar una victoria para satisfacer la hipótesis.

## 2. Qué leer y en qué orden

Lectura mínima, sin cargar todos los archivos enormes al contexto:
1. Este archivo, `estado.json` y `PROMPT.md` de esta carpeta.
2. [ODD con estándares: cohorte GPT completa](../odd-estandares-gpt6-luna-max-1800/README.md).
3. [Optimización con mapas: resultado negativo](../odd-navigator-architecture-luna-max/README.md).
4. [Núcleo/referencias: resultado negativo más reciente](../odd-domain-core-luna-max/README.md).
5. JSON exportados de esas carpetas y scripts concretos al investigar una afirmación.

Para profundizar en la integración Developer y la decisión de producto:
- [Developer candidato2 y build](../developer-v2-dominios-build-gemini-2026-11-05/README.md).
- [Primer Developer candidato1](../developer-v2-alta-gemini-2026-11-05/README.md).
- [Proyecto existente y tarea muy alta](../real-project-gemini-2026-11-05/README.md).
- [Continuidad previa](../../README.md): histórica, anterior a estos ensayos.

Los informes contienen sus protocolos, freezes, referencias y límites. La evidencia
exportada está en `evidencia/`; las trazas completas saneadas están en `laboratorio.tar.gz`
y los hashes en `preservacion.json`. Los temporales no son la única copia.

## 3. Estado local que NO se debe perder

Repositorio usado:
`/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit`.
HEAD observado: `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
`docs/README.md` ya estaba modificado; gran parte de `docs/experimentos/` y scripts
de laboratorio siguen **untracked**. No se hizo commit/push.

Abrir el MISMO checkout. Otro worktree/máquina no recibe esos archivos del remoto.
Para transportar: copiar el conjunto de experimentos y el paquete de herramientas,
o autorizar su versionado mediante el flujo Git correspondiente. No reset/clean.

El kit canónico sigue con5 agentes/11 skills/6 plataformas. No hay ODD instalado,
Developer actual sigue activo y las skills canónicas data-api/ui-design siguen completas.
Los perfiles y variantes solo existen en laboratorios/evidencia. Ninguna prueba
activa o nueva inferencia queda pendiente ejecutándose en segundo plano.

## 4. Decisión Developer que se mantiene separada

El usuario eligió el procedimiento **Developer v2 candidato2** para una futura
sustitución con nombre público **Developer**, IDs `developer` agente/skill, y
deprecación de la implementación anterior sin segundo Developer permanente.
**No se ha implementado ni instalado esa migración.** Investigar ODD no la ejecuta
ni la cancela automáticamente.

Plan portable del Escritorio:
`/Users/pedrogomezvasquez/Desktop/PLAN-Developer-v2-como-Developer-2026-11-05.md`.
SHA256 observado:
`fd62d8aa65605549f3d0321522751b3f35fb5b02af8435fcc2acad9edda97f5b`.
Se incluye copia en `herramientas-y-plan.tar.gz`, sin modificar el original.
Ese documento no autoriza implementación al leerlo.

## 5. Cronología y resultados que importan

### A. Antecedentes y Developer

- Comparación Developer/SDD/ODD Gemini:90 celdas,30/30 funcionales por brazo.
  ODD −18,34% tokens vs Developer, +1,56% duración; corpus pequeño, no equivalencia integral.
- Developer compacto:90 celdas; candidato más corto consumió +6,84% tokens y
  +16,39% tiempo vs actual. **No adoptar.** Texto corto no garantiza menos pasos.
- Proyecto LocalLibrary existente:27 celdas,36 fases, Developer/SDD/ODD6/9 cada uno.
  Todos fallaron T3 por listado heredado de préstamos que filtraba mal sucursales.
  Las43 pruebas originales pasaban. Test existente verde no certifica requisito nuevo.
- Developer candidato1, tarea Alta: nueve celdas,3/3 por brazo. −22,34% tokens vs
  actual y −20,13% vs ODD, pero data-api1/3 y ui-design0/3 en candidato. No garantía
  de preservar aplicación de estándares.
- Developer candidato2 + build, Gemini:12 celdas,3/3 por brazo; candidato carga ambas
  skills3/3 y cinco checks focalizados correctos. −19,48% tokens vs Developer,
  +1,40% vs ODD y −27,26% vs build. ODD ambas1/3; build data2/3,UI0/3.
  No lecturas directas de documentos de proyecto en esa tarea principal.

### B. ODD original vs ODD con estándares

Fuente original histórica: `../odd-vs-sdd-2026-11-04/tratamiento-b.md`, cuerpo entre
marcadores. Ajuste: `../odd-estandares-gemini-2026-11-05/ajuste.md`, añadido sin
reescribir los siete pasos. Incluye carga pertinente, fuentes del proyecto,
consumidores y cierre mediante documentation-orchestrator.

Lotes separados que no se deben borrar ni combinar:

| Carpeta de informe | Estado y razón |
|---|---|
| `odd-estandares-gemini-2026-11-05` |4 intentos/6 previstos; originalR2 timeout600s, snapshot funcional. Ajustado2 conversaciones completas y funcionales. Cinco checks focalizados pasaron. |
| `odd-estandares-reintento-gemini-2026-11-05` |Nuevo lote:4 intentos, ambosR2 APIError403, R3 no iniciado. Consulta de cuotas también403; causa exacta desconocida. |
| `odd-estandares-gpt6-luna-max` |Nueva cohorte `openai/gpt-6-luna --variant max`,600s: ambosR1 timeout, sinR2/R3. Preparaciones fallidas por herramienta edit/apply_patch y cwd preservadas. |
| `odd-estandares-gpt6-luna-max-1800` |Nueva cohorte1800s:6/6 conversaciones sanas. Ajustado3/3 aceptaciones, original2/3; nueve oráculos externos3/3 ambos. |

Gemini devolvió403; **no se confirmó un baneo ni su motivo**. El usuario cambió
explícitamente el modelo a GPT-6 Luna max. No se leyeron credenciales, no se cambiaron
cuentas para sortear bloqueos. No suponer que Gemini ya está disponible.

Cohorte GPT completa de1800s:

| Agregado de tres ejecuciones | ODD original | ODD ajustado con estándares |
|---|---:|---:|
| Tokens comparables |6.161.781|8.428.119|
| Conversación sumada(s) |2.474,107|3.049,399|
| Cargas de cada skill de dominio |0/3|3/3|
| Lectura README / propuesta documental |0/3|3/3|

Ajustado: **+36,78% tokens y +23,25% tiempo**. No llamarlo coste fijo de leer docs:
ahorró tokens en2/3 repeticiones, pero R3 elevó mucho el agregado. No se aislaron causas.
El originalR2 pasó oráculos externos y las43 pruebas originales por separado, pero
falló la suite conjunta por un test añadido por el agente que cerraba SQLite dentro
de TestCase. La aceptación predefinida sigue2/3; no inventar un bug del producto por ello.

### C. Descartado: priorizar mapas como optimización general

Informe `../odd-navigator-architecture-luna-max/README.md`.
Una tarea, una pareja nueva, ambos reciben MISMO baseline con mapas mínimos fieles
del fixture. Control=ODD con estándares; tratamiento=el mismo + ruta-contexto.md.
No son cambios al `.navigator`/`.architecture` canónico del kit.

| Pareja exploratoria | Control | Con ruta selectiva |
|---|---:|---:|
| Tokens |1.781.135|2.774.390|
| Segundos |741,973|1.091,775|
| Herramientas / pasos registrados |60/32|63/41|

Ambos funcionales y con ambas skills antes de producto. Tratamiento leyó navigator
y dos notas de arquitectura; sin modificarlas. Resultado **+55,77% tokens,+47,14% tiempo**.
El usuario pidió **olvidar esta variante**. No adoptarla ni borrar evidencia.
Esto no demuestra que los mapas sean inútiles en tareas mayores o desconocidas.

Corrección de análisis: regex inicial no reconocía «documental». Ambas variantes
propusieron actualización del README; solo control nombró explícitamente al orquestador.
Conservar `summary-audit.json` inicial; usar **`evidencia/summary-final.json`** revisado.
No confundir el esquema heredado `underlying` (tres repeticiones) con el nivel superior
de esta pareja de dos celdas.

### D. Último ensayo: núcleo breve + referencias bajo demanda

Informe `../odd-domain-core-luna-max/README.md`.
Mismo ODD principal en ambos perfiles, sin mapas añadidos. Solo cambió entrega del
contexto de data-api/ui-design, NO el procedimiento ODD ni requisitos:

- Control: skills completas.
- Tratamiento: núcleo + implementation.md (secciones técnicas literales),
  documentation.md (estructura/bootstrap/sync) y original-contract.md íntegro.
- Todas las secciones preservadas y trazadas por heading/hash; plantillas intactas.
- Ambos implementation.md fueron leídos íntegramente antes de producto; cero lecturas
  de documentation.md y original-contract.md. No fue ahorro por omitir estándares.

| Única pareja | Completas | Núcleo/referencias |
|---|---:|---:|
| Aceptación |Pasa|Pasa|
| Tokens comparables |1.226.103|3.256.195|
| Segundos |631,329|1.158,198|
| Herramientas / pasos registrados |48/22|77/45|
| Búsquedas |2|11|
| Nota ODD persistente |Ninguna|Una|

**+165,57% tokens,+83,45% tiempo**. No integrar como ahorro validado. La reducción
local sí existió: archivos núcleo+criterios14.600 bytes vs23.665; salidas observadas
skill+referencias24.608 vs31.324 bytes. El total de read+búsqueda+skill fue146.667 vs
141.895 bytes: otras lecturas/pasos/decisiones anularon esa reducción local. Bytes
no son tokens, ni todo el contexto. No atribuir causalmente todo a la división con n=1.

Ambos leyeron criterios y detectaron README desactualizado, sin editarlo, proponiendo
documentation-orchestrator. Ningún bootstrap. El tratado creó odd/tasks/reservation-flow.md.
Un archivo no demuestra sobreingeniería, pero no excluir su coste. **Organización
correcta y preservación literal no garantizan ejecución eficiente.**

## 6. Qué NO está decidido o probado

- No existe una nueva versión ODD eficiente aceptada. Mantener ODD con estándares
  como referencia de comportamiento, no declararlo barato por definición.
- No usar «menos instrucciones necesariamente menos tokens». Lo refutaron varias
  variantes en estas muestras; tampoco concluir «todo prompt corto es peor».
- Subagente lector, instancia con otro modelo, recuperación determinista/RAG,
  validadores ejecutables y cachés de contexto se discutieron: **no están probados
  ni autorizados para implementación automática**.
- Un subagente debe sumar sus tokens al principal; mover coste no es ahorrarlo.
- Leer skills/documentos no certifica aplicación exhaustiva. Falta auditoría de
  estándares, seguridad/visual, continuidad larga y ciclo documental completo.
- El coste de preparación no está totalmente medido; hubo un recolector inicial
  interrumpido. No inventar un total global de todo el trabajo.

## 7. Siguiente paso recomendado, antes de más inferencia

Investigación acotada y de solo lectura sobre las trazas/exportados ya disponibles:
1. Comparar especialmente control y tratado del último ensayo y la cohorte GPT completa.
2. Clasificar operaciones por exploración, criterios, escritura, pruebas, reparación,
   seguimiento y cierre; identificar lecturas/búsquedas repetidas y qué cambió.
3. Distinguir tamaño de la skill de longitud de la ejecución, contexto acumulado,
   duplicación por turnos y decisiones del modelo. No almacenar razonamiento privado.
4. Verificar si el registro ODD y las búsquedas extra se justifican en la tarea, sin
   asumir que el formato de la skill es la causa. Revisar efectos de orden/visibilidad
   de reglas; partición literal no garantiza igual interpretación.
5. Proponer una hipótesis nueva o una repetición que realmente discrimine causas.
   Definir control, aceptación/fidelidad, consumo TOTAL, número de intentos, límite
   y parada antes de editar o llamar modelos. Esperar aprobación del siguiente plan.

No lanzar otra batería automáticamente por abrir esta sesión. No retocar candidatos
anteriores y reinterpretar sus resultados como aprobados. No usar el runner histórico
`tools/gemini_benchmark.py` para métricas nuevas: su comparación exploratoria fue invalidada.

## 8. Entorno de reproducción y herramientas

Baseline: MDN LocalLibrary commit3120b4302bf87a1b8c84d06662c2b8787f7da5f8,
CC0-1.0, Python3.12.4/Django6.1.1/SQLite,43 tests originales, estáticos preparados.
TASK-2 exacta y oráculos en `evidencia/cases.json` y archivos del laboratorio preservado.
Referencia y oráculos se validaron antes de inferir; fuente de tests original restaurada
en copia separada. Los agentes no recibieron feedback de oráculos para autocorregir.

Último modelo operativo: `openai/gpt-6-luna`, CLI `--variant max`, sin temperatura
por capacidad del modelo; timeout1800s configurado igual en ambos brazos. El parámetro
se envió y se registró; aplicación interna del proveedor no observable. Gemini quedó
bloqueado por403 observado; no cambiar cuentas/modelos sin decisión explícita.

Base de temporales de esta máquina:
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/`.
Raíces recientes: `odd-standards-luna-max-1800-20261105`,
`odd-context-routing-luna-max-v1`, `odd-domain-core-luna-max-v1`.
El kernel se originó en `real-project-gemini-20261104/runner.py`; los adapters privados
dependen de él y del Python venv de ese laboratorio. **No presuponer que existan en
otra sesión/máquina**. Usar paquetes preservados, revisar rutas absolutas y generar
otra raíz/freeze si se autoriza un ensayo. No tocar las congelaciones históricas.

Scripts recientes y sus tests:
`odd_standards_benchmark`, `odd_standards_retry`, `odd_standards_luna`,
`odd_standards_luna_1800`, `odd_context_routing`, `odd_domain_core`, sus reports,
`real_project_report`, `preserve_real_project_lab` y helpers `gemini_three_way` /
`developer_v2_high_benchmark` / `developer_v2_domains_build`.
Snapshot de herramientas en `herramientas-y-plan.tar.gz`; inventario/hash en `manifest.json`.

Último cierre técnico:71 pruebas offline/regresión pasaron en el ensayo core,
preflights2/2, referencia43+9, cero timeouts/errores API de esa pareja e inputs intactos.
Eso valida arnés y caso, no producción ni todas las plataformas.

## 9. Reglas para interpretar y continuar

- Tokens comparables=input+cache_read+cache_write+output; reasoning aparte. Contadores
  ausentes desconocidos, no cero. Caché no es mismo precio; cero coste host no es factura.
- Tiempo sumado no es wall-clock ni espera humana. No mezclar cohortes/modelos para
  un porcentaje único ni seleccionar éxitos/repeticiones baratos.
- Una solución incompleta barata no gana. Separar API/proceso, aceptación funcional,
  tests originales, tests añadidos y fidelidad. Evitar falsas conclusiones por tests
  añadidos defectuosos o por detectores regex sin revisión.
- Permisos de herramientas no son sandbox OS ni bloqueo universal para Python generado.
- Mantener deny/secretos, rutas seguras y trabajo local. No leer/copiar credenciales.
- Sin Engram/RDD, SDD ni delegación/instalación/bootstrap automático. No modificar
  canónicos de documentación ni AGENTS desde Developer; su sincronización corresponde
  a documentation-orchestrator bajo selección manual.

## 10. Cierre documental de esta sesión

Este paquete registra el experimento y la continuidad. Los índices canónicos
`docs/experimentos/README.md` y el punto antiguo `docs/experimentos/CONTINUAR-AQUI.md`
no se reescribieron desde este rol. Para incorporarlos al índice general, el usuario
debe seleccionar documentation-orchestrator; este documento, estado y manifest dan
el contexto portable para hacerlo. No se cambió automáticamente de agente.

**Ahora detenerse.** No queda autorizada otra ejecución por haber leído este archivo.
