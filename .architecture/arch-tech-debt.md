# Deuda técnica de arquitectura

Ordenada por severidad. Hallazgos basados en el código observado; este registro
no modifica los componentes de producción.

## 🔴 Crítica

Sin hallazgos confirmados en el alcance del bootstrap.

## 🟠 Alta

Sin hallazgos confirmados en el alcance del bootstrap.

## 🟡 Media

| # | Hallazgo | Ubicación (archivo:línea) | Impacto | Esfuerzo | Recomendación |
|---|---|---|---|---|---|
| ARQ-001 | El renderer elimina primero el árbol generado de cada plataforma y después lo reconstruye; una excepción puede dejar esa plataforma parcial y una mezcla de versiones entre plataformas. | [`tools/render.py:74-91`](../tools/render.py#L74-L91), [`tools/render.py:111-116`](../tools/render.py#L111-L116) | El siguiente validador detectará discrepancias, pero una salida parcial puede confundir operaciones posteriores o no instalar el contenido pretendido. | Medio | Definir el contrato ante fallo; renderizar en staging y publicar solo tras completar la generación, con limpieza/recuperación probadas. Mantener la validación antes de instalar. |

## 🟢 Baja

Sin hallazgos confirmados en el alcance del bootstrap.

## Seguimiento

`ARQ-001` es una oportunidad de robustez, no un cambio implementado en esta
documentación. La validación ya renderiza en un directorio temporal para comparar
la salida sin modificar `generated/` (`../tools/validate.py:200-216`); el riesgo
se refiere al render normal, que elimina cada destino antes de escribir
(`../tools/render.py:74-91`).

Si se decide implementar la remediación, se recomienda que el usuario continúe
con `@sdd` para definir el contrato ante interrupciones, el límite de publicación
(por plataforma o matriz completa) y sus criterios de verificación en el
renderer y las pruebas. La decisión de preservar la frontera entre canonical,
adapters y generated está registrada en
[`decisions/0001-fuente-canonica-y-adaptadores.md`](decisions/0001-fuente-canonica-y-adaptadores.md).
Esta recomendación no crea `.sdd/` ni modifica código.
