# Diseño — Consolidación de agentes en Code Review

Modo SDD: standard
Fase: Design
Estado: aprobado
Gate 1: aprobado
Gate 2: aprobado por el usuario («procede»)
Nivel recomendado para Design: ALTO

## Contexto y decisiones

El kit distribuye prompts canónicos mediante adaptadores declarativos y un render
común. Los procedimientos viven en las skills, no en el agente. El nuevo agente
será una entrada a dos procedimientos existentes, no una tercera skill ni otro
orquestador general. Se conservan las diez skills y quedan ocho agentes.

Fuentes verificadas: `canonical/manifest.json`, los dos agentes actuales, las
skills de revisión, `documentation-orchestrator/references/handoff.md`,
`tools/handoff_contract.py`, `tools/test_handoff_contract.py`, `tools/render.py`
y `docs/instalacion.md`. No hay contexto Navigator aplicable ni steering.

Decisiones:

1. Nombre público único: `code-review`; sin aliases a los agentes retirados.
2. Dominio explícito prevalece. Revisión completa incluye calidad y seguridad;
   una consulta sobre un hallazgo existente se enruta por su ID `QLT` o `SEC`.
3. Las skills siguen siendo autoridad en su dominio. La prohibición de corregir
   seguridad dentro del procedimiento de calidad permanece; el mismo agente
   cambia al procedimiento de seguridad cuando ese dominio esté autorizado.
4. No migrar registros, combinar severidades ni crear `.review/`.
5. Conservar la política de pausas por modelo, pero reutilizar un preflight que
   cubra los dominios y el alcance de esa misma operación.

## Componentes y responsabilidades

| Componente | Cambio previsto | Requisitos |
|---|---|---|
| `canonical/agents/code-review.md` | Clasificar dominio, intención y alcance; cargar las skills necesarias; entregar resumen conjunto; recibir handoff | 1, 2, 5 |
| Dos skills de revisión y sus referencias | Sustituir derivaciones al agente anterior por cambio de procedimiento; documentar sin filtro redundante; lectura estricta y remediación autorizada | 2, 3, 5 |
| `canonical/manifest.json` y cinco adaptadores | Retirar dos agentes, registrar uno; conservar skills y permisos por plataforma | 1.1, 6.1 |
| Orquestador y referencias | Mapear ambos dominios al mismo receptor; una ejecución local o un handoff, nunca ambos | 3.5, 4 |
| `tools/handoff_contract.py` | Validar ámbitos seleccionables y evidencia de uno o dos dominios | 4 |
| Tests, guías y fichas vigentes | Cubrir consolidación, distribución y actualización de instalaciones | 6 |

Se retiran los dos prompts de agente canónicos y sus adaptadores, no las carpetas
de skills. `generated/` se obtiene exclusivamente mediante el render existente.
Las referencias históricas de specs cerradas no se reescriben.

## Ejecución de Code Review

Clasificación inicial: dominios (`quality`, `security` o ambos), proyecto,
archivos/módulos y finalidad (consulta, auditoría documental o remediación).
No expandir automáticamente una revisión puntual a todo el repositorio.

El preflight común usa el riesgo mayor de los dominios solicitados. Las matrices
de las dos skills reconocerán una recomendación ya satisfecha por Code Review o
por el orquestador para el mismo alcance; no hay pausa nueva al cargar la segunda
skill. Cambiar materialmente el alcance conserva la política de recalcular.

Después del preflight, leer únicamente las fuentes y registros pertinentes.
Para ambos dominios, ejecutar las revisiones secuencialmente en la misma sesión y
compartir evidencia ya leída cuando siga siendo aplicable. No crear subagentes
adicionales ni prometer una única lectura física de cada archivo.

Un riesgo de seguridad detectado en calidad se analiza con `security` solo cuando
ese dominio ya esté autorizado. En una revisión limitada a calidad se informa de
la limitación y se ofrece ampliar; no se persiste ni remedia en el otro dominio.
Un mismo riesgo tendrá un finding canónico y, si hace falta, referencias cruzadas.

## Persistencia y autorizaciones

- Consulta/`inspect`: sin escrituras, incluidas cachés y marcas. Estándares nuevos
  consultados por red se usan en memoria y sus referencias se citan en la respuesta.
