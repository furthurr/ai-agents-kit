# Verificación — orquestacion-handoff-canonical

Fecha: 2026-09-03
Modo: `standard`
Estado: **implementación validada estáticamente; smoke multiplataforma pendiente**

## Ciclo de pruebas final

- `python3 tools/render.py` → OK
- `python3 tools/validate.py` → 10 skills, 9 agentes, 3 plataformas
- `python3 tools/test_handoff_contract.py` → **24 tests semánticos OK**
- `python3 tools/test_sdd_contract.py` → **46/46**
- `python3 tools/test_validate.py` → **14/14**
- `python3 tools/check_links.py` → 60 archivos correctos
- `python3 tools/test_links.py` → **4/4**
- `python3 tools/test_integrity.py` → **252/252**
- `python3 tools/test_install.py` → **72/72**
- `python3 -m py_compile tools/handoff_contract.py tools/test_handoff_contract.py` → OK
- `git diff --check` → OK

## Evidencia por requisito

| Requisito | Evidencia | Estado |
|-----------|-----------|--------|
| H1 continuidad sin duplicación | una sola vía por acción + `handoff_id` + resultado correlacionado | ✅ estático |
| H2 contrato inequívoco | productor, seis receptores y formato de respuesta | ✅ estático |
| H3 bajo demanda | contrato completo en `references/handoff.md` | ✅ |
| H4 límites y rutas | parser estricto, truth table, target→scope, symlinks, rutas Windows/absolutas/`..` | ✅ ejecutable |
| H5 coste medido | delta final documentado | ✅ |
| H6 validación | parser/validador + 24 tests positivos y negativos | ✅ ejecutable |

## Cobertura semántica del contrato

- Ambos ejemplos canónicos (emisión y resultado).
- Todos los targets y acciones.
- Omisión de campos, duplicados, campos extra y texto libre.
- Tipos inesperados sin excepciones.
- Confirmación lectura/escritura.
- Rutas inexistentes, absolutas, Windows, `..`, fragmentos y symlinks.
- Bootstrap con carpeta ausente y rechazo de symlink existente.
- Evidencia como archivo dentro del scope y relativa al `project_root`.
- Resultado correlacionado, `delivered`/`blocked` y campos desconocidos.
- Presencia del protocolo receptor en seis agentes.

## RNF

| RNF | Evidencia | Estado |
|-----|-----------|--------|
| Coste | +345 palabras fijas; +728 bajo demanda | ✅ medido |
| Portabilidad de distribución | canonical renderizado en tres plataformas | ✅ |
| Seguridad lógica | validación semántica ejecutable; `write_scope` no se presenta como sandbox | ✅ con límite declarado |
| No duplicación | skill/agente/contrato: ejecutar o derivar, nunca ambas | ✅ estático |
| Trazabilidad | `handoff_id`, `project_root`, status y evidencia acotada | ✅ ejecutable |

## Delta de contexto

| Medida | Antes (HEAD) | Después | Delta |
|--------|--------------|---------|-------|
| Agentes | 1.417 | 1.650 | **+233 palabras** |
| Skills | 13.756 | 13.868 | **+112 palabras** |
| Referencias bajo demanda | 9.038 | 9.780 | **+742 palabras** |

Coste fijo total: **+345 palabras**; coste bajo demanda: **+742 palabras**. El aumento frente al diseño inicial se debe
al protocolo receptor en seis agentes y a eliminar ambigüedades de seguridad. El
contrato detallado sigue bajo demanda. No se afirma ahorro neto hasta medir tareas.

## Limitaciones honestas

1. El validador ejecutable protege CI/herramientas; los hosts no lo invocan
   automáticamente durante una conversación. La recepción runtime sigue guiada
   por prompt y permisos del host.
2. `write_scope` es límite lógico, no sandbox técnico.
3. El smoke productor–receptor está documentado pero no ejecutado en
   Copilot/OpenCode/Kiro; no se declara todavía portabilidad conductual.
4. El working tree debe versionarse atómicamente para obtener baseline Git.
