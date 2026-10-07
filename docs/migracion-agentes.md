# Migración segura de agentes retirados

El catálogo vigente contiene **6 agentes y 10 skills**. `documentation-orchestrator`
asume arquitectura y navegación mediante las skills **separadas** `architecture`
y `project-navigator`. Los IDs de agentes antiguos no son aliases ni receptores
de handoff; una autorización antigua no se transfiere. Si el host no resuelve una
mención retirada, selecciona el agente vigente y reformula la solicitud.

Esta guía describe una operación del **instalador**, no una acción del agente
documental. Implementar o actualizar el kit no autoriza migrar el perfil real.
Las specs, snapshots legacy y evidencias históricas se conservan.

## Revisar antes de retirar

1. Regenera y valida la distribución que vas a instalar según
   [instalación](instalacion.md). Revisa la ayuda del wrapper de tu plataforma.
2. Identifica los destinos efectivos globales/locales y todos los árboles que el
   host escanea. Comprueba variables de entorno y perfiles alternativos; no supongas
   que el HOME predeterminado es el destino real.
3. Solicita un plan con `--migrate-retired-agents --dry-run`. Una instalación normal,
   `--check-installed` o `--force` no autorizan retirada. `--check-installed` sigue
   siendo solo lectura.
4. Revisa por candidato su ruta exacta, clasificación, SHA-256, baseline histórico,
   acción prevista y destino de respaldo. El dry-run no modifica archivos,
   directorios ni metadatos instalados.

Ejemplo Bash para OpenCode, **solo en el entorno elegido y autorizado**:

```bash
./scripts/install/opencode.sh --migrate-retired-agents --dry-run
```

Sustituye el wrapper por el de tu plataforma. Los seis wrappers PowerShell exponen
`-MigrateRetiredAgents`, `-ApproveRetiredFile`, `-ApproveRetiredSha256` y
`-AdditionalAgentsDest`; los tres últimos reciben listas de strings.
La política compartida es la misma en ambos shells:

```powershell
.\scripts\install\opencode.ps1 -MigrateRetiredAgents -DryRun
```

## Destinos adicionales y OpenCode

La migración incluye el destino global efectivo del wrapper. En OpenCode incluye
por defecto **ambos directorios hermanos `agent/` y `agents/`** bajo el perfil
resuelto (respeta `XDG_CONFIG_HOME`); la instalación vigente sigue copiándose a
`agent/`. No hace falta añadir el hermano global manualmente.

Los destinos locales de proyectos u otros perfiles no se descubren recursivamente.
Decláralos explícitamente con **`--additional-agents-dest RUTA`**, repetible, o
`-AdditionalAgentsDest` como lista PowerShell. Selecciona el directorio de agentes,
no la raíz del proyecto. Estas opciones requieren migración opt-in y amplían solo
los destinos a revisar para retirada, no los destinos de instalación vigente.
Cada aprobación debe apuntar a un candidato exacto dentro de esos destinos.

```bash
# Sustituye por el directorio local absoluto revisado; no ejecutes el placeholder.
LOCAL_AGENTS='/RUTA/ABSOLUTA/DEL/PROYECTO/.opencode/agents'
./scripts/install/opencode.sh --migrate-retired-agents --dry-run \
  --additional-agents-dest "$LOCAL_AGENTS"
```

```powershell
# Sustituye por los directorios locales absolutos revisados.
$LocalAgents = @('C:\RUTA\DEL\PROYECTO\.opencode\agents')
.\scripts\install\opencode.ps1 -MigrateRetiredAgents -DryRun `
  -AdditionalAgentsDest $LocalAgents
