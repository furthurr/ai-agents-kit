# Agente SDD — Spec-Driven Development

## Resumen

| Campo | Información |
|---|---|
| ID | `sdd` |
| Skill | [`sdd-spec`](../../canonical/skills/sdd-spec/SKILL.md) |
| Propósito | Convertir features y bugfixes en trabajo trazable antes de implementarlos |
| Artefactos | `.sdd/specs/<ruta-spec>/`, plana o agrupada por módulo |
| Particularidad | Puede implementar código de producto según la profundidad y sus confirmaciones |

SDD separa el **qué y porqué** del **cómo** y deja decisiones trazables.

## Cuándo usarlo

- Para una feature nueva o un cambio de comportamiento.
- Para un bugfix que necesita regresión y causa raíz.
- Para una decisión con impacto entre capas.
- Para crear un plan rápido de trabajo acotado, claro y de bajo riesgo mediante
  `lite` y Quick Plan.
- Para continuar la implementación de tareas ya aprobadas.

Un cambio trivial, localizado y reversible puede usar `direct`. Tras descartarlo,
SDD selecciona `lite` automáticamente para trabajo acotado, claro y de bajo riesgo.
Si hay dudas, riesgo, contrato público, migración, cruce de capas o un bugfix no
trivial, usa `standard` como modo por defecto y fallback seguro. `deep` solo se
activa por petición explícita.

## Recomendación de nivel de LLM

Antes de cargar contexto pesado, SDD hace un preflight barato y recomienda un nivel
de LLM genérico `BAJO`, `MEDIO` o `ALTO` únicamente para la próxima fase u operación.
El mensaje usa el formato `Nivel de LLM recomendado para <fase>: <nivel>`. La
recomendación es informativa: salvo en `direct`, SDD termina el turno para darte
tiempo a cambiar manualmente de modelo o conservar el actual. Al responder
«continúa» reanuda el proceso sin pedirte que declares qué modelo elegiste.

En cada transición, SDD presenta el resumen verificable, el gate actual y la
recomendación de la próxima fase en el mismo mensaje. Para continuar solo requiere la
aprobación del gate SDD real; después inicia la siguiente fase sin confirmación del
nivel de LLM. Después de Implementación, como no hay gate intermedio, pausa tras
recomendar el nivel para Verification y la ejecuta cuando reanudes. SDD no conoce,
selecciona ni cambia el LLM del host, y no crea gates adicionales.

## Modos

| Modo | Uso | Resultado |
|---|---|---|
| `direct` | Cambio trivial, localizado y reversible | Sin spec; verificación mínima |
| `lite` | Selección automática para trabajo acotado, claro y de bajo riesgo | Quick Plan compacto; artefactos según se planifique o implemente |
| `standard` | Modo por defecto y fallback seguro; obligatorio para bugfixes no triviales | Requirements, design, tasks y verification; Gates 1-4 |
| `deep` | Solo cuando el usuario lo solicita explícitamente | Gates 1-4; más contexto, glosario, diagramas y PBT real si aplica |

Estas son las cuatro profundidades válidas: `direct`, `lite`, `standard` y `deep`.
Quick Plan es obligatorio y exclusivo de `lite`; combinarlo con cualquier otra
profundidad es inválido.

La profundidad y el testing son decisiones independientes. Una feature normal usa
TDD focalizado; TDD estricto solo se activa si se pide explícitamente. Los bugfixes
usan regresión y el legado usa caracterización.

## Flujo y gates

0. **Nivel de LLM:** preflight de la próxima fase; salvo `direct`, termina el turno
   antes de comenzar para permitir un cambio manual opcional. La pausa no es un gate
   de modelo; `direct` no crea spec.
1. **Requirements:** historias, criterios EARS, errores, edge cases y supuestos.
   Gate 1: aprobar requisitos en `standard` y `deep`.
2. **Design:** arquitectura, modelos, errores, pruebas y estrategia de testing.
   Gate 2: aprobar diseño en `standard` y `deep`.
3. **Tasks:** tareas trazadas a requisitos, dependencias y waves.
   Gate 3: aprobar el plan y empezar a implementar en `standard` y `deep`.
4. **Implementación:** ejecutar una tarea o wave, con integrity gate antes de marcarla.
5. **Verification:** tras el preflight y la reanudación, ejecutar pruebas, registrar
   evidencia y revisar requisitos y RNF. Gate 4: cerrar la spec o corregir huecos en
   `standard` y `deep`; después no hay otra recomendación.

En `lite`, Quick Plan genera `requirements.md`, `design.md` y `tasks.md` en una
pasada después del preflight informativo y de que el usuario reanude. No existen Gates 1-3 ni Gate 4. Si el
alcance es solo planificar, termina con esos tres archivos; si también se
implementa, añade un `verification.md` compacto con la evidencia.

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

La estructura completa corresponde a `standard`, `deep` o a un `lite` implementado.
Un `lite` solo de planificación omite `verification.md`; `direct` no crea esta
carpeta.

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

Esta petición usa `lite` automáticamente. `Quick Plan standard`, `Quick Plan deep`
y `Quick Plan direct` son combinaciones inválidas.

## Límites y confirmaciones

- No cruza los Gates 1-4 de `standard` o `deep` sin aprobación explícita.
- El Gate 0 informa el nivel de LLM recomendado y pausa salvo en `direct`, sin
  pedir confirmación del modelo; `lite` pausa antes de Quick Plan, sin crear
  Gates 1-3 ni Gate 4.
- Quick Plan solo existe en `lite` y no se combina con otra profundidad.
- No cambia el modelo del host ni menciona nombres de modelos o proveedores en la
  recomendación.
- No inventa requisitos, cumplimiento, resultados de tests ni evidencia.
- No añade dependencias de testing sin un test que las use en la misma entrega.
- No presenta un Navigator desfasado o sin baseline verificable como vigente.
- No escribe `.navigator/` ni cambia automáticamente a Project Navigator.
- Respeta `.architecture/`, `.design/`, `.data/`, `.security/` y `.quality/` cuando
  existen; si falta contexto, documenta solo lo imprescindible dentro de la spec.
- Confirma acciones destructivas y nunca expone secretos.
