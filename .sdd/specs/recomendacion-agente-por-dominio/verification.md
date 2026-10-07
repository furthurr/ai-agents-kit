# Verificación — Recomendación de agente por dominio

Modo SDD: standard
Fase: Verification
Estado: suite formal verde — refuerzo contractual propagado; runtime posterior bloqueado por HTTP 403
Gate 4: pendiente — no cerrar como verificación completa
Fecha: 2026-10-07

## Resultado y alcance

Implementación y distribución comprobadas estáticamente en seis plataformas.
No se acredita comportamiento conversacional ni instalación actualizada del usuario.
Tarea 4.1 completa en la ejecución actual: suite SDD 505/505; handoff 34/34;
recomendaciones de modelo 437/437; links 4/4 + 71 archivos; validator 10 skills,
6 agentes y 6 plataformas; `git diff --check` verde. Tarea 4.2 incompleta:
R01 pasó tras el primer refuerzo; R04 había fallado por proponer candidatos fuera de v1;
R06/R07/R11 siguen bloqueados; una variante R10 que pedía implementar mediante data-api
intentó editar (el fixture rechazó la escritura). El refuerzo adicional se propagó,
pero sus retries runtime recibieron HTTP 403 antes de respuesta. Ver
[correction-evidence.md](correction-evidence.md) y
[followup-smoke.md](followup-smoke.md). No hay `[x]` huérfanos.
Todos los requisitos tienen artefactos y checks asociados; los requisitos de
interacción conservan una brecha runtime explícita. No hay `[x]` huérfanos.

## Ciclo y resultados observados

Estrategia: TDD focalizado contractual para política, integración y propagación;
checks existentes para documentación. RED/GREEN observado y comandos completos en
[implementation-evidence.md](implementation-evidence.md). No se declara TDD runtime.

| Operación | Resultado observado en Verification |
|---|---|
| `python3 -B tools/test_sdd_contract.py` | Exit 0; 505/505 comprobaciones. |
| `python3 -B tools/test_handoff_contract.py` | Exit 0; 34 tests, OK. |
| `python3 -B tools/test_model_recommendations.py` | Exit 0; 437/437 comprobaciones. |
| `python3 -B tools/test_links.py` | Exit 0; 4/4 pruebas del checker. |
| `python3 -B tools/check_links.py` | Exit 0; enlaces reales correctos, 71 archivos. |
| `python3 -B tools/validate.py` | Exit 0; 10 skills / 6 agentes / 6 plataformas, paridad correcta. |
| `python3 -B tools/measure_context.py` | Exit 0; agentes 3,793, skills 18,533, referencias 15,507 palabras. |
| `git diff --check` | Exit 0. |

RED/GREEN de implementación: política 0/1 → 43/43; integración 0/8 → 51/51
acumulado; propagación 0/30 → 87/87 acumulado; barrera R01 0/15 → 66/66;
whitelist/stop-package focal 91/91 tras render. Fallos RED por ausencia
de los artefactos/reglas previstas, no por infraestructura incidental.
PBT no aplica: sin propiedad algebraica; sin dependencias añadidas.

## Integridad de tareas

| Tarea marcada completa | Artefacto real / evidencia |
|---|---|
| 1.1 | `canonical/skills/sdd-spec/references/agent-routing.md`; `test_agent_routing_policy`; RED/GREEN registrado. |
| 2.1 | `canonical/agents/sdd.md`, `canonical/skills/sdd-spec/SKILL.md`; `test_agent_routing_integration` y regresión SDD verde. |
| 3.1 | `docs/agentes/sdd.md`, `docs/sdd-smoke.md`; guías y doce casos, checker de enlaces verde. |
| 3.2 | Agente, skill y referencia SDD en `generated/` de las seis plataformas; `test_agent_routing_generated`, paridad/validator verde. |
| 4.1 | Este archivo, suite formal anterior, RNF y revisión de estados. |

`tools/test_sdd_contract.py` ejecuta cuatro grupos de routing desde `main()`;
incluye checks de política, integración, barrera R01 y paridad multi-plataforma.
El smoke conversacional no se modela como clasificador de software.

## Matriz de requisitos y evidencia

Abreviaturas de pruebas en `tools/test_sdd_contract.py`: **P** =
`test_agent_routing_policy`, **I** = `test_agent_routing_integration`, **G** =
`test_agent_routing_generated`. **R** = revisión textual de la referencia canónica.
«Contrato OK / runtime pendiente» no significa criterio conversacional demostrado.

