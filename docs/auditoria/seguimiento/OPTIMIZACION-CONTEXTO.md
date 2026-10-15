# Seguimiento — optimización de contexto y coste por flujo

- **Estado general:** fuentes y distribuciones generadas implementadas y validadas; runtime/medición real pendiente donde se indica.
- **Alcance recurrente:** REC-09, REC-10, REC-11, REC-12, REC-13, REC-14, REC-15, REC-16 y REC-17.
- **Backlog relacionado:** FUT-02, FUT-04, FUT-05, FUT-08, FUT-11 y FUT-14.
- **Principio de medición:** volumen de archivos/texto no equivale a tokens reales de una conversación. No se registran ahorros tokenizados ni porcentajes sin lectura de usage del host.

## Cambios y evidencia

| ID | Cambio realizado | Evidencia/estado | Límite abierto |
|---|---|---|---|
| REC-09 | Añadidos `canonical/shared/mas-identity.md` y `project-context.md`; renderer los inserta como fragmentos compactos. Git/release deja de cargar contexto de arquitectura/Navigator. | `tools/test_mas_identity.py`, `tools/test_documentation_core.py`, fixture de renderer, `validate.py` y paridad de seis plataformas pasan. | Los fragmentos se insertan donde se necesitan como artifacts autónomos; no son carga global automática. |
| REC-10 | Descripciones canónicas y los seis descriptores del orquestador precisan operación y destino. Graphify global se limita a solicitudes explícitas; se quitó `trigger` no soportado. | `test_context_efficiency.py` 11/11. Probe OpenCode 1.18.34 con `openai/gpt-6.1-sol`: cargó `project-navigator` ante una consulta de navegación. | La lectura de la referencia externa fue auto-rechazada por permisos; no hubo respuesta final ni cambios. Faltan selección negativa/ambigua y otros hosts; follow-up REC-08. |
| REC-11 | Los tests ya no exigen MASVS/MASWE/MASTG en toda skill; valida fragmento común y conserva identidad específica de seguridad. | `test_mas_identity.py` 235/235 después de render. | Ninguno de distribución. |
| REC-12 | `code-quality` y `security` piden una aprobación para diffs atómicos/reversibles y mantienen micro-pasos estructurales; Code Review remite a la regla de skill. | `test_code_review_contract.py` 7/7; `test_context_efficiency.py` incluye contrato. | No se cuantifican turnos ahorrados. Smoke de interacción real no ejecutado; confirmaciones Git/release permanecen independientes. |
| REC-13 | SDD carga una referencia/fragmento pertinente una vez y reutiliza su contenido; evita lecturas duplicadas sin fusionar referencias bajo demanda. | `test_sdd_contract.py` 613/613; enlaces y paridad de referencias pasan. | Número real de lecturas/latencia no se midió en un smoke SDD; la consolidación 10→4 se descartó porque podría cargar módulos mayores de los necesarios. |
| REC-14 | Agent SDD remite al procedimiento en `sdd-spec`; skill compacta tratamiento nuevo/histórico; testing conserva estrategia normativa. | `test_sdd_contract.py` 613/613, render/validate correctos. | Ninguno de texto/distribución. |
| REC-15 | Eliminadas tablas de tipos, clasificación por extensión, comandos y troubleshooting genérico; reglas propias del kit preservadas. | `test_secret_policy.py` 26/26, test de contexto 9/9, render/validate correctos. | Ahorro reportado como volumen fuente, no tokenizer específico. |
| REC-16 | `measure_context.py` acepta solo archivos observados y compara volumen con ref Git; `docs/developer-smoke.md` ahora pauta comparación baseline/post con consumo y tiempo reportados por el host. | `test_measure_context.py` 5/5; no hay ejecuciones baseline/post del smoke. | El script sigue midiendo bytes/palabras, no usage real, lecturas, interacciones o calidad. REC-16 aplica al MAS; faltan resultados empíricos. |
| REC-17 | Topes/fórmula caracteres→tokens sustituidos por pautas de contenido y lectura ampliable. | `test_context_efficiency.py` 9/9, validate/render y búsqueda canónica. | El número de tokens reales no se infiere de estos límites. |
| FUT-02 | El adaptador Claude de Git/release ya no precarga ambas skills; `Skill` permite cargar la que aplica. | JSON del adaptador; test incluido en `tools/test_context_efficiency.py`. | Runtime Claude pendiente por disponibilidad de CLI/sesión; regeneración. |
| FUT-04 | Navigator usa un presupuesto inicial ampliable y deja de limitar por cantidades rígidas de archivos/capas. | `SKILL.md` y `references/layers.md`. | Medir el comportamiento en consultas transversales reales; puede leer más si lo requiere la evidencia. |
| FUT-05 | El orquestador continúa ramas independientes ya autorizadas cuando otra se bloquea; solicita decisión si cambian dependencias, alcance o autorización. | Skill/workflow canónico y contrato en `tools/test_context_efficiency.py`. | Runtime de flujo del orquestador pendiente de REC-08. |
| FUT-08 | La skill global Graphify perdió `trigger` y la descripción general; ahora se limita a solicitudes explícitas de pipeline/grafo. | `.config/opencode/skills/graphify/SKILL.md` actual no contiene `trigger`; Graphify está disponible en la sesión OpenCode actual. | Cerrado localmente; no es un artefacto versionado en este repositorio. |
| FUT-11 | Investigación de releases no soportadas limitada a caché y dos fuentes oficiales para la petición activa; actualizado el skill canónico y el global. | Canonical, skill global y `technologies/README.md` local; el skill global está cargado en la sesión actual. | Falta probar el flujo ante una release real de tecnología no soportada; no se han medido fuentes/tokens de una ejecución. |
| FUT-14 | Cerrado tras corregir deriva detectada el 2026-10-12: Navigator y arquitectura actualizados a 11 skills/5 agentes/6 plataformas y modos SDD actuales. | Contraste de `.navigator/ai-context.md`, `.architecture/README.md`, `.architecture/07-crosscutting.md`, `docs/catalogo.md` y `docs/uso.md` contra manifest y scope-depth en `10373b3`; `test_documentation_core.py` 17/17 y CI v3.2 SUCCESS. | La regeneración general de Navigator sigue manual; reabrir si reaparece divergencia fuera de los campos cubiertos por el test. |

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

