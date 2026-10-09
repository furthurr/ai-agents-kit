# Verification — Evaluador F07

- Modo SDD: standard
- Fase: 4 — Verification
- Estado: verificación aprobada; sub-spec cerrada
- Gate 1–3: aprobados
- Gate 4: aprobado explícitamente por el usuario («apruebo y autorizo»)
- Kickoff F07: autorizado explícitamente por el usuario con las condiciones de §6
- Continuación para Verification: autorizada por usuario («continúa»)
- Alcance: sub-spec del evaluador; no cierra campaña10/spec principal ni mide el modelo F07

## 1. Resultado y condiciones verificadas

La integridad de las tareas marcadas `[x]` se contrastó con fuentes y reportes
existentes. Los 24 criterios B y seis garantías I disponen de evidencia en el
alcance declarado y bajo los supuestos de host/daemon/imagen confiables.

Se detectó y corrigió durante Verification una clasificación de JSON inválido
emitido por candidato: ahora `run_workers` lo identifica como `candidate_reply_invalid`.
La negativa Docker correspondiente pasa, se regeneró la imagen/calibración y se
reauditó el cambio; revisión anterior archivada, fingerprints actualizados.

**No hubo llamadas al modelo F07.** Referencias/mutaciones y actor falso sirven
para validar el evaluador, no para atribuir éxito a Luna/MAX.

## 2. Evidencia consultable

Abreviaturas; paths relativos a `.agent-lab/sdd-escalation/` salvo S:

- P: `runs/f07-supervisor-check-e935168f80654711b22c0eb9544bad8c/report.json`.
- C: `runs/f07-observed-calibration-9679d6c672cc497a926c36d8c938b815/report.json`.
- L: `runs/pilot-26437e0d-0005-4941-9366-9687e9ccc7ac/` (E2E lite final actualizado).
- A: `runs/pilot-f0002f1f-9682-435c-bdba-4259d712c157/` (E2E standard previo a corrección localizada del decoder; flujo no alterado).
- S: `.security/reviews/f07-2026-10-07.md`, revalidación durante Verification.
- R: `runtime/pilot-review.json`, registro scope F07, IA técnica, no certificación/aprobación humana/modelos.
- G: `runtime/f07-evaluator.local.json`, preparación calibrada, no revisión por sí misma.
- T: `runner/tests/`; código inspector/supervisor en `evaluator/supervisor.py`.
- W: `results/f07-wave1-boundary.md` y reportes del prototipo/reproducción.

Imagen final por content ID:
`sha256:dc7f368671b5cccb0c8c436976aed040fbc106e7dd0e13e5883e29b212eac902`.
R incluye hashes de fuentes y G, por lo que drift de imagen/config invalida el gate.

## 3. Ciclo de pruebas y checks

- Estrategia: regresión/caracterización del prototipo y TDD focalizado selectivo.
- RED observado: validador administrativo ausente, perfil dedicado ausente,
  reentrada que mataba workers activos, actor/runner que bloqueaban tokens N/A.
- Reproducción independiente: falso stock/reserva sin persistencia, writer
  desacoplado y sustitución de path después de `lstat` en W.
- GREEN/integración final: P pasa negativas (incluido JSON inválido), WAL/hot journal,
  reemplazo concurrente/parent protegido, hardlink/FIFO, replay, identidad y cleanup.
- C: referencia **6/6**, skeleton **0/6** (NotImplementedError), falso stock 0/6,
  sin persistencia 0/6, doble cancelación 2/6, sobreventa 3/6 y escritura oficial 0/6.
  Las cinco mutaciones son rechazadas como éxitos completos; criterio/cause individual en C.
- L: actor falso, 3 fases, 6/6, entrega congelada, evaluación aparte, cero modelos.
- A: actor falso, 5 fases, 6/6, cero modelos, decisiones estructurales experimentales.
- Suite de Verification: `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest runner/tests snapshots --import-mode=importlib -m 'not acceptance' -q` → **861 passed, 1 deselected**.
- `compileall` sobre runner/tests/evaluator y registro de revisión; `git diff --check` → pasan.

No se afirma TDD por tests agregados después del GREEN: negativas adicionales,
recuperación y escenarios de carreras son integración/regresión/caracterización.
PBT no añadido según Design §7; PBT F04/F09 de la spec principal sigue pendiente.
La única deselection es aceptación inicial F10 para baseline, no un criterio F07.

## 4. Matriz requisito → tarea → test/evidencia