| Requisito | Tareas | Test/check | Evidencia | Estado |
|---|---|---|---|---|
| REQ-001 Evaluar dominio/límites | 1.1, 2.1, 4.2 | P, I, R; smoke real | R01/R02/R03/R05 y R06 bloqueado | Parcial: R01–R03/R05 OK; R06 bloqueado |
| REQ-002 Solo dos candidatos | 1.1, 3.2, 4.2, 5.2 | P, G; smoke real | R04 anterior al refuerzo falló; whitelist y propagación contractual reforzadas después | Retry runtime HTTP 403 |
| REQ-003 Candidato UI | 1.1, 3.1, 4.2 | P, R; smoke real | R01 repetido y R09 contexto manual | PASS en esos escenarios; R11 bloqueado |
| REQ-004 Candidato datos | 1.1, 3.1, 4.2 | P, R; smoke real | R02 y R10 contexto manual explícito | PASS condicionado; intento edit previo en variante implementadora |
| REQ-005 No asignar alcance mixto | 1.1, 3.1, 4.2 | P, R; smoke real | R03 mantiene SDD por cruce UI/API | PASS |
| REQ-006 Ambigüedad/sin keywords | 1.1, 3.1, 4.2, 5.2 | P, R; smoke real | Regla actual prohíbe enumerar terceros; R04 anterior fue FAIL | Contrato PASS; retry HTTP 403 |
| REQ-007 Candidato verificable | 1.1, 2.1, 4.1, 4.2 | P, I, R; smoke real | Catálogo estático/R12; R11 sin respuesta con UI ausente | Estático PASS; runtime R11 bloqueado |
| REQ-008 Planificar UI compleja | 1.1, 2.1, 3.1, 4.2 | P, I, R; smoke real | R05 mantiene Requirements/Design en SDD | PASS |
| REQ-009 Planificar datos de riesgo | 1.1, 2.1, 3.1, 4.2 | P, I, R; smoke real | R06 timeout en intentos con permisos shell denegados | Bloqueado |
| REQ-010 Conservar spec/tareas | 2.1, 3.1, 4.2 | I, R; smoke real | R07 localiza spec, pide Bash y no responde tras rechazo | Bloqueado |
| REQ-011 Elección no aprueba gates | 2.1, 3.1, 4.1, 4.2 | P, I, R | Referencia §Integración; tests SDD y handoff; R07/R08 | Contrato OK / runtime pendiente |
| REQ-012 Justificar recomendación | 1.1, 2.1, 3.1, 4.2 | P, I, R; smoke real | R01/R02/R03/R05/R10 incompatible justifican; R04 incluye candidatos ajenos | Parcial |
| REQ-013 Dar elección manual | 1.1, 2.1, 3.1, 4.2, 5.2 | P, I, R; smoke real | Regla y stop/package propagados; R01/R09 previos PASS | Contrato PASS; runtime posterior HTTP 403 |
| REQ-014 Sin invocación automática | 1.1, 2.1, 3.1, 3.2, 4.1, 4.2, 5.2 | P, I, G, R; smoke real | Nuevo stop/package; R10 previo edit bloqueado | Contrato PASS; efectividad runtime posterior no verificada |
| REQ-015 No repetir tras elección | 1.1, 2.1, 3.1, 4.2 | P, R; smoke real | R08 fixture con historial explícito dice que no repite | PASS en fixture de control |
| REQ-016 Contexto copiable | 1.1, 2.1, 3.1, 4.2, 5.2 | P, R; smoke real | R09 ui-design y R10 data-api explícito previos entregan contexto; regla actual exige stop | Previo PASS; retry HTTP 403 |
| REQ-017 Selección explícita | 1.1, 2.1, 3.1, 4.2 | P, R; smoke real | R10 incompatible explica límite y pregunta; compatible condicionado a petición explícita de contexto | Parcial |
| REQ-018 Separar ejes/permisos | 1.1, 2.1, 3.1, 4.1, 4.2 | P, I, R; smoke real | R01/R03/R05/R08/R10 incompatible; R07 gate pendiente bloqueado | Parcial; R07 sin salida |
| REQ-019 Paridad | 3.2, 4.1 | G, validator | Copilot, OpenCode, Kiro, Claude, Pi, Antigravity | Contrato OK; runtime de hosts no certificado |
| REQ-020 Verificabilidad de casos | 1.1, 2.1, 3.1, 3.2, 4.1, 4.2 | P, I, G; guía smoke | Tests ejecutados y doce casos reproducibles en docs/sdd-smoke.md | Harness/guía OK; ejecución runtime pendiente |

