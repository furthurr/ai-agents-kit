# Protocolo — comparativa de arneses

## 1. Diseño

Experimento de un factor: **el arnés**. Constantes:

- Proyecto: `mobile-android.zip` (copia limpia por brazo).
- Tarea: `GBA-SEARCH-PROSPECTS` (media-baja), adaptada al paquete real
  `mx.com.bancadigital.crm`.
- Modelo: `openai/gpt-6-luna`, proveedor OpenAI vía OAuth.
- Prompt: contenido íntegro de la tarea adaptada + el mismo recordatorio de
  implementación directa usado en la corrida histórica.
- Límites: 1800 s, 60 pasos.
- Oráculos: `OracleSearchProspectsTest` y suite original
  `:core:domain:testReleaseUnitTest --tests "mx.com.bancadigital.crm.domain.util.*"`.

## 2. Brazos e instalación

| Brazo | Comando | Notas |
|---|---|---|
| v2_reforzado | skill `developer-v2` reforzada + `data-api` + `ui-design`; agente `pilot-v2_reforzado` | snapshot congelado del MAS |
| wshobson | `python3 tools/generate.py --harness opencode --all --prune` + `install_opencode.py install --force` | symlinks a `OPENCODE_CONFIG_DIR` |
| superpowers | copia de `skills/` + plugin en `plugins/superpowers.js` | layout de `tests/opencode/setup.sh` |
| ecc | `node scripts/build-opencode.js` + `install-apply.js --target opencode --profile developer --no-hooks` | perfil de ingeniería por defecto |
| gentle-ai | `gentle-ai install --agents opencode --scope global --components persona,skills,permissions,opencode-gentle-logo` | sin Engram ni Context7 |
| gstack | `./setup --host opencode --no-browser` | Bun local para construir las skills |
| **sdd** | agente `sdd` (cuerpo de `generated/opencode/agents/sdd.md`) + skills `sdd-spec`, `data-api`, `ui-design` | brazo metodológico del MAS; `default_agent=sdd` |
| **superpowers-sdd** | skills `writing-plans` + `subagent-driven-development`; agente `pilot-superpowers-sdd` | plan y ejecución con subagentes |
| **ecc-plan** | subagente `planner` + agente `build` + `code-reviewer` | plan cooperativo y revisión |
| **cc-sdd** | `npx cc-sdd --opencode-skills` + 17 skills; agente `pilot-cc-sdd` | Kiro SDD: spec/design/tasks/impl; artefactos en `.kiro/specs/` |
| **openspec** | `openspec init --tools opencode --language es`; agente `pilot-openspec` | cambios en `openspec/changes/` |
| **spec-kit** | `specify init . --integration opencode`; agente `pilot-spec-kit` | comandos `speckit.*`; artefactos en `specs/` |

## 3. Desviaciones declaradas

1. **Base**: el ZIP histórico `mobile-android.zip` no está
   disponible. Se usa Genera y se adapta la tarea/oráculo de forma mecánica
   (paquete y rutas). Las reglas de negocio no cambian.
2. **v2_reforzado**: se reconstruye desde las fuentes congeladas
   (`agent-candidato2.md`, `SKILL-candidato2.md` + refuerzos A y B). Se ejecuta
   con el mismo sandbox y el mismo prompt que los demás brazos.
3. **gentle-ai**: se omitieron `engram` (memoria con servidor) y `context7` (MCP),
   y `gga` porque intentaba `brew reinstall` sobre taps no confiables. Se conserva
   el orquestador, la persona, las skills y los permisos. El agente usado es su
   `default_agent` (`gentle-orchestrator`).
4. **ECC**: perfil `developer` (el recomendado para ingeniería) y `--no-hooks`,
   para no ejecutar hooks automáticos fuera del sandbox.
5. **gstack**: `--no-browser` evita Chromium; se instaló Bun en el laboratorio.
6. Todos los brazos permiten `task` (subagentes) porque es una capacidad central
   de superpowers, ECC y gentle-ai. La línea base histórica corría con `task: deny`;
   el control nuevo de `v2_reforzado` usa el mismo sandbox que el resto.
