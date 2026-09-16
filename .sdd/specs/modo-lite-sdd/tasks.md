# Tareas — Modo lite de SDD

Modo de esta spec: `standard`
Estrategia: TDD focalizado sobre el contrato textual y los artefactos generados.

## 1. Contrato de modos y selección

- [x] 1.1 [TDD focalizado] Añadir checks contractuales para las cuatro
  profundidades, separación de ejes, precedencia explícita y selección automática;
  observar RED, actualizar `SKILL.md` y `agents/sdd.md` con el mínimo contrato,
  observar GREEN y eliminar duplicación innecesaria. (REQ-001–REQ-007,
  REQ-015–REQ-021)
- [x] 1.2 [TDD focalizado] Añadir checks para que Quick Plan sea obligatorio y
  exclusivo de `lite`, incluidas combinaciones inválidas y fallback confirmado a
  `standard`; observar RED, implementar el contrato mínimo y confirmar GREEN.
  (REQ-008–REQ-014)

## 2. Gates, intención y artefactos lite

- [x] 2.1 [TDD focalizado] Añadir checks para el Gate 0 visible de `lite`, la
  omisión de Gates 1–3 y 4, y la confirmación de reclasificación aunque no cambie
  el nivel de modelo; observar RED, actualizar `model-selection.md` y el contrato
  canónico, confirmar GREEN y refactorizar frases duplicadas. (REQ-029–REQ-034)
- [x] 2.2 [TDD focalizado] Añadir checks para diferenciar planificar de implementar,
  exigir `Modo SDD: lite` y crear `verification.md` compacto solo tras implementar;
  observar RED, actualizar skill y plantillas, y confirmar GREEN. (REQ-022–REQ-028)
- [x] 2.3 [TDD focalizado] Añadir checks para testing independiente, TDD focalizado,
  omisión justificada de tests y evidencia honesta; observar RED, actualizar
  `testing.md`, `integrity-gate.md`, `quality-bar.md` y `templates.md`, y confirmar
  GREEN. (REQ-035–REQ-040)

## 3. Compatibilidad y superficie pública

- [x] 3.1 [TDD focalizado] Añadir checks de preservación de `standard`, `direct` y
  `deep`, compatibilidad legacy y paridad de referencias generadas; observar RED,
  completar el contrato canónico y confirmar GREEN. (REQ-041–REQ-047)
- [x] 3.2 [P] Actualizar las descripciones de los adaptadores SDD de Copilot,
  OpenCode, Kiro y Claude para presentar un flujo proporcional y no prometer
  siempre cuatro fases. (REQ-043–REQ-045)
- [x] 3.3 [P] Actualizar `docs/agentes/sdd.md`, `docs/agentes/README.md`,
  `docs/uso.md` y `docs/catalogo.md` con selección, compatibilidad y experiencia de
  usuario. (REQ-008–REQ-014, REQ-022–REQ-034, REQ-041–REQ-044)
- [x] 3.4 [P] Actualizar `docs/sdd-smoke.md` con escenarios positivos, límites,
  conflictos, escalado, reanudación y evidencia de `lite`; ajustar
  `docs/mejoras.md` para retirar el contrato anterior de Quick Plan transversal.
  (REQ-010–REQ-014, REQ-029–REQ-040, REQ-044, REQ-046–REQ-047)

## 4. Render y validación

- [x] 4.1 Regenerar `generated/{copilot,opencode,kiro,claude}` exclusivamente con
  `python3 tools/render.py` y revisar que no existan ediciones manuales ni tokens
  sin resolver. (REQ-043, REQ-045)
- [x] 4.2 Ejecutar el contrato SDD y la validación reproducible; corregir cualquier
  divergencia sin relajar los criterios aprobados. (REQ-001–REQ-047)
- [x] 4.3 [P] Ejecutar recomendaciones de modelo, integridad, enlaces, validadores,
  medición de contexto y `git diff --check`; registrar comandos y resultados para
  cierre. (REQ-035–REQ-045)
- [x] 4.4 Revisar el diff final para confirmar que `standard` conserva Gates 1–4,
  Quick Plan solo aparece asociado a `lite`, las specs legacy no se migraron y los
  cambios generados proceden de fuentes canónicas. (REQ-008–REQ-014,
  REQ-041–REQ-047)

## 5. Verificación y cierre

- [x] 5.1 Crear `verification.md` con RED/GREEN, suites, matriz completa de
  trazabilidad, integridad de tareas y self-check de RNF. (REQ-001–REQ-047)
- [x] 5.2 Contrastar cada tarea marcada con su path o comando real, declarar
  omisiones honestas y solicitar Gate 4 sin requisitos huérfanos. (REQ-035–REQ-047)

- [omitido: PBT no aplica; el contrato textual no contiene un invariante algebraico]

## Cobertura de requisitos

| Requisitos | Tareas principales |
|---|---|
| REQ-001–REQ-007 | 1.1, 4.2, 5.1 |
| REQ-008–REQ-014 | 1.2, 3.3, 3.4, 4.4, 5.1 |
| REQ-015–REQ-021 | 1.1, 4.2, 5.1 |
| REQ-022–REQ-028 | 2.2, 3.3, 5.1 |
| REQ-029–REQ-034 | 2.1, 3.3, 3.4, 5.1 |
| REQ-035–REQ-040 | 2.3, 3.4, 4.3, 5.1–5.2 |
| REQ-041–REQ-047 | 3.1–3.4, 4.1–4.4, 5.1–5.2 |

## Grafo de waves

```mermaid
flowchart LR
    W1[Wave 1: 1.1 selección] --> W2[Wave 2: 1.2 Quick Plan]
    W2 --> W3[Wave 3: 2.1 gates]
    W3 --> W4[Wave 4: 2.2 artefactos]
    W4 --> W5[Wave 5: 2.3 testing]
    W5 --> W6[Wave 6: 3.1 compatibilidad]
    W6 --> W7[Wave 7: 3.2 adaptadores + 3.3 docs + 3.4 smoke]
    W7 --> W8[Wave 8: 4.1 render]
    W8 --> W9[Wave 9: 4.2 contrato + 4.3 validadores]
    W9 --> W10[Wave 10: 4.4 revisión]
    W10 --> W11[Wave 11: 5.1–5.2 cierre]
```
