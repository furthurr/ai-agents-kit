# Smoke test de SDD y testing adaptativo

Validación manual del agente SDD después de instalarlo. Ejecuta los escenarios en
un repositorio desechable con una suite pequeña y controlada: varios casos escriben
specs, tests y código de producto tras las aprobaciones correspondientes.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala una plataforma y reinicia la herramienta.
3. Abre un repositorio de prueba sin secretos, con Git y tests ejecutables.
4. Selecciona el agente `sdd` y registra plataforma, versión, modelo, fecha y commit.

## Selección explícita de metodología

Estos casos verifican que SDD sea un flujo seleccionado expresamente, no un destino
de routing por dominio. Ejecuta en un host disponible con artefactos actualizados y
un repositorio desechable. Instalar o cambiar configuración requiere autorización
específica; no basta con que el renderer haya generado archivos. `@` no garantiza
una invocación nativa: selecciona el agente en la interfaz del host.

Prepara componentes visuales y un serializador interno, ambos con requisitos claros;
para casos de spec prepara marcadores/gates reales. Usa sesiones separadas salvo
cuando se indique continuidad para comprobar deduplicación. No apruebes cambios de
producto accidentalmente mientras pruebas un gate pendiente.

| Caso | Prompt / condición de prueba | Resultado esperado |
|---|---|---|
| R01 Solo UI | «Cambia solo el color del botón existente; conserva eventos y datos». | Mantener SDD y sus gates; cargar `ui-design` solo si aporta criterio visual. |
| R02 Solo datos | «Ajusta esta serialización interna según estos requisitos; no cambia contrato público ni esquema». | Mantener SDD y sus gates; cargar `data-api` solo si aporta criterio de contrato/datos. |
| R03 Mixto | «Añade una pantalla y el endpoint que necesita». | Mantener SDD como ejecutor de la metodología completa; no fragmentar por skills. |
| R04 Ambiguo | «Mejora cómo manejo los datos». | Aclarar el objetivo y decisiones esenciales dentro del flujo SDD; no cambiar agente por la palabra datos. |
| R05 Rediseño | «Rediseña estas tres pantallas y decide sus nuevos flujos». | Mantener planificación y gates SDD. |
| R06 Datos de riesgo | «Migra el esquema y cambia la compatibilidad de esta API». | Mantener requisitos, diseño, tareas y gates SDD antes de implementar. |
| R07 Gate pendiente | Spec con una tarea visual, pero Gate 3 pendiente; solicitar implementar. | Conservar el gate; ni la petición de implementación ni una habilidad visual lo aprueban. |
| R08 Continuar SDD | Continuar el mismo alcance en el agente SDD seleccionado. | Seguir solo lo autorizado, sin repetir selección de agente ni aprobar un gate implícitamente. |
| R09 Cambio solicitado | «Quiero continuar con Developer para implementar sin SDD». | Preparar contexto portable y detener esta actividad; no cambiar la interfaz ni invocar otro agente. |
| R10 Skill de dominio | «Usa `data-api`» o «usa `ui-design`» dentro de la tarea SDD. | Aclarar que son skills técnicas; conservar SDD como ejecutor seleccionado y aplicar sus gates. |
| R11 Contexto ausente | No existe `.data/`/`.design/` para el dominio solicitado. | Continuar desde fuentes directas; no inicializar documentación ni cambiar agente automáticamente. |
| R12 Distribución | Seleccionar SDD con artefactos renderizados; comprobar acceso a referencia y política. | La selección permanece explícita; paridad estática en seis plataformas no acredita runtime en seis hosts. |

En todos los casos observar que SDD no cambia el agente activo ni invoca subagentes,
y no declara tarea completada sin evidencia. Un cambio de agente requiere petición
explícita y conserva gates pendientes. Una respuesta ambigua se aclara sin pedir
confirmar el modelo.

### Registro de ejecución

No hay resultados runtime incluidos por defecto. Conservar por escenario:

| Caso | Host/versión y fecha | Fuente probada (commit/diff) | Prompt y contexto | Respuesta observada sanitizada | Ruta esperada/observada | PASS/FAIL/bloqueado y motivo |
|---|---|---|---|---|---|---|
| R01–R12 | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado |

