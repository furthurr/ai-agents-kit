# Agente SDD — Spec-Driven Development

## Resumen

| Campo | Información |
|---|---|
| ID | `sdd` |
| Skill | [`sdd-spec`](../../canonical/skills/sdd-spec/SKILL.md) |
| Propósito | Convertir features y bugfixes en trabajo trazable antes de implementarlos |
| Artefactos | `.sdd/specs/<nombre>/` |
| Particularidad | Es el agente del kit que puede implementar código de producto, tras los gates |

SDD separa el **qué y porqué** del **cómo**. La conversación deja requisitos,

## Cuándo usarlo

- Para una feature nueva o un cambio de comportamiento.
- Para un bugfix que necesita regresión y causa raíz.
- Para una decisión con impacto entre capas.
- Para crear un plan rápido de una feature bien entendida mediante Quick Plan.
- Para continuar la implementación de tareas ya aprobadas.

Un cambio trivial, localizado y reversible puede usar `direct`; si tiene riesgo,
contrato público, migración o cruce de capas, debe usar `standard`.

## Modos

| Modo | Uso | Resultado |
|---|---|---|
| `direct` | Cambio trivial, claro y reversible | Sin spec de cuatro fases; verificación mínima |
| `standard` | Default para features y bugfixes | Requirements, design, tasks y verification |
| `deep` | Cuando el usuario lo solicita | Más contexto, glosario, diagramas y PBT real si aplica |

La profundidad y el testing son decisiones independientes. Una feature normal usa
TDD focalizado; TDD estricto solo se activa si se pide explícitamente. Los bugfixes
usan regresión y el legado usa caracterización.

## Flujo y gates

1. **Requirements:** historias, criterios EARS, errores, edge cases y supuestos.
   Gate 1: aprobar requisitos.
2. **Design:** arquitectura, modelos, errores, pruebas y estrategia de testing.
   Gate 2: aprobar diseño.
3. **Tasks:** tareas trazadas a requisitos, dependencias y waves.
   Gate 3: aprobar el plan y empezar a implementar.
4. **Implementación:** ejecutar una tarea o wave, con integrity gate antes de marcarla.
5. **Verification:** ejecutar pruebas, registrar evidencia y revisar requisitos y RNF.
   Gate 4: cerrar la spec o corregir huecos.

Quick Plan genera requirements, design y tasks en una pasada sin gates y omite
`verification.md`, pero conserva la evidencia en tareas y resumen final.

## Qué produce

```text
.sdd/specs/<nombre-feature>/
├── requirements.md   # o bugfix.md
├── design.md
├── tasks.md
└── verification.md
```

No marca una tarea `[x]` sin artefacto real o evidencia. El design debe registrar
la estrategia de pruebas y respetar la barra de calidad de la skill.

## Ejemplos de uso

```text
@sdd Diseña y planifica el bloqueo de cuenta después de tres intentos fallidos.
Usa modo standard y detente en cada gate.
```

```text
@sdd Corrige este bug reproducible con una regresión antes del fix y deja evidencia
de la suite ejecutada.
```

```text
@sdd Quick Plan para una pantalla de ajustes bien definida; registra la estrategia
de testing y no implementes todavía.
```

## Límites y confirmaciones

- No cruza gates sin aprobación explícita, salvo Quick Plan solicitado.
- No inventa requisitos, cumplimiento, resultados de tests ni evidencia.
- No añade dependencias de testing sin un test que las use en la misma entrega.
- Respeta `.architecture/`, `.design/`, `.data/`, `.security/` y `.quality/` cuando
  existen; si falta contexto, documenta solo lo imprescindible dentro de la spec.
- Confirma acciones destructivas y nunca expone secretos.
