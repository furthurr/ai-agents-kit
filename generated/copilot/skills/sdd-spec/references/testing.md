# Verificación adaptativa y PBT

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

La profundidad SDD (`direct`, `tiny`/SDD-Tiny, `lite`/SDD-Lite y `standard` legacy
solo por solicitud explícita) y la estrategia de pruebas son ejes independientes.
Elige una estrategia por comportamiento y riesgo, no por score ni tamaño del diff:

| Estrategia | Cuándo | Evidencia mínima |
|------------|--------|------------------|
| Sin test nuevo | No cambia comportamiento observable: docs, formato o cambio mecánico cubierto por validadores | Check existente o razón concreta |
| Caracterización / regresión | Refactor legado o bugfix | Baseline o reproducción del defecto y suite final |
| Verificación focalizada | Comportamiento nuevo o modificado | Test/check que cubra el criterio, resultado observado y suite aplicable |

Orden de decisión:

1. Para bugfix o legado incierto, usa regresión o caracterización.
2. Para comportamiento nuevo/modificado, usa verificación focalizada adecuada al
   criterio y al riesgo; no impongas una secuencia previa de pruebas.
3. Sin cambio observable, no añadas un test solo por ceremonia; ejecuta checks.
4. Si debería probarse pero no existe un harness viable, registra la excepción y
   evalúa la mejor verificación alternativa. Si el riesgo impide `direct`/`tiny`/`lite`,
   no escales automáticamente: detente y explica cómo reducir/dividir el alcance;
   continúa con `standard` solo ante solicitud explícita del usuario.

Tiny reduce el número de documentos, no controles de comportamiento. El documento
único `spec.md` conserva la estrategia, resultados observados, fallos y reparaciones.
Gate 3 debe aprobar el plan antes de implementar y Gate 4 cierra tras la verificación.

`lite` reduce gates y documentación, no evidencia. Una implementación `lite` usa
la misma decisión adaptativa y registra el ciclo en su `verification.md` compacto.
Un bugfix no trivial conserva `lite` (siempre elegible), aunque el diff sea pequeño.

Tiny/Lite con atención especial exige pruebas de la garantía identificada, incluyendo
concurrencia, reintentos o fallos pertinentes con mecanismos reales o seams
representativos. No sustituirlas por mocks que oculten la garantía. Si no hay
verificación viable, no mantener lite solo por la nota; aplicar `scope-depth.md`.
Entregas incrementales conservan pruebas de integración de criterios transversales.

## Aplicación de la estrategia

- **Caracterización:** captura solo el comportamiento que debe preservarse; el test
  pasa antes y después del refactor. No congeles accidentalmente el defecto.
- **Regresión:** reproduce el defecto cuando sea posible, aplica el arreglo mínimo y
  confirma el resultado y la suite.
- **Verificación focalizada:** implementa el comportamiento acordado y ejecuta tests o
  checks dirigidos a cada criterio observable y seam de riesgo; amplía la suite solo
  cuando aporte cobertura útil.

Una comprobación añadida sobre código existente puede ser cobertura válida o
caracterización según su propósito. Conserva el comando y el resultado relevante; no
pegues logs completos salvo que sean necesarios para diagnosticar.

La implementación debe ser mínima y **correcta**, no artificial para satisfacer un
check. No justifiques interfaces, capas, mocks ni helpers anticipados solo para
facilitar pruebas. Refactoriza solo por duplicación, responsabilidades distintas,
legibilidad demostrable o reutilización real, y mantén la suite verde.

## PBT condicional (no default-heavy)

- **Standard:** propiedades narrativas opcionales, **máx. 5** invariantes críticos en `design.md`. Tests de ejemplo obligatorios para comportamientos testables del dominio.
- **Invariante claro** (ordenación, round-trip, unicidad, partición de estados): 1–3 PBT reales.
- Añadir dependencia PBT **solo** cuando se vaya a escribir al menos un test PBT en la misma wave.
- Nunca marcar tarea PBT como `[x]` sin archivo de test que importe la lib PBT.
- Priorizar propiedades sobre tests de ejemplo **solo** cuando el comportamiento sea algebraico — no como relleno de spec.
- PBT complementa la estrategia elegida; no sustituye la verificación del criterio
  funcional ni obliga a una estrategia más pesada.

## Anti-patrones (prohibidos)

- Declarar 13–21 “Correctness Properties” en modo standard.
- Añadir libs PBT “por si acaso” sin tests que las usen.
- Tags tipo `// Feature: … Property N` en tests de ejemplo haciéndolos pasar por PBT.
- Tests tautológicos (`assert true` sin sujeto).
- Introducir abstracciones o mocks únicamente para aumentar el número de tests.