**Evidencia histórica** de la política de routing anterior: [smoke inicial](../.sdd/specs/recomendacion-agente-por-dominio/runtime-smoke.md),
[corrección R01](../.sdd/specs/recomendacion-agente-por-dominio/correction-evidence.md)
y [smoke de seguimiento](../.sdd/specs/recomendacion-agente-por-dominio/followup-smoke.md).
OpenCode 1.18.34: R01 inicial FAIL y corregido PASS; R04 FAIL por enumerar candidatos
fuera de v1; R06/R07/R11 bloqueados; otros casos con resultados parciales documentados.
No representa certificación de otros hosts ni garantiza decisiones deterministas.

Las pruebas de `tools/test_sdd_contract.py` comprueban instrucciones y propagación,
no sustituyen este registro. Si no hay host disponible, declarar bloqueo y mantener
pendiente la evaluación; no fabricar resultados a partir de búsquedas de texto.

## Esfuerzo previsto del LLM: referencia ReserveLab

Antes de los escenarios funcionales, verifica que SDD analice y defina un alcance
concreto. Solo entonces emite una vez el formato exacto
`Esfuerzo previsto del LLM: <nota e icono>` antes de recomendar profundidad:
1–7 🟢 o 🟠 con atención especial, 8–9 🟠, 10 🔴 o exactamente
`10+ 🔴` si supera claramente X13, nunca enteros mayores de 10. Registra referente,
factores y supuestos en la spec si existe, sin mostrarlos rutinariamente según la
[rúbrica canónica](../canonical/skills/sdd-spec/references/feature-level.md).

- Antes de tener alcance definido, no muestra una clasificación ni recomienda un
  nivel, modelo o proveedor LLM.
- Para la feature definida, la clasificación aparece una sola vez; no vuelve a
  emitirse en Requirements, Design, Tasks, Implementación ni Verification.
- La clasificación no pide confirmación ni detiene el flujo por modelo. No altera
  la aprobación de requisitos/diseño/tasks, la autorización para implementar, ni
  otros gates reales.
- Un cambio sustancial de alcance exige analizarlo de nuevo antes de actualizar la
  clasificación; una recomendación no sobrescribe la elección explícita ni crea un gate.
  Pasar a `standard` requiere una solicitud explícita del usuario.
- Ningún agente recomienda ni selecciona modelo, proveedor o nivel LLM.

### Casos manuales de esfuerzo — pendientes de ejecución en host

Los casos E01–E07, condiciones de contraste y salida esperada se mantienen en el
[respaldo opcional](sdd-effort-examples.md). Para ejecutar un smoke, aporta el
contrato del caso y el inventario de infraestructura, pide evaluar solo la
implementación/verificación y registra host, fuente, resultado y supuestos. Ninguno
se ha ejecutado por búsquedas textuales; E03/E05 son sintéticos, no benchmarks.

| Caso | Host/versión/fecha/fuente | Respuesta sanitizada y supuestos | Resultado |
|---|---|---|---|
| E01–E07 | Pendiente | Pendiente | No ejecutado |

Las suites documentales comprueban contrato, ejemplos y paridad, no sustituyen estas
observaciones ni garantizan el razonamiento de un LLM. No atribuir PASS a este
registro por haber ejecutado solo checks textuales.

## Alcance, atención y entregas — escenarios nuevos

Ejecutar en sesiones separadas con contexto técnico suficiente; no son pruebas
runtime ya realizadas. Los tests de contrato solo verifican instrucciones y paridad.

