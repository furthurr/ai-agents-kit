---
name: git-commit
description: >-
  Crea commits ordenados y optimizados con Conventional Commits en español y
  realiza push solo tras confirmación explícita. Úsala cuando el usuario pida
  "commit", "commitear", "preparar un commit", "subir/pushear cambios", "revisar
  el estado del repo" o generar un mensaje de commit.
  Infiere el ámbito del módulo/carpeta afectada del repositorio actual, agrega
  opcionalmente la referencia al ticket si la rama lo incluye y excluye secretos
  confirmados sin excepción de autorización. Para versionado/tags/CHANGELOG usa la
  skill `release-management`, no esta.
---

# Git Commit & Push

## Identidad del MAS

En este kit, `MAS` significa **Multi-Agent System** (sistema multiagente): agentes,
skills, orquestación, handoffs, adaptadores y artefactos generados. `MAS:` dirige
una instrucción al sistema completo; `@<agente>` dirige a un agente concreto. No
confundas `MAS` con un modelo/proveedor LLM ni con `MASVS`, `MASWE` o `MASTG` de OWASP.

Conocimiento y procedimiento para administrar Git en el repositorio actual:
**commits ordenados y optimizados** siguiendo **Conventional Commits** con
mensajes en **español**, y **push solo después de una confirmación explícita**
del usuario.

## Principios

- Comunícate **en español por defecto**; si el usuario escribe en otro idioma o lo pide, adáptate.
- **Nunca** ejecutes `git commit` ni `git push` sin confirmación explícita del usuario.
- **Siempre** muestra un resumen de los cambios antes de proponer un commit.
- Usa **un solo commit** por defecto. Si hay muchos cambios de áreas distintas, estructura el cuerpo del mensaje con secciones `##` en lugar de dividir en varios commits.
- Los **secretos confirmados quedan excluidos**, aunque exista autorización del usuario. Un nombre sospechoso no confirma un secreto: aplica la revisión contextual del Paso 1.5 sin mostrar valores.
- **Alcance:** esta skill cubre commits y push. El **versionado, tags y CHANGELOG**
  son de la skill `release-management`; si la petición es de release, usa esa.
- Los comandos son **de referencia para bash/zsh**; adáptalos al shell/SO del
  usuario (PowerShell/cmd en Windows) y no dependas de utilidades Unix (`grep`,
  `sed`, `rm`) si no están disponibles.

## Flujo de trabajo

### Paso 1 — Analizar el estado del repositorio

Empieza por metadatos, sin imprimir contenido potencialmente sensible:

```bash
git status
git diff --stat
git diff --staged --stat
git log --oneline -5
git branch --show-current
```

Si el comando indica que no es un repositorio Git, avísale al usuario y detente.

### Paso 1.5 — Política de secretos y revisión contextual

Antes de proponer el commit, revisa candidatos, staged y sin seguimiento. Separa
**indicio por nombre**, **configuración pública**, **placeholder** y **secreto confirmado**.
Estos patrones son pistas para revisar, nunca prueba suficiente de un secreto:

| Patrón | Ejemplos |
|--------|----------|
| Variables de entorno | `.env`, `.env.*`, `local.properties` |
| Llaves y certificados | `*.key`, `*.pem`, `*.p12`, `*.jks`, `*.keystore`, `id_rsa` |
| Credenciales / secretos | `credentials*`, `secrets*`, `*.secret`, `service-account*.json` |
| Config de servicios | `google-services.json`, `GoogleService-Info.plist`, `*-firebase-*.json` |
| Tokens / API keys | archivos con `token`, `apikey`, `api_key`, `password` en el nombre |

#### Control ejecutable de solo lectura

Usa [scripts/check_secrets.py](scripts/check_secrets.py) de **esta skill cargada**;
resuelve su ubicación real, no supongas que el proyecto objetivo tiene `tools/`.
Python 3.10+ y Git son requisitos, no instales nada automáticamente.

