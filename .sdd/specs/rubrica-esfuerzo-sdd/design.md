# Diseño — Compactación del contexto operativo SDD

- **Modo SDD:** standard
- **Fase:** Design
- **Estado:** aprobada; iteración de compactación cerrada
- **Gate 1 de esta iteración:** aprobado («procede»)
- **Gate 2 de esta iteración:** aprobado por el usuario («procede»)
- **Gate 3 de esta iteración:** aprobado por el usuario («procede»)
- **Gate 4 de compactación:** aprobado por el usuario («procede»)
- **Próxima operación:** ninguna; iteración cerrada

## 1. Decisiones y límites

R01–R22 conservan el contrato de la rúbrica; R23–R28 añaden eficiencia de contexto.
El diseño inicial se conserva en `design-initial.md` como evidencia histórica,
no como lectura requerida para implementar esta iteración.

Se mantiene la arquitectura canonical → adapters → generated y el harness Python.
No se introducen motor de scoring, nuevas dependencias, DTOs, configuración global
o políticas operativas. La optimización afecta a SDD, no al resto del catálogo.

La referencia operativa permanece en
`canonical/skills/sdd-spec/references/feature-level.md`. Reducirla no significa
trasladar sus garantías esenciales a documentos que SDD deba abrir después.

## 2. Distribución del contenido

| Capa | Contenido que conserva | Contenido que se elimina o delega |
|---|---|---|
| Agente `canonical/agents/sdd.md` | Exclusividad, alcance de feature y delegación con etiqueta `Esfuerzo previsto del LLM` | Detalles de escala, cuatro campos, ejemplos y explicación repetida de 10+; la referencia define su contrato. |
| Skill `canonical/skills/sdd-spec/SKILL.md` | Cuándo consultar/emisión por modo; alcance definido, no repetición y no gate adicional | Repetición de anclas, iconos, cuatro campos y protocolo detallado; remisión a la referencia. |
| Referencia operativa | Dimensiones, diez perfiles, scaffold relevante, comparación ordinal, 10+, bloque de cuatro campos, separación de conceptos y resultado parcial X13 | Tabla exhaustiva de once presentaciones, casos largos y catálogo detallado de procedencia. |
| Plantillas | Cuatro campos utilizables en standard/lite y referencia de formato | No se añade respaldo ni otra escala. Si no hay duplicación prescindible, se mantienen sin aumento. |
| Respaldo `docs/sdd-effort-examples.md` | Ejemplos exhaustivos, contrastes sintéticos y procedencia detallada de ReserveLab | No instruye lectura automática; no es necesario para aplicar la rúbrica instalada. |

La referencia retendrá un contraste **breve** F10 proporcionado≈8 frente a construir
su coordinación/participantes≈9 y un ejemplo concreto superior a X13. Esos casos
son necesarios para razonar sobre reutilización y exceso; el desarrollo largo
queda en respaldo. También conserva F07 verde sin habilitar lite.

El matiz histórico queda en una síntesis operativa: Luna/MAX, 10/11 familias,
C12 válido, fallo admin_create y ausencia de éxito completo/frontera universal.
La procedencia y naturaleza suplementaria post-hoc se pueden desarrollar en respaldo
sin quitar su aclaración esencial del núcleo.

Los consumidores mantienen el descubrimiento de la referencia existente. Ningún
prompt ordenará abrir el documento de respaldo para puntuar. Los seis hosts reciben
una rúbrica autosuficiente aunque `docs/` y `.agent-lab` no estén instalados.

## 3. Pruebas sin dependencia de prosa extensa

Se reutilizan `tools/test_sdd_contract.py` y `tools/test_model_recommendations.py`.
Los checks de tablas de perfiles y anclas se mantienen sobre **canonical**, no
solo sobre los ejemplos trasladados. Presentaciones/casos exhaustivos se inspeccionan
en el respaldo; sus controles negativos seguirán detectando las mutaciones pertinentes.

Los checks distinguirán ambas responsabilidades:

- **Contrato operativo:** diez perfiles/anclas, límites/iconos, cuatro campos,
  comparación y contraste de scaffold, 10+ explicado, separación de lite y matiz X13.