| Caso | Condición | Resultado esperado |
|---|---|---|
| A01 | Petición ambigua | Preguntar decisiones esenciales; no calificar provisionalmente ni elegir modo. |
| A02 | Transformación pura trivial nivel 1 | Alcance completo → validar/elegir direct → implementar → comprobar; sin spec. |
| A03 | Predicados locales nivel 2 | Aclarar límites/orden, recomendar direct si trivial y verificar. |
| A04 | Cálculo puro de ejemplo nivel 3 | Aclarar redondeo, direct si trivial; no extrapolar a pagos críticos. |
| A05 | Normalización/conflictos acotados nivel 4 | Presentar completo/calificar, recomendar SDD-Tiny y esperar validación y elección antes de crear el spec único. |
| A06 | Reserva nivel 6 con mecanismo y pruebas concurrentes | 6 🟠, advertencia concreta, SDD-Tiny con pruebas y evidencia en el único spec. Standard solo por solicitud explícita. |
| A07 | Reserva nivel 6 sin garantía verificable | Tiny no queda habilitado por la nota; detener/reducir hasta que haya pruebas del mecanismo y garantías. |
| A08 | Alcance conjunto 10/10+ | Recomendar SDD-Lite y ofrecer división segura; standard solo por solicitud explícita. |
| A09 | Entrega dividida sigue 10/10+ | Recomendar SDD-Lite y evaluar otra división útil o pausar; no fragmentar garantías ni seleccionar standard automáticamente. |
| A10 | Elección explícita compatible previa | Respetar modo Direct/Tiny/Lite; resolver validación pendiente. Standard solicitado conserva Gates 1–4. |
| A11 | Elegir UI tras alcance visual claro | Contexto copiable y detener actividad en SDD; sin invocación automática. |
| A12 | Cierres parciales de entregas | No cerrar conjunto sin evidencia de requisitos transversales e integración. |
| A13 | Calificación sin alcance completo previo, incluidas 10/10+ | Mostrar objetivo, comportamientos/reglas, criterios, errores/estados, exclusiones/restricciones/supuestos; validar antes de ejecutar. |
| A14 | Misma versión completa explícitamente validada y vigente | Reutilizar decisión sin repetición. Un resumen breve anterior no la acredita. |
| A15 | Alcance se ajusta o se evalúa una entrega distinta | Mostrar conjunto completo actualizado y volver a validar, no solo delta ni aprobación incompatible. |
| A16 | Respuesta «usa SDD-Lite» a pregunta conjunta | Solo modo resuelto; pedir validación pendiente antes de producir Quick Plan. |
| A17 | Validación de alcance y solicitud explícita de standard | Formalizar requirements y conservar Gate 1; aceptación común no lo aprueba. |
| A18 | Solo planificación y alcance validado | Producir únicamente lo autorizado; no inferir permiso de implementar. |
| A19 | Formalización añade condición funcional | Señalar diferencia y resolver aceptación; no implementarla silenciosamente. |

| Casos | Host/versión/fecha/fuente | Respuesta y evidencia | Resultado |
|---|---|---|---|
| A01–A19 | Pendiente | Pendiente | No ejecutado |

### Casos de modo SDD-Tiny y fronteras de score

Los casos siguen pendientes de ejecución en un host. Los contratos automatizados
verifican la política escrita y sus fronteras; no simulan decisiones de un LLM.

| Caso | Condición | Resultado esperado |
|---|---|---|
| T01 | Feature calificada 4–8, Tiny elegible, implementación solicitada | Recomendar SDD-Tiny; crear `spec.md` con estado `Planificado` antes del código; aprobar Gate 3; completar y verificar el mismo documento; Gate 4 para cierre. |
| T02 | Tiny, solo planificación | Dejar el único spec en `Planificado`; no tocar producto ni inventar resultados. |
| T03 | Tiny con pruebas locales que fallan y luego se reparan | Registrar fallo original, reparación y nuevo resultado real en el mismo documento. |
| T04 | Score 4–8, Tiny no elegible | Explicar conflicto; no forzar Tiny ni aumentar la nota; aplicar reducción/división u otra ruta segura. |
| T05 | Feature score 9 o 10 | Recomendar SDD-Lite y conservar Quick Plan; no sustituirlo por Tiny. |
| T06 | Feature 10+ | Mantener score 10 + `exceeds_x13=true`, recomendar SDD-Lite y ofrecer entregas seguras. |
| T07 | Scope recomienda Direct (1–3), pero cambio no satisface sus límites | Explicar conflicto; conservar nota y guardas, ofrecer la ruta segura vigente. |
| T08 | El usuario eligió explícitamente antes otro modo compatible | Mostrar la recomendación informativa y conservar la elección anterior. |
| T09 | Solicitud explícita de Standard | No rebajar ni sustituir; aplicar Standard con Gates 1–4. |

| Casos | Host/versión/fecha/fuente | Respuesta y evidencia | Resultado |
|---|---|---|---|
| T01–T09 | Pendiente | Pendiente | No ejecutado |

## Continuidad y costo de contexto — escenarios nuevos

Ejecutar con specs y tests reales en un repositorio desechable. La paridad y los
checks textuales no acreditan estos resultados runtime. Mantener autorizaciones.