```bash
# Antes de staging: solo los candidatos explícitos, incluidos untracked
python3 "<ruta-de-la-skill>/scripts/check_secrets.py" --repo "<raíz-del-proyecto>" -- "ruta/candidato"
# Antes de un commit autorizado: contenido exacto del índice completo
python3 "<ruta-de-la-skill>/scripts/check_secrets.py" --repo "<raíz-del-proyecto>" --staged
```

- Salida **1**: firmas detectables rechazadas; no las agregues ni hagas commit
  con ese contenido, aunque el usuario solicite incluirlo. La firma no acredita
  que la credencial esté activa; se excluye también un fixture detectable.
- Salida **2** o control no disponible: evaluación incompleta; detén la operación
  de publicación y explica el pendiente. Nunca equivale a aprobación.
- Salida **0**: sin coincidencias de las reglas soportadas, **no** ausencia de
  secretos. Continúa la revisión contextual antes de permitir la inclusión.

El control detecta cabeceras de claves privadas y formatos completos conocidos
de tokens GitHub por contenido, también en archivos de nombre normal. No cubre
contraseñas arbitrarias, todos los proveedores, ofuscación, historial ni rutas
no evaluadas. `--tracked` revisa el working tree tracked, no el índice.
Enlaces, submódulos y conflictos no cubiertos producen evaluación incompleta.
No tiene excepciones de autorización ni modifica archivos, staging o refs.

#### Decisión según evidencia

1. **Secretos confirmados:** exclúyelos sin excepción de autorización. Informa
   solamente `ruta:línea` y motivo; nunca el valor, fragmentos ni un diff bruto.
   Ofrece excluir o sanear mediante placeholders/referencias con la autorización
   de edición pertinente; **no** ofrezcas incluir el secreto de todas formas.
2. **Indicio no resuelto:** explica qué falta revisar; no declares el archivo seguro
   ni continúes con ese candidato hasta resolverlo o acordar su exclusión.
3. **Configuración pública o placeholders sin secretos confirmados:** un `.env`,
   `google-services.json` o nombre similar no basta para bloquearlo como secreto.
   Explica la clasificación y permite inclusión/exclusión contextual explícita;
   esto no sustituye la confirmación de commit o push.
4. **Sin indicios:** continúa al resumen, conservando las comprobaciones anteriores.

Revisa contenido/diffs sin emitir posibles valores sensibles a mensajes o logs;
no uses un diff bruto como primera detección. Si confirmas un secreto fuera de
las reglas automatizadas, aplica igualmente la exclusión. No desstagees ni edites
trabajo ajeno sin autorización; si hay que modificar staging, acuerda los archivos.
Después de saneamiento/staging vuelve a comprobar el índice. La comprobación es
puntual: si cambia el contenido antes del commit, repítela. El procedimiento y
CI no son un hook universal ni impiden un `git commit` manual que los omita.

### Paso 2 — Presentar un resumen de cambios

Muestra al usuario un resumen estructurado:

```markdown
## Resumen de Cambios

### Modificados (M)
- `ruta/archivo1` (+25, -10)

### Nuevos (A)
- `ruta/nuevo_archivo` (+100)

### Eliminados (D)
- `ruta/archivo_eliminado` (-50)

### Sin seguimiento (?)
- `ruta/archivo_sin_track`

Total: X archivos | +Y líneas | -Z líneas
```

### Paso 3 — Proponer el mensaje de commit

Genera el mensaje siguiendo **Conventional Commits** en español:

```
<tipo>(<ámbito>): <descripción corta en imperativo>

<cuerpo opcional>

<footer opcional>
```

Cuando haya muchos cambios o de varias áreas, usa **un solo commit** con el cuerpo seccionado por títulos:

```
<tipo>(<ámbito>): <descripción corta>

## <Título 1>
- Cambio principal 1
- Cambio principal 2

## <Título 2>
- Cambio principal 3

Refs: ABC-123
```

