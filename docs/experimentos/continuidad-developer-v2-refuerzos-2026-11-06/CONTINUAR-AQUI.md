# Continuidad — Developer v2 candidato2 + dos refuerzos de ODD

**Entrada principal para una sesión nueva. Actualizado: 2026-11-06 UTC.**
Este paquete es continuidad experimental, no documentación canónica sincronizada,
un candidato nuevo ya implementado ni una autorización para instalar o lanzar modelos.

## 1. Decisión actual del usuario

Última petición, conservada literalmente:

> ok documenta todo hasta donde vamos y prepara un MD para continuar el proceso en una sesión nueva, en esa sesión crearemos una Version modificada de este developer V2 :
>
> Developer v2 candidato2 + dos refuerzos de ODD:
>
> Trazabilidad de comprobación y preservación del comportamiento compartido.
> Reanudación reconciliada con código y evidencia vigente.
>
> y realizar las pruebas pertinentes para comprobar su rendimiento.

**Nueva dirección acordada:** Developer v2 candidato2 es la base. Del ODD inicial
solo se toman los dos refuerzos anteriores, no todo su procedimiento. La creación
del candidato derivado y sus pruebas quedan para la próxima sesión. No volver a
preguntar si estos dos refuerzos son el objetivo; sí fijar presupuesto/protocolo
experimental antes de nuevas inferencias, porque no se ha aprobado un número de llamadas.

**Hecho actual:** no se creó ni modificó el candidato derivado; no hay resultados
de rendimiento de ese candidato. No presentar los ensayos de ODD como si lo evaluaran.

## 2. Lectura mínima y fuentes exactas

Leer primero este MD y [estado.json](estado.json). Para arrancar sin historial:

1. Fuentes originales elegidas, no candidato1:
   - [Agente candidato2](../developer-v2-dominios-build-gemini-2026-11-05/candidato/agent.md).
   - [Skill candidato2](../developer-v2-dominios-build-gemini-2026-11-05/candidato/SKILL.md).
   - Copias literales de respaldo: [agente](fuentes/agent-candidato2.md) y
     [skill](fuentes/SKILL-candidato2.md). Son fuentes congeladas, NO el candidato reforzado.
2. [ODD inicial de siete pasos](../odd-vs-sdd-2026-11-04/tratamiento-b.md), cuerpo entre
   marcadores `experimental-instructions`. No es ODD con estándares, mapas, núcleo
   o agrupación. Es una adaptación experimental inline, no el producto upstream completo.
3. [Informe de candidato2 y build](../developer-v2-dominios-build-gemini-2026-11-05/README.md).
4. [Último ensayo: agrupación ODD](../odd-batching-luna-max/README.md),
   [auditoría](../odd-batching-luna-max/auditoria.json) y
   [verificaciones](../odd-batching-luna-max/verificaciones.json).
5. [Continuidad ODD previa](../continuidad-odd-2026-11-06/CONTINUAR-AQUI.md) solo para
   profundizar en los ensayos anteriores, sin cargar trazas enormes por rutina.

Verificar afirmaciones necesarias en JSON, scripts, código y tests. Los informes
son entradas, no sustitutos de evidencia. No leer toda `.architecture/.navigator`
ni regenerar índices para recuperar contexto. Instrucciones del host/proyecto primero.

## 3. Qué es candidato2 y qué falta realmente

El agente es un cargador breve; la skill es la autoridad única del procedimiento.
Candidato2 ya conserva:

- Intención/alcance: implementación clara sin aprobación rutinaria; consulta/PLAN
  de solo lectura; preguntas solo por decisiones funcionales/materiales/irreversibles.
- Contexto suficiente: instrucciones, código y documentación pertinentes; no relectura
  ni inventario rutinario; declarar límites y usar fuentes directas si falta documentación.
- Desarrollo integral UI/negocio/API/persistencia, compatibilidad y trabajo local protegidos.
- Carga selectiva por contenido: API/datos → data-api; visual → ui-design; ambos → ambas;
  ninguno → ninguna. También en PLAN; antes de trabajar el dominio; referencias pertinentes.
- Pruebas significativas, consumidores, errores, persistencia y revalidación tras cambios.
  Test-first si aporta evidencia, no obligación ritual universal.
