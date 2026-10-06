# Selección de nivel de LLM

Recomienda solo `BAJO`, `MEDIO` o `ALTO`. No menciones modelos ni proveedores.

## Preflight

El preflight debe ser barato: solicitud y marcadores compactos.
No puede escribir, ejecutar tests, cargar referencias pesadas.

## Nivel por próxima operación

Recomienda para el **próximo proceso**, no todo el flujo.
Requirements, Design, Implementación, Verification y Quick Plan usan `MEDIO`;
Tasks usa `BAJO`.

Eleva a `ALTO` por ambigüedad, arquitectura, migración, contrato público,
seguridad, concurrencia, integridad o compliance. `direct` usa `BAJO`;
si no aplica, evalúa `lite` y luego `standard`. No rebajes modos explícitos.

## Determinar la próxima fase

- Spec nueva `standard`: Requirements; `lite`: Quick Plan.
- Spec existente: usa `Modo SDD`, `Fase`, `Estado` y gate.
  No inferirá aprobación solo por la existencia del archivo.
- Spec legacy ambigua: pide aclaración y no migra.
- Después de Verification muestra únicamente Gate 4; no hay próxima fase.

## Recomendación informativa y transiciones

- `direct`: informa `Nivel de LLM recomendado: BAJO` y continúa sin esperar.
- `lite`, `standard` y bugfix no trivial: avisa y continúa en el mismo turno,
  salvo aclaración esencial o gate real pendiente.
- En `standard`, una sola recomendación visible por fase; no repitas la misma
  recomendación ya comunicada para el mismo alcance, sin exigir confirmación.
- La transición presenta resumen verificable, gate actual y recomendación de la
  próxima fase condicionada a la aprobación actual. No crea gates.
- Espera únicamente la aprobación del gate real de la fase actual. Tras aprobarlo,
  continúa sin pausa. No preguntes si el usuario seleccionó o cambiará el LLM.
  Si itera, no avances y descarta la recomendación condicionada.
- Después de Implementación no hay gate adicional: presenta el preflight de
  Verification y continúa con Verification sin pausa; evidencia antes de Gate 4.
- Si cambia alcance o riesgo, recalcula y comunica el nivel actualizado antes de
  ejecutar la operación sin esperar por un cambio exclusivo de nivel. Si falta
  autorización de alcance, pregunta. En una reclasificación de `lite` a
  `standard`, espera aprobación del cambio de flujo aunque el nivel no cambie.
- Nunca selecciones ni cambies el modelo del host.

## Salida

```text
Preflight SDD
Trabajo: <tipo> | Modo SDD: <direct|lite|standard>
Alcance: <ruta/spec> | Complejidad: <baja|media|alta>
Próximo proceso: <fase u operación>
Nivel de LLM recomendado para <fase u operación>: <BAJO|MEDIO|ALTO>
Motivos: <1-3 razones verificables>
Puedes cambiar manualmente de modelo; continúo el trabajo autorizado en el mismo turno.
```

Gate 0 es preflight técnico, no humano. No exijas «continúa», «listo» ni confirmar
el modelo. Solo planificación no autoriza implementar.
