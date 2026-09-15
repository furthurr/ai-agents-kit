# Smoke test de SDD y testing adaptativo

Validación manual del agente SDD después de instalarlo. Ejecuta los escenarios en
un repositorio desechable con una suite pequeña y controlada: varios casos escriben
specs, tests y código de producto tras las aprobaciones correspondientes.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala una plataforma y reinicia la herramienta.
3. Abre un repositorio de prueba sin secretos, con Git y tests ejecutables.
4. Selecciona el agente `sdd` y registra plataforma, versión, modelo, fecha y commit.

## Gate 0 de modelo

Antes de los escenarios funcionales, valida estas variantes:

- Una petición `direct` recibe `Modelo recomendado: BAJO` y continúa sin esperar
  confirmación.
- Una feature `standard`, un Quick Plan o un bugfix no trivial muestran un nivel
  global y el perfil de fases pendientes, y terminan el turno.
- Tras responder `continúa con el actual`, el agente no repite el Gate 0 antes de
  cada fase.
- Si el alcance cambia pero conserva el mismo nivel, el agente informa y continúa;
  si cambia el nivel global, muestra de nuevo el Gate 0 y espera.
- La salida usa únicamente los niveles `BAJO`, `MEDIO` y `ALTO`, sin nombres de
  modelos o proveedores, y el agente nunca intenta cambiar el modelo del host.

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

## 3. Feature standard

Prompt:

```text
Añade bloqueo de cuenta después de tres intentos fallidos.
```

Esperado:

- Primero recomienda el nivel, espera confirmación y no carga contexto pesado.
- Selecciona `standard`; no implementa antes de aprobar requisitos, diseño y tareas.
- `design.md` declara TDD focalizado.
- La tarea de comportamiento expresa RED → GREEN → REFACTOR.
- Tras GATE 3, observa RED antes de escribir el comportamiento productivo.
- Fase 4 registra comandos/resultados y no cierra requisitos sin evidencia.

## 4. Deep no implica TDD estricto

Repite la feature anterior solicitando `deep`, pero no TDD estricto.

Esperado: aumenta la profundidad documental permitida y conserva TDD focalizado;
no exige evidencia RED/GREEN por cada incremento interno.

## 5. TDD estricto no implica deep

Prompt:

```text
Planifica e implementa la feature en modo standard con TDD estricto.
```

Esperado:

- Mantiene `standard`.
- Cada incremento productivo comienza con un RED observado.
- Registra excepciones; no adelanta código de comportamiento ni crea abstracciones
  anticipadas solo para facilitar mocks.

## 6. Bugfix reproducible

Prepara un defecto con resultado esperado claro. Esperado:

- Bug trivial puede ser `direct`; el resto usa los gates normales.
- Primero crea una regresión que falla por el defecto.
- Aplica el fix mínimo y confirma regresión + suite verdes.

## 7. Refactor legado

Solicita refactorizar comportamiento existente sin cobertura. Esperado:

- Crea caracterización verde antes y después del refactor.
- Declara qué comportamiento preserva y no congela conscientemente el defecto.
- No llama TDD al baseline verde.

## 8. Quick Plan

Solicita explícitamente Quick Plan para una feature bien entendida. Esperado:

- Aplica una vez el Gate 0 y, tras confirmación, genera requirements, design y tasks
  en una pasada, sin gates de fase ni Fase 4.
- Registra la estrategia adaptativa y el orden del ciclo.
- Si después se implementa, deja evidencia en tareas y resumen final.

## 9. RED falso

Propón un test que el código actual ya satisface. Esperado: el agente lo clasifica
como caracterización o cobertura retroactiva; no afirma haber aplicado TDD.

## 10. Ausencia de harness

Usa un proyecto trivial sin infraestructura de tests. Esperado:

- No instala dependencias «por si acaso» ni crea tests tautológicos.
- Si no cambia comportamiento observable, usa validadores existentes.
- Si sí cambia comportamiento, registra la limitación y verificación alternativa;
  escala a `standard` cuando el riesgo deje de ser trivial.

## 11. Creación agrupada por módulo

Prompt:

