# Design — REC-01: política de secretos

- **Modo SDD:** standard.
- **Fase:** 2 — Design.
- **Estado:** diseño aprobado, implementado y verificado; spec cerrada con evidencia real de host.
- **Gates aprobados:** Gate 1 y Gate 2, respuestas «procede» del usuario a las solicitudes correspondientes.
- **Gates posteriores:** Gate 3 aprobado; Gate 4 aprobado explícitamente mediante «Aprobar cierre REC-01» tras la verificación real.
- **Baseline:** `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`, `main`.
- **Requisitos:** [bugfix.md](bugfix.md).

## Evidencia y causa raíz

1. `canonical/skills/git-commit/SKILL.md:34,83–106` ofrece una autorización de
   inclusión para todos los sensibles sin separar secreto de sospecha por nombre.
2. `canonical/skills/release-management/SKILL.md:314–316` delega a ese procedimiento;
   `docs/agentes/git-release-manager.md:78` repite la autorización genérica.
3. `README.md:174` y `canonical/skills/security/SKILL.md:179,215` prohíben
   exposición; no existe una excepción compatible para credenciales reales.
4. `tools/validate.py` verifica estructura, tokens y reproducibilidad, no secretos.
   `.github/workflows/ci.yml` no invoca un scanner. La búsqueda de gitleaks,
   detect-secrets, trufflehog y controles de secret scanning solo encontró la deuda P0.5.
   `gitleaks` no está disponible en PATH; no se instalará.
5. `tools/render.py:82–91` copia el árbol completo de cada skill, incluidos scripts.
   Permite distribuir un control local sin alterar renderer ni instaladores.

El defecto tiene dos dimensiones: una contradicción de instrucciones y falta de
un control mínimo ejecutable vinculado al flujo. Un scanner no convierte por sí
solo las instrucciones del modelo en enforcement del host.

## Solución mínima y responsabilidades

### 1. Contrato responsable en git-commit (R1–R7, R10, I1)

Actualizar la descripción, Principios y Paso 1.5 para separar:
- **Secreto confirmado:** excluido sin opción «incluir de todas formas»; informar
  ubicación/motivo sin valor. Pedir saneamiento o exclusión antes de continuar.
- **Indicio no resuelto:** revisión pendiente; no afirmar que es seguro.
- **Configuración pública/placeholders sin secreto confirmado:** decisión
  contextual de inclusión; el nombre no basta para clasificar un secreto.

El Paso 1 comenzará por metadatos (`status`, diff de nombres/estadísticas,
historial y rama), no un diff bruto que pueda mostrar credenciales antes del control.
La revisión de contenido se realiza después del control y no imprime archivos
con hallazgos; un resultado negativo no sustituye la revisión contextual.

Antes de `git add` se comprueban candidatos del working tree; después de staging
y antes de un commit autorizado se comprueba el contenido exacto del índice.
Si el control falla, no continuar con commit hasta resolverlo. El agente no obtiene
autorización automática para editar, eliminar o desstagear trabajo ajeno.
No se cambia la autorización existente de commit, push, release ni acciones destructivas.

### 2. Control distribuible, sin dependencias nuevas (R3, R4, R8–R10)

Fuente única: `canonical/skills/git-commit/scripts/check_secrets.py`, Python 3.10+
y biblioteca estándar. Control de solo lectura; sin operaciones de staging/commit.

Entradas de CLI, con `--repo` explícito (por defecto carpeta actual):
- `--staged`: inspecciona blobs del índice, no el working tree ni solo líneas añadidas.
- `--tracked`: inspecciona archivos tracked del working tree, para CI.
- Rutas relativas explícitas: inspecciona candidatos antes de staging, incluidos
  archivos sin seguimiento. Este modo solo acredita esas rutas.

Los modos son mutuamente excluyentes. No existe un flag de autorización, whitelist
por nombre ni opción de continuar con hallazgos. Las rutas se validan contra la raíz;
en modo filesystem se rechazan enlaces que puedan conducir fuera o impedir acreditar
el contenido propuesto. En el índice se informa como evaluación incompleta para
enlaces/submódulos o estados de conflicto no cubiertos, sin leer destinos externos.

Detección acotada por contenido en bytes:
- Cabeceras PEM de claves privadas (genéricas, RSA, EC, DSA y OpenSSH).
- Formatos completos de tokens GitHub conocidos: clásicos con prefijos de token y
  longitud esperada, y PAT de granularidad fina.

Una coincidencia es un indicio accionable que bloquea ese contenido, no una prueba
de que la credencial esté activa. Los fixtures sintéticos deliberadamente detectables
reciben el mismo rechazo. URLs, nombres de variables y valores como `YOUR_TOKEN`,
`${TOKEN}` o `<placeholder>` no son credenciales por nombre.

No detectar contraseñas arbitrarias, secretos cifrados/ofuscados, todos los proveedores,
historial Git ni valores excluidos del conjunto de entrada. No hacer red ni validar
credenciales contra proveedores. El resultado negativo significa «sin coincidencias
en las reglas y entradas evaluadas», nunca «sin secretos».

Salida y errores:
- `0`: evaluación completa, sin coincidencias de las reglas soportadas.
- `1`: hallazgos, con ruta sanitizada, línea y regla; sin fragmentos ni valores.
- `2`: evaluación incompleta, ruta/argumento no admitido, lectura o Git fallido.
- Errores propios con causa fija; no imprimir stdout/stderr bruto de Git, traceback,
  excepciones que puedan contener datos ni contenido. Sanitizar controles de rutas
  y firmas detectables que aparezcan en una ruta antes de emitirla.

### 3. Integración local y CI (R7–R10, I3)

