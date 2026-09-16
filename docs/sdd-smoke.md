# Smoke test de SDD y testing adaptativo

Validación manual del agente SDD después de instalarlo. Ejecuta los escenarios en
un repositorio desechable con una suite pequeña y controlada: varios casos escriben
specs, tests y código de producto tras las aprobaciones correspondientes.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala una plataforma y reinicia la herramienta.
3. Abre un repositorio de prueba sin secretos, con Git y tests ejecutables.
4. Selecciona el agente `sdd` y registra plataforma, versión, modelo, fecha y commit.

## Gate 0 y preflight por fase

Antes de los escenarios funcionales, valida estas variantes:

- Una petición `direct` recibe `Modelo recomendado: BAJO` y continúa sin esperar
  confirmación.
- Una feature `standard` o `deep` nueva muestra solo `Requirements` y
  `Modelo recomendado para Requirements: <nivel>`; no muestra recomendaciones para
  todo el flujo futuro y termina el turno.
- `lite` muestra una sola recomendación para Quick Plan, sin exponer sus pasos
  internos. Un bugfix no trivial sigue el flujo `standard`.
- En cada transición, el agente muestra en un mismo mensaje el resumen verificable,
  el gate actual y la recomendación de la próxima fase, condicionada a la aprobación
  actual. La recomendación no crea un gate adicional.
- Solo una respuesta que apruebe la fase actual y confirme el nivel recomendado o el
  actual inicia la siguiente. `apruebo`, `adelante` o `continúa` por separado deben
  pedir la decisión faltante.
- Si cambia alcance o riesgo, recalcula antes de iniciar. `lite` a `standard` siempre
  solicita confirmar el cambio de flujo aunque el nivel coincida.
- La salida usa únicamente `BAJO`, `MEDIO` y `ALTO`, sin nombres de modelos o
  proveedores, y el agente nunca intenta cambiar el modelo del host.

## 1. Direct sin test nuevo

Prompt:

```text
Corrige un error ortográfico en el README.
```

Esperado:

- Selecciona `direct`, sin spec de cuatro fases ni gates.
- Recomienda `BAJO` de forma informativa y no detiene el flujo.
- No crea un test ceremonial.
- Modifica únicamente el texto y ejecuta un check aplicable si existe.

## 2. Direct con microciclo TDD

Prepara una función pura pequeña con una condición equivocada. Prompt:

```text
Corrige esta condición localizada y verifica el resultado.
```

Esperado:

- Mantiene `direct` si cumple todos sus límites de riesgo.
- Crea u observa un test RED que falla por la condición.
- Implementa GREEN mínimo, ejecuta la suite y no crea una spec innecesaria.

## 3. Selección automática de lite

Prepara un cambio de comportamiento localizado, reversible, con resultado claro,
varios criterios y tests viables, que reutilice un patrón existente y no cumpla el
umbral trivial de `direct`. No menciones un modo. Esperado:

- Descarta `direct` por motivos verificables y selecciona `lite` automáticamente.
- Muestra `Modo SDD: lite`, recomienda normalmente `MEDIO`, explica los criterios
  satisfechos y espera confirmación en el Gate 0.
- Activa Quick Plan y no presenta `lite` como una preferencia que el usuario debía
  haber solicitado expresamente.

## 4. Límite direct / lite

Ejecuta dos variantes sobre el mismo componente: una corrección trivial, localizada
y verificable; después, un cambio claro con varios criterios y tareas trazables.

Esperado:

- La primera usa `direct`, sin spec y con aviso `BAJO` no bloqueante.
- La segunda usa `lite` si satisface todos sus criterios positivos y exclusiones.
- No elige `lite` solo porque el cambio sea pequeño ni fuerza `direct` solo porque
  esté localizado; explica el criterio que separa ambos casos.

## 5. Quick Plan exclusivo de lite

Solicita una feature apta para `lite`, sin decir «Quick Plan». Esperado:

- Al seleccionar `lite`, activa Quick Plan automáticamente como su flujo obligatorio.
- Genera requirements, design y tasks en una pasada tras el Gate 0, sin Gates 1–3.
- No presenta Quick Plan como profundidad ni variante transversal, y no lo ofrece
  fuera de `lite`.

## 6. Plan-only frente a implementación lite

Ejecuta dos variantes equivalentes: «solo planifica este cambio» y «planifica e
implementa este cambio». Esperado:

- Ambas generan el Quick Plan `lite` tras confirmar el Gate 0.
- La variante de solo planificación se detiene después de `tasks.md`, deja las
  tareas pendientes, no modifica producto y no crea `verification.md`.
- La variante con implementación continúa sin Gates 1–3 adicionales, implementa
  las tareas y crea `verification.md` compacto antes de cerrar sin Gate 4.

## 7. Verificación compacta y evidencia TDD de lite

Implementa mediante `lite` un comportamiento observable pequeño con harness viable.
Esperado:

- `design.md` declara TDD focalizado y `tasks.md` ordena RED → GREEN → REFACTOR.
- Antes de producción observa un RED que falla por la razón esperada; registra GREEN
  y la suite final sin inventar resultados.
- `verification.md` compacto contiene estrategia, RED o baseline, GREEN, suite,
  excepciones y matriz requisito → tarea → test/check → evidencia → estado.
- La evidencia principal queda en `verification.md`, no solo en tareas o en el
  resumen final; no abre Fase 4 ni solicita Gate 4.

## 8. Combinaciones inválidas de Quick Plan

Ejecuta `direct con Quick Plan`, `standard con Quick Plan` y `deep con Quick Plan`.
Esperado: rechaza cada combinación, explica que Quick Plan es exclusivo de `lite` y
no omite gates ni convierte silenciosamente el modo solicitado.

## 9. Exclusiones de riesgo de lite

Solicita Quick Plan por separado para una API pública, una migración persistente,
un cambio de autenticación y una coordinación relevante entre capas. Esperado:

- No usa `lite` aunque el diff estimado sea pequeño o el usuario pida Quick Plan.
- Explica la exclusión concreta, propone `standard` y espera confirmación antes de
  generar artefactos o implementar.
- Aplica el mismo fallback ante reglas ambiguas, legado riesgoso o falta de una
  verificación viable.

## 10. Reclasificación lite → standard con el mismo nivel

Inicia un cambio elegible como `lite` con recomendación `MEDIO`; durante la lectura
puntual revela un cruce relevante de módulos que mantiene `MEDIO` como nivel
recomendado. Esperado:

- Se detiene en un punto seguro, conserva como pendiente el estado no completado y
  propone `standard`.
- Solicita confirmación por el cambio de política de gates aunque el nivel de modelo
  siga siendo `MEDIO`; no continúa basándose en el Gate 0 anterior.
- Si además cambia el nivel, combina ambos avisos en una sola salida.

## 11. Standard explícito no se rebaja

Prompt:

```text
Planifica esta feature localizada en modo standard.
```

Esperado: conserva `standard` y Gates 1–4 aunque durante el preflight descubra que
el alcance también podría cumplir `lite`; puede señalar la alternativa, pero no
rebaja el modo solicitado.

## 12. Feature standard

Prompt:

```text
Añade bloqueo de cuenta después de tres intentos fallidos.
```

Esperado:

- Primero recomienda el nivel solo para `Requirements`, espera confirmación y no
  carga contexto pesado.
- Selecciona `standard`; no implementa antes de aprobar requisitos, diseño y tareas.
- Tras Requirements, muestra resumen + Gate 1 + recomendación para Design. La
  respuesta debe aprobar Requirements y confirmar el nivel de Design.
- Tras Design, repite la misma secuencia para Tasks; después de Gate 3, la repite para
  Implementación. No presenta una recomendación como un gate nuevo.
- `design.md` declara TDD focalizado y la tarea de comportamiento expresa RED → GREEN
  → REFACTOR.
