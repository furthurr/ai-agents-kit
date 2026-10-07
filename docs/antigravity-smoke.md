# Smoke de Antigravity 2.0

Procedimiento para obtener evidencia runtime de la integración. **Estado actual:
PENDIENTE; este documento no registra un smoke ejecutado ni certifica el host.**
Los instaladores/exportadores sí cuentan con evidencia automatizada de scripts
con fixtures en Linux, macOS y Windows, detallada a continuación. Esa ejecución
no prueba descubrimiento 6/10, UI, carga de referencias ni `invoke_subagent` en
la aplicación Antigravity; estos pasos runtime siguen **PENDIENTES**.

## Evidencia automatizada de CI

Evidencia de scripts del kit para la publicación 0.4.0:
[run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502),
build del kit en SHA `57aaf7dd2190f6fe44c697179e93b8609a502433`, **Python 3.10**.
Todos los jobs finalizaron en verde.

| OS de CI | Comprobación automatizada | Resultado |
|----------|---------------------------|-----------|
| Ubuntu / Linux | Job `validate`, incluidas pruebas nativas de instalación/exportación Bash | PASS — 22/22 nativas |
| macOS | Pruebas nativas de instalación/exportación Bash | PASS — 22/22 nativas |
| Windows | Pruebas nativas de instalación/exportación PowerShell (`.ps1`) | PASS — 22/22 nativas |

El harness ejecuta scripts en fixtures con HOME/USERPROFILE temporales. Prepara
el directorio de caché PowerShell y deshabilita `gather` en el proceso hijo; los
snapshots no ignoran `AppData`. No son cambios de configuración global ni una
ejecución del producto Antigravity. El SHA identifica el build probado del **kit**,
no una versión/build runtime de la aplicación. La ficha de app/host siguiente
permanece pendiente y este run no marca el smoke como ejecutado.

## Alcance y referencias

- Inventario: seis agentes y diez skills del [catálogo](catalogo.md).
- Destinos 2.0: `~/.gemini/config/agents/<id>.md` y
  `~/.gemini/config/skills/<skill-name>/`, incluidos sus recursos.
- CLI: skills globales en `~/.gemini/antigravity-cli/skills/`, ruta distinta que
  este instalador no cubre. `/agents` solo está documentado para el CLI; no se
  presupone disponible en 2.0. Agentes personalizados del IDE standalone: no
  verificados. Registra cada superficie por separado.
