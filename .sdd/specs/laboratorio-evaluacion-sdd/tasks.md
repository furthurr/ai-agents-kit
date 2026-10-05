# Tareas — Laboratorio de escalamiento SDD

- Modo SDD: standard
- Fase: Tasks
- Estado: implementación en curso
- Gate 1: aprobado
- Gate 2: aprobado por el usuario («procede»)
- Gate 3: aprobado explícitamente por el usuario («procede»)
- Intención: implementar el laboratorio; no ejecutar campañas reales hasta autorización explícita del kickoff
- Testing: TDD focalizado para comportamiento nuevo del runner, el evaluador y los fixtures; tests de regresión para mantener el contrato del harness; PBT real para propiedades de F04 y F09.

## Convenciones de ejecución

- No marcar tarea `[x]` sin artefacto y evidencia verificable; RED → GREEN mínimo correcto → REFACTOR solo si aporta valor.
- `[P]` significa que puede correr en paralelo una vez satisfechas las dependencias indicadas por el grafo; tareas de ramas independientes no se bloquean entre sí.
- Los harnesses usan adaptadores falsos hasta autorizar explícitamente proveedor, modelo, límites y campaña. El plan no autoriza consumo de APIs ni ejecución autónoma real.
- `lite-experimental` y `standard-autonomous` son copias/condiciones del laboratorio; no cambiar la skill SDD canónica.
- La campaña puede automatizar transiciones después del kickoff autorizado, pero la construcción de este laboratorio conserva gates humanos SDD.
- Bloqueantes antes de una campaña: identificar modelo/variante reales seleccionados por el usuario, verificar su propagación en OpenCode sin sustituirlos, y cerrar operador, presupuestos, precios, permisos, política de fallos y revisión especializada de seguridad.

## Wave 1 — Cerrar condiciones de ejecución y custodia

- [x] 1.1 Congelar el alcance aprobado: ReserveLab, Python 3.12, pytest, SQLite y las diez metas con dificultad prevista (evidencia: `design.md` §1–2; Req R01–R05).
- [x] 1.2 Mantener explícita la política local mientras `.agent-lab/` esté ignorado: no cambiar `.gitignore` ni publicar runs; proponer versionado selectivo antes de cualquier distribución del laboratorio (evidencia: `.gitignore:24`, `design.md` §7; Req R10, R42–R45).
- [ ] 1.3 [P] Encargar revisión de seguridad del límite de confianza: cliente de herramientas, ejecución de código no confiable, acceso a pruebas reservadas, secretos, egress y sandbox; resolver hallazgos críticos antes de ejecutar candidatos (Req R21, R43–R44).
- [ ] 1.4 [P] Verificar capacidades del cliente con una prueba no facturable o smoke autorizado: capturar ID real, confirmar que MAX seleccionado por el usuario en la interfaz se aplica a todas las sesiones nuevas, y verificar herramientas/restricciones y métricas disponibles; el runner nunca cambia MAX y bloquea campaña si no puede demostrar aislamiento/herencia (Req R07, R09, R19, R30–R31, R44, R59).
- [ ] 1.5 [P] Fijar modelo auditor/comparador, presupuesto y tarifas, tiempos, repeticiones, reparación y umbrales antes de congelar un manifiesto real (Req R06, R30–R38, R46–R58).
- [x] 1.6 Configurar entrada local `/lab-start`, plantilla de manifiesto y launcher/preflight offline que no invoca modelos ni concede autorización; evidencia: `.opencode/commands/lab-start.md`, `lab.py`, `campaigns/pilot.template.json`, `runner/src/lab_runner/preflight.py`, tests `test_preflight.py` y `test_cli.py` (Req R37, R46, R59–R60). No constituye kickoff ni prueba de aislamiento.

## Wave 2 — Congelar catálogo y snapshots independientes

