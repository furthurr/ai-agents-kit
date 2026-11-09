# Resultados, fidelidad y límites

[Informe y decisión](README.md) · [Protocolo](protocolo.md) ·
[Reproducción](reproduccion.md)

## Ejecución

Baseline MAS: `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
Gentle AI: `3ea08cdfbdce671053c82377a4365915799abe57`.
Modelo `openai/gpt-6.1-sol`, OpenCode 1.18.34, temperatura 0.2.
La fecha exacta está en [congelacion.json](evidencia/congelacion.json), anterior
a las celdas v2. Sus 103 hashes permanecieron intactos durante los lotes y al cierre.

La afirmación anterior describe la verificación histórica del lote GPT, no el
estado actual de los scripts. El runner se modificó más tarde durante Gemini;
la discrepancia y los límites de reproducción se documentan en
[reproducción](reproduccion.md#advertencia-sobre-el-runner-actual). Los JSON
históricos y sus hashes no se recalcularon ni sobrescribieron al archivar.

Se registran 60 celdas distintas, un intento por celda, sin reejecuciones
selectivas. A necesitó 45 invocaciones y B 30; las quince adicionales de A son
respuestas simuladas de gates, no reintentos. No hubo timeouts del runner.
S08-A-r3 supera 240 s agregados porque suma dos invocaciones dentro de sus límites.

## Aceptación por escenario

| Caso | A | B | Evidencia/observación |
|---|---|---|---|
| S01 documento | 3/3 | 3/3 | Solo errata autorizada, sin tests nuevos. |
| S02 función pura | 3/3 | 3/3 | Caja, whitespace, Unicode y fallback. |
| S03 etiquetas | 3/3 | 3/3 | Reglas, límite, errores exactos y entrada intacta. |
| S04 monetario | 3/3 | 3/3 | Decimal, redondeo final, negativos y legado. |
| S05 CLI | 3/3 | 3/3 | Opción local, hermana rechaza; salida/error/exit preservados. |
| S06 literalidad | 3/3 | 3/3 | Mensajes/orden/Unicode y validación de filas ocultas. |
| S07 persistencia | 3/3 | 3/3 | Bytes intactos ante rechazo/fallo replace, orden y limpieza. |
| S08 reanudar | 3 artefactos válidos; 2 ejecuciones completas | 3/3 | A-r3 pasó tests y actualizó spec, pero API interrumpió respuesta/cierre. |
| S09 planificar | 3 planes válidos; 2 ejecuciones completas | 3/3 | A-r3 escribió spec antes del error; producto intacto. |
| S10 consulta | 2/3, r3 sin respuesta | 2/3, r3 sin respuesta | Fallo de cuota; ninguna escritura ni sentinel. |

La aceptación automática de artefactos da **29/30 por brazo**, que no equivale
a 29 ejecuciones completas: A tuvo tres errores de proceso y B uno. Total:
**56 ejecuciones sin error, dos parciales con artefacto válido y dos sin respuesta**.
No atribuir los cuatro errores API a defectos de implementación.

Las 42 celdas de comportamiento pasan suite final y oráculo externo. También se
ejecutaron las 42 suites originales, sin modificar su código de test, contra
las implementaciones finales: todas pasan. Las seis correcciones documentales,
seis planes y seis consultas se evalúan estructuralmente; una suite vacía no es
prueba funcional. En S10-r3 conservar archivos no basta: faltó el diagnóstico.

## Eficiencia comparable: repeticiones completas

Se informa el bloque temporal completo r1+r2, no una selección de escenarios
favorables. Es descriptivo: la promoción requiere las tres repeticiones completas.

| Repetición | Tokens A | Tokens B | Duración A | Duración B |
|---|---:|---:|---:|---:|
| 1 | 3.446.214 | 967.180 | 1.165,168 s | 631,933 s |
| 2 | 3.466.915 | 945.229 | 1.129,144 s | 601,620 s |
| **Total comparable** | **6.913.129** | **1.912.409** | **2.294,312 s** | **1.233,553 s** |

B: **−72,337 % tokens**, **−46,234 % duración**, 241 frente a 423 herramientas y
216 frente a 316 pasos. Dirección favorable de tokens/tiempo en ambas repeticiones
y en los diez escenarios agregados de r1+r2.

Tokens comparables: input + cache-read + cache-write + output. Reasoning se
mantiene separado porque podría estar incluido en output. La caché del proveedor
no se reinició. Duración sumada de celdas concurrentes, no wall-clock ni latencia
humana. La evaluación externa posterior queda fuera; los tests del agente sí cuentan.

## Todas las celdas: observaciones incompletas

[metricas.json](evidencia/metricas.json) conserva todos los intentos y su cobertura:
A observó 10.109.495 tokens y B 2.735.788; duraciones 3.627,768 s y 1.876,593 s.
**No usar sus porcentajes como ahorro de trabajo completo**: S10-A-r3 no tiene
métricas y otras tres celdas tienen ejecuciones parciales. Contador ausente es
desconocido, no cero; el sumador solo agrega contadores que llegaron del host.

| Contador observado en todo el lote | A | B |
|---|---:|---:|
| Input | 886.952 | 492.946 |
| Cache-read | 9.123.456 | 2.197.504 |
| Cache-write | 0 | 0 |
| Output | 99.087 | 45.338 |
| Reasoning, separado | 2.046 | 1.978 |

Coste reportado cero en los pasos observados no acredita facturación cero ni cubre
todo consumo auxiliar, preflights o respuestas perdidas por errores del proveedor.

## Fidelidad y controles

- Tratamiento correcto cargado en 59/60 celdas: S10-A-r3 falló antes de cargar.
  Se contrastó contenido, no solo el nombre de la skill.
- Sin diferencias de perfil ajenas al agente/skill sustituido y las rutas
  temporales de config. El resto del MAS coincide por hashes.
- 463 llamadas de lectura/búsqueda con rutas observables, ninguna fuera del
  fixture/perfil del brazo; sin llamadas a herramientas de red o delegación.
  Esto no convierte Python arbitrario ni permisos del host en sandbox OS.
- Sin cambios de producto antes de Gate 3 ni marcadores de Gate 4 aprobado
  anticipadamente en Tiny. S08-A-r3 dejó cierre pendiente; el usuario simulado
  aprobó después, pero la API impidió aplicar ese cierre.
- A conserva 48 documentos de spec/verificación, contando el sembrado de
  reanudación; B tres, todos de reanudación. Sus planes inline están en respuestas.
  El número de documentos no es calidad por sí mismo.
- B observa RED antes de editar producto y GREEN en las 21 celdas de comportamiento.
  A lo hizo en doce, sin obligación general de test-first. No hubo diferencia de
  calidad funcional que permita atribuir superioridad a esta regla.
- Los planes S09 cubren trim, vacíos, deduplicación ordenada, TypeError y pruebas
  propuestas, sin implementación ni pruebas presentadas como ya realizadas.
- Cuatro alertas AST son cambios sintácticos de assertions, no cuatro pruebas
  debilitadas: por ejemplo `p` pasó a `self.path` al organizar tests. La ejecución
  del código original de tests y los oráculos comprueban preservación aparte.

## Incidentes del evaluador

1. Antes del A/B, frontmatter prevalecía sobre permisos del perfil. Se corrigió
   con merge final `OPENCODE_CONFIG_CONTENT`, comprobando resolución y carga real.
2. `debug skill` masivo no era JSON íntegro. Se guardan tamaño/hash, no se usa
   como inventario válido: se contrastan archivos y cargas reales.
3. v1 abortó tras cuatro celdas por hash de paquetes auxiliares creados por el
   host y por confundir unittest vacío con fallo. Se conserva
   [incidente-v1.json](evidencia/incidente-v1.json). v2 corrige controles, no B,
   fixtures u oráculos; mismo baseline. Ya se habían visto cuatro salidas del
   piloto: v2 no fue una evaluación completamente ciega desde cero.
4. El auditor posterior exigía inicialmente `requirements.md` aun en bugfix Lite,
   donde `bugfix.md` es válido, y confundía «no cerrado» con cierre anticipado.
   Se corrigieron filtros, sin tocar agentes, celdas, artefactos ni criterios
   funcionales congelados. El auditor no se presenta como prerregistrado.
5. Cuota agotada en S08-A-r3, S09-A-r3, S10-A-r3 y S10-B-r3: cinco eventos API 429
   en cuatro celdas. Se preservan [errores tipados](evidencia/errores-proveedor.json).
   Se retiraron headers, cuerpos y metadata opaca de errores; el recibo conserva
   hashes antes/después sin esos valores. No cambió ninguna métrica ni entrada.
   No se cambió proveedor/modelo ni se sobrescribieron celdas.

## Interpretación y decisión

**Exploración Gemini:** su reporte inicial de ahorro queda rectificado como
no inferencial por contaminación posible de skill/agente, cambios de configuración
y selección de éxitos. Véase [el anexo corregido](gemini-flash.md). No se incorpora
a las tablas GPT ni al suplemento y no acredita una segunda familia validada.

**Actualización posterior:** el [suplemento por pares](suplemento.md) terminó
6/6 celdas con éxito para S08–S10 y volvió a favorecer a B en eficiencia. Es
evidencia adicional, no reemplaza los cuatro intentos afectados ni convierte la
tercera repetición original en completa. El análisis y las tablas siguientes
siguen describiendo exclusivamente el lote v2 original.

La evidencia **favorece B en eficiencia bajo las condiciones probadas**; no
demuestra calidad superior ni equivalencia universal. La repetición incompleta
impide satisfacer promoción: **no promover todavía**, sin rechazo técnico de ODD.

Los modos de A estaban preseleccionados. S03 recibió nota 2 y recomendación
Direct, pero conservó Tiny por elección explícita. No se midió elección natural
de profundidad. Longitud de instrucciones, ceremonia documental y gates varían
junto con el método: sus efectos no se separan ni se atribuyen a una regla aislada.

Otros límites: un modelo/host, escenarios sintéticos cortos, efecto techo, sin
revisor ciego, sin otras plataformas, Engram/RDD, commits ni topología nativa.
S08 usa sesión nueva con estado sembrado, no pérdida de contexto real ni
compactación. Los fixtures no tienen commit base: `git diff` no compara archivos
iniciales untracked; el diferencial histórico de ODD no quedó evaluado. Se
comprobó preservación mediante oráculos y tests originales.

Confirmación justificable: nuevo protocolo con cuota suficiente, elección natural
de profundidad y tareas reales de mayor incertidumbre. No sobrescribir v2 ni
aceptar una regla parcial a partir de filas favorables.

La petición posterior del usuario fue conservar el registro y preparar un plan
para un agente ODD separado. Eso permite planificar un piloto opt-in; no cambia
la decisión experimental, no autoriza implementar el agente y no certifica las
reglas individuales del tratamiento B. Developer y SDD siguen vigentes.

## Procedencia y cierre

[Ledger](evidencia/celdas.json): métricas, salidas, aprobaciones simuladas,
errores tipados y archivos finales. [Auditoría](evidencia/auditoria.json): comandos
y pruebas originales ejecutadas. [Preflight](evidencia/preflight.json) y
[procedencia](evidencia/procedencia.json): configuración, hashes del auditor y
trazas externas. No se conserva razonamiento privado.

La carpeta temporal externa no es portable y su permanencia no está garantizada.
Las entradas y snapshots permiten reconstruir implementaciones, pero el repo no
contiene cada evento de herramienta. Los lotes finalizaron; cuota es un límite
de prueba, no una aprobación tácita de cierre. No se activó B en el MAS.

Verificaciones de la entrega:

| Comando/control | Resultado |
|---|---|
| `python3 tools/validate.py` | Correcto: 11 skills, 5 agentes, 6 plataformas. |
| `python3 tools/test_sdd_contract.py` | 762/762 comprobaciones correctas. |
| `python3 tools/check_links.py` | Correcto: 103 Markdown revisados al cierre. |
| `python3 -m py_compile tools/odd_vs_sdd_experiment.py tools/odd_vs_sdd_audit.py` | Correcto. |
| `git diff --check` | Correcto. |
| Auditoría final | 103 hashes intactos; 60 celdas únicas; errores y cobertura registrados. |
| Procesos de filtro/replicación | Finalizados; PIDs ya ausentes al cierre. |
| `AGENTS.md` raíz | Sin cambios: guía e índices existentes cubren esta documentación. |

Archivos añadidos: este paquete documental, sus JSON de evidencia y los dos
scripts experimentales en `tools/`. Se añadió la entrada correspondiente a
`docs/README.md`, preservando la entrada Ponytail y su trabajo documental previo.
Sin commits ni cambios en `canonical/`, `adapters/` o `generated/`.

### Verificación al consolidar el registro histórico

Tras la petición de archivo y planificación ODD, se rectificó el anexo Gemini y
se añadió la advertencia de deriva del runner sin editar el protocolo congelado,
el tratamiento B, los JSON históricos o los scripts experimentales. Las entradas
del paquete siguen siendo README, protocolo y resultados, con anexos conservados.

`python3 tools/check_links.py`: 105 Markdown correctos;
`python3 tools/validate.py`: 11 skills, 5 agentes, 6 plataformas correctos;
`git diff --check`: correcto. Son comprobaciones documentales/distribución, no
una nueva ejecución de modelos ni reevaluación de los resultados del experimento.
El plan de creación de ODD se entregó como Markdown externo en el Escritorio;
no es una definición canónica ni se instala con el kit.
