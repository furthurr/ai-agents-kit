# Verification: soporte de Pi Agent

- **Modo SDD:** standard
- **Fase:** Verification
- **Estado:** verificado parcialmente — pendiente de decisión de Gate 4
- **Gate pendiente:** Gate 4 — ¿cerrar con la limitación registrada o completar el smoke funcional?

## Resultado

La salida canónica, validación, instaladores Bash y pruebas automáticas pasan.
El instalador se probó en un `PI_CODING_AGENT_DIR` temporal y dejó 10 skills y
9 prompt templates; `--dry-run` no escribió en el destino. La prueba directa de
invocación de Pi no pudo confirmar la respuesta del modelo: la llamada terminó
con HTTP 429 (`RESOURCE_EXHAUSTED`, límite mensual del proveedor) antes de
devolver salida. No se instaló nada en el `~/.pi/agent` real.

## Matriz requisito → evidencia

| Req | Resultado | Evidencia |
|-----|-----------|-----------|
| R1 | OK | `canonical/manifest.json`; `generated/pi/`; `python3 tools/validate.py` reporta 10 skills, 9 agentes y 5 plataformas |
| R2 | OK | `generated/pi/skills/*/SKILL.md` y referencias copiadas; `tools/test_mas_identity.py` comprueba las 10 skills Pi |
| R3 | Parcial | `generated/pi/agents/*.md` (9 templates y `$ARGUMENTS`); `python3 tools/test_sdd_contract.py` verifica la descripción del agente SDD. La expansión real del argumento en conversación está pendiente por el 429 |
| R4 | OK | `scripts/install/pi.sh`, `scripts/install/pi.ps1`; instalación temporal con `PI_CODING_AGENT_DIR=<temp>/agent` y preflight posterior: 10 + 9 |
| R5 | OK | `python3 tools/test_install.py` (124/124; cubre dry-run, idempotencia, backup y restauración en HOME temporal); smoke de `pi.sh --dry-run` no creó el destino |
| R6 | Parcial | `scripts/backup/pi.sh`, `scripts/backup/pi.ps1`; `scripts/backup/pi.sh --dry-run` lista los artefactos declarados desde una instalación temporal sin crear import. PowerShell no está disponible para ejecución en este entorno |
| R7 | OK | `docs/instalacion.md` documenta que son templates en una sesión compartida, sin subagentes aislados ni permisos por rol |
| R8 | Parcial | `python3 tools/render.py`, `python3 tools/validate.py`; tests abajo. La CLI Pi inicia la petición pero el proveedor devuelve 429, así que no se confirma el uso funcional end-to-end |
| R9 | OK | `README.md`, `docs/catalogo.md`, `docs/instalacion.md`, `docs/desarrollo.md`; `python3 tools/check_links.py` revisa 70 archivos |

## Suite ejecutada

| Comando | Resultado |
|---------|-----------|
| `python3 tools/render.py && python3 tools/validate.py` | OK — 10 skills, 9 agentes, 5 plataformas |
| `python3 tools/check_links.py` | OK — 70 archivos |
| `python3 tools/test_integrity.py` | OK — 406/406 |
| `python3 tools/test_install.py` | OK — 124/124; incluye Pi y destinos aislados |
| `python3 tools/test_validate.py` | OK — 16/16, incluido `$ARGUMENTS` obligatorio |
| `python3 tools/test_sdd_contract.py` | OK — 211/211 tras corregir descripción Pi para mencionar Quick Plan |
| `python3 tools/test_mas_identity.py` | OK — 235/235 |
| `python3 tools/test_model_recommendations.py` | OK — 141/141 |
| `python3 tools/test_handoff_contract.py` | OK — 24/24 |
| `python3 tools/test_links.py` | OK — 4/4 |
| `bash -n scripts/install/pi.sh scripts/backup/pi.sh` | OK |
| `python3 -m py_compile tools/render.py tools/validate.py tools/test_validate.py` | OK |

## Smoke de instalación aislado

- `scripts/install/pi.sh --dry-run` devolvió 0 y dejó inexistente el directorio destino.
- `scripts/install/pi.sh` con `PI_CODING_AGENT_DIR` temporal devolvió 0; el
  preflight confirmó 10 skills y 9 agentes/plantillas.
- Comprobación del contenido temporal: cada template contiene `$ARGUMENTS` y
  cada skill instalada tiene `SKILL.md`.
- `scripts/backup/pi.sh --dry-run` devolvió 0 y listó las 10 skills y 9 templates
  sin crear `imports/`.
- El smoke `pi --no-tools --offline --print '/sdd test probe'` llegó a una
  respuesta HTTP 429 del proveedor y no produjo respuesta funcional; no se
  interpreta como verificación de expansión del template.
- No hay `pwsh` disponible, por lo que instalador/backup PowerShell solo están
  cubiertos por inspección contractual estática en `test_install.py`.

## Self-check de RNF

1. **Reproducibilidad:** render + validate pasaron después del ajuste final de la descripción SDD.
2. **Seguridad de instalación:** dry-run no escribió y los tests comprueban backups, idempotencia y que no se borren recursos ajenos.
3. **Portabilidad/compatibilidad:** destinos Pi usan `PI_CODING_AGENT_DIR` y defaults documentados; smoke temporal confirma paths y cantidades.
4. **Integridad de prompts:** todos los nueve templates contienen `$ARGUMENTS`; validator rechaza sufijos Pi inválidos.
5. **Permisos/aislamiento:** documentación limita explícitamente que un template no es subagente ni política de permisos. No se reclama aislamiento de Pi.

## Excepciones y decisión pendiente

- La prueba funcional end-to-end de `/sdd` y `/skill:project-navigator` queda
  pendiente: el proveedor configurado rechazó la llamada por cuota mensual
  (`HTTP 429`). Puede repetirse con un proveedor que responda.
- El runtime PowerShell no se probó porque `pwsh` no está instalado; Bash sí pasó
  syntax y tests de instalación.
- Los artefactos de implementación no se describen como TDD: el renderer y
  validación recibieron cobertura retroactiva durante la integración.

**Gate 4:** decidir entre cerrar con estas limitaciones documentadas o completar
primero el smoke funcional con un proveedor disponible y la ejecución de
PowerShell en CI/Windows.
