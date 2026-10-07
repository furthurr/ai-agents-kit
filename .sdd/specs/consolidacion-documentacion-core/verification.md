# Verificación — Consolidación de documentación core

- Modo SDD: standard
- Fase: 4 — Verification
- Estado: cerrada
- Gate aprobado: Gate 4 — cierre mediante «procede» el 2026-10-07
- Gate previo: Gate 3 aprobado; implementación del kit autorizada por «procede» el 2026-10-07

## Ciclo de pruebas

- Estrategia: TDD focalizado para contratos e instalación; caracterización/regresión
  para permisos, targets restantes y baselines; checks para cambios narrativos.
  PBT omitido: sin invariante algebraico nuevo.
- Baseline/RED: suites previas al cambio (33 handoff, 444 SDD, 148 instalación)
  en verde; RED observados antes de cada GREEN: inventario 8≠6 en seis plataformas,
  targets core aún aceptados (1 fallo), contratos core ausentes (22 fallos/subcasos),
  módulo de migración inexistente y 38 fallos/subcasos + 1 error en la revisión de
  destinos de skills, respaldo inválido y quoting de aprobación.
- GREEN / suite: comandos de la tabla inferior, todos exit 0 tras la integración.
- Excepciones: ejecución nativa PowerShell/Windows pendiente (sin `pwsh` en este
  entorno; paridad estática verificada); smoke conversacional LLM pendiente; pruebas
  de texto no acreditan obediencia del modelo.

## Matriz de requisitos

| Requisito | Tarea(s) | Test(s) | Evidencia (path o cmd) | Estado |
|-----------|----------|---------|------------------------|--------|
| R1.1 | 3.1, 4.1 | `test_documentation_core.test_inventory_preserves_skills_without_retired_agents`, `test_validate.py` | `canonical/manifest.json`, `python3 -B tools/validate.py` (10 skills/6 agentes/6 plataformas) | ✅ |
| R1.2 | 2.1, 3.1 | `test_documentation_core`, `test_integrity.test_generated_artifacts` | `canonical/skills/{architecture,project-navigator}/SKILL.md`, `generated/*/skills/` | ✅ |
| R1.3 | 2.1, 3.1 | `test_documentation_core.test_shared_reference_portable_and_selective` | `references/project-context.md`; `.architecture/` y `.navigator/` sin tocar | ✅ |
| R2.1 | 2.1 | `test_documentation_core.test_inspect_distinct_from_default_status`, `test_read_only_specialists_keep_write_gates` | `documentation-orchestrator/{SKILL.md,references/workflows.md}`, `architecture/SKILL.md` | ✅ |
| R2.2 | 2.1 | ídem + `test_sdd_specific_freshness_preserved` | `project-navigator/SKILL.md`, `sdd-spec/references/navigator-context.md` | ✅ |
| R2.3 | 2.1, 2.3 | `test_documentation_core` (cero persistencia, sin bootstrap/sync), `test_retired_agents` (opt-in) | `project-context.md` §Lectura/escritura; `tools/install_preflight.py` | ✅ |
| R2.4 | 2.1 | `test_adapter_descriptions_discover_queries_without_preload` | `adapters/*/agents/documentation-orchestrator.json` sin precarga de skills core | ✅ |
| R3.1–R3.4 | 2.2, 4.1 | `test_every_agent_discovers_context_directly`, `test_relative_skill_links_resolve`, `test_generated_core_inventory_and_reference_parity` | seis `canonical/agents/*.md`, `project-context.md`, `generated/*/` | ✅ |
| R4.1 | 2.1 | `test_read_only_specialists_keep_write_gates`, `test_code_review_contract` (sin escrituras) | `architecture/SKILL.md`, `project-navigator/SKILL.md` | ✅ |
| R4.2 | 2.1 | `test_handoff_contract.test_confirmation_truth_table`, `test_sdd_contract` (gates) | `references/handoff.md` | ✅ |
| R4.3 | 2.2 | `test_sdd_specific_freshness_preserved` (export opt-in), `test_documentation_core` | `navigator-context.md`, `project-context.md` | ✅ |
| R4.4 | 1.1, 3.1 | `test_code_review_contract`, `test_sdd_contract` (465 checks) | difs concurrentes de SDD preservados; permisos de adaptadores sin cambios | ✅ |
| R5.1 | 3.1, 4.1 | `tools/validate.py`, `test_documentation_core`, `test_integrity` (416/416) | manifest, adaptadores, `generated/` en 6 plataformas, CI | ✅ |
| R5.2 | 3.1 | `test_handoff_contract.test_core_targets_retired_without_authorization_transfer` | `tools/handoff_contract.py`, `references/handoff.md` | ✅ |
| R5.3 | 2.3, 2.4 | `test_retired_agents` (26/26), `test_install` (196/196) | `tools/retired_agents.py`, wrappers; HOME temporal | ✅ |
| R5.4 | 1.1, 3.2 | revisión de diffs | specs históricas intactas; `.sdd/` sin cambios de esta spec | ✅ |
| R5.5 | 2.3 | `test_uncertain_requires_exact_path_and_matching_hash`, `test_approval_validation_exact_repeated_paths` | pares ruta exacta + SHA-256 | ✅ |
| R5.6 | 2.3 | `test_copy_failure_and_changed_original_preserved`, `test_bad_backup_and_unique_retry_preserve_evidence`, `test_unlink_failure_preserves_original_and_backup`, `test_post_unlink_failure_recovers_without_overwrite` | `tools/retired_agents.py` | ✅ |
| R5.7 | 2.3, 2.4 | `test_dry_run_zero_writes`, `test_real_wrappers_opt_in_force_dry_run_and_invalid_flags` | snapshot pre/post idéntico | ✅ |
| R5.8 | 2.3, 2.4 | `test_known_backup_restore_and_idempotence`, `test_preflight_current_bytes_and_check_installed_read_only` | `docs/migracion-agentes.md` | ✅ |