7. `OPENCODE_DISABLE_PROJECT_CONFIG=1` para que la configuración de proyecto no
   favorezca a ningún brazo. El `AGENTS.md` del proyecto se trata igual en todos.
8. **SDD**: se usa el agente `sdd` y la skill `sdd-spec` generados por el MAS. El
   prompt añade una preaprobación explícita del Gate 3 y prohíbe preguntas
   interactivas, porque la corrida no tiene usuario. El agente puede crear el
   artefacto `.sdd/specs/<ruta>/spec.md` que exige SDD-Tiny; se contabiliza como
   metodología, no como código de producto.
9. **SDD, lectura de referencias**: el perfil aislado no permite que el agente lea
   directamente archivos de la skill fuera del workspace (p. ej.
   `workspace-trust.md`; en una corrida previa también `scope-depth.md`). El agente
   siguió con el cuerpo de `sdd-spec`, creó el spec y verificó. Es una limitación
   del host, declarada en las limitaciones del README.
10. **SDD, cierre**: el Gate 4 queda pendiente de cierre formal porque no hay
    usuario interactivo; la verificación funcional y la evidencia sí se
    registraron en el `spec.md`.
11. **superpowers-sdd**: se usa el agente de superpowers con las skills
    `writing-plans` y `subagent-driven-development`. El plan se escribe en
    `docs/superpowers/plans/` y se contabiliza como metodología. El sandbox
    necesita `skill: allow`; sin él, el agente se detiene sin tocar código.
12. **ecc-plan**: el agente `build` invoca al subagente `planner` mediante `task`
    y luego usa `code-reviewer`. El plan queda en el resultado del subagente, no
    en un archivo. Es una corrida cooperativa, no un único agente.
13. **Brazos SDD-like**: superpowers se ejecuta como `superpowers-sdd`; ECC como
    `ecc-plan`; y los proyectos externos cc-sdd, OpenSpec y Spec Kit se ejecutan
    con sus flujos propios. gstack, wshobson y gentle-ai se miden con su agente
    por defecto, sin sub-brazo SDD.
14. **cc-sdd**: se instalan sus 17 skills con `npx cc-sdd --opencode-skills` y se
    copian al workspace para que las referencias sean legibles. El piloto
    `pilot-cc-sdd` obliga a generar `.kiro/specs/<feature>/` antes de código. Los
    archivos de instalación (`.opencode/skills`, `.kiro/settings`) se excluyen de
    Git; solo el spec generado cuenta como metodología.
15. **OpenSpec**: se inicializa con `openspec init --tools opencode --language es`;
    el piloto `pilot-openspec` carga `openspec-propose` y `openspec-apply-change`.
    Se permite la CLI local `openspec` en bash. Los archivos de instalación se
    excluyen de Git; el cambio generado en `openspec/changes/` cuenta como
    metodología.
16. **Spec Kit**: se inicializa con `specify init . --integration opencode`; el
    piloto `pilot-spec-kit` sigue los comandos `speckit.*`. El directorio `specs/`
    se crea antes de fusionar el sandbox para que la política de escritura lo
    permita. Los artefactos de instalación (`.opencode/`, `.specify/`) se excluyen
    de Git; `specs/` generado cuenta como metodología.

## 4. Aislamiento

- `HOME` y `XDG_CONFIG_HOME` de laboratorio durante la instalación.
- En ejecución se conserva el `HOME` real solo para leer la credencial OAuth,
  pero `XDG_CONFIG_HOME` y `OPENCODE_CONFIG_DIR` apuntan al perfil aislado.
- `OPENCODE_DISABLE_EXTERNAL_SKILLS=1` y `OPENCODE_DISABLE_CLAUDE_CODE*=1`.
- Sin MCP (`mcp: {}`) y sin `webfetch`/`websearch`.
- `local.properties`, `.secrets`, `.env*`, claves y keystores en `deny`.
- Sin commits, sin red externa desde el agente, sin escritura fuera del workspace.

### 4.1 Regla comodín del sandbox

