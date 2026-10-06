# Verificación: soporte de Google Antigravity

- **Modo SDD:** standard
- **Fase:** Verification
- **Estado:** suite local aprobada; verificación externa bloqueada por falta de evidencia
- **Gate:** Gate 4 — pendiente; no cerrar como soporte completo
- **Autorización:** «procede» tras el aviso de transición a Verification.
- **Entorno observado:** macOS 26.1 arm64, Python 3.12.4, Bash.
- **Evidencia:** ejecución local identificada como `20261006-091257` por el reloj del entorno.

## 1. Resultado ejecutivo

Los **14 comandos de aceptación** terminaron con código `0`. Se incluyen los
11 del prompt original, `test_install.py` y los dos checks nuevos de Antigravity.
No hubo regresiones observadas respecto del baseline local, que también pasó.

El render dejó **288 archivos generados idénticos** antes/después. Las seis
distribuciones tienen 48 archivos cada una; Antigravity contiene ocho agentes,
diez `SKILL.md` y sus recursos. El control separado del baseline confirmó
**333 archivos preexistentes preservados byte a byte**, excluyendo únicamente
el manifiesto autorizado.

Esta evidencia certifica el pipeline y los instaladores Bash en el entorno local,
no la ejecución Windows/Linux ni el descubrimiento real por Antigravity 2.0.
Los criterios externos siguen pendientes y la spec permanece abierta.

## 2. Comandos y resultados

| Comando ejecutado | Exit | Resultado observado |
|---|---:|---|
| `python3 tools/render.py` | 0 | Artefactos regenerados; hashes sin cambios. |
| `python3 tools/validate.py` | 0 | 10 skills, 8 agentes, 6 plataformas. |
| `python3 tools/test_integrity.py` | 0 | 449/449 checks. |
| `python3 tools/test_validate.py` | 0 | 38/38 checks negativos/positivos. |
| `python3 tools/test_model_recommendations.py` | 0 | 466/466 checks. |
| `python3 tools/test_sdd_contract.py` | 0 | 345/345 checks. |
| `python3 tools/test_code_review_contract.py` | 0 | 8 tests. |
| `python3 tools/test_handoff_contract.py` | 0 | 33 tests. |
| `python3 tools/test_mas_identity.py` | 0 | 259/259 checks. |
| `python3 tools/check_links.py` | 0 | 70 archivos Markdown revisados. |
| `python3 tools/test_links.py` | 0 | 4/4 checks. |
| `python3 tools/test_install.py` | 0 | 148/148 checks para seis plataformas. |
| `python3 tools/test_antigravity_install.py` | 0 | 19 tests, Bash/macOS, 6.477 s. |
| `python3 tools/test_antigravity_contract.py` | 0 | 5 tests, 0.146 s. |

Comprobaciones adicionales: `bash -n scripts/install/antigravity.sh
scripts/backup/antigravity.sh` y `git diff --check`, ambas exit `0`.