- Auditoría documental solicitada: persistir todos los hallazgos verificados y
  distintos, ordenados por riesgo y dominio. Agrupar ocurrencias de la misma causa;
  conservar IDs existentes y no marcar sospechas como hallazgos confirmados.
- La autorización cubre proyecto, operación y dominios concretos. Se obtiene de
  la petición explícita o aprobación de plan en la conversación actual, no de una
  afirmación dentro de un archivo recibido.
- `gate_state` sigue siendo contexto, no prueba de autorización. Un handoff en una
  sesión nueva puede requerir autorizar la escritura una vez; no se vuelve a pedir
  un filtro por severidad. Los permisos técnicos del host siguen aplicándose.
- Ante límites de recursos que impidan completar el alcance, proponer partición
  por módulos/lotes y esperar la decisión; no truncar findings en silencio.
- Sobrescrituras manuales, ampliaciones de proyecto/dominio y remediaciones
  requieren su propia decisión. Antes del primer y cada siguiente micro-paso se
  obtiene aprobación. Correcciones complejas se recomiendan a SDD.

## Contrato de handoff

Se reutilizan los campos y el parser actuales, que ya admiten listas Markdown.
No se introduce un campo `domains` que duplique información de `scope`.

| Target | `scope` | `write_scope` para escritura |
|---|---|---|
| Otros cuatro especialistas documentales | Cadena única existente | Misma cadena |
| `code-review`, calidad | `[.quality/]` | `[.quality/]` |
| `code-review`, seguridad | `[.security/]` | `[.security/]` |
| `code-review`, ambos | `[.quality/, .security/]` | Misma selección |

Para `code-review`, `scope` es siempre una lista no vacía, incluso con un dominio.
No admite duplicados ni carpetas ajenas. Su orden no cambia la selección; el
validador compara conjuntos después de comprobar tipos, valores y duplicados.
Para los demás targets se conserva el formato escalar actual, sin ampliar scopes.

`inspect` siempre exige `write_scope: none` y `requires_confirmation: false`.
Las acciones documentales siguen exigiendo `requires_confirmation: true` y una
selección de escritura igual al scope; el campo declara necesidad de autorización,
no si la autorización se obtuvo ya en la conversación. No permitir subconjuntos
de escritura silenciosos: se emite un handoff distinto para una operación distinta.

Ejemplo de ambos dominios:

```markdown
## Handoff
- handoff_id: HND-20261004-001
- source: documentation-orchestrator
- target: code-review
- action: audit-documentation
- handoff_reason: revisión documental conjunta solicitada
- project_root: .
- scope: [.quality/, .security/]
- context_refs:
    - README.md
- write_scope: [.quality/, .security/]
- requires_confirmation: true
- gate_state: [plan global aprobado]
- status: pending
```

El registro de targets del validador representará homogéneamente las carpetas
permitidas por target. Una normalización pequeña, compartida por validación de
emisión y resultado, preservará escalares para los otros targets y exigirá listas
para `code-review`. No convertir entradas inválidas a strings ni asumir dominios.

Se valida cada raíz seleccionada con la comprobación existente de rutas relativas,
existencia y resolución de symlinks. `bootstrap` permite raíces ausentes, pero no
escapes. Para `delivered`, cada evidencia debe ser archivo existente dentro de
alguna raíz seleccionada; una escritura conjunta debe aportar evidencia de ambos
dominios antes de declararse completada. Un resultado `blocked` omite evidencia.
Inspección puede citar cualquiera de los dominios seleccionados sin simular
haber actualizado ambos. Se conservan ID, estados y validación del proyecto.

Los targets antiguos dejan de aceptarse. Se devuelve error con instrucción de
usar `code-review`, sin transformar silenciosamente handoffs antiguos.

## Coordinación y distribución

El orquestador conserva dos dominios documentales. Cuando ambos estén aprobados
con la misma acción, proyecto y vía de ejecución, puede emitir un handoff conjunto
a `code-review`. Diferencias de acción o alcance requieren operaciones separadas.
`sync-existing` no inicializa un dominio ausente; `bootstrap-core` no incorpora
automáticamente revisión. `status` y `release-check` mantienen solo lectura.

