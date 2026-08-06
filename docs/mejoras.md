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

- [ ] **Versionar `project-navigator` como una unidad atómica**: fuente canónica,
  adapters, artefactos generados, manifest y documentación deben entrar juntos.
- [x] **Resolver contradicciones documentales**: README, visión y arquitectura
  deben coincidir sobre si Navigator está planificado, en MVP o estable.
- [ ] **Dejar el árbol generado reproducible desde un clon limpio**, sin depender
  de archivos locales o no rastreados.

Definición de hecho:

- Un clon limpio puede ejecutar render y validación sin archivos faltantes.
- `git status --short` queda vacío después de regenerar.
- README, catálogo, visión y arquitectura describen el mismo estado del producto.

### P0.2 — Validación segura y completa

- [ ] **Hacer `tools/validate.py` no destructivo**: renderizar en un directorio
  temporal configurable y comparar hashes sin renombrar ni borrar `generated/`.
- [ ] **Validar schemas y valores** de `manifest.json`, `platform.json` y adapters:
  tipos, campos obligatorios, IDs, extensiones y frontmatter esperado.
- [ ] **Impedir path traversal y escrituras fuera de destino**: `filename` debe
  ser un nombre relativo seguro y permanecer bajo `generated/<platform>/agents/`.
- [ ] **Detectar IDs y filenames duplicados**, colisiones de salida y entradas
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

- [ ] **Añadir CI en GitHub Actions** para Python soportado y, cuando aplique,
  Linux, macOS y Windows.
- [ ] Ejecutar parseo JSON/YAML, render reproducible, validación e integridad.
- [ ] Comprobar sintaxis de scripts Bash y PowerShell.
- [ ] Añadir pruebas negativas: token sin resolver, adapter incompleto, filename
  inseguro, colisión y artefacto generado desactualizado.
- [ ] Proteger el merge cuando el pipeline no esté verde.

Definición de hecho: el workflow se ejecuta en pull requests, detecta al menos un
fixture inválido por cada clase crítica y pasa desde un clon limpio.

### P0.4 — Instalación estricta y reversible

- [ ] **Fallar con código distinto de cero** si faltan skills, agentes o fuentes
  generadas; no declarar instalación completada tras omitir contenido requerido.
- [ ] Garantizar que `--dry-run` / `-DryRun` no cree ni modifique directorios.
- [ ] Añadir un preflight que compruebe render validado, destinos y herramientas.
- [ ] Definir cómo retirar artefactos obsoletos sin borrar contenido ajeno al kit.
- [ ] Documentar restauración de backup y desinstalación.
- [ ] Probar install, actualización, dry-run y rollback en directorios HOME
  temporales para las tres plataformas.

Definición de hecho: los tests demuestran instalación completa, fallo temprano,
dry-run sin efectos y restauración del estado anterior.

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
- [ ] Añadir el snippet recomendado de `.gitignore` para `.navigator/cache/`.

Definición de hecho: las pruebas cubren índice ausente, desactualizado, parcial y
editado manualmente; el agente no presenta datos obsoletos como actuales.

---

## P2 — Automatización de contexto

Realizar solo después de completar P0 y la evidencia esencial de P1. Estas tareas
reducen dependencia del modelo y hacen que Navigator sea más que una convención
documental.

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
- [x] Pipeline base de render y validación para 9 skills, 8 agentes y 3 plataformas.
- [x] Catálogo, uso y README actualizados inicialmente con Navigator.
- [x] Smoke MVP aprobado en Copilot, OpenCode 1.18.3 y Kiro sobre Genera CRM;
  modelos MiniMax-M3 y Claude 4.6, incluida regresión de instancia raíz y estados
  de capas (2026-08-05).

Estos elementos describen implementación existente, no certifican por sí solos
que el estado actual esté listo para release. Los gates de P0 determinan eso.

---

## Checkpoint de continuidad — 2026-08-05

Estado comprobado al cerrar la sesión:

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

Siguiente gate, en este orden:

1. Revisar el worktree y preservar todos los cambios intencionales existentes.
2. Cerrar P0.1 con una unidad Git atómica y verificarla desde un clon limpio. El
   commit requiere confirmación explícita del usuario.
3. Implementar P0.2 empezando por `validate.py` no destructivo y un output
   temporal configurable en `render.py`.
4. Añadir validación de schemas, IDs, filenames, colisiones, path traversal y
   artefactos huérfanos, con pruebas negativas.
5. Solo después crear CI (P0.3).

No iniciar P2, Graphify ni nuevas skills mientras estos gates P0 sigan abiertos.

---

## Orden de ejecución

1. Completar P0.1 y preparar un estado coherente desde clon limpio.
2. Completar P0.2 y P0.3 para convertir la reproducibilidad en un gate automático.
3. Endurecer instalación y seguridad con P0.4 y P0.5.
4. Ejecutar los smoke tests y la demo de P1 antes de afirmar utilidad o ahorro.
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
- Catálogo: [catalogo.md](catalogo.md)
- Uso: [uso.md](uso.md)
- Arquitectura del kit: [arquitectura-del-kit.md](arquitectura-del-kit.md)
- Instalación: [instalacion.md](instalacion.md)
- Contribución: [desarrollo.md](desarrollo.md)