- [x] 2.1 Definir esquema tipado/versionado del catálogo, IDs F01–F10, factores de dificultad, elegibilidad lite canónico y digests; validar exactamente diez IDs únicos y orden previstos (evidencia: `runner/src/lab_runner/catalog.py`, `runner/tests/test_catalog.py`, `python3 -m pytest -q` → 18 passed; Req R01, R03–R05, R10, R12).
- [x] 2.2 Crear contrato público, snapshot limpio, fixtures y baseline de F01–F04: `catalog/contracts.md` (24 criterios), `snapshots/F01–F04/feature.py` y `test_public.py`, `evaluation/references.py`, `runner/tests/test_feature_harness.py`. Referencias 24/24, skeletons 0/24; baseline público 4 passed (Req R02–R04, R07–R08, R20, R22–R23). El snapshot no contiene soluciones/evaluación reservada; la frontera OS aún está pendiente.
- [ ] 2.3 [P] Crear contrato público, snapshot limpio, fixtures y baseline de F05–F07; incluir persistencia, transacciones y barreras multiproceso sin filtrar pruebas reservadas (Req R02–R04, R07–R08, R20–R23).
- [ ] 2.4 [P] Crear contrato público, snapshot limpio, fixtures y baseline de F08–F10; especificar agenda de fallos determinista, reinicio/recuperación y regresiones, sin servicios reales (Req R02–R04, R07–R08, R20–R23).
- [🔵] 2.5 Suite externa determinista F01–F04 en `evaluation/criteria.py`, ligada a los 24 IDs públicos. Pendiente F05–F10 e integración con aislamiento y límites; no ejecutar candidatos no confiables mediante el grader de calibración (Req R20–R23, R27–R28, R44).
- [🔵] 2.6 Calibración F01–F04: 24 criterios pasan con referencias y nueve mutaciones se rechazan en sus criterios; `test_feature_harness.py` 21 passed. Pendiente calibrar concurrencia/atomicidad/recuperación de F05–F10 (Req R20–R28).
- [ ] 2.7 [P] Añadir propiedad idempotente de normalización para F04 con Hypothesis real y ejemplos deterministas; observar RED antes de la solución de referencia del harness (Req R02, R22–R23; design §6).
- [ ] 2.8 [P] Añadir propiedad de convergencia determinista ante permutaciones/duplicados de eventos para F09, con Hypothesis real y ejemplos de tombstones; fijar la semántica de orden total (Req R02, R22–R23; design §6).

## Wave 3 — Núcleo del runner y evidencia durable

- [🔵] 3.1 Implementar parser/validador del manifiesto de campaña congelado (modelo, modo MAX seleccionado por el usuario, evidencia de herencia, versiones, semilla, repeticiones, límites, precios y feedback); RED/GREEN para rechazo de campos ausentes o cambios no versionados (Req R06, R09–R12, R37, R59).
- [ ] 3.2 Definir estados y errores tipados del run; RED/GREEN para transiciones válidas, inválidas, terminales y reanudación sin sobrescribir IDs ni artefactos (Req R12, R38–R42).
- [🔵] 3.3 Checkpoints JSON atómicos con fsync y rechazo de campaña duplicada implementados solo para escenarios sintéticos en `simulation.py`; no sobrescribir registros de campañas existentes. Pendiente almacén de evidencia real, recuperación, composición e I/O supervisado (Req R19, R30–R32, R41–R45).
- [ ] 3.4 Implementar gestor de snapshots/sandbox efímero: permisos mínimos, sin repo anfitrión, pruebas secretas, runs ajenos, credenciales, socket Docker o egress arbitrario; sanitizar symlinks/rutas/tamaños al extraer entregas (Req R07–R08, R21, R43–R44).
- [ ] 3.5 Implementar evaluador aislado, no privilegiado y sin red, que ejecute entrega no confiable contra suite externa y produzca evidencia por criterio; proteger fixtures oficiales contra escritura (Req R20–R28, R44).
- [ ] 3.6 Implementar política de secretos y sanitización de logs/reportes, con tests sobre tokens y credenciales sintéticas; eliminar o redactar antes de persistir/exportar (Req R42–R45).
- [ ] 3.7 Implementar cuotas y supervisor: límite por intento/global, timeout, repair cap, reservas de costo y estado `not_executed` para pendientes; si no hay hard cap del proveedor, registrar estimación y no prometer corte exacto (Req R30–R31, R37–R40, R57).
- [🔵] 3.8 Implementar adaptador OpenCode detrás de executor inyectable; constructor de argv, parser JSON y errores/timeout probados con procesos falsos en `opencode.py` y `test_opencode.py` (51 tests). Pendiente executor acotado, telemetría real, agentes experimentales aislados y verificación efectiva de selección/sesiones (Req R07, R09, R19, R30–R31, R40–R42, R59–R60).

## Wave 4 — Orquestación experimental autónoma

