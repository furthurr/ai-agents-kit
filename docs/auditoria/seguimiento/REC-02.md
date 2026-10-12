# Resultado de remediación — REC-02: permisos y fronteras de confianza

## Identificación y asignación

- **Estado actual:** integrado localmente en `main`, pendiente de verificación
  completa; abierto, no cerrado. La evidencia integrada y lo que falta se detallan
  al final de esta ficha.
- **Responsable:** sesión implementadora REC-02, sin flujo SDD ni subagentes.
- **Fecha:** 2026-10-11.
- **Repositorio / rama:** `ai-agents-kit` / `remediation/rec-02`.
- **Worktree:** `/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/ai-agents-kit-rec-02`.
- **Baseline HEAD:** `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`.
- **Baseline local heredado:** snapshot de las 32 modificaciones tracked previas
  (635 inserciones/346 eliminaciones) de REC-01; fuente del scanner, tres tools
  de secretos, sus seis copias generadas, documentos de auditoría y los cuatro
  antecedentes SDD de REC-01 copiados mediante diffs Git sin staging ni commit.
  Laboratorio/presentaciones ajenos no se copiaron ni modificaron en el original.
  Los ocho tracked de fuente/docs heredados son `.github/workflows/ci.yml`,
  `canonical/agents/git-release-manager.md`, las skills `git-commit`,
  `release-management`, `security`, `docs/agentes/git-release-manager.md`,
  `docs/desarrollo.md` y `docs/mejoras.md`; los 24 restantes son cuatro copias
  por host del agente Git/release y esas tres skills.
- **Aislamiento:** la implementación se hizo en un worktree propio desde HEAD con
  el baseline local de REC-01; en esa fase no se modificó el worktree principal.
  Después, la coordinadora integró selectivamente el delta en `main` y regeneró
  distribuciones desde las fuentes combinadas. El worktree principal sigue sin
  commit; el HEAD base no contiene los cambios locales REC-01/REC-02.
- **Instrucciones:** ficha REC-02, protocolo y plantilla leídos; no se encontró
  `AGENTS.md` en el árbol del proyecto. README conserva canonical → adapters → generated.
- **Alcance de implementación:** seis adaptadores OpenCode; adaptador Kiro y fuente
  del orquestador; pruebas de integridad/permisos, `docs/permisos-hosts.md`, esta
  ficha y distribuciones regeneradas. La sesión implementadora no editó tableros,
  CI ni docs de REC-01; al integrar, la coordinadora añadió el test estático de
  permisos al workflow de CI y actualizó el tablero de auditoría.
- **Recursos externos:** únicamente perfiles/fixtures temporales y servidores loopback
  propios. Sin configuración global, credenciales heredadas ni instalaciones globales.
- **Coordinación durante la implementación:** la sesión entregó esta ficha sin
  tocar el worktree original ni el consolidado. Después, la sesión coordinadora
  integró el delta y actualizó el tablero; véase la sección final.

## Diagnóstico actual

- **Vigencia:** confirmada estáticamente; no se atribuye un fallo conductual al modelo.
- `canonical/agents/documentation-orchestrator.md:14–25` restringe escritura a
  documentación/índices y prohíbe producto, tests, CI y configuración funcional.
  En baseline `adapters/opencode/agents/documentation-orchestrator.json:8` concede
  `edit: ask` general, sin frontera de rutas. Sus prefijos Git allow admiten opciones
  de escritura como `git diff --output`/`git log --output`.
- `canonical/agents/code-review.md:54–76` distingue consulta, auditoría y remediación;
  `tools/test_code_review_contract.py:83–99` solo comprueba metadata/asks/denies,
  no edición ni comandos efectivos. El baseline pasa sus siete tests.
- Los cinco otros adaptadores OpenCode repiten asks bajo el catch-all ask. La última
  coincidencia y precedencia de reglas del agente se contrastaron con referencia
  oficial; eliminar catch-all o asumir deny-wins sería incorrecto en este host.
- Kiro usa deny > ask > allow; el CLI disponible `2.29.1` es anterior a la referencia
  IDE 1.0/CLI V3. No certificar runtime V3 a partir de ese ejecutable.
- **Deuda vinculada:** P0.5 de `docs/mejoras.md`, permisos efectivos y confianza;
  ese archivo compartido con REC-01 no se editó en esta integración. Fuentes originales D AUD-02,
  M H8 y E EST-002; la variante de instalación local no se cambia ni se presume saneada.
- **Diferencia histórica:** la matriz existente ya advierte que prompt/tools no son
  sandbox; se reutiliza y complementa, sin prometer equivalencia entre hosts.