Reglas del mensaje:

1. **Tipo**: en minúsculas, uno de los tipos válidos (ver tabla).
2. **Ámbito**: opcional, en minúsculas, identifica el módulo o área afectada (ver "Ámbitos").
3. **Descripción**: en imperativo ("agregar", "corregir", "actualizar"), minúscula inicial, sin punto final, máximo 72 caracteres.
4. **Cuerpo**: explica el QUÉ y el PORQUÉ, no el CÓMO.
5. **Footer**: **opcional**. Referencia al ticket derivado del nombre de la rama (`Refs: ABC-123`) y/o breaking changes (`BREAKING CHANGE: ...`). Si no hay ticket, el commit se hace igual sin footer (ver "Footer con ticket").

### Paso 4 — Confirmar con el usuario

Antes de commitear, pregunta explícitamente:

- ¿Usar este mensaje de commit?
- ¿Modificar el mensaje?
- ¿Agregar o quitar archivos del staging?

Espera la respuesta. **No commitees** hasta recibir confirmación.

### Paso 5 — Ejecutar el commit

Solo si el usuario acepta:

```bash
git add <archivos> &&
# Repite Paso 1.5 sobre el índice; salida 1/2 impide continuar
python3 "<ruta-de-la-skill>/scripts/check_secrets.py" --repo "<raíz-del-proyecto>" --staged &&
git commit -m "<mensaje>"
```

Para mensajes con cuerpo de varias líneas, usa varios `-m` o un archivo temporal, evitando saltos de línea problemáticos en la terminal.
Conserva la cadena `&&`: no ejecutes el commit si falla staging o el control ni
uses `;` para ignorar el fallo. La confirmación no permite publicar un secreto.

Tras commitear, informa:

- Hash corto del commit.
- Rama actual.
- Remote configurado (si existe).

### Paso 6 — Push (solo tras confirmación explícita)

**Sí puedes hacer push**, pero **únicamente cuando el usuario lo confirme de forma explícita** en el chat.

1. Pregunta: "¿Deseas que haga push de este commit a `origin/<rama>`?".
2. Si el usuario confirma, ejecuta:

   ```bash
   git push origin <rama-actual>
   ```

   - Si la rama no tiene upstream, usa `git push -u origin <rama-actual>`.
3. Si el push es rechazado por `non-fast-forward`, avisa al usuario y sugiere `git pull --rebase` antes de reintentar. **No** fuerces el push (`--force`) salvo que el usuario lo pida de forma explícita y comprenda el riesgo.

Si el usuario no confirma, **no hagas push** y sugiérele el comando para hacerlo manualmente.

## Tipos de Commit (Conventional Commits)

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `feat` | Nueva funcionalidad | `feat(auth): agregar autenticación biométrica` |
| `fix` | Corrección de bug | `fix(api): corregir timeout en llamadas HTTP` |
| `docs` | Solo documentación | `docs(readme): actualizar instrucciones de instalación` |
| `style` | Formato, espacios (sin cambio de lógica) | `style(ui): aplicar formato` |
| `refactor` | Refactorización de código | `refactor(core): extraer lógica a caso de uso` |
| `test` | Agregar o modificar tests | `test(auth): agregar tests de login` |
| `chore` | Tareas de mantenimiento | `chore(deps): actualizar dependencias` |
| `perf` | Mejora de rendimiento | `perf(list): optimizar renderizado` |
| `ci` | Cambios en CI/CD | `ci(github): agregar workflow de deploy` |
| `build` | Sistema de build o dependencias externas | `build(deps): actualizar versión del framework` |
| `revert` | Revertir un commit anterior | `revert: revertir "feat(auth): agregar biometría"` |

## Ámbitos

El **ámbito** identifica el módulo, paquete o carpeta principal afectada. Es
**opcional** y depende del repositorio actual: no hay una lista fija.