- [ ] 4.1 Capturar con hashes la versión exacta de instrucciones/agente SDD canónicos usada como baseline y versionar aparte el delta de autonomía/override; implementar políticas para `lite-experimental` y `standard-autonomous` con decisiones registradas, sin atribuir aprobación humana ni mezclar resultados de variantes (Req R10, R13–R19, R48–R49).
- [ ] 4.2 [P] Implementar ejecución de la ronda ligera para las diez features, repetición/secuencia congeladas, captura completa de resultado y anotación de override lite forzado para F05–F10 (Req R01, R05–R06, R14–R19, R46–R47).
- [ ] 4.3 Implementar cierre/evaluación de la ronda ligera completa y clasificador independiente de resultado funcional y cumplimiento de proceso; no revelar suite ni diagnóstico reservado al candidato (Req R22–R29, R50).
- [ ] 4.4 Implementar escalamiento de los runs válidos parciales/fallidos o con fallo de proceso; crear run nuevo desde el mismo digest inicial sin código, conversación o feedback previo; aplicar política acotada a runs inválidos, sin contarlos como fallo del modelo (Req R07–R08, R16, R38–R41, R51–R53).
- [ ] 4.5 [P] Implementar política de pausa/reanudación para fallas de infraestructura y agotamiento de presupuesto; reanudar con IDs nuevos y conciliación cuando posible, sin duplicar llamadas a ciegas (Req R38–R41, R53, R57).
- [ ] 4.6 Implementar ronda de control seleccionada por semilla desde éxitos ligeros y tercera ronda opcional de otro modelo; validar mismo snapshot/protocolo, opt-in y advertencia contra inferir ventaja general de un muestreo sesgado (Req R08–R12, R35–R36, R55–R58).
- [🔵] 4.7 Flujo sintético de 10 intentos ligeros + escalamiento, descriptor de baseline idéntico y contexto vacío, límite de intentos y registros no sobrescritos: `simulation.py`, `test_simulation.py`, `test_cli.py`. No usa aún adaptador/evaluador reales, ni implementa recuperación/invalidación/validación efectiva MAX; no equivale al E2E completo (Req R37–R42, R44, R46–R60).

## Wave 5 — Auditoría, métricas y reportes

- [ ] 5.1 Congelar rúbrica y formato de auditoría cualitativa; ejecutar auditor después de candidato sobre copia redactada y separar revisión ciega de código de revisión de proceso (Req R24–R27, R36).
- [ ] 5.2 Implementar cálculo de éxito completo/parcial/fallo por criterios obligatorios, primera entrega frente a reparación, tasas por condición, Wilson 95%, N/A y causas de invalidez/no ejecución (Req R22–R36).
- [ ] 5.3 Implementar costos por run y por política escalonada, contabilizando intentos ligeros fallidos, escalados, auditoría y costo por éxito; etiquetar origen observado/estimado y tarifas/versiones (Req R30–R36, R54).
- [ ] 5.4 [P] Generar reportes legibles y exportación procesable con datos individuales, agregados, incertidumbre, exclusiones, límites, artefactos y advertencia sobre selección de standard solo en fallos (Req R32–R36, R42, R45, R55).
- [ ] 5.5 Verificar integridad del reporte: cada éxito enlaza evidencia para todo criterio obligatorio; comparar IDs y hashes con registro durable para detectar huérfanos o sobrescritura (Req R22, R32, R42, R45).

## Wave 6 — Dry-run, aceptación de seguridad y habilitación

- [🔵] 6.1 Demostración sintética guardada en `runs/offline-demo-001/report.json`: 16 intentos predefinidos, cero modelos, no benchmark. Pendiente conectar referencias/calibración, adaptador falso, MAX observado, métricas y demás ramas del E2E (Req R06–R12, R37–R60).
- [ ] 6.2 Ejecutar pruebas negativas de aislamiento: intentar leer evaluación reservada, modificar otros runs, escapar rutas, extraer credenciales y generar egress; verificar denegación y revisar evidencia con especialista de seguridad (Req R21, R43–R44).
- [ ] 6.3 Completar matriz requisito→tarea→test→evidencia, auditoría de calidad y decisión de Git selectivo; documentar limitaciones de cliente, métricas disponibles, población y confianza (Req R01–R59).
- [ ] 6.4 Preparar manifiesto de piloto real con modelo identificado, evidencia de MAX seleccionado por el usuario/heredado en sesiones nuevas, presupuesto total, límites, repeticiones, precios, modelos auditores y policy digest; solicitar autorización explícita de kickoff antes de cualquier consumo de API (Req R06, R09–R12, R30–R38, R46–R59).
- [ ] 6.5 Tras autorización explícita, iniciar el piloto autónomo monitorizado por límites; detener si capacidades, aislamiento o coste real contradicen el manifiesto, conservar todos los estados y emitir informe (Req R37–R45).