| Req | Tareas | Test / evidencia | Estado |
|---|---|---|---|
| B01 | 1.2,2.1–2.2,3.3,5.1 | UID/administración/imagen y escritura oficial denegados en P,W,C; perfiles y S | Verificado |
| B02 | 1.1,3.1–3.2,4.1 | Inspector separado, stock 999 vs estado 2; `test_f07_rpc.py`, P,C,L | Verificado |
| B03 | 2.3,3.1 | 40 writers `setsid`, quiescencia antes de captura, EVIDENCE protegida; P,S | Verificado |
| B04 | 4.1,4.4 | `ObservedStockMismatch`, falso stock/no persistencia en C, criterio/cause y observación conservados | Verificado |
| B05 | 2.3,3.2,4.4 | `test_failed_quiescence_never_inspects_or_claims_success`, tests de identidad/fallo/report; P | Verificado |
| B06 | 1.2,2.2,3.3 | IDs hex/host path hash, rechazo paths/comandos y group identity; T,P | Verificado |
| B07 | 3.1 | symlink/hardlink/FIFO/replacement negativas, parent rename denegado y ownership/FD; P | Verificado |
| B08 | 1.1,3.1 | Reproducción del open vulnerable en W, replacement concurrente y apertura tras writers eliminados en P | Verificado |
| B09 | 3.1,3.3,4.4 | Causas fijas/paths allowlisted, error checkpoint/terminación, sin contenido del destino; T,P | Verificado |
| B10 | 1.1,4.1,5.1 | Contrato/snapshot congelados en W; F07-01–06 originales, transacciones solo del candidato; C,L | Verificado |
| B11 | 4.2 | Bootstrap/barrier anterior a import, pids e intervalos; carreras de C y P, sin mutex dentro del grupo | Verificado |
| B12 | 4.1–4.2 | Workers/instancias nuevas, initialize reiterado y almacén persistente; F07-04–06 en C | Verificado |
| B13 | 1.1,4.1 | Contrato/snapshot hashes preservados, nuevo perfil/evaluador versionado; no mediador implementa negocio; W,G,S | Verificado |
| B14 | 4.3 | L summary `lite_forced_experimental:true`, no compliance canónico; CLI summary tests | Verificado |
| B15 | 3.4 | Tests stream/actor/pilot/CLI tokens None/N/A, cantidad no corta; fuentes y T | Verificado |
| B16 | 3.4,5.2 | Tests USD/timeout/steps/output independientes; request validation y aprobación obligatoria | Verificado |
| B17 | 3.3 | Duplicates/nonfinite/depth/nodes/bytes, identidad/hashes/tipos; `test_f07_supervisor.py`, `test_f07_rpc.py` | Verificado |
| B18 | 3.3,4.4 | JSON inválido candidato en P, Sticky candidate vs infrastructure y final report tests en T | Verificado |
| B19 | 2.3,5.1 | Scope ownership, `ps` tras remove, cleanup no verificable rechazado, failures saneados; T,P,C | Verificado |
| B20 | 5.1 | C referencia 6/6, skeleton 0/6 por comportamiento ausente; cero modelos | Verificado |
| B21 | 4.1,5.1 | Cinco mutaciones C, causas individuales, escritura oficial denegada y observación externa | Verificado |
| B22 | 5.3 | S,R,G y source fingerprints; findings SEC-0001/2 limitados al scope | Verificado |
| B23 | 4.3,5.4 | Scope/drift/image tests; waiver F01–F04 no admite F07; R vigente para imagen final | Verificado |
| B24 | 3.4,4.3 | CLI required approval/model/variant/USD/time/steps y fake-before-activity tests; ningún launch real aquí | Verificado |
| I01 | 2.1,3.2,5.2 | Candidato solo Docker, inspector en proceso aislado; sin repo/auth/socket/mounts host; P,S | Verificado |
| I02 | 3.4,5.2 | Actor flags/recibos/selection mismatch tests, propagación explícita; suite T | Verificado |
| I03 | 1.1,4.4,5.5 | Nuevos IDs/artifacts exclusivos y reportes históricos preservados, diferencias de condiciones documentadas | Verificado |
| I04 | 5.4 | Waiver sigue limitado sin revisión; R solo F07 y reviewer IA explícito, certification/human approval false | Verificado |
| I05 | 4.3 | L/A metadata autonomous/structural, canonical_gate_compliance false; no skill canónica modificada para campaña | Verificado |
| I06 | 2.1,5.2 | Lab permanece local ignorado por política Git; `.gitignore` no fue editado por esta remediación | Verificado |

## 5. Quality bar y RNF

| RNF (Design §6–8) | Evidencia | Resultado |
|---|---|---|
| Aislamiento | Roles UID, inspector/código protegido, Docker flags efectivos, sin código/SQLite candidata en host | Cumple scope |
| Integridad | Quiescencia, FD/path rejection, contraste stock/holds, hashes y checkpoints, negativa de escritura oficial | Cumple scope |
| Reproducibilidad | G/R content ID y fingerprints, IDs de criterio, mismo snapshot y fuentes, reportes individuales | Cumple scope |
| Límites | USD blando, deadline/steps/bytes/pids/memoria/CPU, tokens sin tope y N/A real | Cumple scope |
| Cleanup | PID handles/reaping/ownership, rechazo de ausencia no verificable, timeout y replay pruebas | Cumple ejecución supervisada |

Composition root en pilot, adaptadores explícitos, storage encapsulado, errores
tipados/saneados y sin singletons. No UI. Excepción de supervisor administrativo
con capacidades mínimas probadas permanece explícita y revisada, no heredada por
el candidato. Fuentes/fixtures adicionales no son nuevas profundidades SDD.

## 6. Límites y decisión de Gate 4

La reauditoría es del asistente IA, no Jecci/auditor humano ni certificación.
Se confía en host/daemon/kernel/imagen base; no SCA/SBOM o garantía de cero CVEs,
cleanup tras muerte del host, tope USD duro o rechazo exhaustivo de todo código hostil.
Las pruebas evalúan el contrato/criterios preparados, no ausencia universal de bugs.

No hay requisitos huérfanos en la matriz dentro del alcance declarado. Se propone
cerrar esta sub-spec en Gate 4; la spec principal/campaña10 siguen abiertas.

Kickoff real independiente propuesto: **un intento F07 lite-experimental forzado**,
modelo `openai/gpt-6-luna`, variante `max`, cuenta existente OpenCode, USD 1 reportado
blando, 1200 s, 32 pasos (máximo actual del piloto), tokens sin tope. No reparar con
feedback reservado ni repetir automáticamente. Un agotamiento se registra como tal;
no se convierte en frontera de capacidad.

La aprobación del Gate 4 no autoriza gasto por sí sola. Para lanzar, el usuario
debe aprobar explícitamente también esos límites y el kickoff propuesto.
