# Resultado de remediación — REC-04: retirar Scalar del flujo de APIs

## Identificación

- **Estado actual:** Cerrado sobre `main` HEAD `8fea7bb`. **Estado en la entrega original:** implementado y distribuido, aún sin commit/CI.
- **Sesión:** coordinadora e implementadora exclusiva en el worktree principal.
- **Fecha:** 2026-10-12.
- **Rama / baseline:** `main`, HEAD `43fd2dc` (`v1.3.0`) más cambios locales preexistentes de Developer y esta tanda. Staging vacío al iniciar.
- **Decisión aprobada:** eliminar la opción interactiva, no conservarla como opt-in.

## Cambio aplicado

- Eliminada la guía de Scalar y su referencia `canonical/skills/data-api/references/api-docs.md`.
- Conservados OpenAPI, JSON Schema y el catálogo de endpoints cuando no existe un contrato OpenAPI.
- Actualizado el catálogo del kit y el contrato de integridad para exigir ausencia de visor/lanzador en las seis plataformas.
- Regenerados los artefactos desde las fuentes canónicas. Los informes originales de auditoría y las entradas históricas del changelog no se reescriben.

## Verificación

| Comando | Resultado |
|---|---|
| `python3 -B tools/test_integrity.py` | 416/416; comprueba contrato OpenAPI/catálogo y ausencia de Scalar en fuentes y seis distribuciones. |
| `python3 -B tools/render.py` + `python3 -B tools/validate.py` | 11 skills, 5 agentes y 6 plataformas. |
| `python3 -B tools/check_links.py` | 90 archivos sin enlaces rotos. |
| `git diff --check` | Correcto. |

## Criterio y entrega

- No queda una instrucción operativa para crear el visor o el lanzador: **verificado en fuentes y artefactos generados**.
- OpenAPI/JSON Schema y catálogo de endpoints siguen siendo la documentación de contrato: **verificado**.
- En la entrega original no había commit ni CI remota; el estado propuesto era **Integrado pendiente de verificación**.

## Revalidación integrada — 2026-10-13

- **Baseline actual:** `main` HEAD `10373b3e9510cc71049eb37c5393b4e18415e40d` (`v3.2.0`).
- **Verificación focalizada local:** `python3 -B tools/test_integrity.py` 416/416; `python3 -B tools/check_links.py` 91 archivos; `git diff --check` correcto.
- **CI integrada actual:** [run 38352143368](https://github.com/furthurr/ai-agents-kit/actions/runs/38352143368), SUCCESS para el mismo HEAD; comprobó integridad, render, validate y artefactos generados.
- **Criterios:** no hay instrucciones operativas ni artefactos Scalar en las seis distribuciones; OpenAPI/JSON Schema y el catálogo de endpoints se conservan.
- **Cierre:** REC-04 **Cerrado**. Los informes y changelog históricos se conservan sin reescritura.
