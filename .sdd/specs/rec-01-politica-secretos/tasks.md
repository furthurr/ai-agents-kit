# Tasks — REC-01: política de secretos

- **Modo SDD:** standard.
- **Fase:** 3 — Tasks.
- **Estado:** tareas completadas y verificadas; cierre aprobado por el usuario mediante Gate 4.
- **Gates aprobados:** Gate 1 (Requirements) y Gate 2 (Design), mediante «procede» del usuario.
- **Gate aprobado:** Gate 3 — el usuario respondió «procede» a la solicitud de aprobar el plan e iniciar implementación.
- **Gate de cierre aprobado:** Gate 4 — respuesta explícita «Aprobar cierre REC-01» tras evidencia real de host y suites satisfactorias.
- **Requisitos:** [bugfix.md](bugfix.md).
- **Diseño aprobado:** [design.md](design.md).
- **Ejecución:** exclusivamente esta sesión en la carpeta original; sin escritores paralelos.

## Tareas secuenciales

- [x] **1. Revalidar baseline, exclusividad y archivos compartidos.**
  (Req I2, I4)
  Comprobar HEAD, estado, ausencia de cambios ajenos sobre fuentes previstas y
  procesos locales detectables; comprobar que REC-02/15 y FUT-17/18 continúan
  sin reserva solapada. Preservar los directorios previos sin seguimiento.
  Registrar el paso a En curso en la ficha y exclusivamente REC-01 del consolidado.
  Si aparece otra escritora o una reserva, detener las ediciones compartidas y coordinar.
  Evidencia: reejecución de status/HEAD y procesos locales; HEAD sin cambios,
  ningún cambio tracked ajeno ni otra escritora detectada; tableros sin reservas solapadas.

- [x] **2. Corregir la política y consumidores mediante regresión.**
  (Req R1–R7, R10, I1)
  Crear en `tools/test_secret_policy.py` una regresión de contrato que falle por
  la oferta actual de inclusión genérica, no por un error incidental. Registrar
  RED explícitamente como textual. Corregir `canonical/skills/git-commit/SKILL.md`,
  `canonical/skills/release-management/SKILL.md`,
  `canonical/agents/git-release-manager.md`,
  `canonical/skills/security/SKILL.md` y
  `docs/agentes/git-release-manager.md` según el diseño; conservar las
  autorizaciones independientes. GREEN y revisión de todas las opciones de
  interacción afectadas, sin convertirlo en prueba runtime.

- [x] **3. Implementar el control distribuible con TDD focalizado.**
  (Req R1–R4, R8–R10, I2)
  Añadir pruebas ejecutables en `tools/test_secret_policy.py`: RED de detección,
  sanitización y estados de salida; implementar el mínimo correcto en
  `canonical/skills/git-commit/scripts/check_secrets.py`; GREEN y REFACTOR
  solamente si elimina duplicación o separa I/O de detección.
  Cubrir firmas sintéticas de clave privada/tokens, nombre normal/sospechoso,
  configuración pública/placeholders, rutas con controles, fallos de lectura,
  rutas externas/enlaces y modos incompatibles. No añadir excepciones de inclusión.
  Construir los valores ficticios en memoria y verificar que no aparecen en
  stdout/stderr, incluso en fallos. No usar ni validar credenciales reales.

- [x] **4. Acreditar índice real e integrar entrada local/CI.**
  (Req R1–R3, R5, R8–R10, I1–I3)
  RED → GREEN de `--staged` y `--tracked` en repositorios temporales creados
  mediante `git init` y `git add`, nunca commit: secreto en índice con working
  tree saneado, caso inverso, archivos normales y errores de Git/conflicto.
  Verificar snapshots de archivos, índice y refs antes/después del control.
  Crear `tools/check_secrets.py` como wrapper sin reglas duplicadas; invocarlo
  en `.github/workflows/ci.yml` antes del render y ejecutar la suite de negativos.
  Probar el entrypoint que usa CI sobre un fixture tracked rechazado; distinguir
  esta ejecución local de una ejecución remota de GitHub Actions.

- [x] **5. Documentar uso, límites y deuda directamente vinculada.**
  (Req R6, R7, R10, I1, I4)
  Actualizar `docs/desarrollo.md` y exclusivamente los puntos pertinentes de
  P0.5 en `docs/mejoras.md`. Documentar cómo ejecutar el script distribuido en
  otro proyecto y el wrapper local, qué evalúan los modos, códigos 0/1/2,
  reglas soportadas, revisión contextual y ausencia de enforcement universal.
  Vincular REC-01 y no cerrar otros puntos de P0.5. Solo marcar completado lo
  acreditado, diferenciando disponibilidad del control de conducta en host.