| Caso | Contexto/petición | Resultado esperado |
|---|---|---|
| C01 | Cambio aislado sin relación encontrada | Búsqueda localizada, sin cargar política de continuidad ni afirmar auditoría exhaustiva. |
| C02 | Ruta explícita o spec activa | Empezar por ella; cabecera y requisito, dependencias según impacto, sin búsqueda global rutinaria. |
| C03 | Nota 2: conservar orden que antes se restablecía | Enmienda actual/propuesto; conservar modo y aprobaciones pertinentes, no forzar direct. |
| C04 | Implementar tarea con Gate 3 pendiente | Mantener spec/gate; no implementar por recalificar la tarea como trivial. |
| C05 | Cambio localizado que conserva requisito | Direct evaluable sin evasión de tarea/gate; evidencia proporcional, sin nueva spec. |
| C06 | Modificar spec cerrada | Revisión explícita o spec vinculada; conservar cierre histórico y distinguir vigencia. |
| C07 | Pruebas/tareas previamente completadas tras enmienda | Revalidar solo afectadas; evidencia anterior histórica, no verificación del requisito nuevo. |
| C08 | Código y spec discrepan; varias specs contradictorias | Determinar tipo/autoridad; preguntar si no es evidente y no elegir por antigüedad. |
| C09 | Varias peticiones pequeñas relacionadas | Evaluar impacto conjunto sin sumar notas ni extender autorización a toda la sesión. |
| C10 | Misma spec sin cambios y luego archivos modificados | Reutilizar contexto al inicio; revalidar tras cambio sin asumir caché fiable. |

Registrar por caso herramientas/búsquedas, archivos/secciones leídos, decisiones,
gates, evidencia y métricas de tokens solo si el host las proporciona. Los presupuestos
estáticos de test_sdd_contract cubren cambio aislado, spec conocida, enmienda y
candidatas múltiples, pero no miden contenido variable del proyecto ni búsquedas reales.

| Casos | Host/versión/fecha/fuente | Respuesta y lecturas observadas | Resultado |
|---|---|---|---|
| C01–C10 | Pendiente | Pendiente | No ejecutado |

## 1. Direct sin test nuevo

Prompt:

```text
Corrige un error ortográfico en el README.
```

Esperado:

- Presenta alcance completo, resuelve validación y selección direct; sin spec ni gates de fase.
- No emite clasificación de feature para una petición puntual que no define una
  feature, ni recomienda niveles o modelos LLM.
- No crea un test ceremonial.
- Modifica únicamente el texto y ejecuta un check aplicable si existe.

## 2. Direct con regresión focalizada

Prepara una función pura pequeña con una condición equivocada. Prompt:

```text
Corrige esta condición localizada y verifica el resultado.
```

Esperado:

- Mantiene `direct` si cumple todos sus límites de riesgo.
- Reproduce la condición incorrecta cuando sea posible y cubre el caso con una regresión.
- Aplica el arreglo mínimo, ejecuta la suite y no crea una spec innecesaria.

## 3. Recomendación SDD-Tiny y selección manual

Prepara una feature de nota 6, localizada y cohesiva, con resultado claro, varios
criterios, mecanismo y tests viables; no menciones un modo. Esperado:

- Define alcance antes de modo, califica y recomienda SDD-Tiny sin prefacio ceremonial.
- Presenta nota, advertencia concreta si aplica y profundidad recomendada, sin
  referente de laboratorio ni explicaciones rutinarias de rangos/exclusiones.
- Combina aceptación del alcance completo y modo; espera ambas decisiones antes de
  escribir el spec único.
- Si ya eligió Tiny compatible, no repite elección; resuelve validación pendiente.

## 4. Límite direct / SDD-Tiny

Ejecuta dos variantes sobre el mismo componente: una corrección trivial, localizada
y verificable; después, un cambio claro con varios criterios y tareas trazables.

Esperado:

- La primera recomienda `direct`, sin spec ni recomendación de modelo.
- La segunda (nota 4–8) recomienda SDD-Tiny si satisface criterios positivos y
  exclusiones; usa un documento, no Quick Plan.
- No elige `lite` solo porque el cambio sea pequeño ni fuerza `direct` solo porque
  esté localizado; explica el criterio que separa ambos casos.

## 5. Quick Plan exclusivo de SDD-Lite

Solicita una feature apta para SDD-Lite, sin decir «Quick Plan». Esperado:

- Al seleccionar `lite`, activa Quick Plan automáticamente como su flujo obligatorio.
- Genera requirements, design y tasks en una pasada tras analizar el alcance,
  sin Gates 1–3.
- No presenta Quick Plan como profundidad ni variante transversal, y no lo ofrece
  fuera de `lite`; rechaza también `tiny` + Quick Plan.