- Registro solo si petición+diff no bastan para reanudar; requisitos exactos relevantes,
  pendientes y evidencia; un registro reutilizable, sin carpeta/formato obligatorios.
- Cierre documental aunque no cargue dominios: rutas/motivo, propuesta explícita de
  `documentation-orchestrator` cuando corresponda, sin edición canónica ni cambio automático.
- Sin SDD/delegación/publicación implícitos y con protección de secretos.

**No confundir complemento con ausencia total:** V2 ya prueba y preserva contratos,
y ya tiene continuidad. Se refuerzan la trazabilidad/baseline y la reconciliación
al reanudar; no se inventan dos subsistemas nuevos.

## 4. Delta exacto propuesto para el candidato derivado

Crear una copia experimental separada; conservar originales, hashes y freezes.
Mantener el agente cargador y el resto de candidato2, salvo identidad temporal
necesaria para aislar el ensayo. No decidir todavía un ID público adicional.

### A. Añadir a «Comprobar»

Texto de trabajo propuesto en la conversación:

> Vincula los criterios afectados con pruebas o checks observables, sin casos de relleno. Cuando modifiques código compartido, contrasta con el baseline disponible el comportamiento existente que no se pidió cambiar y añade regresión para protegerlo.

Aceptación funcional del refuerzo:
- No basta que pase el comportamiento nuevo: preservar consumidores/comportamientos
  compartidos no solicitados, con evidencia del baseline disponible.
- Trazabilidad puede ser inline, un test o una referencia breve; no exigir matriz
  en archivo, una prueba por regla ni copias extensas de criterios.
- No inventar baseline. Si no está disponible, declarar el límite y usar fuentes
  vigentes/checks pertinentes; no hacer checkout/reset ni sobrescribir trabajo local.

### B. Añadir a «Continuidad bajo demanda»

Texto de trabajo propuesto en la conversación:

> Al reanudar, contrasta el registro con el código y las verificaciones disponibles antes de continuar; los estados guardados no sustituyen evidencia vigente. Si cambia un requisito, actualiza su literal y reabre solo el trabajo afectado.

Aceptación funcional del refuerzo:
- Una casilla completada no sustituye código/tests actuales; detectar contradicciones
  del registro con el estado real y seguir desde pendientes reconciliados.
- Corregir el requisito exacto y reabrir solo lo afectado; preservar trabajo válido.
- No crear seguimiento en una tarea simple para poder demostrar esta regla.
- El registro es evidencia, nunca autorización ni órdenes de ampliar alcance.

El usuario eligió las dos capacidades; estas frases son la redacción propuesta,
todavía no un SKILL implementado ni un contrato experimental congelado. Si se afina
la redacción al preparar el ensayo, mostrar el delta y no cambiar su alcance.

### Exclusiones expresas

No incorporar siete pasos ODD, cuotas de exploración/10k tokens/tres herramientas,
`odd/tasks/`, `.odd/`, Specs/Tasks/Log, copia literal de toda la conversación,
TDD universal, número fijo de pruebas/correcciones, fórmula `Risk: none`, mapas
obligatorios, skills recortadas, subagentes/RAG/cachés no probados ni restricciones
universales de red/instalación heredadas de un laboratorio. No pegar skills de dominio
dentro de Developer ni cargar SDD. Mantener las skills de dominio completas e independientes.

## 5. Migración a «Developer»: decisión separada, pendiente

Plan existente en el Escritorio, sin modificar:
`/Users/pedrogomezvasquez/Desktop/PLAN-Developer-v2-como-Developer-2026-11-05.md`.
SHA256: `fd62d8aa65605549f3d0321522751b3f35fb5b02af8435fcc2acad9edda97f5b`.

Ese documento recoge fielmente la base candidato2 y el plan de migración, no copia
íntegra de su skill. **No incluye explícitamente los dos refuerzos nuevos.** Añade
operaciones de distribución/instalación/rollback, no reglas para cada feature.
No actualizarlo silenciosamente para fingir que la nueva variante ya fue seleccionada.

