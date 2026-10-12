# Verificación — Guía documental gestionada en AGENTS.md

- Modo SDD: lite
- Estado: implementación, distribución y contratos estáticos completados; smoke runtime no ejecutado

## Ciclo de pruebas

- Estrategia: TDD focalizado para el contrato estático de las instrucciones.
- Baseline previo: `python3 -B tools/test_documentation_core.py` pasó 12/12 antes de añadir los nuevos checks y antes de aparecer los cambios concurrentes observados.
- RED: los nuevos checks fallaron antes de los cambios canónicos, incluidos los contratos de guía y propiedad de Navigator. La ejecución completa también reflejó entonces cambios concurrentes en agentes; no se atribuyen esos fallos a esta feature.
- GREEN focalizado: los tres checks de guía, ownership Navigator y límites read-only pasaron 3/3.
- Checks finales: render/validate correctos; `tools/test_documentation_core.py` 15/15;
  `tools/test_sdd_contract.py` 613/613; `tools/test_mas_identity.py` 235/235;
  `tools/test_validate.py` 40/40; `tools/test_integrity.py` 415/415; enlaces en 85
  archivos y `git diff --check` limpio.
- Excepciones: no se ejecutó smoke con un host LLM ni se modificó un `AGENTS.md` consumidor. Los tests comprueban texto contractual; no prueban la obediencia runtime.

## Matriz de requisitos

| Requisito | Evidencia disponible | Estado |
|-----------|----------------------|--------|
| Req 1.1–1.9 | Contratos en `canonical/skills/documentation-orchestrator/{SKILL.md,references/workflows.md}` y checks focalizados de flujo, bloque gestionado, seguridad y modo read-only | 🟡 Contrato estático verificado; runtime pendiente |
| Req 1.10 | `canonical/skills/project-navigator/*`, `references/project-context.md` y test de delegación | 🟡 Contrato estático verificado; runtime pendiente |
| Distribución del contrato en seis plataformas | Render, validate, integridad, contrato de documentación y enlaces | ✅ Verificado estáticamente |

## Bloqueo y límites

La regeneración se ejecutó sobre el conjunto de fuentes actual solicitado por el usuario; las salidas se produjeron con el renderer y no se editaron manualmente.

El contrato estático de las seis plataformas está verificado. No se ejecutó un smoke LLM ni se afirma obediencia runtime; sus resultados requerirían evaluación por host aparte.
