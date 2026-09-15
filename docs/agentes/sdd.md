# Agente SDD — Spec-Driven Development

## Resumen

| Campo | Información |
|---|---|
| ID | `sdd` |
| Skill | [`sdd-spec`](../../canonical/skills/sdd-spec/SKILL.md) |
| Propósito | Convertir features y bugfixes en trabajo trazable antes de implementarlos |
| Artefactos | `.sdd/specs/<ruta-spec>/`, plana o agrupada por módulo |
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

## Recomendación de modelo

Antes de cargar contexto pesado, SDD hace un preflight barato y recomienda un
nivel genérico `BAJO`, `MEDIO` o `ALTO`. Para `direct`, el aviso es breve y no
bloquea. Para Quick Plan y trabajo no trivial, presenta una sola vez el nivel
global y un perfil orientativo de las fases pendientes, y espera confirmación.

El usuario puede cambiar manualmente al nivel recomendado o continuar con el
actual. SDD no conoce, selecciona ni cambia el modelo del host. La confirmación se
conserva entre fases mientras no cambien el alcance o el riesgo; no hay una pausa
nueva antes de cada fase.

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

0. **Modelo:** preflight, recomendación y Gate 0 ligero cuando el trabajo no es `direct`.
1. **Requirements:** historias, criterios EARS, errores, edge cases y supuestos.
   Gate 1: aprobar requisitos.
2. **Design:** arquitectura, modelos, errores, pruebas y estrategia de testing.
   Gate 2: aprobar diseño.
3. **Tasks:** tareas trazadas a requisitos, dependencias y waves.
   Gate 3: aprobar el plan y empezar a implementar.
4. **Implementación:** ejecutar una tarea o wave, con integrity gate antes de marcarla.
5. **Verification:** ejecutar pruebas, registrar evidencia y revisar requisitos y RNF.
   Gate 4: cerrar la spec o corregir huecos.

Quick Plan genera requirements, design y tasks en una pasada sin gates de fase y
omite `verification.md`, pero conserva el Gate 0 y la evidencia en tareas y resumen
final.

## Contexto opcional de Project Navigator

Si existe una instancia aplicable de `.navigator/`, SDD comprueba su configuración,
capas y frescura antes de usarla. El orden de lectura es:

1. steering de la plataforma y `.sdd/steering/`;
2. preflight y capa mínima de Navigator;
3. README del dominio y documentación estrictamente necesaria;
4. código y pruebas puntuales según la fase.

Un Navigator `vigente` orienta la exploración inicial. Si está `desfasado` o
`no_verificable`, solo aporta pistas de ubicación y SDD confirma las afirmaciones
en documentación y código reales. Si está `ausente` o resulta `ambiguo`, se omite
y el flujo continúa: Navigator nunca es un requisito para usar SDD.

SDD no crea ni actualiza `.navigator/` automáticamente. Puede recomendar bootstrap
o update, pero el usuario debe decidir si continúa con Project Navigator y sus
propios gates. El código, el steering y los contratos canónicos siguen siendo las
fuentes de verdad.

## Qué produce

```text
.sdd/specs/
├── <nombre-feature>/              # ruta plana, continúa siendo válida
│   ├── requirements.md            # o bugfix.md
│   ├── design.md
│   ├── tasks.md
│   └── verification.md
└── <modulo>/<nombre-feature>/     # agrupación recomendada si hay varias specs
    ├── requirements.md            # o bugfix.md
    ├── design.md
    ├── tasks.md
    └── verification.md
```

La ruta relativa completa identifica la spec. Una carpeta intermedia es solo un
agrupador: la raíz de una spec es la carpeta que contiene `requirements.md` o
`bugfix.md`. Al reanudar sin ruta explícita, SDD busca esos marcadores de forma
recursiva y pregunta si encuentra varias candidatas plausibles.

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

- No cruza gates de fase sin aprobación explícita, salvo Quick Plan solicitado; el
  Gate 0 de modelo aplicable se conserva.
- No cambia el modelo del host ni menciona nombres de modelos o proveedores en la
  recomendación.
- No inventa requisitos, cumplimiento, resultados de tests ni evidencia.
- No añade dependencias de testing sin un test que las use en la misma entrega.
- No presenta un Navigator desfasado o sin baseline verificable como vigente.
- No escribe `.navigator/` ni cambia automáticamente a Project Navigator.
- Respeta `.architecture/`, `.design/`, `.data/`, `.security/` y `.quality/` cuando
  existen; si falta contexto, documenta solo lo imprescindible dentro de la spec.
- Confirma acciones destructivas y nunca expone secretos.
