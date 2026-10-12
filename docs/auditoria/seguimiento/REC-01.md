# Resultado de remediación — REC-01: Unificar la política de secretos

## Identificación y asignación

- **Estado local / estado propuesto:** integrado pendiente de verificación; implementación local y suites acreditadas, conducta del host pendiente. No cerrado.
- **Responsable / sesión:** asistente SDD de esta conversación, asignada exclusivamente a REC-01.
- **Rol:** coordinadora e implementadora exclusiva en la carpeta original; sin subagentes escritores.
- **Fecha de preparación:** 2026-10-10.
- **Fecha de inicio / última actualización:** 2026-10-10 / 2026-10-11.
- **Repositorio / worktree / rama:** `ai-agents-kit`, carpeta original, único worktree registrado, rama `main`.
- **Baseline HEAD y cambios previos sin commit:** `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`; sin diferencias tracked ni staged al inicio. Directorios previos sin seguimiento: `.sdd/specs/laboratorio-evaluacion-sdd/f10-no-sdd/`, `docs/auditoria/` y `docs/presentations/`. Se preservan; los documentos de auditoría no son un commit de preparación.
- **Archivos afectados:** `canonical/skills/git-commit/SKILL.md` y su nuevo `scripts/check_secrets.py`; `canonical/skills/release-management/SKILL.md`; `canonical/skills/security/SKILL.md`; `canonical/agents/git-release-manager.md`; `tools/check_secrets.py`, `tools/test_secret_policy.py`, `tools/test_secret_policy_host.py`; `.github/workflows/ci.yml`; `docs/agentes/git-release-manager.md`, `docs/desarrollo.md`, `docs/mejoras.md`; los cuatro artefactos de `.sdd/specs/rec-01-politica-secretos/`; esta ficha y únicamente REC-01/historial del consolidado. En cada una de las seis plataformas: agente Git/release, skills Git/release/security y nuevo script de Git, regenerados mediante renderer.
- **Recursos externos:** no asignados. Probar con fixtures y perfiles temporales; no instalar configuración global.
- **Entorno verificado:** macOS, Python 3.12.4, Git 2.50.1 (Apple Git-155), OpenCode CLI 1.18.34. No se ejecutó Python 3.10, Windows nativo ni CI remota.
- **Coordinación:** REC-02, REC-15 y FUT-17/18 constan pendientes y sin responsable en sus tableros. Esta sesión no los remedia. La terminal previamente detectada en `.docs/` ya no aparece en la comprobación de procesos al reanudar; no se detectó otra sesión escritora. La comprobación es puntual, no un lock ni garantía sobre sesiones remotas; se repetirá antes de implementación. No se trabaja ni escribe en `.docs/`.
- **Flujo SDD:** standard; Gates 1–3 aprobados mediante «procede» a las solicitudes correspondientes. [Tareas](../../../.sdd/specs/rec-01-politica-secretos/tasks.md) implementadas salvo evidencia conductual de host; [Verification](../../../.sdd/specs/rec-01-politica-secretos/verification.md) registra matriz, límites y hashes de fuentes. Gate 4 pendiente; no se propone cierre con esa evidencia ausente.
- **Ficha de referencia:** [Consolidado, sección REC-01](../CONSOLIDADO-HALLAZGOS-RECURRENTES.md).
- **Protocolo:** [Remediación entre sesiones](../PROTOCOLO-REMEDIACION.md).

## Diagnóstico actual

- **Vigencia:** contradicción confirmada al inicio y corregida en fuentes/distribuciones locales. Dos probes de host incompletos no acreditan resolución conductual.
- **Evidencia histórica:** DeepSeek AUD-01; GPT H04; Estudio EST-001, según la ficha del consolidado.
- **Evidencia de diagnóstico en baseline `ruta:línea`:** `canonical/skills/git-commit/SKILL.md:34,83–106` permitía incluir sensibles con autorización sin separar secretos confirmados; `canonical/skills/release-management/SKILL.md:314–316` heredaba el Paso 1.5; `README.md:174` prohíbe commits de secretos. Estas líneas describen el baseline, no la redacción corregida. Resultado local identificado por hashes en Verification.
- **Deuda existente vinculada:** [Mejoras, sección P0.5 — Seguridad mínima exigible](../../mejoras.md). Punto de política conserva checkbox abierto por host pendiente; control local/CI marcado disponible y verificado con fixtures, sin afirmar run remoto ni detección universal. Los puntos de permisos, gitignore y prompt injection no se modificaron.
- **Diferencias respecto de los informes:** la contradicción ya no aparece en las fuentes corregidas y sus copias; la conducta del modelo no está acreditada. No se afirma una filtración histórica. `.security/` documenta F07, no este flujo; arquitectura/Navigator carecen de baseline Git verificable y solo orientan.