## Grafo de waves

```mermaid
flowchart LR
  subgraph W1[Wave 1 · decisiones y custodia]
    T11[1.1 Decisiones]
    T12[1.2 Versionado]
    T13[1.3 Seguridad]
    T14[1.4 Capacidades cliente y MAX]
    T15[1.5 Presupuesto y auditor]
  end
  subgraph W2[Wave 2 · catálogo y evaluación]
    T21[2.1 Catálogo]
    T22[2.2 F01–F04]
    T23[2.3 F05–F07]
    T24[2.4 F08–F10]
    T25[2.5 Suite externa]
    T26[2.6 Calibración]
    T27[2.7 PBT F04]
    T28[2.8 PBT F09]
  end
  subgraph W3[Wave 3 · runner]
    T31[3.1 Manifiesto]
    T32[3.2 Estado]
    T33[3.3 Evidencia]
    T34[3.4 Sandbox]
    T35[3.5 Evaluador]
    T36[3.6 Secretos]
    T37[3.7 Límites]
    T38[3.8 Adaptador]
  end
  subgraph W4[Wave 4 · orquestación]
    T41[4.1 Política]
    T42[4.2 Ronda lite]
    T43[4.3 Clasificador]
    T44[4.4 Escalamiento]
    T45[4.5 Reanudación]
    T46[4.6 Control/modelo]
    T47[4.7 E2E fake]
  end
  subgraph W5[Wave 5 · análisis]
    T51[5.1 Auditor]
    T52[5.2 Métricas]
    T53[5.3 Costos]
    T54[5.4 Reportes]
    T55[5.5 Integridad]
  end
  subgraph W6[Wave 6 · habilitación]
    T61[6.1 Dry-run]
    T62[6.2 Seguridad negativa]
    T63[6.3 Matriz/evidencia]
    T64[6.4 Manifiesto y autorización]
    T65[6.5 Piloto opt-in]
  end
  T11 --> T21
  T12 --> T31
  T13 --> T34
  T14 --> T38
  T14 --> T64
  T15 --> T64
  T21 --> T22
  T21 --> T23
  T21 --> T24
  T22 --> T25
  T23 --> T25
  T24 --> T25
  T25 --> T26
  T22 --> T27
  T24 --> T28
  T26 --> T35
  T31 --> T32
  T32 --> T33
  T33 --> T34
  T34 --> T35
  T35 --> T37
  T36 --> T33
  T37 --> T38
  T38 --> T41
  T21 --> T42
  T41 --> T42
  T42 --> T43
  T43 --> T44
  T44 --> T45
  T44 --> T46
  T45 --> T47
  T46 --> T47
  T44 --> T51
  T47 --> T52
  T51 --> T52
  T52 --> T53
  T52 --> T54
  T53 --> T54
  T54 --> T55
  T47 --> T61
  T55 --> T61
  T34 --> T62
  T61 --> T63
  T62 --> T63
  T63 --> T64
  T64 --> T65
```

## Mapeo requisito → tarea

| Requisitos | Tareas principales |
|---|---|
| R01–R05 | 2.1–2.4, 4.2 |
| R06–R12 | 1.1, 1.4, 3.1–3.3, 3.8, 4.2, 4.6, 6.1, 6.4 |
| R13–R19 | 1.1, 4.1–4.3, 5.1 |
| R20–R28 | 2.2–2.8, 3.5, 4.3, 5.1–5.2 |
| R29–R36 | 1.1, 4.6, 5.1–5.4 |
| R37–R45 | 1.2–1.4, 3.2–3.8, 4.4–4.7, 5.3–5.5, 6.1–6.5 |
| R46–R60 | 1.4–1.6, 3.1, 3.7–3.8, 4.1–4.7, 5.2–5.4, 6.1, 6.4–6.5 |

Gate 3 pendiente: aprobar este plan antes de implementar. Implementación abarcaría
