# Inventario de pausas por modelo y controles reales

Fecha: 2026-10-05. Inspección de fuentes del checkout, sin ejecutar el MAS en hosts.
Los rangos de línea son los previos al ajuste; no son identificadores permanentes.
`generated/` es derivado y no se modifica a mano. Skills prevalecen sobre agentes.

## 1. Agentes canónicos

Todos los paths de esta tabla están bajo `canonical/agents/`.

| Archivo y líneas | Pausa por retirar | Intervención que se conserva |
| --- | --- | --- |
| `architecture.md:10–20,34–35` | Preflight pesado y puntual antes de herramientas | Alcance y autorización documental |
| `data-api.md:10–20,34` | Preflight pesado y puntual | Decisiones de datos, contratos y escrituras |
| `ui-design.md:10–20,34` | Preflight pesado y puntual | Alcance UI y aprobación de propuestas pendientes |
| `code-review.md:14–27` | Espera inicial de modelo | Selección de dominio, permisos y micro-remediación |
| `documentation-orchestrator.md:12,25–34` | Espera antes de cualquier modo | Plan global y decisiones de escritura |
| `sdd.md:33–45,59–62` | Inicio salvo direct y pre-Verification | Gates reales de fase y reclasificación |
| `project-navigator.md:19–20,28–32` | Espera previa a proceso pesado | Permiso de bootstrap/update/export |

`git-release-manager.md:16–17` no añade una pausa de modelo: conservar commit,
push, tag y controles destructivos. El aviso final de Navigator ya es no bloqueante.

## 2. Skills y referencias canónicas

Paths relativos a `canonical/skills/`.

| Archivo y líneas | Regla redundante o mixta |
| --- | --- |
| `architecture/SKILL.md:23–36` | Hard stop pesado y puntual |
| `data-api/SKILL.md:26–39` | Hard stop pesado y puntual |
| `ui-design/SKILL.md:22–35` | Hard stop pesado y puntual |
| `code-quality/SKILL.md:27–41` | Pausa por modelo también antes de micro-remediación; su autorización real permanece |
| `security/SKILL.md:25–39` | Pausa por modelo incluso en consulta de estado; riesgos y autorización permanecen |
| `architecture/references/model-selection.md:6–25` | Todas las filas Hard stop; pausa ante cambio de nivel; deduplicación depende de confirmación |
| `data-api/references/model-selection.md:6–25` | Mismo patrón |
| `ui-design/references/model-selection.md:6–26` | Mismo patrón |
| `code-quality/references/model-selection.md:6–25` | Mismo patrón |
| `security/references/model-selection.md:6–26` | Mismo patrón |
| `documentation-orchestrator/SKILL.md:8–9,69–89` | Gate 0 incluso para status; reanudación explícita |
| `documentation-orchestrator/references/workflows.md:21–31,58–83,188–201` | Plantilla «continua», fin de turno y reutilización condicionada a reanudación |
| `sdd-spec/SKILL.md:84–116,165–173` | Pausa inicial y espera antes de Verification |
| `sdd-spec/SKILL.md:225–233` | Suite solo tras respuesta de continuación, sin gate real intermedio |
| `sdd-spec/SKILL.md:249–264` | Pausa Quick Plan; no retirar la aprobación de reclasificación |
| `sdd-spec/references/model-selection.md:28–49,53–63` | Inicio, Verification, cambio de nivel y plantilla «continúa» |
| `sdd-spec/references/integrity-gate.md:17–36` | Repite pausa pre-Verification y ante cambio de recomendación |
| `project-navigator/SKILL.md:6–8,43–47,58,86–101` | Aviso previo con reanudación obligatoria |
| `project-navigator/references/bootstrap.md:3–34,38,51,156` | Espera en procesos pesados y deduplicación condicionada a reanudación |

### Controles humanos o técnicos que no se eliminan

- `sdd-spec/SKILL.md:66–82,146–163,190,201,210,232,262–264`: opciones
  retiradas, rutas/marcadores ambiguos, Gates 1–4 y reclasificación.
- `sdd-spec/references/integrity-gate.md:5–15,38–56`: evidencia de tareas,
  tests y cierre. Control técnico no equivale a pregunta humana universal.
- `documentation-orchestrator/SKILL.md:65–67,91–104,128–129` y
  `references/workflows.md:124–126,151–154,188–201`: proyecto/modo ambiguo,
  plan global de escritura, decisiones de especialistas y fallo de una rama.
- `documentation-orchestrator/references/handoff.md:78–90,113–134`: esperar
  resultados, autorización efectiva de escritura y validación de contrato.
  `requires_confirmation` no implica otra pregunta si la autorización efectiva
  ya existe; `gate_state` por sí solo no la demuestra.
- `architecture/SKILL.md:46,91–97,145–158,189–211`,
  `data-api/SKILL.md:51,109–115,158–171,202–207,225–244`,
  `data-api/references/api-docs.md:33`,
  `ui-design/SKILL.md:42–44,117–129,164–182`: ubicación, modo, propuesta,
  generaciones masivas, sobrescritura y frontera hacia implementación.
- `code-quality/SKILL.md:140–149,159–204`,
  `security/SKILL.md:134–143,153–195`, `canonical/agents/code-review.md:55–77`:
  autorización documental versus remediación, cambio de dominio y micro-pasos.