- `tools/check_secrets.py`: wrapper mínimo de la fuente anterior, sin duplicar reglas.
- `.github/workflows/ci.yml`: ejecutar el control `--tracked` y su suite de negativos.
  El control se ejecuta antes del render; un fixture incorporado a un repositorio
  temporal debe producir salida no cero usando el mismo entrypoint que CI.
- La skill referencia su script relativo, ejecutable desde cualquier copia distribuida;
  no presupone que el proyecto objetivo contenga `tools/` del kit.
- El renderer existente distribuye el script a las seis plataformas. No añadir
  hooks globales ni enforcement específico de un host (REC-02 queda fuera).

### 4. Consumidores y documentación (R7, R10, I1–I4)

Actualizar solo lo pertinente:
- `canonical/skills/release-management/SKILL.md`: reutilizar regla y control en
  el commit de versión/CHANGELOG; no limitar revisión a nombres de esos archivos.
- `canonical/agents/git-release-manager.md`: exclusión no exceptuable y controles independientes.
- `canonical/skills/security/SKILL.md`: mantener no exposición y aclarar distinción
  de indicios/placeholders y exclusión al publicar; referenciar el procedimiento Git.
- `docs/agentes/git-release-manager.md`, `docs/desarrollo.md` y `docs/mejoras.md`
  P0.5: política, uso local/CI y límites. No cerrar permisos, prompt injection ni
  otros elementos P0.5 ajenos; no cambiar snapshots legados.
- `generated/`: regenerar, no editar manualmente.
- Spec y registros de REC-01: evidencias y estado real, sin alterar otros IDs.

## Invariantes (máximo cinco)

1. Ninguna autorización conversacional cambia el rechazo de un secreto confirmado.
2. El nombre por sí solo no confirma un secreto ni garantiza que no lo haya.
3. Las salidas del control y la evidencia no contienen el valor del fixture sensible.
4. Evaluación incompleta no produce salida 0 ni autorización de publicación.
5. El control no modifica índice, archivos ni refs; las distribuciones derivan de fuentes.

## Pruebas y evidencia

Estrategia: regresión del contrato y TDD focalizado para el nuevo control; usar
`unittest`/subprocess, coherente con las suites del repositorio. No añadir pytest
ni Hypothesis: no hay una propiedad algebraica que requiera PBT en este alcance.

| Nivel | Casos y evidencia exigida |
|---|---|
| Contrato | Regresión que detecta oferta de inclusión de secretos en Git/consumidores; RED textual identificado como tal, no runtime |
| Scanner | RED antes de implementación y GREEN: firmas sintéticas en nombre normal y sospechoso; placeholders/configuración pública aceptados |
| Índice real | Repositorio temporal con `git init`/`git add` sin commit: secreto staged y working tree saneado debe seguir rechazado; caso inverso diferenciado |
| No exposición | Capturar stdout/stderr, comprobar ausencia del valor; también fallos de lectura/Git y nombres con controles |
| Fallos | Ruta externa, symlink, modo incompatible, Git inválido o evaluación incompleta: salida 2, nunca 0; sin mutaciones |
| CI/local | Entry point del kit y script distribuido sobre los mismos fixtures; sin opción de override; ejecución equivale al paso CI, no al run remoto |
| Distribución | `render`, `validate`, enlaces y suites pertinentes; script presente en seis hosts; comparación con fuente única |
| Host | Solicitud explícita de incluir fixture detectable, sin permiso para commit real; contraste público y placeholder, herramientas y respuesta sanitizadas |

En tests, ensamblar valores ficticios en memoria para no introducir un token
completo ni una cabecera bloqueable literalmente en las fuentes de prueba.
Capturar snapshots de archivos, índice y refs para probar solo lectura.
No realizar commits ni siquiera en repositorios temporales.

Baseline observado antes del fix: `python3 tools/validate.py` correcto (10 skills,
6 agentes, 6 plataformas), `python3 tools/test_mas_identity.py` 231/231,
`python3 tools/check_links.py` 78 archivos correctos. `opencode --version` devuelve
`1.18.34`; disponibilidad de CLI no acredita ejecución del agente modificado.

El escenario host se intentará solo con fuentes actualizadas cargadas explícitamente
y un perfil temporal, sin instalar globalmente ni lanzar escritores paralelos en
esta carpeta. Si requiere una autorización indispensable de entorno/proveedor
que no existe, registrar exactamente el bloqueo; no sustituirlo por un test de
frases ni cerrar REC-01. No se presupone éxito ni equivalencia multi-host.

## Quality bar y RNF críticos

- **Confidencialidad:** valores ausentes de salidas y evidencia; tests de capturas.
- **Integridad:** control de solo lectura; pruebas de snapshots del índice/refs/archivos.
- **Distribución:** código canónico único, wrapper sin reglas y renderer sin cambios;
  validación de hashes y ejecución desde copia distribuida.
- **Errores verificables:** exit codes 0/1/2, causas sanitizadas y negativos reales.
- **Reproducibilidad:** fixtures sintéticos y Python 3.10+ sin instalaciones nuevas;
  comando, entorno y resultado registrados.

Excepciones aplicables: no hay UI, BD, persistencia propia, servicios ni red;
capas/DI de aplicación no aplican. Función de detección separada del adaptador
Git/filesystem y CLI, sin interfaces/servicios anticipados ni singleton de
infraestructura. I/O síncrono en CLI, fuera de cualquier loop de UI.

## Secuencia y cierre

Gate 2 aprobado. Se desglosan tareas trazadas y se solicita Gate 3. Tras implementar,
continuar directamente con Verification. Mantener REC-01 abierto si falta evidencia
conductual o cualquier criterio de cierre; aprobar Design no acredita ninguno.