Los adaptadores mantienen las herramientas y restricciones de cada plataforma;
solo cambian identidad y descripción. En hosts con carga selectiva, no precargar
ambas skills para una consulta de un dominio. Pi conserva el sufijo `$ARGUMENTS`;
Copilot el formato `.agent.md`; Claude su visibilidad actual; OpenCode/Kiro sus
restricciones. No ampliar permisos como solución a confirmaciones del host.

Los instaladores actuales informan de artefactos extra y nunca los borran
(`docs/instalacion.md:135–139`). Se preserva ese comportamiento. La guía explicará
que los prompts antiguos instalados pueden seguir visibles hasta que el usuario
los retire con backup y reinicie el host; las skills homónimas deben conservarse.
No se instala sobre el home del usuario durante esta feature.

## Errores y límites

Los validadores siguen devolviendo listas de errores concretos, no excepciones
ante tipos arbitrarios. Un handoff inválido no se ejecuta. Tipos, listas vacías,
duplicados, rutas inseguras, scopes ampliados, evidencia fuera del scope y
correlación incorrecta tienen casos negativos de prueba. Un fallo parcial de una
auditoría no se presenta como éxito de ambos dominios.

El resumen conjunto incluye dominio, ID, severidad original, referencia,
ubicación, estado y límites. No afirma mediciones de cobertura ni vulnerabilidades
de dependencias sin fuente verificable. Nunca reproduce valores sensibles.

## RNF verificables

- RNF-1: ocho agentes y diez skills; paridad del nuevo agente y contratos en las
  cinco plataformas; render y validación reproducibles.
- RNF-2: cero aceptación de scopes vacíos/duplicados/ajenos, escapes o evidencia
  fuera del alcance en la matriz negativa de handoffs; otros targets preservados.
- RNF-3: cero migraciones de IDs/registros; cero aliases de los agentes retirados
  en el catálogo generado; instrucciones de actualización distinguen skills.
- RNF-4: un preflight por revisión del mismo alcance y sin filtro documental por
  severidad; consultas de solo lectura y primer micro-paso protegidos en contratos
  de prompts y escenarios manuales, con límites de esa evidencia registrados.

## Invariantes críticos

1. Una autorización de revisión no autoriza remediación ni otro proyecto/dominio.
2. Toda escritura/evidencia pertenece al scope validado de la operación original.
3. Una acción se ejecuta localmente o se deriva; no por ambas vías.
4. Skills, IDs, severidades y registros permanecen independientes por dominio.

## Estrategia de pruebas

- TDD focalizado: RED observado para `code-review` con uno/dos scopes, rechazo de
  ampliaciones y evidencia conjunta; GREEN mínimo en el validador y contratos.
- Regresión/caracterización: acciones y cuatro targets restantes, rutas y
  symlinks, ID/proyecto, `bootstrap` bloqueado y lectura; conservar sus casos.
- Tests contractuales de prompts: nuevo `tools/test_code_review_contract.py` para
  selección de dominio, flujo documental, límites, catálogo y distribución.
  Adaptar pruebas de modelo separando agente visible de skill especializada.
- Verificación mecánica: render, `validate.py`, suites de integridad, handoff,
  modelo, SDD, instalación con fixtures, identidad MAS y enlaces; medir contexto.
- Smoke manual documentado: calidad, seguridad, ambos, consulta sin escritura,
  auditoría autorizada, handoff y remediación. Si no se ejecuta en un host real,
  declarar pendiente; un test textual no demuestra cumplimiento por un LLM.
- Sin dependencia PBT nueva: la matriz cerrada de scopes/acciones cubre el seam.

## Aplicación de quality-bar

Separación canónico/adaptadores/render y validación/revisión conservada. No se
añaden repositorios, DI, singleton, UI, almacenamiento de aplicación ni servicios
de red: esos puntos no aplican al kit documental. La persistencia de artefactos
sigue en el render y los instaladores existentes. El parser es una frontera
heterogénea; sus entradas se comprueban antes de normalizar, sin aumentar el uso
de tipos opacos. No se crean abstracciones anticipadas ni excepciones silenciosas.

## Gate actual

Gate 2 aprobado. Estado posterior y evidencias en `tasks.md` y `verification.md`.