## RNF y quality bar

| RNF declarado en Design | Evidencia | Resultado |
|---|---|---|
| Portabilidad | G y validator; referencia idéntica en 6 destinos | OK estático; runtime solo OpenCode |
| Seguridad | Referencia §§Candidatos/Contexto/Integración, secretos/PII y permisos; handoff 34/34 | Escrituras denegadas en fixtures; no acredita aislamiento técnico fuera del host |
| Coste de contexto | measure_context actual: agentes 3,793; skills 18,533; referencias 15,507 palabras | Medición repetida; el working tree incluye cambios concurrentes, delta no atribuible solo a routing; sin umbral inventado |
| Trazabilidad | tasks.md, implementation-evidence.md y matriz anterior | OK; brecha runtime visible |

Spot-check: fuentes comunes en skill/referencia, entrada breve en agente y salidas
por render; sin nuevas capas runtime, storage, DI, singletons o dependencias de tests.
Esos puntos de arquitectura de aplicación no aplican, según Design. El ciclo TDD
contractual tiene RED/GREEN observado y no se presenta como test del LLM.

`git diff -- canonical/agents/ui-design.md canonical/agents/data-api.md
canonical/skills/documentation-orchestrator/references/handoff.md adapters
canonical/manifest.json` no produjo cambios: límites, handoff, catálogo y adaptación
no fueron ampliados. Se preservaron cambios ajenos identificados en implementación.

## Brecha runtime — tarea 4.2 pendiente

Comprobaciones y ejecución aislada registradas en runtime-smoke.md,
correction-evidence.md y followup-smoke.md:

- `command -v opencode`, `command -v kiro-cli`, `command -v pi`: CLIs encontradas;
  `command -v claude` no encontró ese ejecutable en PATH. Esto no prueba credenciales
  ni disponibilidad de sesiones funcionales de esos hosts.
- `opencode --version`: **1.18.34**.
- Lectura de la referencia instalada en
  `~/.config/opencode/skills/sdd-spec/references/agent-routing.md`: **no existe**.
  La instalación actual no acredita las fuentes nuevas; esta sesión estaba cargada
  antes del cambio. No se usó como evidencia runtime de la feature.

El entorno aislado inicial fue autorizado mediante «procede». **R01 falló** en la
primera ejecución e intentó editar CSS antes de recomendar; el fixture rechazó la
escritura. Tras el primer refuerzo, R01 pasó en repetición. Detalles:
[runtime-smoke.md](runtime-smoke.md) y [correction-evidence.md](correction-evidence.md).

Resultados históricos de la segunda ronda aislada: R01 corregido PASS; R02/R03/R05/
R08/R09/R10 incompatible PASS; R10 contexto manual explícito PASS condicionado; R04
FAIL; R06/R07/R11 bloqueados; R12 parcial. R10 compatible anterior intentó editar
cuando el prompt solicitaba aplicar el cambio por medio de data-api; el rechazo de
permiso evitó la escritura, pero cuenta como riesgo de routing. R08 usa historial
sintético explícito; no acredita memoria entre sesiones.

Después el usuario autorizó restringir la whitelist y parar la ejecución al elegir
especialista. El cambio tiene pruebas contractuales y propagación verde. Al reintentar
R04/R06/R07/R10/R11 con fixture sin shell, el proveedor devolvió HTTP 403 antes de
respuesta. No se modificó proveedor/modelo ni se copiaron credenciales. No se acredita
eficacia conversacional posterior al segundo refuerzo. Evidencia: [followup-smoke.md](followup-smoke.md)
y [correction-evidence.md](correction-evidence.md).

No se modificó el perfil global ni se copiaron credenciales; no se seleccionó otro
modelo. El validator y toda la suite contractual actual pasan, pero el comportamiento
conversacional tiene incumplimiento conocido y cobertura parcial.

## Gate 4

Pendiente. La suite formal está verde y whitelist/stop-package se propagaron a seis
plataformas. Los retries conversacionales posteriores quedaron bloqueados por HTTP
403; los resultados anteriores documentan R04 FAIL y bloqueos R06/R07/R11, además
de resultados mixtos R10. Gate 4 solo podrá cerrarse tras conseguir una sesión de
smoke que responda para comprobar los cambios o si el usuario acepta expresamente
la limitación de verificación runtime. No cerrar como totalmente verificada ni
reescribir fallos históricos.