- [x] **6. Regenerar y verificar el resultado integrado.**
  (Req R7–R10, I2, I3)
  Comprobar estado de `generated/` antes de renderizar y ejecutar
  `python3 tools/render.py`, `python3 tools/validate.py`,
  `python3 tools/check_links.py`, `python3 tools/test_secret_policy.py`,
  `python3 tools/test_validate.py`, `python3 tools/test_integrity.py`,
  `python3 tools/test_mas_identity.py`, `python3 tools/test_documentation_core.py`,
  `python3 tools/test_handoff_contract.py` y `python3 tools/test_links.py`.
  Añadir suites pertinentes si los archivos afectados lo requieren.
  Verificar el script copiado a las seis plataformas y ejecutarlo sobre fixtures;
  confirmar fuente única, sin editar `generated/` manualmente. Registrar fallos
  y su resolución. Ningún test crea commits ni instala globalmente.

- [x] **7. Verificar comportamiento en host o registrar bloqueo exacto.**
  (Req R1–R7, R10, I1, I2, I4)
  Preparar el escenario aprobado en un directorio/perfil temporal: cargar fuentes
  modificadas y solicitar explícitamente inclusión de una credencial sintética
  detectable, prohibiendo commit real. Incluir contrastes de configuración pública
  y placeholders. Comprobar respuesta, herramientas, candidatos/staging y ausencia
  de exposición; registrar host/versión, fuentes y resultados sanitizados.
  Si el entorno o su autorización impide ejecutarlo, conservar esta tarea pendiente
  con causa y siguiente acción; no sustituirla por tests textuales ni por scanner.
   No iniciar un segundo escritor en el repositorio original ni modificar configuración global.
   Evidencia final: prueba OpenCode 1.18.34 con modelo real, skill/scanner locales
   identificados por hashes; scanner salida 1 para firma sintética y 0 para configuración
   pública/placeholder; respuesta rechaza excepción de autorización; valor ausente
   de todos los eventos; fixtures/índice/refs sin cambios. [Reporte sanitizado](../../../docs/auditoria/seguimiento/REC-01-live.json), revisado por la coordinadora.

- [x] **8. Registrar Verification y entregar estado acreditado.**
  (Req R1–R10, I1–I4)
  Continuar sin gate intermedio después de implementación con `verification.md`:
  RED/baseline, GREEN, suites, matriz requisito/tarea/test/evidencia, excepciones y
  self-check de los cinco RNF de Design. Auditar cada tarea completada contra
  artefactos y resultados reales. Completar
  `docs/auditoria/seguimiento/REC-01.md` y actualizar solo REC-01/historial del
  consolidado. Si falta evidencia, proponer Integrado pendiente de verificación
  o Bloqueado según la causa; no declarar Cerrado. Si todo está acreditado,
  presentar Gate 4 para el cierre de la spec. Entregar cambios sin commit.

## Dependencias y waves

No hay tareas `[P]`: se ejecutan secuencialmente por la única escritora.

```mermaid
flowchart LR
    W1[1 Baseline y reserva] --> W2[2 Política y regresión]
    W2 --> W3[3 Control y negativos]
    W3 --> W4[4 Índice e integración CI]
    W4 --> W5[5 Documentación y deuda]
    W5 --> W6[6 Render y suites]
    W6 --> W7[7 Evidencia host o bloqueo]
    W7 --> W8[8 Verification y entrega]
```

## Cobertura y reglas de progreso

Evidencia de tareas 2–6 y 8: [verification.md](verification.md), suite
`tools/test_secret_policy.py` (26 tests), artefactos canónicos/wrapper/CI/docs,
render/validate y resultados de suites registrados. Tarea 7 completada mediante
`tools/test_secret_policy_host.py --live`: los dos intentos iniciales sin proveedor
se conservan como bloqueos históricos; no se cuentan como PASS. El reporte real
final acredita ejecución y respuesta, con revisión explícita y Gate 4 aprobado.
La evidencia RED de tarea 4 no se observó separadamente; se registra como
cobertura de integración, no TDD por cada seam (excepción en Verification).

| Requisitos | Tareas |
|---|---|
| R1–R3 | 2, 3, 4, 7, 8 |
| R4 | 2, 3, 7, 8 |
| R5 | 2, 4, 7, 8 |
| R6 | 2, 5, 7, 8 |
| R7 | 2, 5, 6, 7, 8 |
| R8–R9 | 3, 4, 6, 8 |
| R10 | 2–8 |
| I1 | 2, 4, 5, 7, 8 |
| I2 | 1, 3, 4, 6, 7, 8 |
| I3 | 4, 6, 8 |
| I4 | 1, 5, 7, 8 |

- `[x]` solo con artefacto o resultado real acreditado; no se marcan tareas por intención.
- Si no se observa RED conductual, registrar el límite; un RED textual es solo contractual.
- PBT omitido: sin propiedad algebraica relevante; no añadir dependencias de pruebas.
- Los permisos, selección de agentes, clasificación de commits y análisis SemVer
  de otros hallazgos quedan fuera del alcance.
- No commit, push, tag, release ni instalaciones globales sin autorización independiente.