## Solución aplicada

1. Git excluye secretos confirmados sin excepción de autorización. Distingue
   nombre sospechoso, indicio no resuelto, configuración pública y placeholder;
   preserva confirmaciones de commit/push y no desstagea trabajo ajeno automáticamente.
2. Release, seguridad, agente y guía Git/release aplican el mismo criterio. La
   inspección comienza por metadatos; no se imprime un diff bruto para detectar secretos.
3. Control Python distribuible de solo lectura: firmas de claves privadas y formatos
   completos conocidos de tokens GitHub. Modos de candidatos explícitos, blobs del
   índice y working tree tracked; códigos 0/1/2, sin override ni valores en diagnósticos.
   No cambia archivos, staging o refs, no hace red y no garantiza detección universal.
4. Wrapper de fuente única y paso CI `--tracked`, más suite de negativos. Ejemplos
   de publicación usan `&&` y se comprobó la interrupción con una operación ficticia,
   nunca `git commit`. No se instalaron hooks ni restricciones nuevas de REC-02.
5. Distribuciones regeneradas en seis plataformas; documentación y deuda P0.5
   actualizadas según evidencia. Instaladores probados solo con HOME temporales.
6. Probe host reproducible sin heredar credenciales ni configuración global:
   dos intentos incompletos, registrados abajo. No se convirtió el resultado en PASS.

Cambios presentes en esta carpeta original, **sin commit ni staging de esta sesión**.
No se escribieron `.docs/`, configuraciones globales ni registros de otros hallazgos.

## Verificaciones ejecutadas

