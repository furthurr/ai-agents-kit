

# Skill: Data & API (datos, APIs y contratos)

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Esta skill es la **referencia canónica** para documentar, auditar y desarrollar la
**capa de datos y APIs** de un proyecto, sin importar la tecnología. Su objetivo
es que cualquier agente o persona encuentre en `.data/` un contrato claro de qué
datos entran/salen y cómo. `ob-developer` la usa para criterios técnicos de
implementación y `ob-documentation-orchestrator` para trabajo documental. La skill
mantiene autoridad sobre sus estándares de dominio.

> **Regla de dominio:** esta skill define criterios para la **capa de datos y APIs**
> (DTOs, modelos, contratos, clientes de red, repositorios, mappers, serialización,
> esquema de datos). En el flujo documental no escribas UI ni negocio. Cuando
> `ob-developer` la use para una feature multicapa, este límite solo delimita los
> criterios de datos/API: Developer conserva la responsabilidad integral del alcance
> y puede continuar con las demás capas usando su skill propia.

## Cuándo usar esta skill

- Documentar endpoints consumidos/expuestos, modelos/DTOs y sus mapeos.
- Definir o auditar contratos de API y esquemas de datos.
- Ayudar a desarrollar la capa de datos: DTOs, clientes de red, repositorios,
  mappers, serialización, caché.
- Registrar campos sensibles/PII y convenciones (auth, errores, paginación…).
- Auditar y registrar **deuda técnica** de datos/APIs.
- Sincronizar la documentación tras cambios en la capa de datos.

## Elegir el flujo según la intención

- **Consulta sin persistencia:** responde con el código y los contratos existentes.
  No crees `.data/`, archivos ni índices, y no inicies una extracción documental
  completa por una pregunta sobre un endpoint, DTO o modelo.
- **Implementación de producto:** Developer coordina la característica completa;
  esta skill aporta criterios de datos/API bajo demanda. No inicialices ni
  sincronices `.data/` como efecto de implementar un endpoint, modelo o repositorio.
- **Documentación con persistencia:** trabaja en `.data/` solo cuando el usuario
  solicite documentar, inicializar, sincronizar o registrar hallazgos. Una auditoría
  puede limitarse a informar sin escribir. Si falta `.data/`, presenta primero el
  estudio, modo y alcance propuestos; espera su aprobación antes de crearla.

## Estándares que reconoce

**Núcleo (siempre que aplique):**
- **OpenAPI (REST)** → contrato de endpoints. Si el backend ya tiene uno, se
  **referencia**; no lo reescribas. Si no hay, mantén un **catálogo de endpoints**
  equivalente desde el lado del cliente.
- **JSON Schema** → forma y validación de modelos/DTOs.
- **Diagramas ER en Mermaid** (`erDiagram`) → solo si hay **persistencia interna**
  (Room/SQLite/Core Data/Realm/…). Si no hay BD interna, **se omite**.

**Soporte condicional (solo si se detecta en el proyecto):**
- **GraphQL SDL** (si hay GraphQL) · **AsyncAPI** (si hay eventos/colas/streaming)
  · **gRPC/Protobuf** (si hay `.proto`).

## Detección de tecnología (dónde vive la capa de datos)

| Tecnología | Dónde inferir datos/APIs |
|------------|--------------------------|
| Android | Retrofit/Ktor/OkHttp interfaces, `@GET/@POST`, DTOs, repositorios, Room (`@Entity/@Dao`), DataStore, serialización (Moshi/Gson/kotlinx) |
| iOS | `URLSession`/Alamofire, `Codable` models, Core Data, repositorios |
| Flutter | `http`/`dio`, modelos `fromJson/toJson`, repos, `sqflite`/Drift/Isar |
| Backend | controllers/routers, DTOs/entidades, ORM/migraciones, esquema BD, OpenAPI |
| Web/Front | clients/`fetch`/axios, tipos/DTOs, GraphQL queries, esquemas |

Fuentes de verdad: interfaces de red, modelos serializables, repos, entidades de
BD/migraciones, configuración de endpoints y contratos existentes. Cita
`archivo:línea`. No inventes payloads ni respuestas: si un dato no está en el
código, decláralo.

## Uso durante implementación de producto

`ob-developer` determina el flujo global y utiliza su modo PLAN ante requisitos o
decisiones esenciales pendientes, contratos incompatibles, esquemas/migraciones,
varias fuentes o riesgo relevante de pérdida, duplicación o inconsistencia. Esta
skill no recomienda ni inicia SDD; no crea `.sdd/` ni detiene una implementación
multicapa. Implementa solo la parte de datos/API según el plan global aprobado,
conserva la compatibilidad acordada y valida contratos y pruebas pertinentes.

Durante una implementación de producto, no ejecutes el bootstrap/sync completo de
`.data/` salvo que el usuario lo solicite como parte del alcance. Al cierre, Developer
evalúa si `.data/` quedó desactualizada y ofrece la actualización documental
correspondiente.

## Índice de contexto para otros agentes

`.data/README.md` incluye una sección **"Contexto para IA"**: resumen denso de
qué APIs consume/expone la app, modelos clave, fuentes de datos, auth y campos
sensibles. Es el punto de entrada que otros agentes leen para orientarse.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- En trabajo documental, limita las escrituras a datos/APIs; en implementación con
  Developer, aplica estos criterios al dominio de datos sin restringir el alcance
  integral autorizado.
- **Seguridad primero:** nunca expongas secretos, tokens, credenciales ni
  dominios productivos reales; usa placeholders. Marca la PII. Los **hallazgos de
  riesgo de seguridad** (cifrado débil, TLS, fugas) se **derivan a Code Review con `ob-security`**.
- Cita `archivo:línea` como fuente de verdad; no inventes payloads ni respuestas.
- Mantén los diagramas ER y contratos al día; corrige si un cambio los desactualiza.
- Documenta APIs con el contrato OpenAPI existente o con el catálogo de endpoints
  cuando no haya uno; no generes visores interactivos ni lanzadores de documentación.
- git solo de lectura.
