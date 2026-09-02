# Testing adaptativo y PBT

El **stack concreto de pruebas lo define el steering** del proyecto; úsalo
siempre que exista. Si no lo especifica, aplica estos valores por defecto:

| Tecnología | Unitarias | PBT | Async / otros |
|------------|-----------|-----|----------------|
| Android / Kotlin | JUnit + MockK | Kotest (`property`) | Turbine (Flows), Compose UI Test |
| Backend JVM | JUnit 5 | jqwik / Kotest | — |
| iOS / Swift | XCTest | SwiftCheck | — |
| Flutter / Dart | flutter_test | glados | — |
| JS / TS | Jest / Vitest | fast-check | — |
| Python | pytest | Hypothesis | — |
| Go | testing | rapid | — |
| Rust | #[test] | proptest | — |

## Selección de estrategia

La profundidad SDD (`direct`, `standard`, `deep`) y la estrategia de pruebas son
ejes independientes. Elige una estrategia por comportamiento, no por tamaño del
diff:

| Estrategia | Cuándo | Evidencia mínima |
|------------|--------|------------------|
| Sin test nuevo | No cambia comportamiento observable: docs, formato o cambio mecánico cubierto por validadores | Check existente o razón concreta |
| Caracterización / regresión | Refactor legado o bugfix | Baseline verde, o RED por el defecto, y suite final verde |
| TDD focalizado | **Default para comportamiento nuevo o modificado** | RED por comportamiento relevante, GREEN y suite |
| TDD estricto | Solo si el usuario lo solicita | RED/GREEN por cada incremento productivo y suite tras refactor |

Orden de decisión:

1. Si el usuario pide TDD estricto, úsalo sin activar `deep` automáticamente.
2. Para bugfix o legado incierto, usa regresión o caracterización.
3. Para comportamiento nuevo/modificado, usa TDD focalizado.
4. Sin cambio observable, no añadas un test solo por ceremonia; ejecuta checks.
5. Si debería probarse pero no existe un harness viable, registra la excepción y
   la mejor verificación alternativa. Si el riesgo ya no es trivial, escala de
   `direct` a `standard`.

## Ciclos operativos

- **Caracterización:** captura solo el comportamiento que debe preservarse; el test
  pasa antes y después del refactor. No congeles accidentalmente el defecto.
- **Regresión:** reproduce el defecto; observa que falla por la razón esperada,
  aplica el fix mínimo y confirma que pasa.
- **TDD focalizado:** ejecuta RED → GREEN → REFACTOR por criterio observable o seam
  de riesgo, no por cada método interno. Es el default de una feature normal.
- **TDD estricto:** cada incremento de producción empieza con un RED observado. No
  se adelanta comportamiento productivo y toda excepción queda registrada.

Un test añadido sobre código que ya lo satisface es caracterización o cobertura
retroactiva, no evidencia TDD. Conserva comando y resultado relevante; no pegues
logs completos salvo que sean necesarios para diagnosticar.

GREEN implementa el comportamiento mínimo **correcto**, no el mínimo artificial
para engañar al test. TDD no justifica interfaces, capas, mocks ni helpers
anticipados. Refactoriza solo por duplicación, responsabilidades distintas,
legibilidad demostrable o reutilización real, y mantén la suite verde.

## PBT condicional (no default-heavy)

- **Standard:** propiedades narrativas opcionales, **máx. 5** invariantes críticos en `design.md`. Tests de ejemplo obligatorios para comportamientos testables del dominio.
- **Deep** o invariante claro (ordenación, round-trip, unicidad, partición de estados): 1–3 PBT reales.
- Añadir dependencia PBT **solo** cuando se vaya a escribir al menos un test PBT en la misma wave.
- Nunca marcar tarea PBT como `[x]` sin archivo de test que importe la lib PBT.
- Priorizar propiedades sobre tests de ejemplo **solo** cuando el comportamiento sea algebraico — no como relleno de spec.
- PBT complementa la estrategia elegida; no convierte por sí solo TDD focalizado
  en estricto.

## Anti-patrones (prohibidos)

- Declarar 13–21 “Correctness Properties” en modo standard.
- Añadir libs PBT “por si acaso” sin tests que las usen.
- Tags tipo `// Feature: … Property N` en tests de ejemplo haciéndolos pasar por PBT.
- Tests tautológicos (`assert true` sin sujeto).
- Llamar TDD a tests escritos después sin RED observado.
- Introducir abstracciones o mocks únicamente para aumentar el número de tests.
