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
- **Scalar** como vista interactiva opcional de contratos OpenAPI; no sustituye el
  contrato y no se ejecuta automáticamente.
- Convenciones de autenticación, errores, paginación, timeouts, reintentos y
  entornos.

## Recomendación de modelo

Las consultas o cambios localizados reciben un aviso `BAJO` o `MEDIO` sin
bloqueo. Inicializaciones, catálogos completos, migraciones y contratos o riesgos
amplios recomiendan `MEDIO` o `ALTO` y esperan confirmación.

## Cómo trabaja

1. Clasifica el cambio y detecta si es API, modelo, persistencia o integración.
2. Lee `.data/README.md` y solo las fuentes afectadas en tareas puntuales.
3. En la primera ejecución detecta tecnología, contratos, persistencia y tamaño, y
   propone modo `lite` o `full`.
4. Presenta el estudio antes de generar documentación masiva.
5. Antes de implementar una mejora, clasifica la ruta directa o SDD; recomienda
   SDD para contratos, migraciones, compatibilidad o coordinación compleja.
6. El usuario decide si cambia de agente; nunca se crea `.sdd/` automáticamente.
7. Actualiza endpoints, modelos, mapeos, esquema, convenciones y deuda.
8. Registra la marca de sincronización y cita las fuentes reales.

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

Cuando se documenta una API REST con OpenAPI, el agente también prepara un
lanzador manual para la referencia interactiva, por ejemplo:

```text
scripts/api-docs.<extensión>
```

El lanzador comprueba el contrato y Scalar, instala la CLI localmente solo si el
usuario lo solicita y sirve la referencia para pruebas en local o staging. El
agente no lo ejecuta durante la documentación. El backend debe estar arrancado
para que las pruebas funcionen.

## Documentación interactiva

El flujo esperado es:

1. Data & API actualiza `.data/` y el contrato OpenAPI.
2. Data & API crea o conserva `scripts/api-docs.<extensión>`.
3. El usuario ejecuta el lanzador manualmente, por ejemplo:

   ```text
   api-docs --install --serve
   ```

4. Scalar sirve la interfaz y muestra la URL local.
5. El usuario selecciona las operaciones que quiere probar.

Si no existe un contrato OpenAPI válido, el agente informa que Scalar no aplica y
no inventa endpoints. Nunca se incluyen credenciales, tokens, PII ni dominios
productivos en el script o la página.

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
- No instala dependencias ni inicia el servidor Scalar automáticamente; prepara el
  lanzador para que el usuario lo ejecute.
- Identifica PII y deriva los riesgos de seguridad al Security Agent.
- Si recomienda SDD, cita el hallazgo/contrato y se detiene antes de modificar código.
- La primera documentación masiva requiere estudio, propuesta y confirmación.