## Solución aplicada

- OpenCode orquestador: default deny de edición, excepciones ask por seis nombres
  documentales, relativos y absolutos; task deny salvo los tres especialistas con ask; shell Git de
  escritura y `rm` deny, consultas Git ask para revisar opciones y efectos.
- Cinco roles OpenCode restantes: mantienen edición/shell ask para remediación,
  desarrollo y release autorizados; se eliminan asks duplicados y se explicitan
  asks de delegación/acceso exterior. No se altera política de secretos.
- Kiro orquestador: frontera fs_write deny con exclusiones documentales y asks de
  escritura/shell/subagent. No usar allow posterior para anular deny.
- Integridad Kiro acepta `match` omitido, válido para reglas por capability completa,
  y verifica tipos de `match`/`exclude` cuando están presentes. No debilita la
  detección de strings inválidos ni cambia contratos ajenos a permisos.
- Fuente del orquestador: workspace/web como evidencia, steering aplicable bajo
  reglas superiores; consentimiento técnico no reemplaza gates ni plan.
- [Matriz y decisiones por host/agente/modo](../../permisos-hosts.md): restricciones,
  red necesaria, mecanismos no soportados, shell como límite residual y recarga.
- **Archivos modificados por REC-02 — delta sobre el baseline heredado:**
  - `adapters/opencode/agents/code-review.json`
  - `adapters/opencode/agents/data-api.json`
  - `adapters/opencode/agents/documentation-orchestrator.json`
  - `adapters/opencode/agents/git-release-manager.json`
  - `adapters/opencode/agents/sdd.json`
  - `adapters/opencode/agents/ui-design.json`
  - `adapters/kiro/agents/documentation-orchestrator.json`
  - `canonical/agents/documentation-orchestrator.md`
  - `tools/test_integrity.py`
  - Nuevos: `tools/test_permissions.py`, `tools/test_permissions_host.py`,
    `docs/permisos-hosts.md` y `docs/auditoria/seguimiento/REC-02.md`.
  - Generados: los seis agentes de `generated/opencode/agents/`; el orquestador
    de `generated/kiro/agents/`, `generated/claude/agents/`,
    `generated/antigravity/agents/`, `generated/pi/agents/` y
    `generated/copilot/agents/documentation-orchestrator.agent.md`.
  Son **24 archivos** del delta REC-02; otras diferencias visibles contra HEAD
  pertenecen al baseline REC-01 y no deben incluirse como correcciones propias.
- **Distribución:** render/validate correctos en seis hosts; once agentes con
  delta REC-02, nunca edición manual de generated. Skills de secretos preservadas.
- **Cambios sin commit:** todo el trabajo de esta sesión; no staging, commit ni push.

## Verificaciones ejecutadas

