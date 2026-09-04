# Data & API Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `data-api` |
| Skill | [`data-api`](../../canonical/skills/data-api/SKILL.md) |
| Propósito | Documentar, auditar y ayudar a desarrollar la capa de datos y APIs |
| Memoria | `.data/` |
| Alcance | Endpoints, DTOs, modelos, repositorios, serialización, contratos y persistencia |

Data & API Agent explica qué datos entran y salen del sistema y cómo se transforman
entre red, almacenamiento y dominio. Puede ayudar a desarrollar esa capa, pero no
se ocupa de la presentación ni de la lógica de negocio ajena a datos.

## Cuándo usarlo

- Para documentar APIs consumidas o expuestas.
- Para catalogar endpoints, DTOs, modelos y mapeos.
- Para definir o auditar contratos.
- Para revisar repositorios, clientes de red, caché o serialización.
- Para documentar persistencia, migraciones y campos sensibles/PII.
- Para registrar deuda técnica de datos y APIs.

## Qué skill utiliza

La skill `data-api` reconoce:

- **OpenAPI** para contratos REST o, si no existe, un catálogo equivalente.
- **JSON Schema** para la forma y validación de DTOs.
- **ER en Mermaid** solo cuando hay base de datos interna.
- **GraphQL, AsyncAPI y gRPC/Protobuf** si aparecen en el proyecto.
- Convenciones de autenticación, errores, paginación, timeouts, reintentos y
  entornos.

## Cómo trabaja

1. Clasifica el cambio y detecta si es API, modelo, persistencia o integración.
2. Lee `.data/README.md` y solo las fuentes afectadas en tareas puntuales.
3. En la primera ejecución detecta tecnología, contratos, persistencia y tamaño, y
   propone modo `lite` o `full`.
4. Presenta el estudio antes de generar documentación masiva.
5. Actualiza endpoints, modelos, mapeos, esquema, convenciones y deuda.
6. Registra la marca de sincronización y cita las fuentes reales.

## Qué produce

En modo `lite`, normalmente un `.data/README.md` con contexto, endpoints, modelos,

En modo `full` puede organizarse así:

```text
.data/
├── README.md
├── 01-endpoints.md
├── 02-models.md
├── 03-mapping.md
├── 04-schema.md
├── 05-conventions.md
├── 06-sensitive-data.md
├── 07-environments.md
├── contracts/
└── data-tech-debt.md
```

## Ejemplos de uso

```text
@data-api Documenta los endpoints de autenticación, sus DTOs y el mapeo al dominio.
No inventes payloads; cita archivo y línea.
```

```text
@data-api Revisa si este modelo serializable contiene PII y registra solo la
existencia y ubicación, nunca el valor real.
```

## Límites y seguridad

- Solo trabaja datos, APIs, persistencia, contratos e integraciones.
- No modifica UI ni lógica de presentación.
- No inventa respuestas, payloads ni endpoints que no existan.
- Usa placeholders para dominios, tokens, credenciales y valores productivos.
- Identifica PII y deriva los riesgos de seguridad al Security Agent.
- La primera documentación masiva requiere estudio, propuesta y confirmación.
