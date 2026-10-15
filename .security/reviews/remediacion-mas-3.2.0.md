# Remediación de pendientes — MAS 3.2.0

## Alcance autorizado

El usuario aprobó trabajar secuencialmente los seis pendientes y las políticas
propuestas: instrucciones de proyecto subordinadas al alcance autorizado,
inspección/documentación/remediación diferenciadas, rechazo de symlinks al importar,
acciones CI fijadas a SHA y retirada explícita respaldada de agentes obsoletos.
Baseline: `10373b3` (`v3.2.0`) más cambios locales preexistentes, preservados.
Este registro no certifica hosts ni instalaciones del usuario.

## SEC-0005 — Criterios de aceptación

1. Las instrucciones de proyecto aplicables siguen siendo utilizables, sin poder
   aprobar gates, ampliar permisos o autorizar acciones por sí mismas.
2. Código, documentos, resultados de herramientas y web se tratan como evidencia;
   sus instrucciones embebidas no autorizan ejecución ni envío de datos.
3. Se comprueba alcance y permisos antes de actuar y se distingue aprobación de
   herramienta de aprobación del plan. No se presenta el prompt como sandbox.
4. La política aparece en agente y skill canónicos y se distribuye a seis plataformas.

Implementación: sección `Frontera de confianza` en agente y skill SDD, con carga
obligatoria de `references/workspace-trust.md`; contrato de regresión estático en
`tools/test_sdd_contract.py` y propagación a seis plataformas.

Verificación: `python3 -B tools/test_sdd_contract.py`, 653/653 comprobaciones.
El primer intento excedió presupuestos de contexto; se extrajo la política a una
referencia obligatoria y se compactaron las entradas sin relajar los presupuestos.
La referencia es contexto obligatorio adicional, no medido por los escenarios
históricos de la suite que solo suman los archivos allí enumerados.
La resistencia dinámica a prompt injection y los permisos
efectivos en cada host requieren evidencia adicional; no se cierran por texto.

OpenCode SDD solicita ahora aprobación de webfetch, además de los controles de
escritura/ejecución ya existentes. No se modifican configuraciones instaladas.

## SEC-0001 — Capacidades de Code Review

Política por operación antes del contexto del workspace, distribuida a seis hosts.
Kiro añade `ask` para `fs_write` y `shell`, conservando los `deny` destructivos.
OpenCode añade `ask` para `webfetch`; edición, Bash, task y exterior ya usaban ask.
Los adaptadores restantes conservan herramientas para documentación/remediación;
sin configuración verificable de aislamiento por operación, no se promete modo
read-only efectivo. El agente detiene acciones sin control/autorización aplicable.

Verificación: `test_code_review_contract.py` (7 tests) y `test_permissions.py`
(9 tests), ambos OK. Son contratos estáticos. Pendiente comprobar permisos reales
y escenarios de abuso en los hosts; documentación en `docs/agentes/code-review.md`.

## SEC-0003 — Importador

Rechazo de enlaces/reparse points en raíces, padres y árboles declarados; lectura
de archivos regulares antes de crear la instantánea. Reutiliza `safe_path`,
`safe_directory` y `read_regular` de `retired_agents.py`. No sigue entradas ajenas.
Mantiene modos de archivos; no usa `copytree/copy2` que siguen enlaces por defecto.
Supuesto: origen estable; no protege contra un actor concurrente que sustituya
directorios entre las comprobaciones y aperturas.

`python3 -B tools/test_import_installed.py`: 9 tests OK. El baseline falló ante
enlaces de archivo/directorio/raíz y dry-run; los bucles de subcasos se ajustaron
con finally para limpiar fixtures aun tras una aserción fallida. Cobertura final:
importación regular, ajenos, dry-run, enlaces internos/externos/rotos, raíces y
rutas inseguras, FIFO y orígenes ausentes. Todos usan perfiles temporales.

CI de v3.3.0 reveló que Windows normaliza paths cortos 8.3 (`RUNNER~1`) a su
forma larga. El importador ahora usa inspección por componentes de `safe_directory`
en Windows, sin comparar las dos representaciones. Añadido contrato Windows
simulado; importador 10/10 y Antigravity 22/22 en macOS. Reejecutar workflow Windows
tras integrar el fix para completar evidencia multiplataforma.

## SEC-0002 — CI inmutable

Todos los `uses:` de `.github/workflows/ci.yml` fijados a SHA completos verificados
por `git ls-remote` en repositorios oficiales: checkout v4.4.0 y setup-python v5.6.0.
Coinciden con los tags major previamente usados al revisar; no se cambia major.
Dependabot (`.github/dependabot.yml`) propone revisión mensual de GitHub Actions.
Antes de aprobar una actualización: verificar SHA/tag oficial, revisar cambios y
compatibilidad del runner, conservar SHA completo y comprobar ambos jobs de CI.
No hay automerge. La comprobación local no sustituye una ejecución remota de Actions.

## SEC-0004 — Retirada de agentes

La política aprobada ya está implementada en MAS 3.2.0: catálogo de agentes
retirados, modo opt-in, respaldos verificados y aprobación ruta/SHA para bytes
desconocidos. `--force` no aprueba retiradas. Los avisos distinguen instalación
vigente de migración pendiente. No se requiere modificar el código existente.

`python3 -B tools/test_retired_agents.py`: 26 tests OK (22.670 s), con wrappers
Bash reales en perfiles temporales para seis plataformas. Verifica dry-run sin
efectos, preservación por defecto, retiro/backup, aprobación de personalizados,
conservación de agentes ajenos y repetición idempotente, además de casos negativos.
La suite incluye paridad estática PowerShell; no prueba ejecución nativa Windows.
Las instalaciones reales no migradas mantienen agentes anteriores hasta el opt-in;
cerrar la implementación no declara migradas dichas instalaciones.

## QLT-0001 — Calidad

Eliminadas expresiones duplicadas en `test_ps1_repo_root_references` sin cambiar
las variantes realmente distintas. Comprobación focalizada: 24/24 OK.
`test_integrity.py`: 416/416 OK en reejecución final. La primera ejecución había
fallado por un enlace temporal/no presente en el estado final; no persiste el fallo.
Registro canónico en `.quality/` actualizado tras verificar.

## Verificación adicional del motor OpenCode

Comando: `AI_AGENTS_TEST_TMP=<temporal-aprobado> python3 -B tools/test_permissions_host.py`.
OpenCode 1.18.34, HOME/config/cache temporales, proveedor local simulado sin LLM
remoto ni credenciales del usuario. Resultado: 22 escenarios de control PASS y
2 limitaciones observadas (shell aprobado puede escribir fuera de raíces del rol;
enlace interno puede redirigir una escritura aprobada). Ocho escenarios añadidos
comprueban rechazo de edición/shell y aprobación/rechazo de webfetch para Code Review
y SDD. No acredita consentimiento humano ni conducta de un LLM real.

Dos intentos iniciales del probe se interrumpieron al consultar `/permission` por
metadatos `timeout` indefinidos en webfetch; el fixture ahora indica timeout explícito
y reporta errores de la API aislada. El intento final completó todos los escenarios.

Otros checks: `validate.py` OK (11 skills, 5 agentes, 6 plataformas),
`test_context_efficiency.py` 12/12, `test_install.py` 250/250 y contrato SDD 653/653.
