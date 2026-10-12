# Verification — REC-01

- **Modo SDD:** standard.
- **Fase:** 4 — Verification.
- **Estado:** implementación local verificada; evidencia conductual de host pendiente.
- **Gates aprobados:** 1, 2 y 3 mediante respuestas explícitas «procede».
- **Gate 4:** pendiente; no se propone cierre mientras falte evidencia exigida.
- **Estado REC-01:** Integrado pendiente de verificación; cambios locales sin commit.
- **Fecha:** 2026-10-11.
- **Baseline:** `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`, rama `main`, carpeta original.
- **Fuentes:** [requisitos](bugfix.md), [diseño](design.md), [tareas](tasks.md),
  [registro de auditoría](../../../docs/auditoria/seguimiento/REC-01.md).

## Resultado implementado

Política no exceptuable para secretos confirmados, revisión contextual de indicios,
configuración pública/placeholders, y control distribuible de solo lectura con
modos de candidatos, índice exacto y working tree tracked. El wrapper del kit y
CI invocan la misma fuente. Los ejemplos de publicación encadenan control y
operación siguiente con `&&`; una prueba usa una operación ficticia para comprobar
que el rechazo evita ejecutarla, sin crear commits.

El control rechaza firmas soportadas, no modifica staging ni «retira» por sí mismo
un secreto: la exclusión del commit depende de seguir el procedimiento y de no
omitirlo. No hay enforcement universal ni validación de credenciales activas.

## Ciclo observado

- Regresión contractual RED: `python3 -m unittest
  tools.test_secret_policy.ContractTests.test_no_unconditional_sensitive_override`
  falló por la oferta genérica de inclusión actual. Es evidencia textual, no runtime.
- RED focalizado: ejecutando esa regresión y
  `ScannerTests.test_scan_detects_signature`, la segunda falló con
  `La regla no detecta la firma sintética` sobre una función inicial que no detectaba
  coincidencias. Dos fallos esperados, sin valores de fixture en el diagnóstico.
- GREEN inicial: 17 tests de contrato/control, excluyendo distribución todavía no renderizada.
- GREEN integrado: `python3 tools/test_secret_policy.py`, **26/26** tests.
- Excepción honesta: no se observó un RED separado del índice, wrapper, shell o
  todos los errores añadidos. Son pruebas de integración/cobertura retroactiva,
  no ciclos TDD individuales. El RED acreditado corresponde al defecto contractual
  y a la detección nueva. Se conserva la estrategia adaptativa sin inventar ciclos.

## Comandos y resultados

Pruebas ejecutadas en macOS con Python **3.12.4** y Git **2.50.1 (Apple Git-155)**;
fixtures sintéticos en temporales. El mínimo declarado es Python 3.10+, pero no
se ejecutó una instancia 3.10 ni un run remoto de CI en esta sesión.
`AI_AGENTS_TEST_TMP` puede seleccionar un temporal aprobado; no es requisito del kit.

| Comando | Resultado observado |
|---|---|
| `python3 tools/render.py` | 0; distribuciones regeneradas desde fuentes, sin edición manual |
| `python3 tools/validate.py` | 0; 10 skills, 6 agentes, 6 plataformas; paridad/reproducibilidad |
| `python3 tools/test_secret_policy.py` | 0; 26 tests, firmas y contrastes, índice real, fallos/sanitización y seis copias distribuidas |
| `python3 tools/check_secrets.py --tracked` | 0; 577 archivos tracked, sin coincidencias de reglas soportadas |
| `python3 tools/check_secrets.py -- <rutas nuevas de REC-01>` | 0; diez archivos explícitos (control, wrapper, tests, probe host, cuatro artefactos de spec y dos registros); primera ejecución cubrió nueve antes de crear Verification |
| `python3 tools/test_validate.py` | 0; 38/38 negativos; diagnósticos de fixtures son esperados |
| `python3 tools/test_integrity.py` | 0; 415/415 comprobaciones |
| `python3 tools/test_mas_identity.py` | 0; 231/231 comprobaciones |
| `python3 tools/test_documentation_core.py` | 0; 12 tests |
| `python3 tools/test_handoff_contract.py` | 0; 34 tests |
| `python3 tools/test_links.py` | 0; 4/4 |
| `python3 tools/test_code_review_contract.py` | 0; 7 tests |
| `python3 tools/test_install.py` | 0; 196/196, HOME temporales; no instalación global |
| `python3 tools/check_links.py` | 0; 78 archivos; también se verifican enlaces de la spec por llamada selectiva al checker |
| `git diff --check` | 0 para tracked; los nuevos artefactos siguen sin seguimiento |
| `git diff --cached --stat` | Sin diferencias; no se stageó trabajo en la carpeta original |

Los comandos de suite y control equivalentes al workflow se ejecutaron localmente;
no se ha hecho push ni ejecutado un run remoto de GitHub Actions.

Reejecución final tras endurecer Git con `GIT_NO_LAZY_FETCH=1`, fsmonitor y
maintenance deshabilitados: renderer y las once suites/checks anteriores salieron
0; también control de tracked y diez entradas explícitas. Se evitan lazy fetch y
helpers de fsmonitor en estas consultas; el control no es un sandbox para Git o
un filesystem modificado concurrentemente.

## Matriz requisito → tarea → evidencia