Logs completos y `results.json`:
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/antigravity-verification-20261006-091257/`.
Cada comando tiene `<nombre>.log`. Es evidencia local temporal, no un run de CI
duradero. Esta tabla conserva los resultados observados aunque los logs temporales
sean eliminados; para revisión externa se necesitan logs/run identificables.

## 3. Ciclo de pruebas e integridad de tareas

- **Baseline:** 11 checks existentes aprobados antes de cambios de producto;
  snapshot de fuentes/artefactos y working tree con modificaciones previas.
- **TDD focalizado:** esquema RED con 19 fallos esperados → GREEN 38/38;
  distribución RED con 4 fallos por manifest/adapters ausentes → GREEN;
  inventario instaladores RED por plataforma ausente → GREEN.
- **Instaladores/exportadores:** RED antes de crear scripts con 16 fallos por
  ausencia esperada → GREEN 16 tests. Ampliación por recursos ausentes/alterados:
  RED 3 fallos nuevos → GREEN 19 tests. Evidencia de implementación en
  `implementation.md`, además de la suite final ejecutada en esta fase.
- **Caracterización:** renderer, importador compartido y contratos comunes; no se
  les atribuye un RED nuevo cuando ya satisfacían el comportamiento.
- **Sin test nuevo:** redacción documental y YAML declarativo, cubiertos por
  revisión, enlaces, comandos locales y ejecución futura de CI.
- **PBT:** no añadido; excepción justificada en Design por contratos discretos.
- **Integridad:** auditoría independiente de solo lectura confirma artefactos y
  contenido para las diez tareas `[x]` 1.1–5.1; sin `[x]` huérfanos. Workflow y
  procedimiento smoke cuentan como preparación, no como ejecución externa.

## 4. Matriz de criterios y evidencia

**APROBADO** = comportamiento requerido comprobado dentro del alcance indicado;
**PARCIAL** = artefacto/contrato local comprobado, falta aceptación externa;
**PENDIENTE** = evidencia obligatoria no disponible. Los estados no se deducen
solo de que exista un archivo.

| Criterio | Tareas | Test / evidencia | Estado |
|---|---|---|---|
| R1.1 | 2.2, 4.1, 6.1 | Manifest y `test_manifest`/integridad. | APROBADO |
| R1.2 | 2.2, 5.1, 6.1 | `test_render_and_resources`: conjunto igual al manifest. | APROBADO |
| R2.1 | 2.2, 5.1, 6.1 | Recursos canónicos iguales en render y `test_install_hashes_and_references_spaces`. | APROBADO |
| R2.2 | 2.2, 6.1 | Metadata de skills conservada por render y contrato. | APROBADO |
| R2.3 | 2.2, 6.1 | Tests de tokens en validación; generated sin tokens pendientes. | APROBADO |
| R3.1 | 2.1, 2.2, 6.1 | Ocho filenames planos y cuerpos adaptados; contrato/schema. | APROBADO |
| R3.2 | 2.1, 2.2, 6.1 | Campos del frontmatter comprobados por helper y contrato. | APROBADO |
| R3.3 | 2.2, 6.1 | Ocho `mainAgent: true`; selección efectiva cubierta por R10. | APROBADO (configuración) |
| R3.4 | 2.2, 6.1 | Ocho `subagent: true`; invocación efectiva cubierta por R10. | APROBADO (configuración) |
| R3.5 | 2.2, 6.1 | `test_agents`: ocho `model: inherit`; contrato de modelos. | APROBADO |
| R3.6 | 2.2, 6.1 | Contrato SDD y `test_agents`: términos requeridos y excluidos. | APROBADO |
| R4.1 | 2.1, 2.2, 4.4, 6.3 | Nombres respaldados por Hooks/Subagents; falta build objetivo y mapeo runtime. | PARCIAL |
| R4.2 | 2.2, 6.1 | Listas por rol, prohibiciones canónicas y `test_agents`. No promete sandbox. | APROBADO (contrato) |
| R4.3 | 2.1, 6.1 | `test_antigravity_adapter_schema`: campos/types/tools inválidos rechazados. | APROBADO |
| R4.4 | 2.2, 4.3, 6.1 | Token nominal `sdd`, suffix del host y documentación de routing. | APROBADO |
| R4.5 | 2.2, 3.1, 6.1 | Sustitución steering y pruebas de preservación de reglas/settings. | APROBADO |
| R5.1 | 3.1, 6.1 | Destino skills y comparación de contenido en HOME temporal. | APROBADO (macOS) |
| R5.2 | 3.1, 6.1 | Destino agents y bytes de los ocho archivos. | APROBADO (macOS) |
| R5.3 | 3.1, 4.2, 6.2 | Cuatro scripts, flags/paridad estática; ejecución macOS; falta Linux/Windows. | PARCIAL |
| R5.4 | 3.1, 6.1 | Tests de skill/agente/referencia ausentes: fallo antes de escrituras. | APROBADO (Bash) |
| R5.5 | 3.1, 6.1 | stdout + exit 1, postflight, fallo copia y referencias corruptas: no éxito falso. | APROBADO (Bash) |
| R6.1 | 3.1, 6.1 | DryRun vacío/poblado: snapshots completos sin diferencias. | APROBADO (Bash) |
| R6.2 | 3.1, 6.1 | Backup de skill/agente y restauración manual; colisión evita sobrescribir respaldo. | APROBADO (Bash) |
| R6.3 | 3.1, 6.1 | Force sin carpeta de backup. | APROBADO (Bash) |
| R6.4 | 3.1, 3.2, 6.1 | Extras propios intactos; extras generated ignorados; import filtrado. | APROBADO (Bash) |
| R6.5 | 3.1, 3.2, 6.1 | Settings/reglas/credenciales ficticias preservadas; HOME real no usado. | APROBADO (Bash) |
| R7.1 | 3.2, 6.1 | `test_export_filtered_content`: ruta y contenido imports temporal. | APROBADO (Bash) |
| R7.2 | 3.2, 6.1 | Snapshot canonical/adapters idéntico tras exportación. | APROBADO (Bash) |
| R7.3 | 3.2, 4.2, 6.2 | Ambos wrappers, error 7 propagado por Bash; PowerShell sin ejecución disponible. | PARCIAL |
| R8.1 | 2.2, 5.1, 6.1 | Sin nuevos cuerpos comunes; diferencias en adapter; snapshot de canonical. | APROBADO |
| R8.2 | 1.1, 5.1, 6.1 | validate temporal y hashes de 288 archivos sin cambios tras render. | APROBADO |
| R8.3 | 1.1, 4.1, 6.1 | Baseline verde y suite final verde; cinco distribuciones previas preservadas. | APROBADO (suite local) |
| R8.4 | 3.1, 4.1, 6.1 | Inventarios integrity/install y `test_installer_inventory`. | APROBADO |
| R8.5 | 4.2, 6.2 | Job Windows escrito; sin logs de ejecución real PowerShell/Windows. | PENDIENTE |
| R9.1 | 4.3, 6.1 | README, catálogo, instalación, arquitectura; enlaces 70 archivos. | APROBADO |
| R9.2 | 4.3, 4.4, 6.3 | Invocación documentada sin promesas no acreditadas; recarga/selección real aún pendientes. | PARCIAL |
| R9.3 | 4.3, 6.1 | Distinción 2.0/CLI/IDE y garantías explícitamente limitadas. | APROBADO |
| R9.4 | 4.3, 6.1 | Restauración skills y agents; fusión y ausencia de rollback documentados. | APROBADO |
| R10.1 | 4.4, 6.3 | No hay versión/build identificados mediante smoke. | PENDIENTE |
| R10.2 | 4.4, 6.3 | 8/10 archivos entregados, sin evidencia de descubrimiento por el host. | PENDIENTE |
| R10.3 | 4.4, 6.3 | Skill/recurso en disco, carga por agente no observada. | PENDIENTE |
| R10.4 | 4.4, 6.3 | Protocolo preparado, invocación padre/hijo no ejecutada. | PENDIENTE |
| R10.5 | 6.3 | Bloqueo registrado y sin anuncio de soporte completo. | APROBADO |

## 5. Spot-check de calidad y RNF del diseño

| RNF | Evidencia | Estado |
|---|---|---|
| Reproducibilidad | `validate.py` renderiza en temporal; 288 hashes iguales tras render final. | APROBADO |
| No regresión | Suite completa exit 0; 333 hashes de fuentes/artefactos previos preservados. | APROBADO local |
| Simulación sin escrituras | Tests de perfiles vacíos/poblados y exportación DryRun. | APROBADO Bash |
| Preservación del usuario | Inventario explícito, fusión sin delete, backup y fixtures de contenido propio. | APROBADO Bash |
| Evidencia multiplataforma | macOS real; workflow Linux/Windows preparado pero no ejecutado aquí. | PARCIAL |

Quality bar: separación canonical/adapters/generated/I/O mantenida, helpers
locales sin nuevas dependencias, errores visibles y códigos de salida. No existen
UI, BD, DI ni singletons de infraestructura nuevos a auditar. No se presentan
listas de tools ni restricciones de prompts como aislamiento técnico del host.

## 6. Bloqueos y límites residuales

1. **6.2 / Windows y Linux:** no hay resultados reales de esos OS asociados a esta
   distribución. macOS está aprobado. Escribir la CI no demuestra su ejecución.
   No se hizo push ni se dispararon workflows remotos; tampoco se instalaron tools.
2. **6.3 / Antigravity:** no se dispone de sesión/version/build ni evidencia de UI
   y tools del host. `agy` ausente del PATH no demuestra por sí mismo que el IDE
   no esté instalado; simplemente no hay acceso runtime verificable en esta sesión.
3. **Importador compartido:** precisión de segundos; dos exportaciones pueden
   colisionar y, con solo agentes, sobrescribirse. Límite previo documentado en
   `docs/instalacion.md`; no se modificó ese helper fuera del alcance acordado.
4. **Evidencia temporal:** logs completos locales; faltan referencias duraderas
   para ejecuciones remotas. No hay certificación de Python 3.10 solo por escribirlo
   en el workflow; la ejecución local fue Python 3.12.4.

## Gate 4 — pendiente con huecos

No cerrar la spec como verificada mientras falten R8.5 y R10.1–R10.4, además de
las aceptaciones parciales relacionadas. Próximas acciones verificables: aportar
ejecuciones Linux/Windows del harness y ejecutar el procedimiento de smoke en un
perfil Antigravity autorizado. Cualquier instalación en HOME real, commit/push
o cambio del alcance requerirá su propia autorización explícita.

## Preparación de publicación autorizada

El usuario confirmó publicar el alcance completo, incluidos cambios previos,
como `v0.4.0`, con push de rama/tag y GitHub Release que conserva los límites.
Esto no aprueba ni cierra el Gate 4.

La revisión del staging detectó una línea vacía final heredada en cinco
`canonical/skills/{architecture,code-quality,data-api,security,ui-design}/references/templates.md`.
Se eliminó únicamente esa línea en las fuentes y se regeneraron las seis
distribuciones; no se editaron los generados a mano ni cambiaron instrucciones.
El control histórico de 333 archivos idénticos corresponde al estado anterior
a esta normalización de formato explícitamente registrada.

Tras preparar `VERSION=0.4.0`, CHANGELOG y la normalización, los mismos **14
comandos volvieron a terminar con exit 0**, con los mismos recuentos de checks.
Los 288 archivos generados volvieron a ser idénticos antes/después del render.
Logs locales de esa ejecución:
`/var/folders/d7/z7388kp51w532q4c0rj7hqqh0000gn/T/opencode/antigravity-verification-20261006-112128/`.
Windows/Linux/runtime siguen pendientes hasta que se reciban sus resultados.
