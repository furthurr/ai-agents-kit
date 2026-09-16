# Selección de nivel de modelo

Contrato para recomendar solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres de
modelos, proveedores.

## Preflight

El preflight debe ser barato. Puede usar solicitud, steering y
marcadores compactos. No puede escribir, ejecutar tests, cargar referencias pesadas.

## Nivel por próxima operación

Recomienda capacidad para el **próximo proceso**, no para todo el flujo ni para un
gate. Requirements, Design, Implementación, Verification y Quick Plan usan `MEDIO`;
Tasks usa `BAJO`.

Eleva a `ALTO` por ambigüedad, arquitectura, migración, contrato público, seguridad,
concurrencia, integridad o compliance. `direct` trivial usa
`BAJO`; si no es elegible, evalúa `lite` y después `standard`. `standard` o `deep`
explícitos no se rebajan automáticamente.

## Determinar la próxima fase

- Spec nueva `standard` o `deep`: Requirements. Spec nueva `lite`: Quick Plan, sin
  pasos internos.
- Spec existente: usa `Modo SDD`, `Fase`, `Estado` y su gate para localizar la
  primera operación pendiente. No inferirá aprobación solo por la existencia del archivo.
- Spec legacy sin estado suficiente: pide aclaración y no migra.
- Después de Verification muestra únicamente Gate 4; no hay próxima fase.

## Gate 0 y transiciones

- `direct`: informa `Modelo recomendado: BAJO` y continua sin esperar.
- `lite`, `standard`, `deep` y bugfix no trivial: muestra la recomendación de la
  próxima operación y detiene el turno.
- En `standard` y `deep`, hay una sola recomendación visible por cada fase que vaya
  a iniciar. No repitas la misma recomendación dentro de una fase sin cambio.
- La transición presenta un resumen verificable, el gate actual y la recomendación
  de la próxima fase, condicionada a la aprobación de la fase actual. No crea gates.
- Inicia la siguiente fase solo con aprobación de la fase actual y confirmación del
  nivel recomendado o actual. Si falta una decisión, pide la parte faltante.
- Si el usuario itera, no inicia la siguiente fase ni aplica la recomendación pendiente.
- Si cambia alcance o riesgo, recalcula. En `lite` a `standard`, solicita confirmar
  el nuevo flujo aunque el nivel coincida. Para una fase confirmada, si cambia el
  alcance o riesgo, detente de nuevo solo si cambia el nivel o la política de gates.
- Nunca selecciones ni cambies el modelo del host ni afirmes conocer el activo.

Una transición puede responderse con `apruebo y usaré el nivel recomendado` o
`apruebo y continúo con el nivel actual`. Si responde únicamente `apruebo`,
`adelante` o `continúa`, pedirá la parte faltante.

## Salida

```text
Preflight SDD
Trabajo: <tipo> | Modo SDD: <direct|lite|standard|deep>
Alcance: <ruta/spec> | Complejidad: <baja|media|alta>
Próximo proceso: <fase u operación>
Modelo recomendado para <fase u operación>: <BAJO|MEDIO|ALTO>
Motivos: <1-3 razones verificables>
Antes de iniciar: responde "listo" para usar el nivel recomendado o
"continúa con el actual" para mantener tu nivel.
```
