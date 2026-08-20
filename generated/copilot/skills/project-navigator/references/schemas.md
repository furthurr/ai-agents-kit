# Schemas de las capas de navegación

Contratos normativos de los índices persistentes de `.navigator/`. Las
plantillas bajo `templates/` son ejemplos; si una plantilla y este documento
divergen, manda este documento.

## Reglas comunes

- `version` identifica la versión del schema; el MVP usa `1`.
- `generated_at` usa ISO-8601 en UTC.
- `source_commit`, si hay Git, usa el object ID completo devuelto por
  `git rev-parse HEAD`; se omite si no hay un commit verificable.
- `root` es relativo al repositorio y coincide con `config.project.root`.
- Todos los paths almacenados son relativos a `root`, nunca absolutos.
- No incluir archivos excluidos, dependencias descargadas ni outputs de build.
- No almacenar secretos, credenciales, PII ni literales sensibles.
- Ante datos inciertos, omitirlos en lugar de inventarlos.

## `.navigator/module-map.json`

### Campos raíz

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `version` | number | Sí | Versión del schema; MVP = `1` |
| `generated_at` | string ISO-8601 | Sí | Fecha y hora de generación o actualización |
| `source_commit` | string | No | Commit Git usado como baseline verificable |
| `root` | string | Sí | Subárbol indexado, relativo al repositorio |
| `modules` | array | Sí | Unidades navegables detectadas |

### Campos por módulo

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `id` | string | Sí | Identificador único y estable |
| `name` | string | Sí | Nombre legible |
| `path` | string | Sí | Path relativo a `root` |
| `responsibility` | string | Sí | Responsabilidad en una frase |
| `kind` | string | Sí | `app`, `package`, `service`, `feature`, `lib` u `other` |
| `tech` | string[] | No | Tecnologías principales |
| `entrypoints` | string[] | No | Archivos, directorios o targets de entrada |
| `depends_on` | string[] | No | IDs de otros módulos del mismo archivo |
| `tags` | string[] | No | Etiquetas libres |
| `notes` | string | No | Nota corta |

### Invariantes

1. Cada `id` es único y permanece estable entre actualizaciones.
2. Todo valor de `depends_on` apunta a un `id` existente.
3. `path` existe bajo `root` al generar el índice.
4. Si una dependencia no es clara, se usa `depends_on: []`.
5. El MVP modela unidades de primer nivel o features detectables, no cada archivo.
6. Productos independientes no se mezclan en el mismo mapa; cada instancia de
   `.navigator/` indexa únicamente su `project.root`.

Ejemplo: `templates/module-map.template.json`.

## `.navigator/symbols.json`

Capa opt-in. Solo se genera cuando `layers.symbols: true` o el usuario lo pide.
Su cobertura es best-effort; no representa un AST completo.

### Campos raíz

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `version` | number | Sí | Versión del schema; MVP = `1` |
| `generated_at` | string ISO-8601 | Sí | Fecha y hora de generación o actualización |
| `source_commit` | string | No | Commit Git usado como baseline verificable |
| `root` | string | Sí | Subárbol indexado, alineado con config y module-map |
| `symbols` | array | Sí | Símbolos localizados con confianza suficiente |

### Campos por símbolo

| Campo | Tipo | Obligatorio | Descripción |
| --- | --- | --- | --- |
| `id` | string | Sí | ID único y estable, por ejemplo `path#Name` |
| `name` | string | Sí | Nombre del símbolo |
| `kind` | string | Sí | `class`, `function`, `method`, `interface`, `type`, `enum`, `component`, `endpoint` u `other` |
| `file` | string | Sí | Archivo relativo a `root` |
| `line` | number | Sí | Línea inicial, base 1 |
| `end_line` | number | No | Línea final, base 1 |
| `signature` | string | No | Firma pública corta |
| `module_id` | string | No | ID existente en `module-map.json` |
| `summary` | string | No | Responsabilidad en una frase |
| `exported` | boolean | No | Si forma parte de la API pública o exportada |
| `tags` | string[] | No | Etiquetas libres |

### Invariantes

1. `id` permanece estable entre actualizaciones mientras no cambie la definición.
2. `file` existe bajo `root` y `line >= 1`.
3. Si existe, `end_line >= line`.
4. Si existe, `module_id` apunta a un módulo del mapa vigente.
5. Se priorizan símbolos públicos y entrypoints frente a privados masivos.
6. Si no hay confianza en `file` y `line`, se omite el símbolo.
7. `signature` y `summary` no contienen cuerpos completos ni valores sensibles.
8. Callers, callees, imports y AST completo quedan fuera de este schema.

Ejemplo: `templates/symbols.template.json`.

## Consulta y actualización

- No volcar un índice completo al contexto del modelo.
- Filtrar por ID, nombre, módulo o path y devolver solo resultados relevantes.
- Tras localizar un símbolo, usar código puntual en `file:line` para el detalle.
- Si falta una capa, degradar según `config.md` y declarar la limitación.
- En updates, regenerar las capas o módulos afectados y conservar IDs estables.
- Al completar un bootstrap/update con working tree limpio, actualizar
  `source_commit` en cada artefacto tocado. Con cambios locales relevantes, no
  presentar ese hash como si incluyera contenido sin commit.

## Evolución

Un cambio incompatible incrementa `version` y requiere una nota de migración.
Añadir un campo opcional compatible no exige incrementar la versión, pero sí
actualizar este contrato y su plantilla. Validación automática mediante JSON
Schema queda en el backlog hasta que exista tooling determinista.
