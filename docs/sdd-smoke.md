# Smoke test de SDD y testing adaptativo

Validación manual del agente SDD después de instalarlo. Ejecuta los escenarios en
un repositorio desechable con una suite pequeña y controlada: varios casos escriben
specs, tests y código de producto tras las aprobaciones correspondientes.

## Preparación

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala una plataforma y reinicia la herramienta.
3. Abre un repositorio de prueba sin secretos, con Git y tests ejecutables.
4. Selecciona el agente `sdd` y registra plataforma, versión, modelo, fecha y commit.

## 1. Direct sin test nuevo

Prompt:

```text
Corrige un error ortográfico en el README.
```

Esperado:

- Selecciona `direct`, sin spec de cuatro fases ni gates.
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

- Genera requirements, design y tasks en una pasada, sin gates ni Fase 4.
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

## Criterio de cierre

La prueba pasa si los diez escenarios conservan proporcionalidad, respetan gates,
distinguen TDD de caracterización/cobertura retroactiva y aportan evidencia real sin
inflar código, documentación o dependencias. No marques una plataforma aprobada sin
ejecutar todos los escenarios.

| Plataforma | Versión | Modelo | Fecha | Commit kit | Resultado | Evidencia / fallos |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| OpenCode | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
| Kiro | Pendiente | Pendiente | Pendiente | Pendiente | No ejecutado | — |