```

Revisa en el plan todos los destinos efectivos y mantenlos idénticos al autorizar
la ejecución. Para una instancia local OpenCode que use también `agent/`, añade
ese directorio explícitamente a la lista: la inclusión automática del hermano
se aplica al destino principal, no a cada destino adicional.

## Clasificación y aprobación específica

| Candidato | Tratamiento |
|---|---|
| Archivo regular en ruta permitida con hash histórico conocido | Puede retirarse dentro del opt-in, tras respaldo verificado. |
| Personalizado por el usuario, sin hash histórico coincidente | El tooling lo clasifica como incierto; conservar hasta aprobación específica de ruta y bytes tras revisión. |
| Hash desconocido o procedencia incierta | Conservar hasta aprobación específica; informar migración incompleta. |
| Ausente | No-op; repetir no crea nuevos respaldos para ese candidato. |
| Symlink, ruta fuera del destino o archivo ilegible | Bloquear ese candidato; no seguir enlaces ni declarar migración completa. |
| Extra ajeno no seleccionado | Informar y conservar. |

Los hashes conocidos provienen de bytes de artefactos históricos verificados,
con plataforma y baseline de origen, en `tools/retired_agents.json`; el catálogo
actual fija un commit histórico, no infiere una versión de release.
Coincidir es un criterio operativo de copia conocida, no una prueba absoluta de
autoría. **Las versiones anteriores no tenían un registro general de propiedad**:
ni el nombre ni estar en una carpeta del host demuestran ownership del kit.
Sin baseline fiable, un hash diferente significa *incierto*, no necesariamente
*personalizado*. No se inventan hashes ni se adoptan extras como propios.

Para personalizados/inciertos usa el par **`--approve-retired-file PATH`
`--approve-retired-sha256 SHA`**, una vez por archivo, después de revisar contenido,
hash y plan. La ruta debe ser **absoluta y exacta**; el SHA debe ser el valor real
del plan para ese archivo, **64 caracteres hexadecimales en minúscula**.
Las dos opciones son repetibles y sus listas se emparejan por posición: primera
ruta con primer SHA, segunda ruta con segundo SHA. No admite wildcard, rutas
duplicadas ni aprobación global; `--force` no reemplaza esta selección.
Omitir un SHA o desbalancear las listas es un error de argumentos (`2`). Si el
hash aprobado no coincide con los bytes actuales, el candidato se conserva y la
migración queda pendiente/error (`1`): aprobar una ruta no aprueba cambios nuevos.

```bash
# Sustituye rutas y placeholders con los valores EXACTOS del plan revisado.
# Los placeholders SHA siguientes NO son hashes válidos ni ejemplos ejecutables.
ARCH_FILE='/RUTA/ABSOLUTA/DEL/PLAN/architecture.md'
NAV_FILE='/RUTA/ABSOLUTA/DEL/PLAN/project-navigator.md'
ARCH_SHA='<SHA256_REAL_DE_64_HEX_MINUSCULAS_DEL_PLAN_PARA_ARCH_FILE>'
NAV_SHA='<SHA256_REAL_DE_64_HEX_MINUSCULAS_DEL_PLAN_PARA_NAV_FILE>'

# Primero vuelve a simular con los pares ruta/SHA revisados.
./scripts/install/opencode.sh --migrate-retired-agents --dry-run \
  --approve-retired-file "$ARCH_FILE" --approve-retired-sha256 "$ARCH_SHA" \
  --approve-retired-file "$NAV_FILE" --approve-retired-sha256 "$NAV_SHA"

# Solo tras revisar el plan y autorizar esa instalación/migración concreta:
./scripts/install/opencode.sh --migrate-retired-agents \
  --approve-retired-file "$ARCH_FILE" --approve-retired-sha256 "$ARCH_SHA" \
  --approve-retired-file "$NAV_FILE" --approve-retired-sha256 "$NAV_SHA"
```

Ejemplo PowerShell con las listas paralelas reales del wrapper:

```powershell
# Sustituye TODOS los placeholders por rutas exactas y SHA reales del plan.
$Files = @('C:\RUTA\EXACTA\DEL\PLAN\architecture.md',
           'C:\RUTA\EXACTA\DEL\PLAN\project-navigator.md')