| Fecha | Comando / escenario | Entorno / fuente probada | Resultado real | Evidencia sanitizada |
|---|---|---|---|---|
| 2026-10-10 | `git status --short --untracked-files=normal`, `git rev-parse HEAD`, `git branch --show-current`, `git worktree list --porcelain`, `git diff --stat`, `git diff --cached --stat` | Carpeta original / `main` | HEAD y único worktree confirmados; tracked/staging sin diferencias; tres directorios previos sin seguimiento | Baseline y lista de directorios en esta ficha; sin dumps de contenido |
| 2026-10-10 | `ps -axo pid,ppid,comm` y `lsof -a -d cwd -F pn`, filtrados al repositorio; comprobación de descendientes de la terminal 9371 | Procesos locales al reanudar | Terminal antes detectada en `.docs/` ausente; procesos transitorios de las herramientas de esta sesión; ninguna otra sesión escritora detectada | Comprobación puntual, sin garantía de exclusión mutua |
| 2026-10-10 | Lectura directa de Git, release, README y deuda P0.5 | Fuentes actuales | Contradicción confirmada; no es prueba runtime | Referencias actuales en Diagnóstico |
| 2026-10-10 | `python3 tools/check_links.py` | Documentación del repositorio | Primera ejecución: salida 1 por dos anclas de esta ficha (una previa, otra añadida). Se sustituyeron por enlaces al documento con sección indicada. Reejecución: salida 0, 78 archivos correctos | Diagnósticos de rutas/anclas, sin contenido sensible |
| 2026-10-10 | `python3 -c 'from tools.check_links import ROOT, check_links; paths=[ROOT/".sdd/specs/rec-01-politica-secretos/bugfix.md", ROOT/"docs/auditoria/seguimiento/REC-01.md", ROOT/"docs/auditoria/CONSOLIDADO-HALLAZGOS-RECURRENTES.md"]; errors=check_links(ROOT,paths); print("\n".join(errors) if errors else "Enlaces de REC-01: 3 archivos correctos"); raise SystemExit(bool(errors))'` | Spec y dos registros de REC-01 | Salida 0; enlaces de los tres archivos correctos, incluida la spec fuera del escaneo predeterminado | Comprobación documental; no acredita el fix ni runtime |
| 2026-10-10 | `git diff --check` y `git status --short --untracked-files=normal` | Working tree | Salida 0; la spec y auditoría siguen sin seguimiento. `diff --check` solo cubre diffs tracked, no esos archivos nuevos | Sin staging, commit, push ni instalaciones |
| 2026-10-10 | `python3 tools/validate.py` | Fuentes y distribuciones previas al fix | Salida 0; 10 skills, 6 agentes, 6 plataformas | Baseline, no prueba del control propuesto; el validador renderiza solo en temporal |
| 2026-10-10 | `python3 tools/test_mas_identity.py` | Contratos previos al fix | Salida 0; 231/231 comprobaciones | Identidad MAS preservada en baseline |
| 2026-10-10 | `opencode --version`; búsqueda de scanner en fuentes y CI; `command -v gitleaks` | CLI local y repositorio | OpenCode 1.18.34 disponible; no se encontró scanner integrado; gitleaks no disponible en PATH | Ninguna ejecución de agente ni instalación global |
| 2026-10-11 | `python3 -m unittest tools.test_secret_policy.ContractTests.test_no_unconditional_sensitive_override tools.test_secret_policy.ScannerTests.test_scan_detects_signature` | Contrato previo y detector inicial sin coincidencias | RED: dos fallos esperados por oferta genérica y falta de detección de firma sintética. No es RED runtime del modelo | Motivos de fallo, sin valores del fixture; primera ejecución contractual por separado también falló |
| 2026-10-11 | `python3 tools/test_secret_policy.py` (con `AI_AGENTS_TEST_TMP` temporal aprobado localmente) | Resultado integrado, Git temporal sin commits y seis scripts distribuidos | GREEN final: 26/26; firmas, contrastes, sanitización, índice exacto, fallos, solo lectura y cadena `&&` | Tests con capturas comprueban ausencia del valor; pruebas tardías de integración no se atribuyen a TDD individual |
| 2026-10-11 | `python3 tools/check_secrets.py --tracked`; control sobre nueve rutas nuevas explícitas | 577 tracked del working tree, más control/wrapper/tests/probe/spec/registros nuevos | Salida 0; sin coincidencias soportadas, no certifica ausencia universal | No se imprimió contenido; selección de entradas descrita en Verification |
| 2026-10-11 | `python3 tools/render.py`; `python3 tools/validate.py`; `python3 tools/check_links.py` | Carpeta integrada tras el cambio | Salida 0; seis distribuciones coherentes, 10 skills/6 agentes; 78 documentos con enlaces correctos | No edición manual de generated; copias ejecutadas sobre fixtures en suite REC-01 |
| 2026-10-11 | `python3 tools/test_validate.py`; `python3 tools/test_integrity.py`; `python3 tools/test_mas_identity.py` | Fuentes/distribuciones locales | Salida 0: 38/38, 415/415 y 231/231, respectivamente | Diagnósticos de negativos esperados, no fallos de la suite |
| 2026-10-11 | `python3 tools/test_documentation_core.py`; `python3 tools/test_handoff_contract.py`; `python3 tools/test_links.py`; `python3 tools/test_code_review_contract.py` | Contratos pertinentes | Salida 0: 12, 34, 4 y 7 pruebas, respectivamente | Autorizaciones/identidad/contratos preservados; no prueban runtime |
| 2026-10-11 | `python3 tools/test_install.py` | Instalaciones en HOME temporales | Salida 0: 196/196 | Sin instalación global; no certifica runtime de agentes |
| 2026-10-11 | `python3 tools/test_secret_policy_host.py` (con temporal local aprobado); `opencode run --help` | OpenCode CLI 1.18.34; HOME/XDG nuevos, sin credenciales heredadas; fuentes modificadas copiadas/cargadas explícitamente | Intento 1: probe sale 2, proveedor/modelo o autenticación no disponible. Intento 2 endurecido: sale 2 por timeout de 90 s. **No PASS** | Solo resúmenes sanitizados; ningún evento bruto conservado ni decisión de inclusión acreditada |
| 2026-10-11 | `git hash-object` de fuentes críticas; `git diff --cached --stat`; `git diff --check` | Resultado local sin commit | Hashes de fuente en Verification; staging original sin diferencias; check tracked sale 0 | No commit, push, tag ni release |
| 2026-10-11 | Reejecución final: render; validate, suite REC-01, validate negativos, integrity, MAS identity, documentation core, handoff, links tests, code review, install y check_links; control tracked y diez rutas nuevas explícitas | Resultado integrado tras deshabilitar lazy fetch/fsmonitor/maintenance en el adaptador Git del control | Todos salen 0; 26 tests REC-01; 577 tracked y diez entradas sin coincidencias soportadas | Hash final del scanner `3d13289b49d1ef0ee1dae2465425068d32600576`; controles no son sandbox ni detección universal |

## Criterios de cierre