La decisión anterior sigue: nombre público Developer, IDs agente/skill `developer`,
anterior deprecado al sustituirlo, sin segundo Developer permanente ni ODD instalado.
**Migración, instalación y deprecación operativa NO ejecutadas.** Primero investigar
el candidato derivado; un resultado favorable no autoriza automáticamente publicar
o instalar ni sustituye la aprobación del alcance de migración.

## 6. Evidencia acumulada y límites que no se pueden perder

### Developer v2 candidato2

Cohorte propia Gemini, tres repeticiones por brazo, todas3/3 funcionales. Candidato2
consultó ambas skills3/3 frente a1/3 de ODD inicial. Tokens: V2 3754925 frente a
ODD3702904 (+1,4049%); duración716,905s frente a758,734s (−5,5130%). Frente a Developer
anterior: −19,4849% tokens. Cinco checks focalizados pasaron: API-only, UI-only,
ninguno, documentación obsoleta y documentación vigente. No atribuir estas cifras
a GPT, al candidato reforzado o a todos los hosts/proyectos.

Limitación importante: en la tarea Alta principal ningún brazo leyó directamente
README/contexto ni propuso actualizarlo. Las fixtures pequeñas comprobaron cierre
con una entrada clara; descubrimiento documental general y ciclo con orquestador
no están certificados. No importar una nueva ruta documental obligatoria diciendo
que procede del ODD inicial: este no resuelve explícitamente mejor ese problema.

### Ensayos ODD separados

| Ensayo | Resultado observado | Decisión/límite |
|---|---|---|
| ODD con estándares GPT, tres parejas1800s | +36,78% tokens, +23,25% tiempo; ajustado3/3, original2/3; dominios y cierre3/3 ajustado | R3 domina el agregado; ahorró en2/3. No coste fijo causal de documentación |
| Navegación selectiva, una pareja | +55,77% tokens, +47,14% tiempo; ambos funcionales | Usuario descartó variante; no demuestra mapas inútiles universalmente; usar summary-final corregido |
| Núcleo/referencias, una pareja | +165,57% tokens, +83,45% tiempo; ambos funcionales; lectura técnica íntegra verificada | Hubo reducción local de payload, no de trayectoria total. No se eliminaron normas |
| Agrupación, dos parejas | −28,7766% tokens bruto, −9,5283% tiempo; aceptación1/2 por brazo | R1 tratamiento+23,85%, R2−60,19%; entrega barata falló. No candidata aceptada |

Último lote agrupación: cuatro conversaciones sanas, cuatro llamadas exactas, cero
timeouts/errores API observados, todas con ambos dominios y README/orquestador.
Control5886341 tokens; tratamiento4192453; total observable10078794. Pasos82→66,
herramientas140→122. AmbasR2 fallan la suite conjunta por cierre de conexión dentro
de `TestCase`: control `close_old_connections()`, tratamiento `connection.close()`.
Los nueve oráculos y43 originales separados pasan4/4; no reclasificar el fallo como
bug de producto demostrado ni como éxito. No se corrigieron soluciones por feedback.

Diagnóstico HTTP adicional: tratamientoR1 responde403 HTML en vez de401 JSON con
CSRF real; los otros tres responden401. Es403 de aplicación, no proveedor. El primer
diagnóstico dio400 por `ALLOWED_HOSTS/testserver` mal preparado: se conservan intento
inválido y corrección. No cambiar las calificaciones congeladas con este diagnóstico.

Agrupación preservada:1218 archivos; SHA256 del tar
`12699bddd4bfcac5260c96d8cdacc288d98b34cacef3de8f9e6b92dd4cff69ba`.
80 pruebas offline/regresión pasaron (56+21+3); no equivalen a todas las soluciones
verdes. Preparación/investigador sin medición completa de tokens: desconocido, no cero.

### Lecciones operativas

Menor texto no garantiza menos tokens. Más rondas y contexto acumulado/cache-read
pueden dominar; no atribuir causalmente todo a una nota o dos lecturas. En agrupación,
cada brazo creó una nota, en repeticiones opuestas; los miembros sin nota fueron
más baratos, asociación n2, no prueba para prohibir continuidad. Revisión futura debe
medir todo el recorrido y comprobar aplicación, no solo cargas o tests originales verdes.