- Tras confirmar Implementación, observa RED antes de escribir el comportamiento
  productivo. Al terminar, muestra resumen + preflight de Verification y espera su
  nivel antes de ejecutar la suite.
- Fase 4 registra comandos/resultados; después solo muestra Gate 4 y no cierra
  requisitos sin evidencia.

## 13. Deep no implica TDD estricto

Repite la feature anterior solicitando `deep`, pero no TDD estricto.

Esperado: aumenta la profundidad documental permitida y conserva TDD focalizado;
no exige evidencia RED/GREEN por cada incremento interno.

## 14. TDD estricto no implica deep

Prompt:

```text
Planifica e implementa la feature en modo standard con TDD estricto.
```

Esperado:

- Mantiene `standard`.
- Cada incremento productivo comienza con un RED observado.
- Registra excepciones; no adelanta código de comportamiento ni crea abstracciones
  anticipadas solo para facilitar mocks.

## 15. Bugfix no trivial usa standard

Prepara un defecto reproducible que no cumpla todos los límites triviales de
`direct`. Esperado:

- Selecciona `standard`, aunque el resultado esperado sea claro y el fix estimado
  parezca localizado; un bugfix no trivial queda excluido de `lite`.
- Un bug realmente trivial todavía puede ser `direct` si cumple todos sus límites.
- Primero crea una regresión que falla por el defecto.
- Aplica el fix mínimo y confirma regresión + suite verdes.

## 16. Refactor legado

Solicita refactorizar comportamiento existente sin cobertura. Esperado:

- Crea caracterización verde antes y después del refactor.
- Declara qué comportamiento preserva y no congela conscientemente el defecto.
- No llama TDD al baseline verde.

## 17. Ambigüedad legacy de tres archivos

Prepara una spec anterior a `lite` con estos archivos, sin marcador de modo ni
`verification.md`:

```text
.sdd/specs/perfil-edicion/requirements.md
.sdd/specs/perfil-edicion/design.md
.sdd/specs/perfil-edicion/tasks.md
```

Solicita reanudarla. Esperado:

- No infiere que sea un plan `lite` ni un `standard` incompleto solo por tener tres
  archivos.
- Muestra la ruta y pregunta qué modo/estado debe conservar antes de continuar.
- No añade retroactivamente `Modo SDD: lite` ni migra los artefactos sin aprobación.

## 18. RED falso

Propón un test que el código actual ya satisface. Esperado: el agente lo clasifica
como caracterización o cobertura retroactiva; no afirma haber aplicado TDD.

## 19. Ausencia de harness

Usa un proyecto trivial sin infraestructura de tests. Esperado:

- No instala dependencias «por si acaso» ni crea tests tautológicos.
- Si no cambia comportamiento observable, usa validadores existentes.
- Si sí cambia comportamiento, registra la limitación y verificación alternativa;
  escala a `standard` cuando el riesgo deje de ser trivial.

## 20. Creación agrupada por módulo

Prompt:

```text
Crea una spec standard en .sdd/specs/modo-invitado/android-contactos/.
```

Esperado:

- Usa exactamente la ruta indicada y conserva los gates de `standard`.
- Crea los artefactos en la carpeta final, no directamente en `modo-invitado/`.
- No crea una segunda spec plana en `.sdd/specs/android-contactos/`.

## 21. Compatibilidad con ruta plana

Prompt:

```text
Crea una spec standard en .sdd/specs/perfil-edicion/.
```

Esperado: acepta la ruta plana sin exigir un módulo ni añadir niveles artificiales.

## 22. Reanudación recursiva

Prepara una única spec incompleta en
`.sdd/specs/modo-invitado/android-contactos/`, con `requirements.md` y
`design.md`. Solicita continuar la spec sin indicar su ruta.

Esperado:

- Encuentra la spec mediante búsqueda recursiva del archivo marcador.
- Trata `modo-invitado/` como agrupador, no como una spec incompleta.
- Reanuda en la carpeta hoja y no crea una copia plana.

