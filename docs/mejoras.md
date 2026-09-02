# Mejoras del kit / framework

Hoja de ruta priorizada para convertir el kit en una distribución confiable,
reproducible y demostrablemente útil. La prioridad no es aumentar la nota
percibida ni añadir más agentes: es reducir riesgos, probar el comportamiento
real y facilitar una adopción sostenible.

## Evaluación de partida y objetivo

La calificación separa la calidad de la idea de la madurez del producto que se
instala y ejecuta:

| Dimensión | Estado actual aproximado | Objetivo |
| --- | ---: | ---: |
| Diseño conceptual y arquitectura | 7.5/10 | 8.5/10 |
| Producto instalable y operación | 5.5/10 | 7.5–8.0/10 |
| Evidencia de utilidad | 4.0/10 | 7.5/10 |

Estas notas son orientativas. Completar tareas no aumenta la calificación de
forma automática: cada salto exige evidencia reproducible y criterios de salida
cumplidos.

| Hito | Resultado esperado |
| --- | --- |
| Tras P0 | Release coherente, validación segura, CI verde e instalación estricta |
| Tras P0 + P1 | Adopción clara, smoke tests multiplataforma y demo medible |
| Tras P0 + P1 + P2 selectivo | Bootstrap e índices menos dependientes del prompt |

## Principios al priorizar

1. Corregir primero riesgos de distribución, seguridad y reproducibilidad.
2. Preferir controles técnicos a instrucciones que solo dependen del prompt.
3. No afirmar compatibilidad, seguridad o ahorro de tokens sin evidencia.
4. Toda mejora debe tener una definición de hecho y un método de verificación.
5. No unificar `project-navigator` y `architecture`: tienen alcances distintos.
6. No auto-seleccionar ni fijar un modelo desde el kit.
7. No añadir nuevas skills hasta demostrar la adopción de las existentes.

---

## P0 — Estabilización y confianza

Bloque obligatorio antes de presentar el estado actual como una release estable.
Meta: llevar el producto instalable a una base defendible de **~7/10**.

### P0.1 — Estado de entrega coherente

- [x] **Versionar `project-navigator` como una unidad atómica**: fuente canónica,
  adapters, artefactos generados, manifest y documentación deben entrar juntos.
- [x] **Resolver contradicciones documentales**: README, visión y arquitectura
  deben coincidir sobre si Navigator está planificado, en MVP o estable.
- [x] **Dejar el árbol generado reproducible desde un clon limpio**, sin depender
  de archivos locales o no rastreados.

Definición de hecho:

- Un clon limpio puede ejecutar render y validación sin archivos faltantes.
- `git status --short` queda vacío después de regenerar.
- README, catálogo, visión y arquitectura describen el mismo estado del producto.

### P0.2 — Validación segura y completa

- [x] **Hacer `tools/validate.py` no destructivo**: renderizar en un directorio
  temporal configurable y comparar hashes sin renombrar ni borrar `generated/`.
- [x] **Validar schemas y valores** de `manifest.json`, `platform.json` y adapters:
  tipos, campos obligatorios, IDs, extensiones y frontmatter esperado.
- [x] **Impedir path traversal y escrituras fuera de destino**: `filename` debe
  ser un nombre relativo seguro y permanecer bajo `generated/<platform>/agents/`.
- [x] **Detectar IDs y filenames duplicados**, colisiones de salida y entradas
  canónicas o generadas huérfanas.
- [x] **Dejar `tools/test_integrity.py` completamente verde**, incluida la
  referencia README ↔ `scripts/backup/`.