| Fecha | Comando / escenario | Entorno | Resultado real | Evidencia |
|---|---|---|---|---|
| 2026-10-11 | Git status/worktree/HEAD/diff | Original antes de escribir | Un worktree main; 32 tracked modificados y nuevos REC-01; staging vacío | Baseline arriba |
| 2026-10-11 | `python3 -B tools/test_code_review_contract.py` | Baseline original | 7/7 PASS; solo estático | Contrato no comprueba ejecución de tools |
| 2026-10-11 | `git diff --check` | Baseline tracked original | Exit 0 | No incluye archivos nuevos |
| 2026-10-11 | Referencias oficiales | OpenCode/Kiro/Claude/Copilot/Antigravity/Pi | Semánticas contrastadas; dos URLs Antigravity exploratorias 404, sustituídas por subagents vigente | Enlaces en matriz; ningún 404 cuenta como referencia |
| 2026-10-11 | CLI versions | PATH local | OpenCode 1.18.34; Kiro 2.29.1; Pi 0.99.2 | No Claude/Copilot/Antigravity CLI en PATH |
| 2026-10-11 | `git worktree add -b remediation/rec-02 ... HEAD`; diffs Git | Worktree temporal propio | Creado e incorporado baseline sin commit; tres whitespace históricos en informe copiado | No corregir informes históricos por otro hallazgo |
| 2026-10-11 | `python3 -B tools/test_permissions.py` | Contratos estáticos | 8/8 inicialmente; 9/9 final tras añadir límite de patrones absolutos | Matriz de positivos/negativos y operaciones legítimas; no runtime |
| 2026-10-11 | `python3 -B tools/render.py`; `python3 -B tools/validate.py` | Worktree propio, tras ambas variantes de patrones | Exit 0; 10 skills, seis agentes, seis plataformas; hash-tree reproducible | Sin render en original |
| 2026-10-11 | Probe OpenCode durante desarrollo | HOME/XDG/fixtures temporales; proveedor local simulado | Intentos incompletos: timeout sin llamadas al proveedor; diagnóstico posterior `ProviderModelNotFoundError`, resuelto con modelo fixture explícito. Después FAIL de escritura legítima por patrones relativos. Variante absoluta: primer write PASS y espera incorrecta tras reject; corregida espera a estado idle y rutas temporales resueltas | Ningún intento incompleto cuenta como PASS; no falla atribuida a LLM real |
| 2026-10-11 | `AI_AGENTS_TEST_TMP=... python3 -B tools/test_permissions_host.py` | OpenCode 1.18.34; agentes generados reales; proveedor Anthropic simulado loopback | Final exit 0: **14 escenarios de controles + 2 limitaciones observadas**, tabla abajo. Un intento adicional al lanzar suites simultáneas agotó timeout antes de iniciar; reejecución aislada completa | Capturas API y efectos en archivos, sin eventos privados/credenciales; prompts/modelo no son evaluación de LLM |
| 2026-10-11 | `... python3 -B tools/test_permissions_host.py --host pi` | Pi 0.99.2; plantilla distribuida realmente cargada; modelos/config temporales, offline | Exit 0: tres escrituras por defecto confirman limitación (doc/producto/exterior); `--tools read` excluye write | No hay gate técnico por rol en la plantilla; ninguna equivalencia con OpenCode |
| 2026-10-11 | `... python3 -B tools/test_permissions_host.py --host kiro-formats` | Kiro CLI 2.29.1; HOME/XDG temporal, sin credenciales | CLI validate exit 1; wrapper exit 2: **bloqueado para runtime de reglas V3** | Solo comprobación de formato, no comandos/edición en host; no se atribuye la incompatibilidad al fix sin comparar baseline |
| 2026-10-11 | `python3 -B tools/test_integrity.py` | Worktree propio | Primera ejecución 414/415: test exigía match incluso cuando es opcional según referencia. Ajuste pertinente; final **415/415** | Incluye validate, negativos, links, identidad y documentación core |
| 2026-10-11 | `python3 -B tools/test_validate.py`; `python3 -B tools/test_mas_identity.py` | Distribución regenerada | 38/38 y 231/231 | Diagnósticos negativos esperados no son fallos |
| 2026-10-11 | `python3 -B tools/test_code_review_contract.py`; `python3 -B tools/test_documentation_core.py`; `python3 -B tools/test_handoff_contract.py` | Contratos preservados | 7, 12 y 34 pruebas correctas | Sin ampliar REC-03 ni modificar sus alcances |
| 2026-10-11 | `python3 -B tools/test_secret_policy.py` | Baseline REC-01 heredado, fuentes/copies regeneradas | 26/26 PASS | Regresión pertinente; no añade política de secretos |
| 2026-10-11 | `python3 -B tools/check_links.py`; `git diff --check` | Documentación y diffs tracked | Enlaces 80 archivos correctos; whitespace tracked exit 0 | Revalidación documental final tras completar ficha |
| 2026-10-11 | `git hash-object` de ocho archivos REC-01, en original y worktree | Original / copia aislada | Ocho hashes idénticos; original conserva diff de 32 tracked, 635/346; staging vacío | Scanner `3d13289b49d1ef0ee1dae2465425068d32600576`; ningún cambio REC-02 en original |
| 2026-10-11 | Integración selectiva del delta REC-02; paso CI para `tools/test_permissions.py` | `main`, con cambios locales REC-01 preservados | Fuentes/adaptadores/tests/docs copiados desde la rama de trabajo; sin aplicar el diff global del worktree | Se conservó la worktree `remediation/rec-02`; no hubo staging ni commit |
| 2026-10-11 | `python3 tools/render.py`; `python3 tools/validate.py` | `main`, fuentes REC-01 + REC-02 | Exit 0; validación correcta: 10 skills, 6 agentes y 6 plataformas | Distribuciones regeneradas desde canonical/adapters combinados |
| 2026-10-11 | Tests integrados: integridad, permisos, secretos, Code Review, documentación core y handoff | `main` | 415/415; 9/9; 26/26; 7/7; 12/12; 34/34 PASS, respectivamente | `tools/test_permissions.py` queda incluido en CI; CI remoto no ejecutado |
| 2026-10-11 | `AI_AGENTS_TEST_TMP=/tmp python3 -B tools/test_permissions_host.py` | OpenCode 1.18.34, fuentes/distribuciones integradas | 14 escenarios de controles PASS + 2 limitaciones observadas | Harness local simulado; no acredita conducta de LLM ni consentimiento humano |
| 2026-10-11 | `AI_AGENTS_TEST_TMP=/tmp python3 -B tools/test_permissions_host.py --host pi` | Pi 0.99.2, distribución integrada | 3 limitaciones observadas + exclusión explícita de `write` con `--tools read`; exit 0 | No hay gate técnico por rol en la plantilla |
| 2026-10-11 | `python3 tools/check_links.py`; `git diff --check` | `main` | Enlaces correctos en 80 archivos; whitespace tracked exit 0 | `git diff --check` no incluye archivos nuevos no rastreados |