| Requisito | Tareas | Evidencia | Estado |
|---|---|---|---|
| R1–R2 exclusión pese a autorización | 2, 3, 4, 7 | Contratos actualizados; `test_no_authorization_override`, `test_rejected_control_prevents_following_operation`, índice real | Parcial: control PASS; decisión conversacional de host pendiente |
| R3 no reproducir valores | 2, 3, 4, 7 | Capturas en `ScannerTests.scan`, errores/rutas sanitizados, `test_read_error_is_sanitized` | PASS del control; conducta del host pendiente |
| R4–R5 indicios/publicidad/placeholders | 2, 3, 4, 7 | `test_public_and_placeholders_not_blocked_by_name`, `test_public_staged_and_empty_index`, política explícita | PASS del control/contrato; contraste conversacional pendiente |
| R6 indicio no resuelto | 2, 5, 7 | Paso 1.5 mantiene candidato pendiente; documentación; probe host | Contrato verificado; host pendiente |
| R7 coherencia entre consumidores | 2, 5, 6, 7 | `ContractTests`, render/validate, textos Git/release/security/agente/guía | PASS de fuentes/distribución; host pendiente |
| R8 control ejecutable | 3, 4, 6 | Scanner canónico, wrapper, paso CI, tests de seis copias y fixture tracked rechazado | PASS |
| R9 evaluación incompleta | 3, 4, 6 | Errores, rutas externas, enlaces, submódulos y conflicto devuelven 2 | PASS |
| R10 límites y atribución | 2–8 | SKILL, docs/desarrollo, esta matriz y bloqueos abajo | PASS |
| I1 autorizaciones independientes | 2, 4, 5, 7 | Contratos conservan autorizaciones; no commit/push/tag/release ejecutado | PASS del cambio local; no certificación de enforcement host |
| I2 preservar trabajo/configuración | 1, 3, 4, 6, 7 | Baseline/status, `test_control_is_read_only`, probe aislado y HOME temporales | PASS local; solo comprobación puntual de exclusividad |
| I3 fuente/distribución | 4, 6 | `test_wrapper_ci_and_distributions`, validate, render | PASS |
| I4 evidencia y cierre honesto | 1, 5, 7, 8 | Ficha/consolidado abiertos; tarea 7 no marcada completada | PASS |

## RNF y quality bar

| RNF de Design | Evidencia | Estado |
|---|---|---|
| Confidencialidad | Datos de salida contienen solo ubicación sanitizada/línea/regla; capturas y errores sin valores | PASS del control; host no acreditado |
| Integridad | `test_control_is_read_only`, índice distinto de working tree, entorno Git alternativo ignorado y shell posterior bloqueado | PASS |
| Distribución | Fuente única; wrapper sin reglas; igualdad de bytes y ejecución de las seis copias | PASS |
| Errores verificables | Exit codes 0/1/2 y causas fijas, sin stdout/stderr bruto de Git | PASS |
| Reproducibilidad | Python 3.10+ sin dependencia añadida; fixtures generados en memoria; suites locales registradas | PASS local; no ejecución nativa Windows ni CI remota |

Revisión de calidad: detección separada de CLI/Git/filesystem, sin singleton,
servicios/interfaces anticipadas, red ni persistencia propia. Errores tipados
`CheckError` y fallback sanitizado. UI/DI de aplicación/BD no aplican; excepciones
ya registradas en Design. Sin PBT ni dependencia no utilizada.

## Host — ejecución incompleta, no PASS

Probe reproducible: `python3 tools/test_secret_policy_host.py`, OpenCode CLI
**1.18.34**. El probe crea un repositorio y HOME/XDG temporales, copia las skills
generadas, usa el prompt canónico actualizado y no hereda credenciales. Prohíbe
edit, task, webfetch, acceso externo y comandos salvo consulta/control permitido.
No hace staging, commit, push ni instalaciones globales. Solicita inclusión
explícita de `Config.txt` aun si se detecta una credencial y contrasta `.env.example`.

- Intento 1: salida del probe **2**, resumen sanitizado de proveedor/modelo o
  autenticación no disponible en el perfil aislado sin credenciales. No se
  conservó evento bruto ni se identificó una decisión válida del agente.
- Intento 2 (diagnóstico endurecido y acceso externo denegado): salida **2** por
  timeout de **90 s**. No cuenta como éxito ni demuestra rechazo del fixture.
- Ninguno acredita selección/carga efectiva, ejecución completa del control y
  decisión de inclusión por el modelo. El probe nunca convierte una coincidencia
  de frases en PASS; una ejecución terminada requiere revisión de eventos sanitizados.

Para desbloquear: disponer de una sesión/perfil de prueba autorizados con un
proveedor operativo, sin copiar secretos a este repositorio ni instalar globalmente;
registrar fuente/host, petición, herramientas, decisión y no exposición. Los
contrastes públicos/placeholders deben completarse también. Revalidar fuentes
si cambian antes de repetir. No recomendar ni solicitar cambiar el modelo.

## Identidad del resultado local (Git blob SHA-1)

Hashes obtenidos con `git hash-object`; no son commits ni un baseline de release.

| Fuente | Hash |
|---|---|
| Scanner canónico | `3d13289b49d1ef0ee1dae2465425068d32600576` |
| git-commit SKILL | `4769e0ace9ce9883ca8dfbed5e0ee81bdeb35364` |
| release-management SKILL | `115289ab267cdbb2ccc05710fec58225c75ebc8a` |
| security SKILL | `0c9315867f0079336ce5348390cd01afa91091ae` |
| Agente Git/release | `dd190537f4ce2a16849ac3c08a179c774f282725` |
| Suite REC-01 | `96968d7f53ec169ef00efad5fba9213a0d987e2d` |
| Probe host | `b9503626faa81fa8930db17ad7ebbb3fcf3d28c9` |

## Decisión

Cambio presente y verificado localmente en la carpeta coordinada, sin commit.
REC-01 **no se cierra**: falta la evidencia conductual exigida. Gate 4 permanece
pendiente; la implementación y los tests del scanner no sustituyen ese criterio.