- **Ejemplos y procedencia:** coherencia con la escala y contraste sintético,
  sin afirmar inferencias de modelos ni importar el laboratorio.
- **Consumidores:** agente/skill delegan y no duplican el contrato; exclusividad,
  modos/gates/routing intactos; referencia y plantillas distribuidas idénticas.

La inspección de secciones/tablas se adapta a su responsabilidad, sin obligar a
conservar las frases largas de los casos en el prompt operativo. Las anclas y notas
esperadas siguen siendo expectativas explícitas independientes; no se crea scorer.
Se actualizan enlaces de docs activos al respaldo cuando ayuden, sin una lectura nueva
obligatoria. La enumeración de ejemplos no se presenta como prueba del razonamiento.

## 4. Medición y aceptación

Se reutiliza el baseline exacto de Requirements: agente 1.066 palabras/7.580
caracteres; skill 2.357/16.378; referencia 1.774/12.303; plantillas 863/5.722.
Los conteos usan texto Unicode y palabras por whitespace, con el mismo método.

Antes/después debe mostrar reducción en cada uno de agente, skill y referencia;
plantillas no aumentarán. Se reportan estos escenarios sin sumar seis distribuciones:

1. Agente + skill: contexto inicial cuando ambos se cargan.
2. Agente + skill + rúbrica: evaluación de una feature.
3. Los anteriores + plantillas: planificación cuando también se consultan.

Cualquier lectura **obligatoria** añadida se contabiliza en su escenario. El respaldo
opcional se cuantifica aparte; no se vende una reducción del inventario total como
ahorro de ejecución, ni inventario de archivos como telemetría de carga real.
No hay cuota porcentual, tokenizer nuevo ni estimación de costo facturado.

Checks de eficiencia pequeños en la suite existente contrastarán palabras y
caracteres con el baseline. Son guardas de no crecimiento, no pruebas suficientes
de claridad/utilidad: la revisión cualitativa de R01–R22 sigue siendo obligatoria.

## 5. Estrategia y trazabilidad

Regresión/caracterización del contrato existente. TDD focalizado de organización y
eficiencia: primero checks con consumidores todavía extensos → RED por crecimiento
o duplicación/respaldo ausente → compactación correcta y render → GREEN. Los checks
de comportamiento previo no se reclasifican falsamente como TDD nuevo.

| Decisión | Archivos | Requisitos |
|---|---|---|
| Delegación y reducción inicial | Agente y SKILL.md | R14, R16–R17, R23–R24 |
| Núcleo autosuficiente compacto | feature-level.md | R01–R18, R21, R23–R25 |
| Respaldo opcional, sin lectura equivalente | docs/sdd-effort-examples.md y enlaces pertinentes | R08–R13, R18–R19, R22, R25 |
| Checks por responsabilidad y eficiencia | Ambas suites existentes | R06–R22, R26–R27 |
| Render y verificación de seis plataformas | generated vía renderer existente | R19–R21, R28 |

## 6. Invariantes, RNF y quality bar

1. Se conserva el contrato R01–R22, incluidas todas las anclas y 10+.
2. Reducir el núcleo no crea una lectura obligatoria de respaldo equivalente.
3. Agente, skill y referencia disminuyen; plantillas no absorben el ahorro.
4. Generated refleja canonical; políticas, historia y cambios ajenos intactos.
5. Conteos textuales no se presentan como tokens/facturación o conducta de un LLM.

Se mantienen RNF-1–RNF-5 del diseño inicial: autosuficiencia, paridad en seis
plataformas, políticas intactas, preservación y stdlib compatible con Python 3.10.
**RNF-6:** reducción verificable en cada fuente operativa, sin nueva lectura obligatoria;
se comprueba con conteos y auditoría de instrucciones de carga. El self-check
prioriza cinco RNF (1–4 y 6); RNF-5 se conserva mediante regresión de compatibilidad
y dependencias, sin crear garantías nuevas de runtime.

Quality bar proporcional: separación de fuentes y reutilización; sin capas, DI,
persistencia o singletons nuevos. Helpers locales tipados y sin catches vacíos;
sin motores ficticios, PBT o dependencias anticipadas. Verification registra
regresión, RED/GREEN nuevos, mediciones y límites, sin cerrar Gate 4 automáticamente.