- **Infiere el ámbito** de la ruta de los archivos modificados (nombre del módulo,
  carpeta o feature). Ejemplos comunes: `auth`, `api`, `ui`, `core`, `data`, `deps`.
- Si los cambios abarcan **muchas áreas**, omite el ámbito o usa uno general.
- Si el repositorio tiene una **convención de ámbitos propia**, respétala.
- El ámbito es opcional: `feat: ...` sin ámbito también es válido.

## Determinar tipo y ámbito

- Archivos nuevos que aportan funcionalidad → `feat`.
- Correcciones sobre código existente → `fix`.
- Solo archivos `.md` → `docs`.
- Solo formato/estilo sin cambio de lógica → `style`.
- Cambios en dependencias o configuración de build → `build` o `chore`.

## Footer con ticket (opcional)

El ticket de gestión (Jira, GitHub Issues, etc.) es **totalmente opcional**: da
trazabilidad entre el commit y la tarea, pero **su ausencia nunca impide crear el
commit**.

Muchos equipos incluyen el identificador en el nombre de la rama (ej. `ABC-123`,
`feature/PROJ-45-...`). Intenta extraerlo con:

```bash
git branch --show-current
```

Del nombre de la rama, **extrae tú mismo** el identificador `TICKET-123` (prefijo
de 2–10 letras + guion + números), **sin depender de `grep`** ni otras utilidades
Unix que no existen en todos los shells (p. ej. PowerShell en Windows).

### Evita falsos positivos
El patrón puede coincidir con texto que **no es un ticket** (`UTF-8`, `SHA-256`,
`COVID-19`, `H2-2024`, `UTF-16`, `BASE-64`). Antes de usar la coincidencia:

1. Toma el identificador **solo si aparece como un segmento del nombre de rama**
   (ej. `feature/ABC-123-...`, `bugfix/PROJ-45`), no incrustado en otra palabra.
2. **Descártalo** si parece un estándar/codificación conocido (UTF, SHA, BASE,
   MD, ISO, RGB, etc.) o el año/número no encaja con un ticket.
3. Si hay **varias** coincidencias o **dudas**, no adivines: pregunta brevemente
   al usuario cuál es el ticket (o si no aplica) y continúa sin footer si no responde.

### Si se encuentra un ticket válido
Agrégalo automáticamente al footer del commit: `Refs: ABC-123`.

### Si NO se encuentra un ticket
**No interrumpas ni bloquees el flujo.** Procede así:

1. Genera el commit **igual, sin footer** (es válido y correcto).
2. Comenta al usuario de forma **breve y amable**, sin tecnicismos ni alarma. Ejemplo:
   > "Nota: no detecté un número de ticket en la rama, así que preparé el commit sin
   > esa referencia. Si quieres, dime el número y lo agrego; si no, continuamos sin
   > problema."
3. Si el usuario da un número, añádelo como `Refs: <ticket>`. Si no responde o no lo
   tiene, **continúa normalmente** sin footer.

**Importante:** nunca presentes la falta del ticket como un error ni obligues al
usuario a entender qué es. Es solo un dato extra y opcional.

## Comandos de referencia

```bash
# Estado y cambios
git status
git status -s
# Solo contenido ya revisado, sin imprimir posibles valores sensibles
git diff
git diff --staged
git diff --stat

# Staging
git add <archivo>
git add .
git add -p

# Commit
git commit -m "mensaje"

# Push
git push origin <rama>
git push -u origin <rama>

# Información
git log --oneline -10
git branch -vv
git branch --show-current
git remote -v
```

## Solución de problemas

| Problema | Solución |
|----------|----------|
| "nothing to commit" | No hay cambios staged, usa `git add`. |
| "rejected - non-fast-forward" | Sugiere `git pull --rebase` antes del push. |
| "permission denied" | Verifica credenciales / SSH. |
| Conflictos de merge | Resuélvelos manualmente antes del commit. |
| Mensaje muy largo | Usa el cuerpo del commit para los detalles. |