### Evidencia del motor OpenCode — fixture determinista

La configuración global artificial concede allow general y prefijos shell allow
más específicos; los agentes distribuidos cargados conservan su prioridad.
Cada `once`/`reject` es una respuesta real a una solicitud de permisos del servidor,
emitida **por el harness**, no por una persona. Ningún script hace commit o push.

| Escenario | Tool / consentimiento observado | Resultado |
|---|---|---|
| Escritura `.architecture/approved.txt` | write / edit → once | Archivo creado con contenido fixture; PASS |
| Escritura `.data/rejected.txt` | write / edit → reject | Error de permisos y archivo ausente; PASS |
| Producto `src/denied.txt` | write / deny, sin solicitud | Error de regla y archivo ausente; PASS |
| Spec `.sdd/denied.txt` | write / deny, sin solicitud | Error de regla y archivo ausente; PASS |
| Archivo exterior `../outside.txt` | external_directory → once, luego edit deny | Archivo ausente; PASS |
| Remediación de code-review `src/remediation.txt` | write / edit → once | Archivo creado; operación legítima preservada, PASS |
| Consulta Git del orquestador | bash → once | git status correcto; PASS |
| Consulta Git del especialista bajo allow global específico | bash → once | Catch-all ask del agente prevalece; PASS |
| `git add --dry-run src` del orquestador | bash / deny sin solicitud | Error de permisos antes de comando; PASS |
| `rm nonexistent-rec02-fixture` | bash / deny sin solicitud | Error de regla, sin borrados; PASS |
| Shell escribe documentación | bash → once | Archivo fixture creado; PASS |
| Shell intenta escribir producto | bash → reject | Error de permisos, archivo ausente; PASS |
| `git status && python3 ...` | bash → reject | Comando compuesto bloqueado, archivo ausente; PASS |
| `.data/` en directorio externo | external_directory → reject | Archivo ausente; PASS de consentimiento, no deny absoluto de ese nombre |
| Shell escribe producto tras aprobar | bash → once | Archivo creado: **LIMITACIÓN**, no PASS de aislamiento |
| `.architecture/link` apunta a `src/` | write / edit → once | Escritura llega a producto: **LIMITACIÓN**, no PASS de aislamiento |

No se prueban aquí delegación real, todos los agentes/modos, `edit`/`apply_patch`
ni ataques conversacionales. Los patrones por nombre no fijan el cwd, no resuelven
symlinks y el shell aprobado conserva capacidad de escritura. Una frontera fuerte
requiere sandbox/controles del proceso configurados por sesión y probados; el kit
no instala ese entorno como parte de REC-02.

### Snapshot de fuentes probadas — hashes Git de contenido

| Archivo | Hash |
|---|---|
| `canonical/agents/documentation-orchestrator.md` | `8b55eef943aaa9a668ff2012b705cc8055a6804d` |
| `adapters/opencode/agents/documentation-orchestrator.json` | `b1daaea77684914ef390dd19d9d887e37ee3f52b` |
| `adapters/kiro/agents/documentation-orchestrator.json` | `4b7c02ec2a2adca306b2ba377dffa61fc1874043` |
| `tools/test_permissions.py` | `a2525c6ff164593b72cd6ce57e3004af8fb6754d` |
| `tools/test_permissions_host.py` | `34c92c2d4bf9fac934efe2a0667afb82ca95655b` |
| `tools/test_integrity.py` | `e6111ef88f7b3105a829279940c11f7abc6124e9` |
| `docs/permisos-hosts.md` | `5cc7fcb868dec3f7cdf6ccaa642404d2ea258c46` |

## Criterios de cierre

