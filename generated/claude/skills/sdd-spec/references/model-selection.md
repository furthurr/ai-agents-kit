# Selección de nivel de LLM

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones modelos ni proveedores.

## Preflight

El preflight debe ser barato: solicitud y marcadores compactos.
No puede escribir, ejecutar tests, cargar referencias pesadas.

## Nivel por próxima operación

Recomienda para el **próximo proceso**, no para un gate ni todo el flujo.
Requirements, Design, Implementación, Verification y Quick Plan usan `MEDIO`;
Tasks usa `BAJO`.

Eleva a `ALTO` por ambigüedad, arquitectura, migración, contrato público,
seguridad, concurrencia, integridad o compliance. `direct` usa `BAJO`;
si no aplica, evalúa `lite` y luego `standard`. No rebajes modos explícitos.

## Determinar la próxima fase

- Spec nueva `standard` o `deep`: Requirements; `lite`: Quick Plan.
- Spec existente: usa `Modo SDD`, `Fase`, `Estado` y su gate para localizar la
  primera operación pendiente. No inferirá aprobación solo por la existencia del archivo.
- Spec legacy ambigua: pide aclaración y no migra.
- Después de Verification muestra únicamente Gate 4; no hay próxima fase.

## Recomendación informativa y transiciones

- `direct`: informa `Nivel de LLM recomendado: BAJO` y continúa sin esperar.
- `lite`, `standard`, `deep` y bugfix no trivial: muestra el nivel recomendado para
  la próxima operación y termina el turno antes de iniciarla. Permite cambiar
  manualmente de modelo o continuar con el actual. Reanuda cuando el usuario
  indique continuar, sin confirmar el modelo elegido ni repetir el aviso.
- En `standard` y `deep`, una sola recomendación visible por fase; no repitas
  la misma recomendación sin cambios.
- La transición presenta resumen verificable, gate actual y recomendación de la
  próxima fase condicionada a la aprobación actual. No crea gates.
- Espera únicamente la aprobación del gate real de la fase actual. Tras aprobarlo,
  inicia la fase siguiente. No preguntes si el usuario seleccionó o cambiará el LLM.
  Si el usuario itera, no avances y descarta la recomendación condicionada.
- Después de Implementación no hay gate adicional: presenta el preflight de
  Verification y termina el turno. Cuando el usuario reanuda, inicia Verification
  sin pedir confirmación del nivel.
- Si cambia alcance o riesgo, recalcula y comunica el nivel actualizado antes de
  ejecutar la operación; si cambia la recomendación sin gate intermedio, termina el
  turno para permitir el cambio manual. En una reclasificación de `lite` a
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
Puedes cambiar manualmente de modelo o seguir con el actual; indica «continúa» para reanudar.
```

Omite la última línea en `direct`. No solicites confirmar el modelo.
