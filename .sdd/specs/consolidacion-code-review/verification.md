# Verificación — Consolidación de agentes en Code Review

Modo SDD: standard
Fase: Verification
Estado: cerrada con límites de evidencia aceptados
Gate 3: aprobado
Continuación a Verification: autorizada por el usuario («continúa»)
Gate 4: aprobado por el usuario («adel»)

## Resultado

La suite automática pasa. El catálogo contiene ocho agentes y diez skills en las
cinco plataformas; `code-review` sustituye los dos agentes anteriores. No se
detectaron regresiones en los validadores, distribución, instaladores ni enlaces.

La evidencia de comportamiento conversacional se limita a contratos de prompts
y escenarios definidos: no se ha ejecutado el smoke de Code Review en un host
real. Esta limitación queda explícita para la decisión de cierre, no se considera
una prueba E2E aprobada.

## Ciclo de pruebas

- Estrategia: TDD focalizado para contratos nuevos; regresión para validación y
  distribución existentes; checks mecánicos para documentación.
- Baseline: 24 tests de handoff y 141 checks de modelo verdes antes del cambio.
- RED observado: `CodeReviewScopeTest`, catálogo/agente/scopes inexistentes,
  flujo documental y preflight anteriores, adaptadores ausentes y catálogo
  generado con nueve agentes. Detalle y resultados en `execution.md`.
- Regresión adicional con RED: una raíz `.quality/` redirigida por symlink a
  `.security/` podía ampliar el dominio; ahora se rechaza.
- GREEN: contratos nuevos y suite final indicados abajo.
- Sin PBT adicional: matriz cerrada de scopes/acciones, sin dependencia nueva.
- Excepción de evidencia: los checks textuales prueban presencia/coherencia de
  instrucciones, no su cumplimiento por un LLM. `docs/code-review-smoke.md`
  conserva los escenarios pendientes para un host real.

## Comandos y resultados observados

Todos los comandos siguientes terminaron con exit 0 durante Verification.
Los mensajes de rechazo de fixtures de `test_validate.py` son pruebas negativas
esperadas, no fallos de la suite.

| Comando | Resultado |
|---|---|
| `python3 tools/test_code_review_contract.py` | 7 tests OK |
| `python3 tools/test_handoff_contract.py` | 33 tests OK |
| `python3 tools/test_model_recommendations.py` | 141/141 checks |
| `python3 tools/test_sdd_contract.py` | 211/211 checks |
| `python3 tools/test_integrity.py` | 391/391 checks |
| `python3 tools/test_validate.py` | 16/16 checks negativos |
| `python3 tools/test_install.py` | 124/124 checks; instalaciones Bash en HOME temporal; PowerShell estático |
| `python3 tools/test_mas_identity.py` | 223/223 checks |
| `python3 tools/test_links.py` | 4/4 tests |
| `python3 tools/validate.py` | 10 skills, 8 agentes, 5 plataformas; paridad y reproducibilidad correctas |
| `python3 tools/check_links.py` | 69 archivos Markdown, sin enlaces rotos |
| `python3 tools/measure_context.py` | 3.334 palabras de agentes; 17.721 de skills; 13.818 de referencias |
| `git diff --check` | Sin errores de whitespace |

No se suman estos contadores como tests independientes: integridad también
ejecuta algunos checks ya incluidos en otras suites.

## Matriz de trazabilidad

Estados:
- **A**: comprobación automática ejecutada del código o artefacto correspondiente.
- **C**: contrato/documentación revisados y checks estáticos verdes; su ejecución
  conversacional en host real permanece pendiente.

Los nombres de test remiten a `tools/test_code_review_contract.py` y
`tools/test_handoff_contract.py` salvo indicación distinta.

