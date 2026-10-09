# Evidencia de implementación — Compactación del contexto SDD

- **Modo SDD:** standard
- **Fase:** Implementación
- **Estado:** compactación implementada; Verification requiere reanudación
- **Gate 1 de iteración:** aprobado
- **Gate 2 de iteración:** aprobado
- **Gate 3 de iteración:** aprobado por el usuario («procede»)
- **Gate 4:** pendiente

## RED/GREEN de la iteración

La implementación inicial conserva su evidencia en `implementation-evidence-inicial.md`;
sus RED/GREEN no se atribuyen a esta compactación.

| Fase | Comando/acción | Evidencia observada |
|---|---|---|
| RED nuevo | Actualizar contrato de `tools/test_sdd_contract.py` para fuente compacta, respaldo opcional y budgets; ejecutar contra la versión extensa. | `python3 -B tools/test_sdd_contract.py` → exit 1; **457/482** checks correctos. Fallaron controles de compactación, respaldo y límites de contexto esperados antes de reducir fuentes. |
| Compactación | Editar canonical, crear documentación opcional y adaptar docs activos/tests. | Agente/skill delegan la escala; el núcleo conserva perfiles y criterios. No se exige cargar el respaldo para puntuar. |
| Render | `python3 -B tools/render.py` | Exit 0; seis hosts regenerados mediante el renderer, nunca editados a mano. |
| GREEN inicial | `python3 -B tools/test_sdd_contract.py` | Exit 0; **482/482** comprobaciones tras render. |
| GREEN | `python3 -B tools/test_model_recommendations.py` | Exit 0; **5/5** tests. Exclusividad/gates y ningún consumidor obliga a cargar ejemplos opcionales. |
| Higiene | `git diff --check` | Exit 0; sin errores de whitespace en el diff versionado comprobado. |

No se atribuyen estos checks textuales a una evaluación de host o a una garantía
de razonamiento real del LLM. La suite completa de validación/enlaces/integridad
se reservó para Verification.

Verification añadió un check semántico para representación numérica/indicador 10+.
Su primera ejecución detectó un literal de prueba demasiado estricto (482/483);
se ajustó al contrato semántico, no cambió el producto, y la suite final pasó
483/483. Ver `verification.md`.

## Medición antes/después

Baseline de Requirements, previo a compactar. Medición repetida con el mismo método:
Python `len(text.split())` para palabras y `len(text)` para caracteres Unicode.
Son conteos del texto, **no tokens ni costo facturado**.

| Fuente operativa | Antes: palabras/caracteres | Ahora: palabras/caracteres | Cambio |
|---|---:|---:|---:|
| `canonical/agents/sdd.md` | 1.066 / 7.580 | 975 / 6.957 | −91 / −623 |
| `canonical/skills/sdd-spec/SKILL.md` | 2.357 / 16.378 | 2.216 / 15.394 | −141 / −984 |
| `canonical/skills/sdd-spec/references/feature-level.md` | 1.774 / 12.303 | 662 / 4.610 | −1.112 / −7.693 |
| `canonical/skills/sdd-spec/references/templates.md` | 863 / 5.722 | 863 / 5.722 | 0 / 0 |

| Escenario de consumo | Antes | Ahora | Ahorro |
|---|---:|---:|---:|
| Agente + skill (inicio) | 3.423 palabras / 23.958 caracteres | 3.191 / 22.351 | **232 / 1.607 (6,8 % / 6,7 %)** |
| Agente + skill + rúbrica (scoring) | 5.197 / 36.261 | 3.853 / 26.961 | **1.344 / 9.300 (25,9 % / 25,6 %)** |
| Anterior + plantillas | 6.060 / 41.983 | 4.716 / 32.683 | **1.344 / 9.300 (22,2 % / 22,2 %)** |

El respaldo opcional `docs/sdd-effort-examples.md` tiene **550 palabras / 3.797
caracteres**, fuera de los escenarios obligatorios y no enlazado desde agente,
skill, plantillas o rúbrica operativa. Los diez descriptores, dimensiones, anclas,
10+, formato, independencia de lite y matiz de X13 se conservan en la referencia;
salidas enumeradas y procedencia extensa quedan en el respaldo.

No hay tokenizer específico disponible (`tiktoken` no está instalado); no se infieren
tokens efectivos del cociente de caracteres ni facturación. Tampoco hay
instrumentación de carga real por host.

## Archivos por responsabilidad

| Cambio | Artefactos/evidencia |
|---|---|
| C1.1, C1.2, C3.1 | `tools/test_sdd_contract.py`: anclas y perfiles en canonical, reglas por rango, tres contrastes, mutaciones semánticas, respaldo opcional y budgets. |
| C2.1 | `canonical/agents/sdd.md`: delegación breve y etiqueta de salida. |
| C2.2 | `canonical/skills/sdd-spec/SKILL.md`, `references/feature-level.md`: momento de emisión y rúbrica compactados. |
| C2.3 | `docs/sdd-effort-examples.md`: salidas, contrastes y procedencia, claramente opcionales. |
| C3.2 | `docs/catalogo.md`, `docs/uso.md`, `docs/agentes/sdd.md`, `docs/agentes/README.md`, `docs/sdd-smoke.md`, `docs/model-recommendations-smoke.md`. |
| Exclusividad | `tools/test_model_recommendations.py`: cinco tests; confirma consumidor SDD y ausencia de referencias obligatorias al respaldo. |
| C4.1 | `generated/`: renderer; `git diff --name-only -- generated/` mostró 24 archivos, cuatro artefactos SDD por cada plataforma. |
| C4.2 | Ambos comandos GREEN arriba y mediciones en este registro. |

## Preservación y límites

Se preservaron cambios ajenos en `.security/`, `.sdd/specs/laboratorio-evaluacion-sdd/`,
`.opencode/commands/lab-pilot.md` y specs/fixtures locales del laboratorio. `.agent-lab`
y su evidencia no se modificaron; tampoco `.gitignore`, adapters, manifest, renderer,
instaladores, CI ni configuración global. La evidencia de la primera iteración sigue
identificada como `*-inicial.*`, no como prueba de este cambio.

Los casos de host siguen pendientes. No se instalaron consumidores, llamaron modelos
ni ejecutó Docker. La configuración OpenCode cargada no se cambió; una instalación
futura de estos artefactos requiere reiniciar el host para que los recargue.