| Criterio original | Estado | Evidencia / siguiente paso |
|---|---|---|
| Capacidades por agente y modo; consulta vs remediación autorizada | Documentado y parcialmente probado | OpenCode acredita doc y remediación aprobadas; selección semántica de modo/gates pendiente de modelo real |
| Matriz por host y semántica vigente | Documentado | Referencias oficiales; distinguir Kiro V3 y CLI 2.x |
| Restricciones soportadas y redundancias con precedencia comprobada | Parcial acreditado | OpenCode: pruebas estáticas y motor sobre allow global específico; Kiro por documentación/esquema, runtime V3 pendiente |
| Pruebas inocuas de edición/comandos dentro y fuera de alcance | Parcial acreditado | OpenCode y Pi ejecutados; Kiro compatible/Claude/Copilot/Antigravity pendientes; límites de shell/enlaces observados |
| Evidencia de autorizaciones reales | Motor acreditado; conducta/humano pendiente | Solicitudes y replies del servidor ejercitados por harness; no aprobación humana ni gates de plan/modelo |
| Red justificada sin ask universal | Documentado | `webfetch: allow` preservado por necesidad de investigación; shell/MCP no cubiertos |
| Fronteras de confianza workspace/web y controles no soportados | Documentado; límites runtime observados; conducta pendiente | Matriz, fuente y probes; no afirmar resistencia a prompt injection sin prueba |
| Distribuciones y resultado integrado verificados | Integrado localmente; verificación parcial | Render/validate y suites locales correctos en `main`; falta CI remoto y runtime en hosts no disponibles |

## Pendientes y entrega

- **Bloqueos concretos:** Kiro compatible V3 no disponible; Claude/Copilot/Antigravity
  CLI ausentes en PATH; no se dispuso de sesión de LLM real/perfil de consentimiento
  humano para estos contratos. No instalar ni copiar credenciales para resolverlo.
- **Pendientes concretos:** probar edición y comandos con reglas Kiro V3 activas;
  scopes/gates en las otras superficies; OpenCode delegación y variantes edit/patch;
  consulta/auditoría/remediación con LLM real, autorización humana y solicitudes
  embebidas en web/workspace. Ejecutar CI remoto en un flujo autorizado.
- **Estado actual:** integrado localmente en `main`, pendiente de verificación completa;
  hallazgo abierto. Los límites documentados no se presentan como enforcement efectivo
  ni como fallos totalmente remediados.
- No se administran fases SDD; antecedentes copiados se conservan como baseline.
- No hubo staging, commit ni push. La worktree fuente `remediation/rec-02` permanece
  abierta; sus cambios se copiaron selectivamente, pero no se hizo un `git merge`.
  Conservarla hasta coordinar su limpieza.

## Historial local

| Fecha | Evento | Evidencia | Pendientes |
|---|---|---|---|
| 2026-10-11 | Diagnóstico → bloqueado por aislamiento | Única carpeta ocupada por REC-01; diagnóstico solo lectura | Worktree propio |
| 2026-10-11 | Aislamiento → en curso | Usuario pide continuar; rama/worktree propio y baseline local heredado | Corrección/verificación posible |
| 2026-10-11 | En curso → corregido en rama parcial | Fuentes, nueve tests, 415 checks, 16 escenarios OpenCode y cuatro Pi; render/validate locales; hashes registrados | Runtime restante, humano/LLM e integración; no cierre |
| 2026-10-11 | Rama parcial → integrado pendiente de verificación | Delta selectivo en `main`; render/validate y suites integradas PASS; probes OpenCode/Pi repetidos | Kiro V3, otros hosts, LLM/consentimiento humano y CI remoto; no cierre |

## Integración y cierre

- **Destino y baseline:** `main`, HEAD base `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`, más los cambios locales preexistentes de REC-01 y el delta selectivo de REC-02. No se aplicó el diff completo de la worktree parcial.
- **Fecha / responsable:** 2026-10-11; sesión coordinadora.
- **Integración:** fuentes, adaptadores, pruebas y matriz copiados de forma selectiva; se añadió `tools/test_permissions.py` al workflow CI; se regeneró `generated/` desde las fuentes combinadas. La ficha de REC-02 y el tablero fueron actualizados.
- **Verificación integrada:** `render.py`, `validate.py`, integridad (415/415), permisos (9/9), secret policy (26/26), Code Review (7/7), documentación core (12/12), handoff (34/34), enlaces (80 archivos), OpenCode (14 escenarios + 2 limitaciones) y Pi (limitaciones documentadas + `--tools read`) pasaron según los resultados registrados arriba.
- **Estado global:** integrado localmente, pendiente de verificación completa y abierto. No se ejecutó CI remoto; falta runtime Kiro V3, otros hosts y evidencia de conducta LLM/consentimiento humano.
- **Git:** sin staging, commit ni push. La worktree de origen `remediation/rec-02` sigue abierta como snapshot de implementación; no se eliminó.