## Revalidación de estados — 2026-10-13

- **HEAD:** `main` `10373b3e9510cc71049eb37c5393b4e18415e40d` (`v3.2.0`).
- **Pruebas locales:** `test_context_efficiency.py` 11/11; `test_sdd_contract.py` 604/604; `test_code_review_contract.py` 7/7; `test_measure_context.py` 5/5; aserción FUT-14 1/1; `test_model_recommendations.py` 5/5; permisos 9/9; instaladores 250/250 + Antigravity 22/22; enlaces 91/91.
- **CI actual:** [run 38352143368](https://github.com/furthurr/ai-agents-kit/actions/runs/38352143368), SUCCESS para el mismo HEAD. La suite documental y `validate.py` pasan en v3.2.0.
- **Smoke runtime REC-10 / FUT-07:** OpenCode 1.18.34 con `openai/gpt-6.1-sol` cargó `project-navigator` ante una consulta de navegación; la lectura de referencia externa fue auto-rechazada, por lo que no hubo resultado conductual evaluable. El mismo arranque generó avisos de `frontend-slides` duplicado entre roots y bundles plugin.
- **Lectura de estados:** estos resultados acreditan contratos estáticos e integración; no cierran los smokes de REC-10/12/13 ni la medición empírica de REC-16, que siguen pendientes según sus criterios.

No se hicieron commits ni push. Los cambios globales de OpenCode son locales; reiniciar OpenCode para que recargue las descripciones modificadas.