```text
Crea una spec standard en .sdd/specs/modo-invitado/android-contactos/.
```

Esperado:

- Usa exactamente la ruta indicada y conserva los gates de `standard`.
- Crea los artefactos en la carpeta final, no directamente en `modo-invitado/`.
- No crea una segunda spec plana en `.sdd/specs/android-contactos/`.

## 12. Compatibilidad con ruta plana

Prompt:

```text
Crea una spec standard en .sdd/specs/perfil-edicion/.
```

Esperado: acepta la ruta plana sin exigir un módulo ni añadir niveles artificiales.

## 13. Reanudación recursiva

Prepara una única spec incompleta en
`.sdd/specs/modo-invitado/android-contactos/`, con `requirements.md` y
`design.md`. Solicita continuar la spec sin indicar su ruta.

Esperado:

- Encuentra la spec mediante búsqueda recursiva del archivo marcador.
- Trata `modo-invitado/` como agrupador, no como una spec incompleta.
- Reanuda en la carpeta hoja y no crea una copia plana.

## 14. Reanudación ambigua

Prepara estas specs incompletas:

```text
.sdd/specs/modo-invitado/android-contactos/requirements.md
.sdd/specs/modo-registrado/android-contactos/requirements.md
```

Solicita continuar `android-contactos` sin indicar la ruta completa. Esperado:

- No selecciona por el nombre final compartido.
- Muestra ambas rutas relativas y pregunta cuál debe continuar.

## 15. Rechazo de ruta insegura

Prompt:

```text
Crea la spec en .sdd/specs/../../src/.
```

Esperado: rechaza la ruta porque escapa de `.sdd/specs/` y solicita una ruta
relativa segura; no escribe fuera de `.sdd/specs/`.

## 16. Navigator vigente

Prepara `.navigator/config.yaml`, `ai-context.md` y `module-map.json` con el mismo
`source_commit` que el repositorio limpio. Solicita una feature `standard` sobre un
módulo indexado.

Esperado:

- Lee primero el steering y ejecuta el preflight de Navigator.
- Usa únicamente la capa mínima para localizar el módulo.
- Después consulta el contexto de dominio y el código puntual requerido por la fase.
- Presenta Navigator como orientación, no como sustituto del código.

## 17. Navigator ausente

Elimina `.navigator/` del repositorio desechable y solicita una feature.

Esperado:

- Continúa con steering, documentación aplicable y código puntual.
- No crea `.navigator/`, no añade un gate propio de Navigator y no bloquea los
  gates normales de SDD.
- Puede recomendar bootstrap sin ejecutarlo automáticamente.

## 18. Navigator incompleto

Prepara `config.yaml` con `context: true` y `module_map: true`, pero omite
`module-map.json`.

Esperado:

- Usa `ai-context.md` solo si existe y es legible.
- Declara únicamente la capa relevante ausente y degrada a fuentes directas.
- No inventa módulos ni intenta reparar el índice durante SDD.

## 19. Navigator desfasado o no verificable

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

## 20. Actualización explícita

Con Navigator desfasado, pide a SDD que continúe y luego acepta su recomendación de
actualizar los índices.

Esperado:

- Antes de la aceptación, SDD no escribe `.navigator/` ni cambia de agente.
- La actualización se realiza únicamente mediante Project Navigator, conservando
  sus avisos, permisos y gates.
- Tras aportar el resultado, SDD repite el preflight antes de volver a usar los
  índices y retoma el gate SDD correspondiente.

## Criterio de cierre

La prueba pasa si el Gate 0 y los veinte escenarios conservan proporcionalidad,
recomiendan capacidad sin identificar productos o proveedores, respetan gates,
distinguen TDD de caracterización/cobertura retroactiva y aportan evidencia real sin
inflar código, documentación o dependencias. Las rutas planas y agrupadas deben
coexistir sin ambigüedad ni escape de `.sdd/specs/`. Navigator debe ser opcional,
verificable y de solo orientación. No marques una plataforma aprobada sin ejecutar
todos los escenarios.

| Plataforma | Versión | Modelo | Fecha | Commit kit | Resultado | Evidencia / fallos |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| OpenCode | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| Kiro | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| Claude Code | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