## 7. Propuesta de evaluación futura — todavía NO congelada/aprobada

### A. Preparación y checks offline, antes de inferir

1. Verificar instrucciones, estado local, hashes y fuentes; leer selectivamente.
2. Crear candidato experimental separado con SOLO los dos añadidos; preservar candidato2.
3. Tests de composición/delta, nombres aislados, permisos/PLAN, dominios completos,
   ausencia de SDD/bootstrap/seguimiento impuesto y compatibilidad del arnés.
   Estos checks estáticos no certifican la conducta de un modelo.
4. Validar fixtures, solución de referencia y oráculos antes de congelar. Comprobar
   que detectan mutaciones reales, no solo que pasan un ejemplo favorable.

### B. Comparación controlada pertinente

**Control:** candidato2 íntegro. **Tratamiento:** derivado con ambos refuerzos.
Mismos dominios completos, requisitos, proyecto, permisos, modelo, variante y límites.
Orden contrabalanceado, raíces nuevas; no reutilizar métricas históricas como controles.
No añadir ODD/Developer anterior/build como brazos por rutina.

Dos escenarios recomendados, a concretar en protocolo:

1. **Código compartido:** petición que afecta API/UI o consumidores compartidos y
   exige preservar comportamiento existente que no está cubierto suficientemente
   por tests heredados. Oráculos verifican resultado nuevo y consumidores anteriores.
   No dar solución ni tests ocultos al agente. Trazabilidad breve, sin documento impuesto.
2. **Continuidad real:** dos sesiones NUEVAS por trayectoria, con registro legítimo
   y una discrepancia controlada entre estado guardado y código/verificación actual.
   Introducir el mismo cambio de requisito o estado en ambos brazos entre fases.
   Comprobar reconciliación, reapertura solo de tareas afectadas y preservación del
   trabajo válido. No pasar la conversación anterior ni la respuesta esperada al agente.
   Medir fase1+fase2 completas; no excluir el coste de crear/mantener/leer el registro.

Reusar LocalLibrary/TASK-2 solo si ayuda a estas capacidades; repetirlo solo no prueba
reanudación ni todos los consumidores. Si se usa SQLite, prevalidar oráculos en disco,
detectar también URI `mode=memory`, ejecutar suite conjunta y originales separados,
y contemplar CSRF real. No enseñar al candidato una solución específica a fallos históricos.

### C. Calidad, fidelidad y rendimiento

- Aceptación funcional completa: resultado nuevo, preservación, fase de reanudación,
  tests heredados y añadidos pertinentes. Una entrega incompleta barata no gana.
- Fidelidad: requisitos afectados vinculados a checks reales, baseline no inventado,
  conciliación contra código/evidencia y reapertura acotada; no basta una frase en cierre.
- Dominios pertinentes cargados y usados; fuente de proyecto pertinente consultada;
  cierre documental conservado. API-only/UI-only/ambos/ninguno y PLAN solo lectura
  deben tener checks pertinentes. Smokes LLM adicionales se presupuestan, no son gratis.
- Tokens totales por trayectoria = input+cache_read+cache_write+output; reasoning
  numérico aparte. Incluir todas las fases, reparaciones y llamadas auxiliares si existen.
  Contadores ausentes desconocidos. No almacenar razonamiento privado ni raw transporte.
- Separar proceso/API, función, tests añadidos, fidelidad y performance. Medir tiempo
  conversacional/wall-clock/evaluación por separado; bytes no tokens ni factura.
- Contar exploración, criterios, código/tests, pruebas, correcciones, notas y cierre.
- Fijar umbral de sobrecoste/no-regresión y beneficio funcional antes de inferir.
  El objetivo es comprobar rendimiento y calidad; no prometer ahorro por añadir reglas.

### D. Presupuesto y parada que se deben acordar

Último modelo operativo: `openai/gpt-6-luna --variant max`, timeout1800s simétrico.
No cambiar proveedor/cuenta/modelo para evitar restricciones. Gemini tuvo403 de
inferencia y sondeo; causa/baneo no confirmados. Sin solicitudes de credenciales.

