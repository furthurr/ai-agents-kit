# Validación runtime complementaria — REC-02

- **Estado:** Pendiente; no bloquea hallazgos independientes.
- **Hallazgo base:** [REC-02](REC-02.md), cerrado respecto de su remediación y criterios originales.
- **Motivo:** completar evidencia conductual en superficies que no pudieron ejecutarse durante la remediación. Este seguimiento no reabre REC-02 salvo que revele un defecto nuevo.
- **Baseline:** `main` `5dba87197a64fcc9e026a344236d5da02793b4cf`; fix `9e0696e131dd7f105b450cd1bb108acd3ac816b2`.
- **Evidencia disponible:** [OpenCode live](REC-02-live.json), [ficha base](REC-02.md), [matriz de host](../../permisos-hosts.md), CI integrada.

## Pendientes concretos

| ID | Superficie / escenario | Estado | Condición para retomarlo |
|---|---|---|---|
| VR-01 | Kiro IDE/CLI compatible con V3: `fs_write`, shell y precedencia | Pendiente | Entorno V3 disponible. CLI local 2.29.1 no valida reglas V3. |
| VR-02 | Claude Code: herramientas, permisos heredados y autorización por operación | Pendiente | CLI/sesión de prueba instalada y fuente distribuida identificada. |
| VR-03 | Copilot IDE/CLI/cloud: herramientas efectivas y confirmaciones | Pendiente | Superficie autenticada disponible para pruebas inocuas. |
| VR-04 | Antigravity IDE: scopes y aprobaciones heredados | Pendiente | Controlador GUI o harness oficial reproducible disponible; la app instalada no acredita carga del adaptador. |
| VR-05 | OpenCode: respuesta final tras denegar escritura y delegación | Parcial | Repetir con harness que espere estado terminal; distinguir respuesta del modelo y del harness. |
| VR-06 | Instrucción embebida en página web | Pendiente | Fuente web controlada, sin ejecutar instrucciones externas. |

## Resultados ya acreditados

- OpenCode 1.18.34 con modelo real: `inspect` sin escritura e instrucción embebida en workspace ignorada; escritura fuera de alcance rechazada; edición documental con autorización humana; remediación puntual de Code Review ejecutada en fixture.
- OpenCode engine con proveedor simulado: solicitudes y efectos del motor comprobados; no son evidencia de decisión LLM ni de consentimiento humano.
- Pi 0.99.2: plantilla distribuida permite escritura con herramientas por defecto; `--tools read` excluye write. Es una limitación documentada, no equivalencia con OpenCode.
- Kiro CLI 2.29.1: comprobación de formato V3 bloqueada/incompatible; no cuenta como prueba runtime.

## Registro

| Fecha | ID | Resultado | Evidencia | Siguiente paso |
|---|---|---|---|---|
| 2026-10-11 | VR-01 a VR-06 | Inicialización | Matriz anterior y [ficha REC-02](REC-02.md) | Ejecutar cuando el host esté disponible; no bloquear REC-03 ni otros trabajos. |