$Hashes = @('<SHA256_REAL_DEL_PLAN_PARA_FILES_0>',
            '<SHA256_REAL_DEL_PLAN_PARA_FILES_1>')
.\scripts\install\opencode.ps1 -MigrateRetiredAgents -DryRun `
  -ApproveRetiredFile $Files -ApproveRetiredSha256 $Hashes

# Solo tras revisar el plan y autorizar esa instalación/migración concreta:
.\scripts\install\opencode.ps1 -MigrateRetiredAgents `
  -ApproveRetiredFile $Files -ApproveRetiredSha256 $Hashes
```

En PowerShell pasa un array por parámetro, no repitas el mismo nombre de parámetro.
Si las rutas aprobadas son locales, añade también los mismos destinos explícitos
con `--additional-agents-dest` o `-AdditionalAgentsDest` en **ambas ejecuciones**.

No añadas aprobaciones para archivos que no has revisado. Si solo uno necesita
aprobación, selecciona únicamente ese. Un cambio del original entre inspección y
retirada debe impedir la acción hasta nueva revisión.

## Respaldo obligatorio y resultados parciales

La secuencia valida fuentes/rutas, instala y verifica contenido vigente, revalida
candidatos/autorización, copia cada candidato a un respaldo único, verifica el
SHA-256 de la copia y que el original no cambió, retira solo el aprobado y verifica
ausencia. **El respaldo debe estar fuera de todos los árboles escaneados por el
host**, incluidos perfiles globales/locales; no basta renombrar el archivo dentro
de `agents/` o `prompts/`. No se reutiliza ni sobrescribe un respaldo previo.
Los wrappers usan una raíz de retirada separada, `.ai-agents-kit-retired-backups`
bajo HOME en Bash o USERPROFILE en PowerShell, con subdirectorio único por archivo.
El preflight Python admite `--backup-root`; valida siempre su separación de los
destinos activos. No confundas ese respaldo con el backup previo de sobrescrituras
vigentes de [instalación](instalacion.md).

El respaldo de retirada es obligatorio **incluso con `--force`**. Ese flag solo
mantiene su semántica anterior para sobrescrituras de contenido vigente; no
autoriza desconocidos ni permite omitir el respaldo de retirada.
Si falla la validación del destino, copia, hash o revalidación del original,
se conserva el candidato activo. No hay atomicidad de toda la instalación:
se informa el estado de cada archivo, respaldo, hash y recuperación.

Distingue **contenido vigente instalado** de **migración completada**. Candidatos
pendientes o fallidos impiden declarar la segunda; una migración solicitada
incompleta devuelve error `1`. Argumentos inválidos devuelven `2`. Extras ajenos
con lo requerido instalado pueden dar aviso y salida `0`, sin atribuirles propiedad.
Reinicia/recarga el host cuando corresponda y comprueba el catálogo descubierto;
ver archivos copiados no demuestra funcionamiento runtime.

**Nunca se borran skills, `.architecture/` ni `.navigator/` en esta migración**.
Sus formatos, índices, ADRs y documentación permanecen intactos. El catálogo de
retirados determina candidatos; no extiendas el alcance a otros archivos por nombre.

## Restauración segura por archivo

1. Conserva la ruta de respaldo, hash, ruta original y resultado reportados.
   Verifica que el respaldo es regular, legible y coincide con el SHA-256 registrado.
2. Comprueba el destino efectivo y sus padres: deben estar dentro del perfil
   esperado y no ser enlaces. Si el archivo original existe, **no lo sobrescribas**,
   aunque parezca idéntico; revisa los cambios y resuelve la colisión aparte.
3. Restaura solo el archivo seleccionado a un destino ausente usando una operación
   de copia con creación exclusiva/no-clobber; verifica hash y contenido después.
   No copies en bloque un respaldo sobre carpetas activas ni uses `-Force` para
   recuperar un agente retirado. Conserva el respaldo original.
4. Si un fallo ocurrió después de retirar, recupera únicamente cuando esas
   condiciones sean seguras; en caso contrario informa el bloqueo y la ubicación
   del respaldo. Reinicia el host si deseas cargar temporalmente el agente recuperado.

Restaurar un agente retirado puede volver a mostrar su ID antiguo; no lo convierte
en receptor vigente. Registra la recuperación y vuelve a revisar antes de reintentar.

## Smoke de migración en fixtures — PENDIENTE

No ejecutar sobre HOME/USERPROFILE real. Preparar destinos y perfiles aislados,
incluidos árboles escaneados simulados; las pruebas no necesitan un LLM runtime.

| Caso | Esperado | Resultado / evidencia |
|---|---|---|
| Instalación normal y `--force`, sin opt-in | Ningún retirado eliminado | PENDIENTE |
| Copia conocida + opt-in | Respaldo fuera de árboles activos, hashes iguales, ausencia verificada | PENDIENTE |
| Personalizado/incierto sin aprobación de ruta y SHA | Conservado; instalación y migración distinguidas; salida 1 | PENDIENTE |
| Dos inciertos, par ruta/SHA aprobado solo para uno | Retira únicamente los bytes revisados y respaldados; otro pendiente | PENDIENTE |
| Aprobación sin SHA, SHA inválido o listas desbalanceadas | Error de argumentos (2) antes de copiar; ningún candidato retirado | PENDIENTE |
| SHA aprobado distinto de los bytes actuales | Candidato conservado; migración pendiente/error (1) | PENDIENTE |
| OpenCode global `agent/` y `agents/` | Ambos revisados por defecto; vigentes instalados en `agent/` | PENDIENTE |
| Locales seleccionados con destinos adicionales / locales no seleccionados | Solo los destinos explícitos entran en el plan; otros conservados | PENDIENTE |
| Hash de versión anterior no catalogada, sin registro de propiedad | Incierto y conservado, sin inferencia por nombre | PENDIENTE |
| Backup inválido/dentro del árbol escaneado, copia fallida o symlink | Candidato activo conservado; fallo visible | PENDIENTE |
| Original cambia tras plan o durante respaldo | No retirada; nueva revisión requerida | PENDIENTE |
| Dry-run con migración y aprobaciones | Plan completo; snapshot pre/post idéntico, sin metadatos nuevos | PENDIENTE |
| Opt-in con `--force` | Respaldo obligatorio; desconocidos sin aprobación conservados | PENDIENTE |
| Repetición tras retirada y ausencia inicial | No-op sin respaldo duplicado | PENDIENTE |
| Restaurar a destino ausente / destino con archivo nuevo | Copia verificada / colisión conservada sin overwrite | PENDIENTE |
| Paridad Bash/PowerShell, seis plataformas | Mismas clasificaciones, límites y códigos | PENDIENTE |
| Skills y contexto core; extras ajenos | Snapshot intacto de skills, `.architecture/`, `.navigator/` y extras | PENDIENTE |

**Windows nativo: PENDIENTE** para este flujo de migración y recuperación.
Verificar parámetros en el código o pasar fixtures en POSIX no acredita ejecución
PowerShell/Windows. La retirada no es una comparación-y-borrado atómica portable:
POSIX usa `dir_fd` cuando está disponible; Windows recurre a una comprobación
final `lstat`. No se promete ausencia absoluta de carreras entre esa comprobación
y la retirada, ni atomicidad de toda la instalación.

Ficha por ejecución: fecha/responsable, commit del kit y baseline histórico,
plataforma/OS/shell/Python, ID del fixture y autorización, comando/flags,
destinos globales/locales seleccionados, pares ruta/SHA aprobados,
clasificación y hashes, rutas original/respaldo, snapshot pre/post, exit code,
resultado observado, recuperación y bloqueos: **PENDIENTE**. Ningún escenario
se declara aprobado solo por estar documentado o por evidencia de versiones previas.