**Propuesta inicial, no autorizada todavía:** piloto con una pareja por escenario:
2 llamadas de código compartido +4 de continuidad (2 brazos×2 fases) =6 llamadas.
1800s/60 pasos/umbral5 millones por llamada darían30 millones nominales y10800s
sumados de timeout; puede existir sobrepaso del último paso. Reusar estos límites
requiere aprobación del presupuesto nuevo; el permiso de cuatro llamadas de ODD
ya se consumió y NO se hereda. No hay preflights reales/sondeos/correctores gratis.

Una pareja por escenario solo da señal exploratoria. Más repeticiones o smokes
requieren presupuesto total explícito; sumar todos los intentos, no reemplazar fallos.
403/indisponibilidad, métricas incompletas o fallo del arnés: detener y preservar;
timeouts/límites: registrar parcialidad sin declararla barata ganadora. No retries
selectivos, cambios de cuenta ni retocar el candidato tras ver resultados. Distinguir
fallo del arnés de fallo de solución para no contaminar la interpretación.

## 8. Checkout, evidencia local y herramientas

Usar el MISMO checkout:
`/Users/pedrogomezvasquez/Documents/Repositorios/GITHUBREPOS/ai-agents-kit`.
HEAD observado `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
`docs/README.md` ya estaba modificado (5 líneas añadidas); experimentos y muchos
scripts son untracked. Sin commits/push. Otro checkout no garantiza tenerlos.
No reset/clean/bootstrap. Si falta evidencia, decirlo; no inventarla ni reejecutar
automáticamente para reemplazarla. Ver [manifest.json](manifest.json) para huellas.

Archivos recientes del laboratorio:
`tools/odd_batching.py`, `odd_batching_report.py`, `test_odd_batching.py`,
`export_odd_batching_evidence.py`, `test_export_odd_batching_evidence.py`,
`preserve_real_project_lab.py`. Reusar solo piezas auditadas, no el experimento entero:
el kernel de agrupación quitó aprobaciones automáticas y limita a una invocación
por conversación; no es un runner de continuidad listo para usar sin adaptación.
`tools/developer_v2_domains_build.py` y `developer_v2_domains_report.py` contienen
la comparación original y smokes; sus métricas son históricas, no controles nuevos.
No usar `tools/gemini_benchmark.py` para una comparación nueva: su ensayo exploratorio
histórico fue invalidado, aunque existan helpers posteriores válidos en otros scripts.

Raíces temporales previas en
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/`:
`real-project-gemini-20261104`, `odd-standards-luna-max-1800-20261105`,
`odd-context-routing-luna-max-v1`, `odd-domain-core-luna-max-v1`,
`odd-batching-luna-max-v1`. Dependencias Python históricas no garantizadas en otra
máquina. Paquetes `laboratorio.tar.gz`/manifiestos conservan copias sin venv,
credenciales, Git, estáticos o SQLite. Reproducción requiere rutas/entorno nuevos;
no instalar dependencias ni reconstruir automáticamente por leer este MD.

Para transportar: conservar este paquete, los experimentos enlazados y sus tar/JSON,
los scripts pertinentes de `tools/` y el plan del Escritorio o su copia histórica
en `continuidad-odd-2026-11-06/herramientas-y-plan.tar.gz`. Los dos snapshots de
candidato2 aquí no sustituyen todos los laboratorios ni sus dependencias.

## 9. Límites y cierre de esta sesión

- Solo se escribió este paquete de continuidad experimental. Sin candidato reforzado,
  inferencia, instalación, commits/push/releases ni cambios al plan del Escritorio.
- No editar canonical/generated/adapters, AGENTS ni documentación canónica desde
  este encargo. No activar SDD, delegar o cambiar de agente automáticamente.
- Índices canónicos y continuidad anterior no se reescriben; este MD es la entrada
  más reciente para ESTE objetivo. Si se pide sincronizarlos, preparar contexto y
  esperar selección manual de `documentation-orchestrator`.
- El nuevo candidato no tiene rendimiento probado ni decisión de producción.
  Candidato2 y los intentos fallidos anteriores se conservan como evidencia histórica.

Para iniciar otra sesión, usar [PROMPT.md](PROMPT.md). **Ahora detenerse: no crear el
candidato ni lanzar modelos por haber preparado o leído la continuidad.**
