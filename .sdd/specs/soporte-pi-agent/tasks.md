# Tareas: soporte de Pi Agent

- **Modo SDD:** standard
- **Fase:** Verification
- **Estado:** verificado parcialmente — Gate 4 pendiente
- **Gate pendiente:** Gate 4 — decisión de cierre

## Grafo de waves

```text
Wave 1 ──► Wave 2 ──► Wave 3 ──► Wave 4 ──► Wave 6 ──► Wave 8
                │                   │
                │                   ▼
                │              Wave 5 (tests)
                │                   │
                └────────────► Wave 7 (docs) ──┘
```

## Wave 1 — Fundación del manifest y adapter de plataforma

- **T1** [x] [P] Añadir `"pi"` a `platforms` en `canonical/manifest.json` (Req R1)
- **T2** [x] [P] Crear `adapters/pi/platform.json` con sustituciones
  `{{sdd_agent}}`→`/sdd`, `{{gate_instruction}}`→`""`,
  `{{steering_paths}}`→`` `AGENTS.md`, `CLAUDE.md`, `.pi/APPEND_SYSTEM.md` `` (Req R1, R2, R3)

## Wave 2 — Adapters de agentes

- **T3** [x] Crear los 9 archivos `adapters/pi/agents/<id>.json` con `filename`,
  `frontmatter.description`, `frontmatter.argument-hint` y
  `body_suffix` (`"\n\n## Tarea del usuario\n\n$ARGUMENTS\n"`) (Req R3)
  - `architecture.json`, `code-quality.json`, `data-api.json`,
    `documentation-orchestrator.json`, `git-release-manager.json`,
    `project-navigator.json`, `sdd.json`, `security.json`, `ui-design.json`

## Wave 3 — Renderer y validación

- **T4** [x] Añadir soporte `body_suffix` a `tools/render.py`: campo opcional en
  adapter JSON que se añade tras el cuerpo canónico al escribir el agente (Req R3)
- **T5** [x] Añadir comprobación Pi en `tools/validate.py`: `body_suffix` debe ser
  string y contener `$ARGUMENTS` (Req R3, R8)

## Wave 4 — Instalación y backup

- **T6** [x] Crear `scripts/install/pi.sh` con preflight, backup, dry-run y
  verificación post-instalación (Req R4, R5, R6)
- **T7** [x] Crear `scripts/install/pi.ps1` equivalente para Windows (Req R4, R5, R6)
- **T8** [x] Crear `scripts/backup/pi.sh` que llama a `tools/import_installed.py`
  con rutas de Pi (Req R6)
- **T9** [x] Crear `scripts/backup/pi.ps1` equivalente (Req R6)

## Wave 5 — Tests

- **T10** [x] Actualizar `tools/test_integrity.py`: añadir `pi` a `essential_dirs`
  y `test_scripts_exist` (Req R8)
- **T11** [x] Actualizar `tools/test_install.py`: añadir entrada `pi` en `PLATFORMS`
  con rutas `.pi/agent/skills`, `.pi/agent/prompts`, `.pi-kit-backup` (Req R8)
- **T12** [x] Añadir test negativo en `tools/test_validate.py`: adapter Pi sin
  `$ARGUMENTS` en `body_suffix` → error (Req R8)

## Wave 6 — Render, validación y suite completa

- **T13** [x] Ejecutar `python3 tools/render.py` y verificar `generated/pi/`
  (10 skills + 9 agentes con `$ARGUMENTS`) (Req R1, R2, R3, R8)
- **T14** [x] Ejecutar `python3 tools/validate.py` sin errores (Req R8)
- **T15** [x] Ejecutar la suite: `test_integrity.py`, `test_install.py`,
  `test_validate.py`, `test_mas_identity.py`, `test_model_recommendations.py`,
  `test_handoff_contract.py`, `test_sdd_contract.py`, `test_links.py` (Req R8)

## Wave 7 — Documentación [P con Wave 5–6]

- **T16** [x] [P] Actualizar `README.md`: añadir Pi a la lista de plataformas y
  comando de instalación (Req R9)
- **T17** [x] [P] Actualizar `docs/catalogo.md`: añadir Pi a la tabla de plataformas
  con rutas de destino (Req R9)
- **T18** [x] [P] Actualizar `docs/instalacion.md`: sección Pi con rutas, opciones
  y ejemplo de uso (`/sdd ...`, `/skill:sdd-spec ...`) (Req R7, R9)
- **T19** [x] [P] Actualizar `docs/desarrollo.md`: pasos para añadir plataforma Pi
  y nota sobre `body_suffix` (Req R9)

## Wave 8 — Verificación manual

- **T20** [omitido: verificación funcional no concluyente] Smoke test en Pi:
  la CLI está instalada y la instalación temporal completa pasó, pero la
  invocación `/sdd` terminó con HTTP 429 por límite mensual del proveedor antes
  de devolver respuesta; queda por confirmar manualmente descubrimiento y
  expansión de `$ARGUMENTS` con un proveedor disponible (Req R7, R8, R9).

## Trazabilidad

| Req | Tareas |
|-----|--------|
| R1 | T1, T2, T13 |
| R2 | T2, T13 |
| R3 | T2, T3, T4, T5, T13 |
| R4 | T6, T7 |
| R5 | T6, T7 |
| R6 | T6, T7, T8, T9 |
| R7 | T18, T20 |
| R8 | T5, T10, T11, T12, T13, T14, T15 |
| R9 | T16, T17, T18, T19, T20 |