| Requisito | Tarea(s) | Test/check | Evidencia | Estado |
|---|---|---|---|---|
| 1.1 Entrada única | 1.2, 2.1, 2.4, 3.2, 4.1 | `test_single_agent_and_separate_skills`, `test_generated_catalog` | `canonical/manifest.json`, `canonical/agents/code-review.md`, cinco adaptadores y generated | A |
| 1.2 Un dominio explícito | 2.1, 3.3 | `test_routing_and_evidence_contract`; smoke solo calidad/seguridad | Agente: selección y alcance; `docs/code-review-smoke.md` | C |
| 1.3 Revisión conjunta | 2.1, 2.3, 3.3 | Contrato de routing y reutilización de modelo | Agente: revisión completa y resumen; matrices de ambas skills | C |
| 1.4 Aclarar alcance material | 2.1, 3.3 | Revisión del contrato y escenarios de alcance | Agente: ambigüedad, no ampliación puntual | C |
| 2.1 Dos skills especializadas | 2.1, 2.3, 2.4, 4.1 | `test_single_agent_and_separate_skills`, `test_generated_catalog` | Diez skills declaradas; Sonar y OWASP conservados | A |
| 2.2 Registros e IDs | 2.1, 2.2 | `test_skill_documentation_and_read_only_contract`; spot-check | Ambas skills, IDs QLT/SEC y carpetas independientes; ninguna migración añadida | C |
| 2.3 Riesgo de seguridad descubierto | 2.1, 2.2, 3.3 | Contrato de routing; smoke de dominio no autorizado | Agente y skill de calidad: cambio de procedimiento solo con dominio autorizado | C |
| 2.4 Severidad original | 2.1 | `test_routing_and_evidence_contract` | Agente: resumen por dominio; escalas de skills conservadas | C |
| 3.1 Todas las severidades verificadas | 2.2, 3.3 | `test_skill_documentation_and_read_only_contract` | Fase A de ambas skills; eliminación del filtro documental | C |
| 3.2 Agrupar ocurrencias | 2.2, 3.3 | Mismo contrato, regla de misma causa | Ambas skills y agente: ubicaciones agrupadas, no finding por ocurrencia | C |
| 3.3 Solo lectura sin cachés/marcas | 2.2, 3.1, 3.3 | Contrato de lectura; `test_confirmation_truth_table`, matriz inspect | Agente/skills y validador: `inspect` sin escritura | C; guard del validador A |
| 3.4 Preguntar por excepciones | 2.2, 3.3 | Spot-check de instrucciones y smoke | Agente/skills: ambigüedad, ampliación, trabajo manual y límites de recursos | C |
| 3.5 Reutilizar autorización acotada | 2.2, 2.3, 3.1, 3.3 | `test_orchestrator_domain_mapping`; spot-check | Orquestador, workflows y handoff: sesión efectiva; `gate_state` no autoriza | C |
| 4.1 Derivar al mismo receptor | 1.2, 3.1, 3.3 | Mapping y `test_skill_prevents_duplicate_execution` | Orquestador y handoff con target `code-review` | C |
| 4.2 Scopes/evidencia acotados | 1.2, 1.3, 3.1 | `test_review_scope_matrix`, resultado por dominio, evidencia conjunta | `tools/handoff_contract.py`; 33 tests verdes | A |
| 4.3 Rechazar handoff inválido | 1.2, 1.3, 3.1, 5.1 | Casos negativos, paths, symlinks, tipos, targets retirados | Normalización y validación de emisión/resultado | A |
| 4.4 Inspect sin escritura | 1.2, 1.3, 3.1, 5.1 | `test_confirmation_truth_table`, matriz de acciones | `write_scope: none` y confirmación falsa exigidos | A |
| 4.5 Preservar límites y correlación | 1.1–1.3, 3.1, 5.1 | Matriz de targets/acciones, ID/proyecto, resultado correlacionado | Formato escalar de otros cuatro targets conservado; permisos de adaptadores | A |
| 5.1 Seguridad más allá del código | 2.1, 3.3 | Spot-check y smoke de TLS/almacenamiento | Agente y security: configuración, auth, red, permisos y dependencias | C |
| 5.2 No exponer valores sensibles | 2.1, 2.2, 3.3 | Contratos y spot-check | Agente/skills/handoff: placeholders y prohibición de secretos/PII | C |
| 5.3 Primer y siguientes micro-pasos | 2.2, 3.3 | `test_routing_and_evidence_contract`; contrato de skills | Agente y Fase B de ambas skills: aprobación independiente | C |
| 5.4 Recomendar SDD antes de cambios amplios | 2.2, 3.3 | `test_sdd_contract.py`, contrato del agente | Agente y gates de ruta de ambas skills | C; integración estática A |
| 5.5 Verificar antes de resolver | 2.2, 3.3 | Spot-check de reauditoría y escenario de estado | Agente y ambas skills: estados y evidencia de resolución | C |
| 6.1 Cinco plataformas y catálogo | 2.1, 2.4, 3.2, 4.1, 5.1 | Catálogo generado, integridad, validate y instalación | 8 agentes/10 skills; cinco instalaciones temporales correctas | A |
| 6.2 Guías y actualización | 3.2, 5.1 | `check_links.py`; lectura de guías | `docs/agentes/code-review.md`, catálogo/uso/instalación; retiro manual documentado | A |
| 6.3 Pruebas de contratos | 1.1–1.3, 2.1–2.4, 3.1, 3.3, 4.1, 5.1 | Todas las suites de la tabla anterior | Tests de revisión/handoff/modelo/SDD y paridad verdes | A |
| 6.4 Evidencia y límites honestos | 1.1, 3.3, 4.1, 5.1, 5.2 | Auditoría de tasks y bitácora | `execution.md`, esta matriz y smoke marcado no ejecutado | A |

