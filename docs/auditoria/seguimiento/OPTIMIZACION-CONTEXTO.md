# Seguimiento — optimización de contexto y coste por flujo

- **Estado general:** fuentes y distribuciones generadas implementadas y validadas; runtime/medición real pendiente donde se indica.
- **Alcance recurrente:** REC-09, REC-10, REC-11, REC-12, REC-13, REC-14, REC-15, REC-16 y REC-17.
- **Backlog relacionado:** FUT-02, FUT-04, FUT-05, FUT-08, FUT-11 y FUT-14.
- **Principio de medición:** volumen de archivos/texto no equivale a tokens reales de una conversación. No se registran ahorros tokenizados ni porcentajes sin lectura de usage del host.

## Cambios y evidencia

| ID | Cambio realizado | Evidencia/estado | Límite abierto |
|---|---|---|---|
| REC-09 | Añadidos `canonical/shared/mas-identity.md` y `project-context.md`; renderer los inserta como fragmentos compactos. Git/release deja de cargar contexto de arquitectura/Navigator. | `tools/test_mas_identity.py`, `tools/test_documentation_core.py`, fixture de renderer, `validate.py` y paridad de seis plataformas pasan. | Los fragmentos se insertan donde se necesitan como artifacts autónomos; no son carga global automática. |
| REC-10 | Descripciones canónicas y los seis descriptores del orquestador precisan operación y destino. Graphify global se activa para su propio pipeline/grafo; se quitó el metadato `trigger` no soportado. | `tools/test_context_efficiency.py` valida límites de descripciones del kit; frontmatter global revisado en la máquina actual. | Las tasas de activación positiva/falsa requieren smokes del host; se vinculan a REC-08. La skill global requiere reiniciar OpenCode para cargar su nueva descripción. |
| REC-11 | Los tests ya no exigen MASVS/MASWE/MASTG en toda skill; valida fragmento común y conserva identidad específica de seguridad. | `test_mas_identity.py` 235/235 después de render. | Ninguno de distribución. |
| REC-12 | `code-quality` y `security` piden una aprobación para diffs atómicos/reversibles y mantienen micro-pasos estructurales; Code Review remite a la regla de skill. | `test_code_review_contract.py` 7/7; `test_context_efficiency.py` incluye contrato. | No se cuantifican turnos ahorrados. Smoke de interacción real no ejecutado; confirmaciones Git/release permanecen independientes. |
| REC-13 | SDD carga una referencia/fragmento pertinente una vez y reutiliza su contenido; evita lecturas duplicadas sin fusionar referencias bajo demanda. | `test_sdd_contract.py` 613/613; enlaces y paridad de referencias pasan. | Número real de lecturas/latencia no se midió en un smoke SDD; la consolidación 10→4 se descartó porque podría cargar módulos mayores de los necesarios. |
| REC-14 | Agent SDD remite al procedimiento en `sdd-spec`; skill compacta tratamiento nuevo/histórico; testing conserva estrategia normativa. | `test_sdd_contract.py` 613/613, render/validate correctos. | Ninguno de texto/distribución. |
| REC-15 | Eliminadas tablas de tipos, clasificación por extensión, comandos y troubleshooting genérico; reglas propias del kit preservadas. | `test_secret_policy.py` 26/26, test de contexto 9/9, render/validate correctos. | Ahorro reportado como volumen fuente, no tokenizer específico. |
| REC-16 | `measure_context.py` acepta solo archivos observados y compara volumen con ref Git. | `test_measure_context.py` 5/5; ejemplos generados por OpenCode abajo. | Métricas son proxy estático, no usage real, interacciones, tiempo o calidad; requiere host con contador de tokens para cerrar la medición empírica. |
| REC-17 | Topes/fórmula caracteres→tokens sustituidos por pautas de contenido y lectura ampliable. | `test_context_efficiency.py` 9/9, validate/render y búsqueda canónica. | El número de tokens reales no se infiere de estos límites. |
| FUT-02 | El adaptador Claude de Git/release ya no precarga ambas skills; `Skill` permite cargar la que aplica. | JSON del adaptador; test incluido en `tools/test_context_efficiency.py`. | Runtime Claude pendiente por disponibilidad de CLI/sesión; regeneración. |
| FUT-04 | Navigator usa un presupuesto inicial ampliable y deja de limitar por cantidades rígidas de archivos/capas. | `SKILL.md` y `references/layers.md`. | Medir el comportamiento en consultas transversales reales; puede leer más si lo requiere la evidencia. |
| FUT-05 | El orquestador continúa ramas independientes ya autorizadas cuando otra se bloquea; solicita decisión si cambian dependencias, alcance o autorización. | Skill/workflow canónico y contrato en `tools/test_context_efficiency.py`. | Runtime de flujo del orquestador pendiente de REC-08. |
| FUT-08 | La skill global Graphify perdió `trigger` y la descripción general; ahora se limita a construir/consultar `graphify-out` y grafos/exportes. | `.config/opencode/skills/graphify/SKILL.md` local revisado; el campo ausente verificado. | Cambio local no versionado en el repo. Reiniciar OpenCode para recargar metadatos. |
| FUT-11 | Investigación de releases no soportadas limitada a caché y dos fuentes oficiales para la petición activa; no abrir búsqueda general. Actualizado el skill canónico y el local. | Canonical, skill global y `technologies/README.md` local. | Cambio del skill global no versionado y requiere reinicio de OpenCode; no se ha medido uso real de fuentes/tokens. |
| FUT-14 | No vigente: Navigator, arquitectura, catálogo y guía de uso actuales muestran seis plataformas, tres profundidades y responsabilidades UI/Data correctas. | Contraste de `.navigator/ai-context.md`, `.architecture/README.md`, `docs/catalogo.md` y `docs/uso.md`. Historial/specs antiguas conservados. | Reabrir si el contexto operativo diverge de las fuentes actuales. |

