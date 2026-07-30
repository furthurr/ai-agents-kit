# Stack de Testing y PBT

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

## PBT condicional (no default-heavy)

- **Standard:** propiedades narrativas opcionales, **máx. 5** invariantes críticos en `design.md`. Tests de ejemplo obligatorios para comportamientos testables del dominio.
- **Deep** o invariante claro (ordenación, round-trip, unicidad, partición de estados): 1–3 PBT reales.
- Añadir dependencia PBT **solo** cuando se vaya a escribir al menos un test PBT en la misma wave.
- Nunca marcar tarea PBT como `[x]` sin archivo de test que importe la lib PBT.
- Priorizar propiedades sobre tests de ejemplo **solo** cuando el comportamiento sea algebraico — no como relleno de spec.

## Anti-patrones (prohibidos)

- Declarar 13–21 “Correctness Properties” en modo standard.
- Añadir libs PBT “por si acaso” sin tests que las usen.
- Tags tipo `// Feature: … Property N` en tests de ejemplo haciéndolos pasar por PBT.
- Tests tautológicos (`assert true` sin sujeto).