## Suite ejecutada — 2026-10-07

| Comando | Resultado |
|---|---|
| `python3 -B tools/validate.py` | 10 skills / 6 agentes / 6 plataformas |
| `python3 -B tools/test_validate.py` | 38/38 |
| `python3 -B tools/test_documentation_core.py` | 12/12 |
| `python3 -B tools/test_retired_agents.py` | 26/26 |
| `python3 -B tools/test_install.py` | 196/196 (HOME temporal) |
| `python3 -B tools/test_handoff_contract.py` | 34/34 |
| `python3 -B tools/test_sdd_contract.py` | 465/465 |
| `python3 -B tools/test_code_review_contract.py` | 8/8 |
| `python3 -B tools/test_model_recommendations.py` | 437/437 |
| `python3 -B tools/test_antigravity_contract.py` | 5/5 |
| `python3 -B tools/test_antigravity_install.py` | 22/22 (perfiles aislados) |
| `python3 -B tools/test_links.py` + `check_links.py` | 4/4 + 71 archivos |
| `python3 -B tools/test_integrity.py` | 416/416 |
| `bash -n` sobre 12 instaladores + 6 backups | OK |
| Render idempotente (`render.py` ×2, diff `generated/` estable) | OK |
| `git diff --check` | OK |

Ajuste de verificación: `tools/test_code_review_contract.py` fijaba el inventario antiguo
de 8 agentes; se derivó del manifest/fuentes y se conservó la intención semántica
(un solo agente para quality/security). Sin RED previo posible: la aserción era
legado que debía seguir a la retirada autorizada; registrado como ajuste de contrato.

## Self-check RNF (declarados en design.md)

| RNF | Evidencia (búsqueda / path) | Estado |
|-----|----------------------------|--------|
| RNF-1 Portabilidad en seis plataformas | `tools/validate.py`; paridad `generated/` (core 12/12); `test_install` 196/196; `test_antigravity_install` 22/22 | ✅ |
| RNF-2 Contexto cargado bajo demanda | `project-context.md` «Orden de lectura bajo demanda»; adaptadores sin precarga de skills core (`test_adapter_descriptions_discover_queries_without_preload`) | ✅ |
| RNF-3 Preservación de autorizaciones y permisos | diffs de adaptadores solo en `description` (permisos intactos); `test_confirmation_truth_table`; gates de skills core conservados | ✅ |
| RNF-4 Migración recuperable sin tocar archivos ajenos | `test_retired_agents` (respaldo verificado, restore sin overwrite, extras preservados, symlinks bloqueados, backup fuera de árboles escaneados) | ✅ |

Invariantes 1–5 de `design.md`: skills/destinos sobreviven y agentes desaparecen del
catálogo; consulta no concede escritura; ausencia/desfase no acredita vigencia;
targets retirados no ejecutan ni heredan autorización; distribución replica fuentes
(render idempotente + tests de paridad).

## Integrity gate — tareas `[x]`

Las 10 tareas de `tasks.md` tienen artefacto en disco o comando de verificación
(documentado en su tabla de evidencia). Sin `[x]` huérfanos ni tests tautológicos.

## Huecos y limitaciones (no aprobados)

1. **PowerShell/Windows nativo:** no ejecutable aquí (`pwsh` ausente). Paridad
   estática de flags/orden y quoting verificada; comportamiento de junctions/ACL y
   binding nativo pendiente en CI Windows.
2. **Smoke conversacional LLM:** pendiente en host real; los contratos estáticos no
   prueban obediencia del modelo.
3. **Migración sobre instalación real:** no ejecutada (fuera del alcance autorizado).
   Ningún perfil del usuario fue modificado; implementar el kit no migró nada.
4. **TOCTOU residual:** comparación+unlink no es atómico en portable; se revalida
   identidad y se ancla el padre en POSIX (`remove_verified`). Aceptado en design.
5. **Trabajo concurrente:** los cambios de routing SDD (spec `recomendacion-agente-por-dominio`)
   están presentes y preservados; su suite (465 checks) pasa, pero su verificación
   runtime propia no se atribuye a esta spec.

## Gate 4

Aprobado y cerrado mediante «procede» el 2026-10-07, aceptando los huecos declarados
como límites conocidos. El cierre no instaló ni migró el perfil del usuario: esa
operación queda separada y requiere su propia autorización.