- Referencias oficiales: [Skills](https://antigravity.google/docs/skills/),
  [Subagents](https://antigravity.google/docs/subagents/),
  [Hooks: herramientas](https://antigravity.google/docs/hooks/#supported-tools) y
  [Rules](https://antigravity.google/docs/rules/). Hooks respalda nombres; este
  procedimiento no instala hooks.

El primer smoke completo exitoso fijará la versión de referencia. No extrapoles
el resultado a otra versión, superficie u OS ni anuncies certificación completa
de los seis hosts del kit.
El bridge `GEMINI.md` → `AGENTS.md` **no está implementado**; las rutas de
steering documentadas no acreditan ese mecanismo.

## Ficha de ejecución

Completa antes de empezar; si no hay acceso, conserva `PENDIENTE` y explica el
bloqueo. Usa un identificador de fixture sin rutas personales en la evidencia.

| Campo | Valor por registrar |
|-------|--------------------|
| Fecha y responsable | PENDIENTE |
| Producto, versión/build exactos y fuente del dato | PENDIENTE |
| Superficie (2.0, CLI o IDE standalone) | PENDIENTE |
| OS y versión; shell y Python si se ejecutan scripts | PENDIENTE |
| Perfil aislado / proyecto fixture y autorización | PENDIENTE |
| Mecanismo real de recarga y selección del agente | PENDIENTE |
| Herramientas expuestas por el host, padre y rol seleccionado | PENDIENTE |
| Resultado por paso: PASS / FAIL / PENDIENTE | PENDIENTE |
| Evidencia observable, comando/acción, exit code si aplica | PENDIENTE |
| Bloqueos y pasos no ejecutados | PENDIENTE |

Guarda únicamente resúmenes observables: IDs descubiertos, herramienta ejecutada,
archivo fixture leído/escrito, referencia cargada y resultado. **No adjuntes
capturas de pantalla, secretos, credenciales ni transcripciones privadas** de
conversaciones. Un resultado omitido no es PASS.

## 1. Preparar un entorno autorizado

1. Usa un perfil de prueba aislado y un proyecto desechable con `fixture.txt`
   (texto público, por ejemplo `antigravity-smoke`) y un directorio `scratch/`.
   Define explícitamente lectura del fixture y escritura únicamente en scratch.
   No instales en el HOME real sin autorización adicional explícita.
2. Identifica build, OS y superficie desde la información del producto. Enumera
   las herramientas **realmente expuestas** antes de probarlas; contrasta los
   nombres con las tablas siguientes. No inventes aliases si falta una tool.
3. Si se comprueban scripts, ejecuta render/validación y simulación en una copia
   temporal del repo con HOME/USERPROFILE temporales. Registra comando y código
   de salida. Después, instala únicamente en el perfil aislado autorizado:

   ```bash
   ./scripts/install/antigravity.sh --dry-run
   ./scripts/install/antigravity.sh
   ./scripts/backup/antigravity.sh --dry-run
   ./scripts/backup/antigravity.sh
   ```

   ```powershell
   .\scripts\install\antigravity.ps1 -DryRun
   .\scripts\install\antigravity.ps1
   .\scripts\backup\antigravity.ps1 -DryRun
   .\scripts\backup\antigravity.ps1
   ```

   Estos comandos requieren que el entorno temporal ya esté preparado. No los
   ejecutes en un perfil personal por defecto. `--force`/`-Force` omite el
    respaldo previo de sobrescrituras vigentes; nunca el de retirada de agentes.
    No es necesario para el smoke runtime.
4. Reinicia la superficie de prueba tras instalar. Registra qué acción recargó
   agentes y skills y comprueba el descubrimiento de nuevo tras una actualización.
   Si reiniciar no basta, registra el bloqueo sin asumir otro menú/comando.

## 2. Descubrir 6 agentes y 10 skills

Registra para cada ID si el host lo descubre, no solo si existe el archivo.
Extras del usuario no cuentan en estas cantidades y no se borran.

| Agente esperado | Descubierto / seleccionable | Resultado |
|-----------------|----------------------------|-----------|
| `code-review` | PENDIENTE | PENDIENTE |
| `data-api` | PENDIENTE | PENDIENTE |
| `documentation-orchestrator` | PENDIENTE | PENDIENTE |
| `git-release-manager` | PENDIENTE | PENDIENTE |
| `sdd` | PENDIENTE | PENDIENTE |
| `ui-design` | PENDIENTE | PENDIENTE |

| Skill esperada | Descubierta / recurso cargable | Resultado |
|----------------|-------------------------------|-----------|
| `architecture` | PENDIENTE | PENDIENTE |
| `code-quality` | PENDIENTE | PENDIENTE |
| `data-api` | PENDIENTE | PENDIENTE |
| `documentation-orchestrator` | PENDIENTE | PENDIENTE |
| `git-commit` | PENDIENTE | PENDIENTE |
| `project-navigator` | PENDIENTE | PENDIENTE |
| `release-management` | PENDIENTE | PENDIENTE |
| `sdd-spec` | PENDIENTE | PENDIENTE |
| `security` | PENDIENTE | PENDIENTE |
| `ui-design` | PENDIENTE | PENDIENTE |

Para cada skill, abre su `SKILL.md` y un recurso asociado que exista en el árbol
instalado; registra la ruta relativa y un encabezado público reconocible. Ver un
nombre en un listado no demuestra carga del recurso. No ejecutes scripts de
referencia por el mero hecho de cargarlos.

## 3. Selección principal y carga de recursos

1. Selecciona `sdd` como principal mediante la UI efectiva de esta build; registra
   el mecanismo observado y el ID activo. **La selección está pendiente hasta
   este paso**, no se prescribe un nombre de menú sin evidencia.
2. Activa la skill con el slash documentado `/sdd-spec`. Pide una consulta de
   solo lectura del procedimiento, sin crear una spec ni implementar producto.
   Comprueba carga de `SKILL.md` y
   `sdd-spec/references/integrity-gate.md`; registra el encabezado identificado.
3. Verifica `model: inherit`, `mainAgent: true`, `subagent: true` y tools por rol
   en el artefacto; distingue esos campos de lo que la UI realmente permite.
   Las recomendaciones BAJO/MEDIO/ALTO son informativas y no cambian el modelo.
4. Comprueba que `sdd` se usa como ID nominal, sin presentar `@sdd` como comando
   nativo confirmado. `@<agente>` es routing semántico del kit. El descubrimiento
   de skills es global; no se añade un campo `skills` con resolución ambigua.

## 4. Probar herramientas individualmente

El conjunto procede de la referencia de Hooks; no es el catálogo exhaustivo del
host. Registra por **cada herramienta** nombre expuesto, rol, acción, resultado y
evidencia. No basta con probar una herramienta de cada grupo. Usa operaciones
cortas: sin servidores, watchers, REPL, comandos interactivos ni esperas indefinidas.
Define un límite de 30 segundos por operación; al agotarse, cancela por el
mecanismo del host y registra FAIL/bloqueo, sin reintentos sin límite. Una espera
de aprobación humana se registra aparte, no como cuelgue ni éxito automático.

| Grupo | Tool documentada | Prueba acotada en fixture autorizado |
|-------|------------------|---------------------------------------|
| L | `view_file` | Leer `fixture.txt` y reconocer el texto público |
| L | `list_dir` | Listar el directorio fixture |
| L | `find_by_name` | Localizar `fixture.txt` dentro del fixture |
| L | `grep_search` | Buscar `antigravity-smoke` solo en el fixture |
| D | `write_to_file` | Crear `scratch/tool-check.txt` con texto público |
| D | `replace_file_content` | Sustituir una línea del archivo creado y releer |
| G | `run_command` | Ejecutar `git --version`, sin mutación ni proceso persistente |
| W | `read_url_content` | Leer una página pública oficial y registrar título/URL |
| W | `search_web` | Buscar documentación pública de skills Antigravity |
| Q | `ask_question` | Formular una pregunta de aprobación y registrar la respuesta |

Si red o una tool no están disponibles, conserva el paso pendiente o registra
FAIL según el bloqueo; no simules el resultado ni cambies el contrato para ocultarlo.
Las aprobaciones también pueden expresarse en el chat; para acreditar esta tool
hay que observar `ask_question` realmente, no sustituirla silenciosamente.

| Rol | Tools declaradas | Límite canónico que se mantiene |
|-----|------------------|--------------------------------|
| `code-review` | L + D + G + W + Q | `inspect` no escribe; remediación aprobada por micro-paso |
| `data-api` | L + D + G + W + Q | `.data/` y datos/APIs autorizados; no UI |
| `documentation-orchestrator` | L + D + G + W + Q | `inspect` core sin escritura; skills architecture/navigator locales; documentación/indexado autorizados, no producto/CI/Git mutante |
| `git-release-manager` | L + D + G + W + Q | Git/release solo dentro de las aprobaciones explícitas |
| `sdd` | L + D + G + W + Q | Specs; producto solo con intención y gates aprobados |
| `ui-design` | L + D + G + W + Q | `.design/` y UI autorizada; no APIs/negocio |

Para las escrituras D del fixture usa `sdd` con una microtarea `direct` de cambio
local explícitamente autorizada en scratch, separada de la consulta de solo
lectura anterior. No autorices a otro rol a sobrepasar su alcance para probar D.
Comprueba las listas efectivas de los seis roles y las tools correspondientes
cuando la operación sea compatible con su rol. El resultado de una tool en un
rol no demuestra su disponibilidad en los demás. Listas y prohibiciones son
instrucciones más permisos heredados, **no sandbox por carpeta o comando**.

## 5. Invocación de subagente solicitada explícitamente

Usa un **padre del host** que exponga `invoke_subagent`; los seis roles del kit
no reciben esa herramienta. El usuario debe pedir esta prueba explícitamente.
No encadenes hijos ni automatices handoffs. Si no existe padre habilitado, deja
la comprobación pendiente con ese bloqueo.

Pasa al hijo `sdd` un contexto autocontenido, sin depender de historia heredada:

```text
Objetivo: consulta de solo lectura sobre el fixture de este smoke.
Agente hijo solicitado: sdd.
Proyecto: <ruta del fixture aislado>.
Lectura autorizada: <fixture.txt>, <SKILL.md instalado de sdd-spec>,
  <references/integrity-gate.md instalado>.
Escritura autorizada: ninguna.
Acciones autorizadas: cargar skill y referencia; leer el fixture; resumir evidencia.
Gates: no se ha aprobado Requirements, Design ni Tasks de una spec nueva.
Prohibiciones: no crear spec, no implementar, no Git mutante, no delegar otro hijo.
Retorno: ID activo, tools realmente usadas, recurso/encabezado cargado,
  resultado observable y bloqueos; sin secretos ni transcripción privada.
```

Registra que el padre invocó realmente `invoke_subagent`, el ID seleccionado y
las tools del hijo. Comprueba que el hijo carga skill/referencia globales y usa
herramientas válidas dentro del contexto recibido. No supongas que hereda la
conversación: omite deliberadamente del bloque un marcador público que solo
conozca el padre y comprueba que el hijo no afirma conocerlo ni inventa permisos.
Solicita continuar una fase que requiera un gate no aprobado y comprueba que
se detiene para la aprobación real; el nivel LLM informativo no es un gate nuevo.
El hijo no debe escribir, saltar gates ni ampliar el alcance.

## 6. Registro y criterio de resultado

| Comprobación | Resultado actual | Evidencia necesaria |
|--------------|------------------|---------------------|
| Versión/build, OS y superficie | PENDIENTE | Información observada del producto |
| Descubrimiento 6 agentes / 10 skills | PENDIENTE | IDs observados en host; skills core separadas |
| Recarga y selección principal | PENDIENTE | Acción real e ID activo |
| Carga de skills y referencias | PENDIENTE | Rutas relativas y encabezados reconocidos |
| Herramientas individuales por rol | PENDIENTE | Nombre expuesto, acción y resultado |
| Padre invoca hijo con contexto explícito | PENDIENTE | Tool real, ID, recursos, límites y gates respetados |

La evidencia de instalación/exportación en los tres OS se registra en la sección
[automatizada de CI](#evidencia-automatizada-de-ci), separada de esta matriz
runtime. Sus resultados PASS no completan los pasos de app/host pendientes.

La evidencia CI citada corresponde a la publicación anterior; no valida por sí
sola la consolidación core ni su migración. Añade una consulta `inspect` de
arquitectura y una de navegación con `documentation-orchestrator`: ambas deben
cargar solo la skill necesaria, citar fuentes y no escribir ni emitir handoff core.
Resultado y evidencia: **PENDIENTE**. Si aparecen agentes retirados, registra el
residuo y revisa la [migración opt-in](migracion-agentes.md), sin borrarlos por nombre.

Un smoke completo exige evidencia de todos los pasos runtime, no únicamente
instalación. Si falla el mapeo de tools o la carga global en hijos, registra el
fallo y revisa el contrato del adapter con autorización; no introduzcas paths
absolutos de una máquina en generated ni declares aceptación parcial como soporte
completo. Conserva los pendientes externos identificados por separado.

Restauración manual de skills y agentes, backup previo frente a exportación y
límites de fusión: [instalacion.md](instalacion.md). Uso y semántica del routing:
[uso.md](uso.md) y [mas.md](mas.md).