## Self-check de RNF

| RNF | Evidencia | Resultado |
|---|---|---|
| RNF-1 Distribución reproducible | `validate.py`, catálogo generado, instalación temporal de cinco plataformas | Verificado automáticamente |
| RNF-2 Scopes cerrados | Matriz de validación positiva/negativa, evidencia por dominio, symlinks y correlación; 33 tests de handoff | Verificado automáticamente |
| RNF-3 Sin migración/aliases | Manifest y agentes generados, conservación de skills; `docs/instalacion.md:141–159` | Artefactos verificados; continuidad de datos en host pendiente de smoke |
| RNF-4 Interacciones y autorización | Siete contratos de revisión; 141 checks de modelo; guards inspect y escenarios manuales | Contrato verificado; cumplimiento conversacional pendiente |

## Integrity gate y quality-bar

- Cada tarea 1.1–4.1 marcada `[x]` tiene artefacto y/o comando en `execution.md`.
  Tarea 5.1 enlaza la suite de este archivo; 5.2 enlaza la matriz y RNF aquí.
- Separación canónico/adaptadores/generados conservada; no edición manual de
  `generated/`. Validación reproduce el render sin diferencias.
- `_selected_scopes` comprueba tipos y vocabulario antes de usar conjuntos;
  los errores se devuelven como listas y las rutas usan resolución segura.
- Autorización documental no equivale a remediación; `gate_state` no concede
  permisos. El contrato y los permisos de cada plataforma mantienen esa frontera.
- No hay capas de aplicación/DI/BD/UI nuevas ni dependencia PBT sin uso.
  Esos puntos de quality-bar no aplican al kit, como se declaró en Design.
- La medida de contexto es una medición de palabras actual, no de tokens reales
  ni una promesa de ahorro de latencia: agentes 3.334, skills 17.721,
  referencias bajo demanda 13.818 palabras.

## Límites y decisión de cierre

1. Smoke conversacional de Code Review no ejecutado en un host real; sus casos
   están definidos en `docs/code-review-smoke.md`.
2. PowerShell validado estáticamente; no ejecución de instalación en Windows.
3. La instalación probada usa HOME temporal. Para activar el cambio en el host
   real se requiere instalar la plataforma y reiniciar; retirar copias antiguas
   solo tras revisar backup, conservando las skills homónimas.
4. El cambio concurrente `.navigator/` registrado en la bitácora no pertenece a
   esta feature; esta verificación usa fuentes directas.

Gate 4 aprobado por el usuario («adel»): spec cerrada con los límites de evidencia
anteriores aceptados. No hay bloqueadores automáticos ni requisitos sin
artefacto/evidencia de contrato. El cierre no convierte el smoke pendiente en una
prueba aprobada ni afirma verificación E2E de los criterios marcados C.