## Volumen de texto medido (proxy, no tokens)

Medición del texto canónico actual frente a `HEAD` anterior, incluyendo archivos de agente/skill y referencia cuando se especifica. **No es una lectura del contexto real inyectado por un host ni un token count.** Los fragmentos compartidos se inyectan al render y deben medirse sobre `generated/` después de regenerar.

| Flujo de fuentes | Archivos medidos | Bytes actuales / Δ vs HEAD | Palabras actuales / Δ vs HEAD |
|---|---|---:|---:|
| Git commit en OpenCode | agente/skill `generated` | 14,178 / −3,390¹ | 2,039 / −493¹ |
| SDD scope en OpenCode | agente, skill y `scope-depth` `generated` | 32,193 / −2,147¹ | 4,544 / −276¹ |

¹ Volumen estático de artefactos renderizados seleccionados frente a sus blobs en `HEAD`; lista explícita de fuentes, no historial observado de carga. Es una proxy textual, no token count ni ahorro porcentual de uso real.

## Verificación complementaria pendiente

La verificación del build actual pasó después de integrar Navigator/contexto. Para cerrar la medición empírica, queda:

1. Medir activaciones de REC-10, approvals REC-12 y lecturas REC-13 en hosts con instrumentación, si se pretende afirmar mejoras de comportamiento/latencia.
2. Medir tokens, turnos, tiempo y calidad en flujos comparables con y sin skill; declarar `no disponible` cuando el host no exponga el contador.
3. Actualizar REC/FUT según evidencia; no afirmar ahorro de tokens por reducción de palabras sin tokenizer/usage real.

## Verificación en esta sesión

| Comando | Resultado | Interpretación |
|---|---|---|
| `python3 -B tools/test_context_efficiency.py` | 9/9 | Contratos estáticos de fragmentos, triggers, approvals, referencias, Git y budgets. |
| `python3 -B tools/test_measure_context.py` | 5/5 | Métricas por fuentes explícitas, baseline y rechazo de paths/symlinks no permitidos. |
| `python3 -B tools/test_code_review_contract.py` | 7/7 | Contratos Code Review, incluidas aprobaciones de remediación. |
| `python3 -B tools/test_validate.py` | 40/40 | Renderer/validador, incluido un fixture de fragmentos compartidos. |
| `python3 -B tools/test_sdd_contract.py` | 613/613 | Contratos y paridad SDD en seis plataformas. |
| `python3 -B tools/test_documentation_core.py` | 15/15 | Contratos y referencias generadas coinciden con el estado final coordinado. |
| `python3 -B tools/test_mas_identity.py` | 235/235 | Identidad compacta renderizada en seis plataformas. |

No se hicieron commits ni push. Los cambios globales de OpenCode son locales; reiniciar OpenCode para que recargue las descripciones modificadas.
