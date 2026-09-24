# Selección de nivel de LLM

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones modelos ni proveedores ni
afirmes conocer el nivel activo del host.

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

## Recomendación informativa y transiciones

- `direct`: informa `Nivel de LLM recomendado: BAJO` y continúa sin esperar.
- `lite`, `standard`, `deep` y bugfix no trivial: muestra el nivel recomendado para
  la próxima operación y continúa sin detenerse por la recomendación.
- En `standard` y `deep`, hay una sola recomendación visible por cada fase que vaya
  a iniciar. No repitas la misma recomendación dentro de una fase sin cambio.
- La transición presenta un resumen verificable, el gate actual y la recomendación
  de la próxima fase, condicionada a la aprobación de la fase actual. No crea gates.
- Espera únicamente la aprobación del gate real de la fase actual. Tras aprobarlo,
  inicia la fase siguiente. No preguntes si el usuario seleccionó o cambiará el LLM.
  Si el usuario itera, no avances y descarta la recomendación condicionada.
- Después de Implementación no hay gate adicional: presenta el preflight de
  Verification y continúa con ella sin esperar confirmación del nivel.
- Si cambia alcance o riesgo, recalcula y comunica el nivel actualizado sin detenerte
  a pedir una decisión sobre el nivel de LLM. En una reclasificación de `lite` a
  `standard`, espera aprobación solo para el cambio de flujo SDD.
- Nunca selecciones ni cambies el modelo del host.

## Salida

```text
Preflight SDD
Trabajo: <tipo> | Modo SDD: <direct|lite|standard|deep>
Alcance: <ruta/spec> | Complejidad: <baja|media|alta>
Próximo proceso: <fase u operación>
Nivel de LLM recomendado para <fase u operación>: <BAJO|MEDIO|ALTO>
Motivos: <1-3 razones verificables>
```

Esta recomendación es informativa: no solicites confirmación ni detengas el proceso
por la elección del nivel. Espera solo las aprobaciones de gates SDD reales.