| Criterio | Estado | Evidencia | Próximo paso |
|---|---|---|---|
| Política coherente entre Git, release, seguridad y consumidores pertinentes | Acreditado en fuentes/distribuciones | Contratos, regresión y render/validate | Revalidar si cambian fuentes; conducta de host no incluida en este PASS documental. |
| Fixture sintético detectable excluido aunque se solicite incluirlo | Parcial; host pendiente | Control rechaza, sin override; cadena `&&` no ejecuta operación ficticia posterior; probes host incompletos | Acreditar decisión del agente ante petición explícita de inclusión; sin commit real. |
| Configuración pública y placeholders no clasificados por nombre solamente | Acreditado en control; host pendiente | Contrastes `.env`, servicios públicos, placeholders y staging aceptados por contenido | Completar contraste conversacional en host. |
| Mensajes no reproducen valores sensibles | Acreditado en control; host pendiente | Capturas stdout/stderr, errores/rutas sanitizados; evidencia sin valores | Completar respuesta y herramientas de host; no atribuir ausencia universal a un probe incompleto. |
| Deuda existente vinculada y actualizada según evidencia | Acreditado | P0.5 actualizado; política abierta por conducta pendiente y control integrado registrado | No cerrar política/P0.5 completo hasta evidencia; otros puntos quedan intactos. |
| Fuentes y distribuciones coherentes y comprobaciones pertinentes satisfechas | Acreditado localmente | Render/validate, 26 tests y suites, seis copias distribuidas ejecutadas | No afirmar CI remota, Windows nativo ni runtime multi-host no ejecutados. |

## Pendientes y entrega

- **Bloqueos:** conducta en host sin ejecución completa: perfil aislado sin proveedor/autenticación operativo acreditado; segundo intento agotó 90 s. No copiar credenciales al repo ni instalar globalmente para resolverlo.
- **Verificaciones no acreditadas:** decisión conversacional de exclusión pese a solicitud, contrastes públicos/placeholders y mensajes/herramientas sin exposición en ejecución completa del agente; CI remota no ejecutada por ausencia de push autorizado. No se certifica runtime multi-host ni Windows nativo.
- **Solapamientos:** consumidores/test con REC-02; skill Git con REC-15/FUT-17; release con FUT-18. Sin asignaciones en tableros; coordinar si cambia esa condición.
- **Estado propuesto:** integrado pendiente de verificación; cambio local coordinado sin commit, **no cerrado**.
- **Siguiente acción:** disponer de un perfil/sesión de prueba autorizado con proveedor operativo; ejecutar escenario de inclusión y contrastes con fuentes identificadas y registrar herramientas/decisión sanitizadas. No solicitar cambio de modelo ni reemplazar conducta por coincidencias textuales. Solo después resolver Gate 4 y cierre de REC-01.

## Historial local

| Fecha | Transición / evento | Trabajo y evidencia | Pendientes |
|---|---|---|---|
| 2026-10-10 | Preparación → Pendiente | Ficha y prompt creados; ninguna corrección aplicada. | Asignar, inspeccionar, implementar y verificar. |
| 2026-10-10 | Pendiente → Confirmado | Sesión SDD asume coordinación e implementación exclusiva; baseline `03f30be` / `main`; contradicción confirmada y requisitos propuestos. Sin fix ni commit. | Gate 1; diseño, tareas, implementación y verificación posteriores. |
| 2026-10-10 | Confirmado → Confirmado; avance SDD | Gate 1 aprobado por el usuario; diseño propuesto con control acotado y límites; baseline técnico verde. Sin fix ni commit. | Gate 2; Tasks, Gate 3, implementación y verificación. |
| 2026-10-10 | Confirmado → Confirmado; avance SDD | Gate 2 aprobado; ocho tareas trazadas y secuenciales propuestas. Ninguna tarea implementada ni commit realizado. | Gate 3 para empezar; verificación host pendiente de ejecución. |
| 2026-10-11 | Confirmado → En curso | Gate 3 aprobado mediante «procede»; baseline/exclusividad revalidados y sin reservas solapadas en tableros; inicia implementación exclusiva. | Regresiones, control, distribución y evidencia conductual. |
| 2026-10-11 | En curso → Integrado pendiente de verificación | Política/control/CI/docs presentes en carpeta original sin commit; 26 tests REC-01 y suites pertinentes verdes; distribuciones coherentes. Verification registra fuentes/hashes y dos probes incompletos. | Conducta de host pendiente; no cerrado. |

## Integración y cierre — completa la coordinadora

- **Destino y baseline final:** carpeta original `main`, HEAD permanece `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880` más cambios locales sin commit. Hashes de fuentes críticas y matriz en Verification; no se presenta HEAD como commit del fix.
- **Fecha / responsable de integración:** 2026-10-11 / esta sesión SDD coordinadora e implementadora exclusiva; integración local, no merge Git.
- **Verificación del resultado integrado:** suites y distribución acreditadas; host incompleto. No se altera trabajo previo de laboratorio/presentaciones ni otros registros.
- **Estado global final / pendientes:** integrado pendiente de verificación; falta evidencia conductual del agente. No cierre ni Gate 4 aprobado.
- **Fecha de cierre o no vigencia:** no aplica.
- **Fila e historial del tablero actualizados:** únicamente REC-01 y sus entradas históricas; integración local pendiente de conducta, sin alterar otros IDs ni informes originales.