Definición de hecho:

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/test_integrity.py
git diff --exit-code -- generated/
```

Todos los comandos terminan con código `0`. Una interrupción de `validate.py` no
altera `generated/`.

### P0.3 — Integración continua

- [x] **Añadir CI base en GitHub Actions** para Linux con Python 3.10: render,
  validación, integridad, enlaces y paridad de `generated/`.
- [ ] Ampliar la matriz a Python soportado y, cuando aplique, Linux, macOS y
  Windows.
- [ ] Ejecutar parseo explícito de JSON/YAML en la matriz de CI.
- [x] Ejecutar render reproducible, validación e integridad en CI.
- [x] Comprobar sintaxis de scripts Bash.
- [ ] Comprobar sintaxis de scripts PowerShell en un runner Windows.
- [x] Añadir pruebas negativas: token sin resolver, adapter incompleto, filename
  inseguro, colisión y artefacto generado desactualizado.
- [x] Validar enlaces Markdown internos y referencias bajo `references/`.
- [ ] Proteger el merge cuando el pipeline no esté verde.

Definición de hecho: el workflow se ejecuta en pull requests, detecta al menos un
fixture inválido por cada clase crítica y pasa desde un clon limpio. La ejecución
de scripts PowerShell y el parseo explícito JSON/YAML siguen pendientes hasta
ampliar la matriz de CI.

### P0.4 — Instalación estricta y reversible

- [x] **Fallar con código distinto de cero** si faltan skills, agentes o fuentes
  generadas; no declarar instalación completada tras omitir contenido requerido.
- [x] Garantizar que `--dry-run` / `-DryRun` no cree ni modifique directorios.
- [x] Añadir un preflight que compruebe render validado, destinos y herramientas.
- [x] Definir cómo retirar artefactos obsoletos sin borrar contenido ajeno al kit.
- [x] Documentar restauración de backup y desinstalación.
- [x] Probar install, actualización, dry-run y rollback en directorios HOME
  temporales para las tres plataformas.
- [ ] **Ejecutar los instaladores PowerShell en un runner Windows.** Su contrato
  hoy solo está garantizado de forma estática (test `[7]` de `test_install.py`);
  no se han ejecutado nunca. Bloqueo: se necesita la matriz de SO de P0.3.

Definición de hecho:

```bash
python3 tools/test_install.py     # instalación, fallo temprano, dry-run, rollback
for s in scripts/install/*.sh scripts/backup/*.sh; do bash -n "$s"; done
```

Ambos terminan en `0`. `test_install.py` ejecuta los instaladores contra un `HOME`
temporal, de modo que la instalación real del desarrollador nunca se toca.

### P0.5 — Seguridad mínima exigible

- [ ] **Unificar la política de secretos**: un secreto real no puede incluirse en
  un commit aunque exista autorización conversacional.
- [ ] Añadir secret scanning automatizado en CI y una opción local documentada.
- [ ] Ampliar `.gitignore` con patrones locales razonables sin ocultar fixtures de
  prueba deliberados.
- [ ] Reducir permisos efectivos por agente donde cada host lo permita.
- [ ] Documentar explícitamente qué límites son enforcement técnico y cuáles son
  solo instrucciones al modelo.
- [ ] Tratar README, `AGENTS.md`, steering, código y web como contenido no
  confiable frente a prompt injection.

Definición de hecho: un fixture con secreto bloquea CI, la documentación no
promete aislamiento inexistente y la matriz de permisos justifica cada tool.

### P0.6 — Defectos verificados de la skill SDD

Hallazgos reproducibles en `canonical/skills/sdd-spec/` y `canonical/agents/sdd.md`.
Cada uno se comprueba por lectura directa o `grep`; ninguno depende de criterio.

- [x] **Corregir el enunciado de GATE 3** en `SKILL.md`: decía
  `"¿Apruebo el plan y empiezo a implementar?"` mientras los otros tres gates usan
  segunda persona. Tal como estaba, el agente se preguntaba a sí mismo.
- [x] **Reparar el render de `{{gate_instruction}}`**: el token solo contenía una
  frase completa para Copilot; Kiro y OpenCode heredaban el fragmento descabezado
  `"El gate se / implementa de forma natural:"`. Mover la parte común al canonical
  y dejar en el token únicamente lo específico de cada plataforma.
- [x] **Eliminar o usar `{{sdd_start_instruction}}`**: estaba definido en los tres
  `platform.json` y no aparecía en ningún archivo de `canonical/`.
- [x] **Detectar sustituciones no usadas en `tools/validate.py`**: validaba
  tokens → sustituciones y nunca al revés, así que la config muerta pasaba el CI.
- [x] **Añadir sección de RNF a la plantilla de `design.md`**: `quality-bar.md` §7,
  `integrity-gate.md` paso 3 y la matriz de `verification.md` exigen auditar
  «3–5 RNF críticos del propio spec», pero ninguna plantilla los capturaba. El
  agente debía inventarlos retroactivamente en Fase 4, que es exactamente el
  cumplimiento inventado que la skill prohíbe.
- [x] **Alinear el techo de `design.md`**: `SKILL.md` decía `~≤250 líneas` y
  `quality-bar.md` §10 decía `~200–250`.

Definición de hecho:

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/test_sdd_contract.py
grep -rn "sdd_start_instruction" canonical/ adapters/   # sin config muerta
grep -n "GATE 3" canonical/skills/sdd-spec/SKILL.md     # segunda persona
git diff --exit-code -- generated/
```

Los comandos son coherentes entre sí, `generated/` queda en paridad y la plantilla
de `design.md` produce los RNF que la Fase 4 audita.

---

## P1 — Adopción y evidencia

Este bloque demuestra que el kit funciona en la práctica y explica cuándo aporta
valor. Meta acumulada tras P0: **7.5–8.0/10** como producto instalable.

### P1.1 — Uso y público objetivo

- [ ] Añadir al README una sección honesta **“Para quién / No es para”**.
- [ ] Añadir en [uso.md](uso.md) un árbol de decisión de una pantalla:
  Navigator vs Architecture vs SDD vs especialistas vs Git & Release.
- [ ] Añadir en [catalogo.md](catalogo.md) una tabla de solapes: “si preguntas X,
  usa Y y no Z”.
- [ ] Explicar el coste de mantener `.navigator/`, `.architecture/`, `.quality/`
  y las demás carpetas canónicas.

Definición de hecho: un usuario nuevo puede elegir agente y flujo sin conocer la
arquitectura interna del kit.

### P1.2 — Smoke tests multiplataforma

- [x] Crear `docs/navigator-smoke.md` con un checklist post-install de cinco
  minutos: instalación, bootstrap y tres consultas de prueba.
- [x] Ejecutar y registrar el smoke test en Copilot, OpenCode y Kiro.
- [x] Verificar carga del agente, activación de la skill, escritura permitida,
  rechazo de trabajo fuera de alcance y formato de respuesta degradada.
- [x] Completar los criterios de [navigator-smoke.md](navigator-smoke.md)
  únicamente con evidencia enlazada.

Definición de hecho: existe una tabla fechada de resultados por plataforma y
versión, con pasos reproducibles y fallos conocidos.

### P1.3 — Demo y medición

- [ ] Crear `examples/mini-app/` con un repositorio pequeño y una `.navigator/`
  representativa, sin convertirla en un caso artificialmente perfecto.
- [ ] Documentar cinco preguntas de onboarding, localización e impacto.
- [ ] Comparar cada pregunta con y sin índices: archivos leídos, tokens estimados,
  tiempo, calidad de fuentes y corrección de la respuesta.
- [ ] Registrar limitaciones y resultados negativos, no solo casos exitosos.

Definición de hecho: otra persona puede repetir la comparación y obtener una
tendencia similar. No se publica un porcentaje de ahorro sin esos datos.

### P1.4 — Confiabilidad del Navigator

- [x] Fijar el formato degradado: `fuentes`, `capas_ausentes`,
  `capas_deshabilitadas` y `confianza`; validado en Copilot, OpenCode y Kiro.
- [ ] Añadir una regla de frescura: antigüedad de `generated_at`, commit indexado
  y desfase evidente antes de confiar en los índices.
- [ ] Documentar actualización parcial y resolución de ediciones manuales.
- [ ] Unificar el aviso de modelo para evitar divergencias entre documentos.
- [x] Añadir el snippet recomendado de `.gitignore` para `.navigator/cache/`.

Definición de hecho: las pruebas cubren índice ausente, desactualizado, parcial y
editado manualmente; el agente no presenta datos obsoletos como actuales.

### P1.5 — Coherencia del agente SDD

SDD es la skill más compleja del kit (4 fases, 3 variantes, 5 referencias) y la
única que escribe código de producto. P0.6 ya está cerrado y el contrato TDD junto
con el smoke test base ya están implementados; quedan pendientes de estado,
reanudación y evidencia manual.

- [ ] **Añadir lectura de estado al iniciar**, como ya hacen `security` y
  `code-quality`: qué gates se aprobaron, en qué fase está la spec y qué tareas
  quedan abiertas. Hoy no existe ningún paso 0 ni registro de gates aprobados, así
  que una sesión interrumpida tras GATE 2 no puede reconstruir el estado.
- [ ] **Resolver la promesa de reanudación**: el adapter de Copilot ofrece
  «deja vacío para continuar una spec existente» y la skill no define ningún
  procedimiento de reanudación. Manda la fuente canónica: o se implementa el flujo
  o se retira la promesa del adapter.
- [ ] **Usar IDs de requisito estables** (`REQ-001`) en lugar de posicionales
  (`Req 1.1`). Reordenar o borrar una historia rompe en silencio las referencias de
  `tasks.md` y `verification.md`. El resto del kit ya usa IDs no posicionales
  (`SEC-0001`, `QLT-0001`, ADRs numerados).
- [ ] **Declarar el alcance de escritura del agente**: es el único sin frontera
  documentada y el de mayor blast radius (`read/write/shell/web`). Debe decir
  explícitamente que escribe en `.sdd/` más el código que exigen las tareas
  aprobadas, y nada más.
- [ ] **Definir dueño y formato de `.sdd/steering/`**: lo leen el agente, la skill
  y `project-navigator`, pero ninguna skill lo crea ni especifica su contenido.
- [ ] **Consolidar las reglas de PBT**: `agents/sdd.md` ya delega la estrategia en
  `references/testing.md`, pero aún conviene separar o justificar las reglas
  complementarias de `references/integrity-gate.md` y `references/testing.md`.
- [x] **Dar criterio verificable al modo `direct`**: alcance claro, localizado y
  reversible; sin contrato público, migración, decisión arquitectónica, cruce de
  capas ni riesgo relevante. Evidencia: `SKILL.md` y `tools/test_sdd_contract.py`.
- [x] **Completar las variantes**: Bugfix declara gates normales salvo el caso
  trivial, regresión antes del fix y manejo honesto de un defecto no reproducible;
  Quick Plan declara qué evidencia queda en tareas/resumen al omitir Fase 4.
- [ ] **Definir la reconciliación de contexto de dominio**: cuando falta
  `.architecture/`, la skill documenta el dominio dentro de `design.md` y nadie lo
  promueve después, porque `documentation-orchestrator` tiene prohibido tocar
  `.sdd/`. El conocimiento queda enterrado en specs cerradas.
- [x] **Crear el documento base `docs/sdd-smoke.md`** con escenarios de gates,
  proporcionalidad y testing adaptativo, siguiendo el formato de
  [navigator-smoke.md](navigator-smoke.md).
- [ ] **Completar y ejecutar el smoke SDD multiplataforma**: añadir casos
  explícitos de rechazo del integrity gate ante un `[x]` sin artefacto y de trabajo
  fuera de alcance, y registrar evidencia para Copilot, OpenCode y Kiro.
- [x] **Retirar las cifras de coste sin medición** (`Baseline +~10 %`, `+40–80 %`)
  y sustituirlas por carga documental cualitativa; cualquier porcentaje futuro
  exige una comparación reproducible.

Definición de hecho del bloque restante: una spec se puede abandonar y reanudar en
otra sesión sin perder el estado de los gates, los IDs de requisito sobreviven a un
reordenado de historias y existe una tabla fechada de smoke por plataforma y versión.

#### Extensión implementada: testing adaptativo

- [x] Separar profundidad SDD de estrategia de pruebas.
- [x] Aplicar TDD focalizado por defecto a comportamiento nuevo/modificado y
  reservar TDD estricto para petición explícita.
- [x] Definir regresión para bugfix, caracterización para legado y excepción
  verificable cuando no cambia comportamiento observable o falta un harness viable.
- [x] Evitar test-after en plantillas y exigir evidencia RED/GREEN en el integrity gate.
- [x] Añadir contrato automatizado (`tools/test_sdd_contract.py`) y el documento
  base [sdd-smoke.md](sdd-smoke.md).
- [ ] Ejecutar el smoke manual en las tres plataformas y completar sus casos de
  integrity gate y alcance; sin esa evidencia no se marca la matriz como aprobada.

---

## P2 — Automatización de contexto

Realizar solo después de completar P0 y la evidencia esencial de P1. Estas tareas
reducen dependencia del modelo y hacen que Navigator y el integrity gate de SDD
sean más que una convención documental.

- [ ] **Bootstrap semideterminista** (`tools/navigator_bootstrap.py`): detectar
  stack y módulos evidentes, validar exclusiones y generar stubs de `config.yaml`,
  `ai-context.md` y `module-map.json` para revisión de la IA.
- [ ] **Métrica real de `.navigator/`**: estimar tokens de todos los artefactos,
  incluidas plantillas y datos anidados, y avisar al superar los topes.
- [ ] **Symbols best-effort** con heurísticas probadas en uno o dos lenguajes;
  declarar cobertura y falsos positivos.
- [ ] **Formalizar schemas ejecutables** de `config`, `module-map` y `symbols`,
  con validación automática y notas de migración. Los contratos Markdown v1 ya
  están documentados en canonical.
- [ ] **Integrar Navigator ↔ Architecture**: Navigator sugiere Architecture si
  falta contexto arquitectónico; Architecture consume `.navigator/ai-context.md`
  de forma selectiva cuando existe.
- [ ] **Integrity gate ejecutable de SDD** (`tools/sdd_integrity.py`): parsear
  `tasks.md`, resolver los paths citados por cada `[x]` y salir con código distinto
  de cero ante tareas marcadas sin artefacto ni evidencia. Hoy el control central
  de SDD depende por completo del prompt y lo verifica el mismo actor que produjo
  el trabajo, en contra del principio 2 de este backlog.
- [ ] Añadir i18n opcional de descripciones visibles, manteniendo español por
  defecto y evitando duplicar la lógica canónica.

Definición de hecho: fixtures y tests verifican salidas deterministas, schemas,
presupuestos y actualización incremental. La IA completa o revisa resultados,
pero no inventa desde cero toda la estructura.

---

## P3 — Diferido o condicionado a evidencia

- [ ] Adapter Graphify real para Capa 3, solo si la demo muestra consultas donde
  el grafo supera claramente a mapa de módulos + búsqueda puntual.
- [ ] AST multilenguaje, SCIP o LSIF, solo si las heurísticas de P2 no alcanzan la
  precisión necesaria.
- [ ] Enforcement duro de rutas de escritura por host, cuando las plataformas
  ofrezcan controles compatibles.
- [ ] Matriz multi-vendor de modelos, solo si existe una necesidad de producto
  distinta de seleccionar automáticamente el modelo.
- [ ] Nuevas skills de dominio, solo con evidencia de adopción de las actuales.

### No hacer

| Idea | Motivo |
| --- | --- |
| Unificar `project-navigator` + `architecture` | Roles, contexto y permisos diferentes |
| Auto-selección o hardcode de modelo | Reduce portabilidad y control del usuario |
| Prometer “≥90 % menos tokens” sin medición | Crea una expectativa no demostrada |
| Añadir agentes para cubrir cada tarea | Aumenta solapes y coste de adopción |
| Confiar en el prompt como sandbox | Las instrucciones no sustituyen permisos técnicos |

---

## Hecho

- [x] Contrato MVP migrado a `canonical/skills/project-navigator/` y criterios
  manuales extraídos a [navigator-smoke.md](navigator-smoke.md).
- [x] Skill y agente `project-navigator` creados en `canonical/`.
- [x] Adapters de OpenCode, Copilot y Kiro añadidos al árbol de trabajo junto al manifest.
- [x] Pipeline base de render y validación para 10 skills, 9 agentes y 3 plataformas.
- [x] Catálogo, uso y README actualizados inicialmente con Navigator.
- [x] Smoke MVP aprobado en Copilot, OpenCode 1.18.3 y Kiro sobre Genera CRM;
  modelos MiniMax-M3 y Claude 4.6, incluida regresión de instancia raíz y estados
  de capas (2026-08-05).
- [x] P0.1 cerrado como unidad Git atómica (commit `1730348`) y verificado desde
  clon limpio: render, validate e integrity en exit `0` y `git diff --exit-code`
  limpio.
- [x] P0.2: `validate.py` no destructivo (render en tmp, `generated/` intacto),
  validación de manifest/adapters (tipos, campos, IDs, frontmatter), protección
  contra path traversal en `render.py` y `validate.py`, detección de filenames
  duplicados, colisiones y artefactos huérfanos. `render.py` acepta `--output`.
  Pruebas negativas en `tools/test_validate.py` (14/14) e integradas en
  `test_integrity.py` (252/252).
- [x] CI base en GitHub Actions y validación de enlaces Markdown locales mediante
  `tools/check_links.py` y `tools/test_links.py`.
- [x] P1.4: snippet de `.navigator/cache/` publicado en [uso.md](uso.md).
- [x] P0.4 cerrado salvo la ejecución en Windows. Estado previo reproducido y
  corregido: los tres instaladores bash declaraban «Instalación completada» con
  exit `0` sin haber copiado nada cuando faltaba `generated/`, y `--dry-run`
  creaba 3 directorios en Kiro y 4 en OpenCode. Nuevo `tools/install_preflight.py`
  centraliza la definición de «instalación completa» a partir del manifest y lo
  comparten los seis instaladores (`--check-source` antes de escribir,
  `--check-installed` antes de declarar éxito). Artefactos no declarados se
  informan y **nunca** se borran, por no poder distinguirlos de skills propias.
  Corregido además `find -printf` (extensión GNU ausente en macOS) y las rutas de
  backup de Copilot, que usaban etiquetas con espacios, paréntesis y `~`.
  Evidencia: `tools/test_install.py` pasa 72/72 (antes 28/42 con los mismos
  tests), `bash -n` limpio en los 6 scripts, y ambos pasos añadidos al CI.
  Restauración y desinstalación documentadas en
  [instalacion.md](instalacion.md).
- [x] Mitad Bash de la comprobación de sintaxis de P0.3: `bash -n` sobre
  `scripts/install/*.sh` y `scripts/backup/*.sh` en CI. La mitad PowerShell sigue
  abierta porque requiere un runner Windows.
- [x] P0.6 cerrado. El bloque del gate se reescribió en dos oraciones: el token
  lleva solo el matiz de plataforma (o cadena vacía) y la frase común vive en
  canonical, de modo que las tres plataformas rinden prosa gramatical. La
  validación de sustituciones destapó un **segundo** token muerto que el análisis
  inicial no vio, `{{platform_name}}`, también declarado en las tres plataformas y
  sin usar; se retiró junto a `{{sdd_start_instruction}}` y la tabla de tokens de
  [arquitectura-del-kit.md](arquitectura-del-kit.md) se corrigió para reflejar los
  tres que quedan. `validate.py` gana dos comprobaciones: sustitución declarada y
  no usada, y token fuera de `SKILL.md` (que `render.py` no sustituiría y llegaría
  literal al modelo). Evidencia: `test_validate.py` 14/14 (antes 12/12) con dos
  pruebas negativas nuevas, `test_integrity.py` 252/252 y el resto del pipeline en
  verde. Coste medido: **0 tokens por turno** (`SKILL.md` varía entre −2 y +1
  caracteres) y **+56 tokens netos** en referencias bajo demanda, concentrados en
  `templates.md`.
- [x] Commit `67b76fc` (2026-09-01): testing adaptativo integrado en SDD. Una
  feature normal usa TDD focalizado; TDD estricto queda bajo petición explícita;
  bugfix usa regresión y legado usa caracterización. Evidencia: contrato SDD
  `tools/test_sdd_contract.py` en 46/46, `tools/test_validate.py` en 14/14,
  `tools/test_integrity.py` en 252/252 y `tools/test_install.py` en 72/72.
  Medición de contexto posterior: 1.417 palabras de agentes, 13.756 de skills y
  9.038 de referencias bajo demanda. Son métricas de contexto, no un porcentaje
  de coste por feature.

Estos elementos describen implementación existente, no certifican por sí solos
que el estado actual esté listo para release. Los gates de P0 determinan eso.

---

## Registro histórico — 2026-08-05

Estado comprobado antes del cierre de P0.1 y P0.2. Se conserva como evidencia
histórica; no define el siguiente trabajo vigente.

- Canonical de Project Navigator actualizado con schemas, gate de disponibilidad,
  compactación post-bootstrap y resolución determinista de instancia.
- Artefactos regenerados para Copilot, OpenCode y Kiro.
- Instalaciones globales de las tres plataformas comparadas byte a byte con
  `generated/`: 9 skills y 8 agentes por plataforma.
- Smoke MVP aprobado en las tres plataformas; evidencia en
  [navigator-smoke.md](navigator-smoke.md).
- `tools/validate.py` correcto y `tools/test_integrity.py` en 230/230.
- El antiguo framework quedó como redirección temporal; su contrato vive en
  canonical y el runbook temporal de smoke fue eliminado.

Los gates P0.1 y P0.2 de este registro quedaron cerrados posteriormente, con la
evidencia indicada bajo **Hecho**. En ese momento, el siguiente trabajo vigente era
P0.3; el estado actual se describe en las secciones superiores.

No iniciar P2, Graphify ni nuevas skills mientras estos gates P0 sigan abiertos.

---

## Orden de ejecución

1. Completar P0.3, empezando por la matriz de SO. Es lo único que puede validar
   los tres instaladores PowerShell, cuyo contrato hoy solo está garantizado de
   forma estática, y desbloquea el último ítem abierto de P0.4.
2. Endurecer la seguridad con P0.5.
3. Ejecutar los smoke tests y la demo de P1 antes de afirmar utilidad o ahorro.
4. Completar los pendientes restantes de P1.5; medir el coste de cualquier texto
   nuevo antes de incorporarlo al prompt.
5. Implementar P2 solo donde los resultados de P1 muestren una limitación real.
6. Mantener P3 diferido hasta que exista evidencia de retorno.

## Cómo actualizar este backlog

1. Tomar el primer ítem abierto de la prioridad activa.
2. Implementar el cambio mínimo y sus pruebas.
3. Ejecutar los comandos de la definición de hecho correspondiente.
4. Marcar el checkbox solo con evidencia verificable.
5. Añadir bajo **Hecho** una referencia breve a la evidencia, fecha o commit.
6. Si un criterio no puede verificarse, mantenerlo abierto y documentar el bloqueo.

## Referencias

- Contrato Navigator: [`canonical/skills/project-navigator/SKILL.md`](../canonical/skills/project-navigator/SKILL.md)
- Smoke test Navigator: [navigator-smoke.md](navigator-smoke.md)
- Contrato SDD: [`canonical/skills/sdd-spec/SKILL.md`](../canonical/skills/sdd-spec/SKILL.md)
- Agente SDD: [`canonical/agents/sdd.md`](../canonical/agents/sdd.md)
- Catálogo: [catalogo.md](catalogo.md)
- Uso: [uso.md](uso.md)
- Arquitectura del kit: [arquitectura-del-kit.md](arquitectura-del-kit.md)
- Instalación: [instalacion.md](instalacion.md)
- Contribución: [desarrollo.md](desarrollo.md)