## 6. Plan-only frente a implementación SDD-Lite

Ejecuta dos variantes equivalentes: «solo planifica este cambio» y «planifica e
implementa este cambio». Esperado:

- Ambas generan Quick Plan tras validar alcance completo y resolver selección SDD-Lite, sin pausa por modelo.
- La variante de solo planificación se detiene después de `tasks.md`, deja las
  tareas pendientes, no modifica producto y no crea `verification.md`.
- La variante con implementación continúa sin Gates 1–3 adicionales, implementa
  las tareas y crea `verification.md` compacto antes de cerrar sin Gate 4.

## 7. Verificación compacta y evidencia de SDD-Lite

Implementa mediante SDD-Lite un comportamiento observable pequeño con harness viable.
Esperado:

- `design.md` declara verificación focalizada y `tasks.md` vincula los criterios a tests/checks.
- Implementa y comprueba el comportamiento sin imponer tests antes del código;
  registra los resultados y la suite final sin inventarlos.
- `verification.md` compacto contiene estrategia, baseline o comprobación inicial, resultados, suite,
  excepciones y matriz requisito → tarea → test/check → evidencia → estado.
- La evidencia principal queda en `verification.md`, no solo en tareas o en el
  resumen final; no abre Fase 4 ni solicita Gate 4.

## 8. Combinaciones inválidas de Quick Plan

Ejecuta `direct con Quick Plan`, `tiny con Quick Plan` y `standard con Quick Plan`.
Esperado: rechaza cada combinación, explica que Quick Plan es exclusivo de `lite` y
no omite gates ni convierte silenciosamente el modo solicitado.

## 9. Exclusiones de riesgo de Tiny/Lite

Solicita Quick Plan por separado para una API pública, una migración persistente,
un cambio de autenticación y una coordinación relevante entre capas. Esperado:

- No fuerza Tiny o `lite` aunque el diff estimado sea pequeño o el usuario pida Quick Plan.
- Explica la exclusión concreta y se detiene; propone reducir/dividir el alcance.
- No selecciona `standard` como fallback. Solo continúa en ese modo si el usuario lo
  solicita explícitamente; de lo contrario no genera artefactos ni implementa.
- Aplica la misma pausa ante reglas ambiguas, legado riesgoso o falta de verificación viable.

## 10. Cambio de alcance Tiny/Lite y solicitud de Standard

Inicia un cambio como Tiny o SDD-Lite; durante la lectura puntual revela un cruce
relevante de módulos. Esperado:

- Se detiene en un punto seguro y conserva como pendiente el estado no completado;
  no supone elegibilidad por score y adapta los controles al cruce descubierto.
- Ofrece reducir/dividir alcance; solo continúa con `standard` legacy si el usuario
  solicita explícitamente ese modo. Una clasificación previa no autoriza el cambio.
- Reanaliza el alcance y actualiza la clasificación solo si el alcance definido cambió
  sustancialmente; no recomienda niveles o modelos LLM.

## 11. Standard explícito no se rebaja

Prompt:

```text
Planifica esta feature localizada en modo standard.
```

Esperado: conserva `standard` y Gates 1–4 aunque durante el preflight descubra que
el alcance también podría cumplir `lite`; puede señalar la alternativa, pero no
rebaja el modo solicitado.

## 12. Solicitud explícita de standard legacy

Prompt:

```text
Añade bloqueo de cuenta después de tres intentos fallidos. Solicito explícitamente
el modo standard legacy y sus gates.
```

Esperado:

- Analiza y define el alcance de la feature; después emite una sola vez
  `Esfuerzo previsto del LLM: <nota e icono>` y el bloque ReserveLab documentado.
  No recomienda LLM.
- Conserva `standard` por solicitud explícita; no implementa antes de aprobar
  requisitos, diseño y tareas.
- Tras Requirements, muestra resumen + Gate 1. Tras Design y Tasks presenta sus gates
  reales; no repite la nota de esfuerzo.
- La aprobación de cada gate real permite la transición correspondiente; no existe
  confirmación de modelo ni pausa por modelo.
- `design.md` declara verificación focalizada y la tarea de comportamiento identifica
  los criterios y checks necesarios, sin imponer tests antes del código.
- Tras aprobar Gate 3, implementa y verifica el comportamiento productivo.
  Al terminar, muestra resumen y ejecuta la suite automáticamente dentro del alcance
  aprobado; no repite la clasificación ni espera por modelo.
