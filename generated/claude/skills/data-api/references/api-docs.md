# Referencia — documentación interactiva de APIs con Scalar

Esta referencia define el contrato para crear un lanzador local de documentación
interactiva cuando el alcance confirmado incluye una API REST. El lanzador puede
prepararse antes que OpenAPI, pero no puede instalar ni servir Scalar hasta que el
contrato exista y sea válido.

## Principio

- OpenAPI sigue siendo la fuente de verdad.
- Scalar solo presenta el contrato y permite probar manualmente las operaciones.
- El agente genera el lanzador; no lo ejecuta ni instala dependencias durante la
  sesión de documentación.
- La ausencia de OpenAPI bloquea la ejecución del lanzador, no su creación.
- La interfaz generada no es UI del producto: es una herramienta de documentación
  de la capa de datos/API.

## Cuándo crear el lanzador

Créalo cuando se cumplan todas estas condiciones:

1. La documentación de una API REST forma parte del alcance confirmado.
2. El proyecto permite añadir una herramienta local de documentación.

No lo crees para una auditoría puntual, para proyectos sin APIs REST ni para
sustituir un contrato oficial del backend. Si todavía no existe un OpenAPI oficial
o aprobado a partir de fuentes reales, crea el lanzador protegido, registra su
estado `bloqueado` e informa que Scalar necesita ese contrato. Un catálogo en
Markdown no desbloquea el lanzador. No inventes ni generes automáticamente OpenAPI.

En la primera documentación, crea el lanzador una sola vez. En sincronizaciones
posteriores, reutilízalo y actualízalo solo si cambió la ruta del contrato o su
comportamiento; no sobrescribas personalizaciones sin confirmación.

## Artefactos esperados en el proyecto

Usa nombres coherentes con el proyecto, respetando archivos existentes:

```text
.data/
├── contracts/
│   └── openapi.yaml              # opcional al crear; oficial o aprobado
└── README.md                     # incluye instrucciones y estado del lanzador

scripts/
└── api-docs.<extensión>          # lanzador manual, según el entorno
```

El HTML o la página servida por Scalar es un artefacto generado, no la fuente de
verdad. Puede quedar en una carpeta de salida ignorada o publicarse mediante el
pipeline del proyecto, pero nunca debe requerir edición manual para reflejar el
contrato.

Si el proyecto necesita ser multiplataforma, genera un lanzador equivalente para
cada shell soportada por el proyecto. No introduzcas una plataforma nueva solo
para generar la documentación.

## Comportamiento mínimo del lanzador

El lanzador debe:

1. Resolver la raíz del proyecto desde su propia ubicación para funcionar aunque
   se invoque desde otro directorio.
2. Localizar el contrato de forma determinista: primero una configuración explícita
   del proyecto y después la ruta documentada en `.data/README.md`.
3. Fallar con un mensaje claro si el contrato no existe, no es válido o la ruta es
   ambigua. Esta comprobación ocurre antes de instalar dependencias o iniciar Scalar.
4. Comprobar que existen Node.js y un gestor de paquetes capaz de ejecutar Scalar.
   No debe instalar Node.js automáticamente.
5. Detectar una instalación local de la CLI oficial de Scalar (`@scalar/cli`).
6. Si falta Scalar, instalarlo únicamente cuando el usuario lo solicite de forma
   explícita, por ejemplo con `--install`, y el contrato ya haya superado las
   comprobaciones; usar una dependencia local o una ejecución efímera del gestor
   del proyecto, nunca una instalación global.
7. Validar el contrato antes de servirlo cuando la CLI lo permita.
8. Servir la referencia interactiva con la CLI de Scalar a partir del contrato,
   por ejemplo mediante `document serve`, mostrando el puerto y la URL local.
9. Aceptar al menos un puerto configurable y, cuando sea útil, modo de observación
   (`watch`) para refrescar la referencia después de cambios en OpenAPI.
10. Mantenerse en primer plano hasta que el usuario lo detenga y explicar cómo
    finalizarlo.

Una interfaz servida por Scalar genera el HTML en tiempo de ejecución; no es
obligatorio guardar un `index.html` estático. Si el proyecto necesita publicar un
artefacto estático, usa la integración HTML oficial de Scalar y deja documentada
la diferencia entre generar y servir.

## Interfaz del comando

Adapta la sintaxis al sistema del proyecto, pero conserva estas intenciones:

```text
api-docs --check                 Comprueba contrato, Node y Scalar
api-docs --install --serve       Instala localmente si falta y sirve la referencia
api-docs --serve --port <puerto> Sirve con un puerto concreto
api-docs --watch                 Recarga al cambiar el contrato, si está soportado
```

El uso normal debe ser manual y explícito. Si se ejecuta sin `--install` y Scalar
no está disponible, no debe modificar el proyecto: debe indicar el comando o la
opción necesaria para instalarlo. Si falta un OpenAPI válido, `--check`, `--serve`
y cualquier combinación con `--install` deben terminar con error antes de comprobar
o instalar Scalar.

## Actualización de `.data/README.md`

Cuando se crea el lanzador, añade una sección equivalente a esta:

```markdown
## Documentación interactiva
- Estado: disponible | requiere instalación | bloqueado | no aplica
- Contrato: `contracts/openapi.yaml`
- Lanzador: `scripts/api-docs.<extensión>`
- Comando: `api-docs --install --serve`
- URL local: `http://127.0.0.1:<puerto>`
- Entorno de pruebas: local o staging; nunca producción por defecto
- Requisito: el servidor de la API debe estar ejecutándose
```

Usa rutas y puertos reales del proyecto solo si están documentados y no son
secretos. Si no se conocen, conserva placeholders y decláralo. Usa `bloqueado`
cuando el lanzador existe pero falta un OpenAPI válido, e incluye el motivo y la
ruta esperada. Reserva `no aplica` para alcances sin API REST o sin permiso para
añadir la herramienta.

## Pruebas desde Scalar

- Scalar no inicia el backend: el servicio que se quiere probar debe estar
  ejecutándose y ser accesible.
- Las pruebas deben apuntar a local o staging, con datos de prueba y permisos
  limitados.
- No envíes solicitudes automáticamente durante la documentación; el usuario
  decide cuándo pulsar la acción de prueba.
- Si el navegador bloquea las solicitudes por CORS, informa el problema. No
  habilites CORS inseguro ni uses un proxy de terceros que pueda recibir tokens o
  datos sensibles sin una decisión explícita.
- No guardes tokens, contraseñas, cookies ni credenciales en el HTML, el script o
  la configuración. Mantén la persistencia de autenticación desactivada salvo que
  el proyecto la apruebe expresamente.

## Fallos y límites

- Sin OpenAPI válido: conserva el lanzador bloqueado, no instala ni sirve Scalar y
  registra el motivo y la ruta esperada. No genera el contrato automáticamente.
- Sin Node.js/gestor de paquetes: informa el requisito y no intenta instalarlo.
- Sin permiso o conexión para instalar: conserva el lanzador y explica cómo
  preparar el entorno manualmente.
- Si el contrato solo declara producción, no lo uses para pruebas; solicita un
  entorno local/staging o deja la prueba deshabilitada.
- Scalar no reemplaza las pruebas automatizadas de contrato, integración ni
  seguridad.