## 23. Reanudación ambigua

Prepara estas specs incompletas:

```text
.sdd/specs/modo-invitado/android-contactos/requirements.md
.sdd/specs/modo-registrado/android-contactos/requirements.md
```

Solicita continuar `android-contactos` sin indicar la ruta completa. Esperado:

- No selecciona por el nombre final compartido.
- Muestra ambas rutas relativas y pregunta cuál debe continuar.

## 24. Rechazo de ruta insegura

Prompt:

```text
Crea la spec en .sdd/specs/../../src/.
```

Esperado: rechaza la ruta porque escapa de `.sdd/specs/` y solicita una ruta
relativa segura; no escribe fuera de `.sdd/specs/`.

## 25. Navigator vigente

Prepara `.navigator/config.yaml`, `ai-context.md` y `module-map.json` con el mismo
`source_commit` que el repositorio limpio. Solicita una feature `standard` sobre un
módulo indexado.

Esperado:

- Lee primero el steering y ejecuta el preflight de Navigator.
- Usa únicamente la capa mínima para localizar el módulo.
- Después consulta el contexto de dominio y el código puntual requerido por la fase.
- Presenta Navigator como orientación, no como sustituto del código.

## 26. Navigator ausente

Elimina `.navigator/` del repositorio desechable y solicita una feature.

Esperado:

- Continúa con steering, documentación aplicable y código puntual.
- No crea `.navigator/`, no añade un gate propio de Navigator y no bloquea los
  gates normales de SDD.
- Puede recomendar bootstrap sin ejecutarlo automáticamente.

## 27. Navigator incompleto

Prepara `config.yaml` con `context: true` y `module_map: true`, pero omite
`module-map.json`.

Esperado:

- Usa `ai-context.md` solo si existe y es legible.
- Declara únicamente la capa relevante ausente y degrada a fuentes directas.
- No inventa módulos ni intenta reparar el índice durante SDD.

## 28. Navigator desfasado o no verificable

Ejecuta dos variantes: primero usa un `source_commit` anterior y cambia un archivo
del módulo consultado; después omite el baseline o usa baselines distintos entre
los artefactos.

Esperado:

- Clasifica la primera variante como `desfasado` y la segunda como
  `no_verificable`; `generated_at` no basta para elevar la confianza.
- Usa el mapa únicamente como pista de ubicación.
- Confirma en documentación y código real toda afirmación relevante.
- Un cambio local claramente ajeno no se presenta automáticamente como desfase del
  módulo; si la relevancia es incierta, conserva `no_verificable`.

## 29. Actualización explícita

Con Navigator desfasado, pide a SDD que continúe y luego acepta su recomendación de
actualizar los índices.

Esperado:

- Antes de la aceptación, SDD no escribe `.navigator/` ni cambia de agente.
- La actualización se realiza únicamente mediante Project Navigator, conservando
  sus avisos, permisos y gates.
- Tras aportar el resultado, SDD repite el preflight antes de volver a usar los
  índices y retoma el gate SDD correspondiente.

## Criterio de cierre

La prueba pasa si el Gate 0 y los veintinueve escenarios conservan proporcionalidad,
recomiendan capacidad para la próxima fase sin identificar productos o proveedores, respetan gates y
distinguen TDD de caracterización/cobertura retroactiva. `lite` debe quedar entre
`direct` y `standard`, con Quick Plan exclusivo, intención respetada, escalado
conservador y evidencia compacta real sin inflar código, documentación o
dependencias. Las rutas planas y agrupadas deben coexistir sin ambigüedad ni escape
de `.sdd/specs/`; las specs legacy ambiguas requieren aclaración. Navigator debe ser
opcional, verificable y de solo orientación. No marques una plataforma aprobada sin
ejecutar todos los escenarios.

| Plataforma | Versión | Modelo | Fecha | Commit kit | Resultado | Evidencia / fallos |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| OpenCode | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| Kiro | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| Claude Code | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