- Fase 4 registra comandos/resultados; después solo muestra Gate 4 y no cierra
  requisitos sin evidencia.

## 13. Solicitud de profundidad retirada

Prompt:

```text
Planifica esta feature en modo deep.
```

Esperado:

- Informa que `deep` fue retirado y pide elegir Direct/SDD-Tiny/SDD-Lite o solicitar
  explícitamente el modo legacy `standard`.
- No crea artefactos ni inicia Requirements mientras esa elección esté pendiente.
- Solo después de que el usuario pida `standard`, usa ese modo y sus Gates 1-4; la
  solicitud de modo no aprueba Gate 1.
- No presenta `deep` como una cuarta profundidad ni convierte la solicitud
  silenciosamente.

## 14. Verificación sin secuencia obligatoria de pruebas

Prompt:

```text
Planifica e implementa esta feature y añade pruebas después del código.
```

Esperado:

- Conserva la metodología y los gates del modo elegido, sin añadir un gate de testing.
- Declara pruebas focalizadas de criterios, errores y riesgos; no rechaza su orden de escritura.
- Ejecuta tests/checks y suite aplicable antes de cerrar, con comandos y resultados reales.
- No exige un fallo previo artificial ni introduce abstracciones para facilitar tests.

## 15. Bugfix no trivial no escala automáticamente a standard

Prepara un defecto reproducible que no cumpla todos los límites triviales de
`direct`. Esperado:

- Conserva `lite` para bugfix no trivial según la política vigente; no puntúa el bug.
- No escala a `standard` automáticamente aunque el fix no sea trivial.
- Un bug realmente trivial todavía puede ser `direct` si cumple todos sus límites.
- Reproduce el defecto cuando sea posible y cubre el caso con una regresión.
- Aplica el fix mínimo y confirma regresión + suite verdes.

## 16. Refactor legado

Solicita refactorizar comportamiento existente sin cobertura. Esperado:

- Crea caracterización verde antes y después del refactor.
- Declara qué comportamiento preserva y no congela conscientemente el defecto.
- Conserva el baseline como evidencia del comportamiento que debe preservarse.

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

## 18. Cobertura sobre código existente

Propón un test que el código actual ya satisface. Esperado: el agente lo clasifica
según su propósito como caracterización o cobertura válida; no fuerza un fallo
artificial ni inventa una ejecución previa.

## 19. Ausencia de harness

Usa un proyecto trivial sin infraestructura de tests. Esperado:

- No instala dependencias «por si acaso» ni crea tests tautológicos.
- Si no cambia comportamiento observable, usa validadores existentes.
- Si sí cambia comportamiento, registra la limitación y verificación alternativa;
  no escales automáticamente a `standard` si el riesgo impide Direct, Tiny o Lite.
  Detente y pide reducir/dividir alcance o una solicitud explícita del modo legacy.

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
- La actualización se realiza mediante `documentation-orchestrator` con la skill
  Project Navigator local, conservando permisos y gates reales sin aviso de LLM.
- Tras aportar el resultado, SDD repite el preflight antes de volver a usar los
  índices y retoma el gate SDD correspondiente.

## Criterio de cierre

### Comprobación multiagente de ausencia de recomendaciones LLM

En una instalación nueva y con cada agente, solicita una consulta puntual y una
operación amplia. Ninguno debe recomendar nivel, modelo o proveedor LLM ni hacer
depender la continuidad de una selección de modelo. SDD debe cumplir el escenario
de clasificación única del nivel de feature definido arriba. Los gates de escritura,
remediación, release y fases SDD continúan requiriendo sus aprobaciones efectivas;
los permisos `ask`/`deny` del host no cambian.

Estos checks interactivos se registran como no ejecutados hasta realizarlos en
cada plataforma; los tests textuales y el render no los sustituyen.

La prueba pasa si los escenarios conservan proporcionalidad, recomiendan `direct`/Tiny/Lite
según la rúbrica y solo activan `standard` legacy ante solicitud explícita. SDD califica
una sola vez después de definir el alcance, no puntúa trabajos no-feature, no recomienda
modelos, respeta elecciones/gates y usa verificación focalizada, regresión o
caracterización según el caso. Tiny crea/actualiza un spec único y conserva tests/evidencia; Lite mantiene
Quick Plan exclusivo; Direct conserva sus guardas. Se respeta intención, pausa segura ante
exclusiones y evidencia real sin inflar código, documentación o
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