OpenCode evalúa la regla comodín `"*"` del objeto `permission` con semántica de
última coincidencia. Si queda al final, anula las reglas explícitas de
`read`/`edit`/`write` y las herramientas de archivo desaparecen de la sesión.
Por eso `merge_sandbox` fuerza `"*": "deny"` como **primera** clave en todos los
brazos. Este defecto se detectó con gentle-ai: su configuración base ya traía
`permission`, y al fusionar el sandbox la comodín quedaba al final. El primer
intento falló con 0 archivos; tras corregir el orden se reinstaló y repitió solo
ese brazo. El incidente está documentado en el README y no se usa como resultado
del arnés.

### 4.2 Artefactos de metodología

Los brazos SDD producen artefactos de proceso antes o durante el código:

- SDD-Tiny: `.sdd/specs/<ruta>/spec.md`.
- superpowers-sdd: `docs/superpowers/plans/<plan>.md`.
- ecc-plan: el plan se devuelve en el resultado del subagente `planner`, sin
  archivo.
- cc-sdd: `.kiro/specs/<feature>/{requirements,design,tasks}.md` + `spec.json`;
  los archivos de instalación `.opencode/skills` y `.kiro/settings` se excluyen
  de Git.
- OpenSpec: `openspec/changes/<cambio>/` (proposal, specs, design, tasks); los
  archivos de instalación `.opencode/` y `openspec/config.yaml` se excluyen.
- Spec Kit: `specs/<feature>/{spec,plan,tasks}.md`; `.opencode/` y `.specify/`
  se excluyen.

`evaluate_arm` separa:

- `methodology_files` / `methodology_lines`: rutas bajo `.sdd/`,
  `docs/superpowers/`, `plans/`, `.kiro/specs/`, `openspec/` o `specs/`.
- `product_lines` y `out_of_scope_files`: código de producto; esos artefactos no
  cuentan como fuera de alcance.

Así el coste de trazabilidad se mide sin confundirlo con una violación del
alcance de producto. En esta corrida el spec del MAS tuvo 28 líneas, el plan de
superpowers 45, el spec de cc-sdd 61 y el producto 102–186.

## 5. Evaluación

1. Se copia el oráculo a la ruta esperada y se ejecuta.
2. Se elimina el oráculo y se ejecuta la suite original.
3. Se calcula `git status --porcelain -uall` y `git diff --numstat HEAD`.
4. Se comparan los archivos tocados contra los tres archivos esperados por la tarea.
5. Se separan artefactos de metodología (`.sdd/`, `docs/superpowers/`, `plans/`)
   de archivos de producto y se calculan `product_lines` y `methodology_lines`.
6. Se guarda `{install,preflight,run,eval}.json` y `events.jsonl` por brazo en
   `…/task_1/evidence/`.

## 6. Reproducción

```bash
# 1. Preparar copias limpias, instalar cada arnés y fusionar el sandbox.
python3 tools/real_android_harness_benchmark.py --install-only

# 2. Comprobar configuración, skills y agente por defecto (no ejecuta la tarea).
python3 tools/real_android_harness_benchmark.py --preflight

# 3. Ejecutar la tarea, evaluar oráculo y suite, y consolidar resultados.
python3 tools/real_android_harness_benchmark.py --run-only
```

Para repetir un solo brazo:

```bash
python3 tools/real_android_harness_benchmark.py --install-only --arms gentle-ai
python3 tools/real_android_harness_benchmark.py --run-only --arms gentle-ai
```

Para SDD:

```bash
python3 tools/real_android_harness_benchmark.py --install-only --arms sdd
python3 tools/real_android_harness_benchmark.py --run-only --arms sdd
```

Para los brazos SDD-like:

```bash
python3 tools/real_android_harness_benchmark.py --install-only --arms superpowers-sdd ecc-plan cc-sdd openspec spec-kit
python3 tools/real_android_harness_benchmark.py --run-only --arms superpowers-sdd ecc-plan cc-sdd openspec spec-kit
```

Tras una repetición parcial, regenerar `resultados.json` con todos los brazos
para no perder la evidencia de los demás (el runner escribe el resumen con los
brazos seleccionados).

Los resultados se escriben en `resultados.json` y la evidencia cruda permanece
en la carpeta temporal del sistema.