- `project-navigator/references/bootstrap.md:40,81–110,137–165` y
  `references/config.md:87–105,129–140`: ubicación, presupuestos, exportación y
  sobrescritura. Disponibilidad/degradación no es una pausa humana universal.
- `sdd-spec/references/navigator-context.md:75–93`: ausencia/desfase no bloquea;
  actualización auxiliar no se ejecuta sin aprobación.
- `git-commit/SKILL.md:31,55,106,169–177,196–210,272` y
  `release-management/SKILL.md:35–38,97,113,157–159,194–203,241,288–331,351–355`:
  ambigüedad, commit/push, versión/tag/publicación y sobrescritura.
- `tools/install_preflight.py:140–154,171–202`: validación técnica de instalación,
  no es una espera por modelo; se conserva.

## 3. Adapters y derivados

Descripciones bloqueantes en `adapters/<host>/agents/documentation-orchestrator.json`:
OpenCode línea 4, Copilot línea 5, Claude línea 5 y Pi línea 4.
La descripción Kiro no exige esta espera.

Conservar permisos host, por ejemplo
`adapters/opencode/agents/code-review.json:7–19` y
`adapters/kiro/agents/documentation-orchestrator.json:11–23`.
Conservar `adapters/copilot/platform.json:4`, adaptación de preguntas/gates reales.

El renderer propaga agentes, skills y referencias a `generated/{copilot,opencode,
kiro,claude,pi}/`. No listar cada duplicado como otra regla independiente.
`copilot/` y `opencode/` raíz son snapshots legados: en esta inspección solo tienen
directorios vacíos. Los instaladores consumen generated; cambiar el repositorio
no actualiza por sí solo las instalaciones globales ni esta sesión.

## 4. Pruebas activas afectadas

| Archivo y líneas | Cambio requerido / protección |
| --- | --- |
| `tools/test_model_recommendations.py:46–90,96–104,117–150` | Cambiar esperas, matrices y dependencia de confirmación; conservar manualidad, deduplicación y paridad |
| `tools/test_sdd_contract.py:154–210,243–272,294–303` | Cambiar inicio, Quick Plan y pre-Verification; conservar gates, proporcionalidad y distribución |
| `tools/test_code_review_contract.py:45–62,74–107` | Retirar dependencia del literal Hard stop; conservar reutilización, permisos y catálogo |
| `tools/test_handoff_contract.py:98–111,315–329` | Conservar permisos y no duplicación; adaptar selector de sección `Flujo tras Gate 0` si se renombra |
| `tools/handoff_contract.py:119–126` | Conservar validación inspect/write; no confundirla con pausa por modelo |
| `tools/validate.py:200–216` | Conservar reproducción determinista de generated |

Son mayoritariamente pruebas textuales, no evidencia de comportamiento real del
LLM. Añadir/actualizar smokes y registrar honestamente si se ejecutan en hosts.

## 5. Documentación activa afectada

- `docs/model-recommendations-smoke.md:6–24,33–37`.
- `docs/documentation-orchestrator-smoke.md:14–29,42–44,73–82,94–95,138–141`.
- `docs/code-review-smoke.md:13,22,26,39–40`.
- `docs/sdd-smoke.md:14–36,80,182,194,408–434`.
- `docs/navigator-smoke.md:28–34` (separar permiso de índices y aviso de modelo).
- `docs/agentes/README.md:49–76`.
- `docs/agentes/architecture.md:37–43`, `data-api.md:39–45`,
  `ui-design.md:35–40`, `code-review.md:21–22`.
- `docs/agentes/documentation-orchestrator.md:41–46`,
  `project-navigator.md:75–77`, `sdd.md:33–44,70–85,160–164`.
- `docs/uso.md:96–109,148–150` (línea 97 ya contradice fuentes: puntual no bloquea).
- `docs/vision.md:131–134`, `docs/arquitectura-del-kit.md:226–237`,
  `docs/catalogo.md:22–25`, `README.md:103` (referencia a smoke Gate 0).

`docs/desarrollo.md:100–114,129–136` mantiene pruebas, precedencia y controles
Git/release/destructivos; no retirarlos.

## 6. Evidencia histórica y cambios ajenos

No migrar `.sdd/specs/pausa-preflight-llm-sdd/` ni
`.sdd/specs/recomendacion-por-fase-sdd/`, que registran decisiones anteriores.
No reescribir `CHANGELOG.md:34–48,58–67` ni evidencia histórica de
`docs/model-recommendations-smoke.md:43–55` como si validara la nueva política.

Estado local inicial ajeno al ajuste, que debe preservarse:

- Modificado `.opencode/commands/lab-start.md`.
- Modificado `.sdd/specs/laboratorio-evaluacion-sdd/tasks.md`.
- No rastreado `.opencode/commands/lab-docker-check.md`.

## Conclusión

Eliminar la espera exclusivamente informativa en todas las familias anteriores.
Conservar decisiones pendientes, autorizaciones y validaciones reales. La regla
resultante no concede nuevas facultades ni elimina restricciones del host.

### Ajustes menores encontrados durante Verification

- `canonical/skills/documentation-orchestrator/references/handoff.md:31`: el
  ejemplo conservaba `Gate0 aprobado`. Se retiró esa entrada del ejemplo,
  conservando `plan global aprobado`, campos, parser y permisos intactos.
- `docs/navigator-smoke.md`: separar explícitamente el registro histórico MVP de
  agosto del contrato nuevo no ejecutado en hosts, sin reescribir los resultados.
