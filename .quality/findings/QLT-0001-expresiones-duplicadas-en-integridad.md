# QLT-0001: Expresiones duplicadas en pruebas de integridad

- Estado: Pendiente
- Severidad: 🟢 Low
- Regla Sonar: `python:S1764` · Cualidad: Maintainability
- Ubicación: `tools/test_integrity.py:163, 167-170`
- Fecha detección: 2026-10-05
- Esfuerzo estimado: bajo (aprox. 10 minutos)

## Descripción

La condición de la línea 163 repite el mismo operando a ambos lados de `or`:
`"$RepoRoot" in content or "$RepoRoot" in content`. En las líneas 167-170
también se repiten las mismas expresiones `in content`; cambiar comillas simples
por dobles no cambia los valores de esas cadenas en Python.

Estas alternativas redundantes no comprueban casos adicionales y hacen menos
claro qué formas distintas de referencia pretende cubrir el test. Son un code
smell de mantenibilidad de bajo impacto, alineado con `python:S1764`.

## Plan de remediación (micro-pasos)

- [ ] Paso 1: eliminar las expresiones idénticas y conservar únicamente las
  comprobaciones que representen formas realmente distintas de la ruta.

## Bitácora

- 2026-10-05: hallazgo auditado en el snapshot local. No se modificó código.
