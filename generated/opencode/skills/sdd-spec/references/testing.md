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

## Reglas de PBT

- Deriva propiedades desde los requisitos EARS (una por comportamiento invariante).
- Si el proyecto no tiene soporte PBT, propón la dependencia como primera tarea.
- Prioriza propiedades sobre tests de ejemplo cuando el comportamiento es
  algebraico o tiene invariantes claros.
