# Seleccion de nivel de modelo

Contrato breve para recomendar solo `BAJO`, `MEDIO` o `ALTO`. No menciones nombres
de modelos, proveedores ni equivalencias comerciales.

## Preflight

Debe ser barato y de solo lectura. Puede usar la solicitud, steering minimo,
marcadores de la spec, nombres, metadatos e indices compactos. No puede escribir,
ejecutar tests, cargar referencias pesadas, leer todo el repositorio ni resolver la
peticion antes de confirmar. Si falta un dato esencial, haz una sola pregunta breve.

## Nivel inicial

| Trabajo | Nivel |
| --- | --- |
| `direct` trivial, localizado y reversible | `BAJO` |
| Quick Plan claro, feature `standard` localizada o bugfix reproducible | `MEDIO` |
| Exploracion puntual o continuacion de una spec aprobada | `BAJO`/`MEDIO` |
| `deep`, migracion, contrato publico o cruce de capas | `ALTO` |
| Seguridad, concurrencia, integridad critica, compliance o arquitectura ambigua | `ALTO` |

Si `direct` no cumple todos sus limites, usa `standard` y al menos `MEDIO`. Solo
eleva por factores dentro del alcance.

## Perfil por fase

Muestra solo fases pendientes; es orientativo y no crea gates nuevos:

| Fase | Base | Subir a `ALTO` por |
| --- | --- | --- |
| Requirements | `MEDIO` | ambiguedad, actores multiples o compliance |
| Design | `MEDIO` | arquitectura, migracion, contrato o riesgo critico |
| Tasks | `BAJO` | dependencias o paralelizacion complejas |
| Implementacion | `MEDIO` | seguridad, concurrencia, integridad o migracion |
| Verification | `MEDIO` | integracion, regresion, evidencia o compliance |

## Gate 0

- `direct`: informa `Modelo recomendado: BAJO` y continua sin esperar.
- Quick Plan, `standard`, `deep` y bugfix no trivial: muestra la salida y detiene
  el turno. Continua con `listo`, `continua`, `procede`, `ya seleccione el modelo` o
  `continua con el actual`.
- La confirmacion vale para las fases pendientes. No repitas el gate por fase.
- Si cambia el alcance o el riesgo, recalcula; detente de nuevo solo si cambia el
  nivel global.
- Nunca selecciones ni cambies el modelo del host ni afirmes conocer el activo.

## Salida

```text
Preflight SDD
Trabajo: <tipo> | Alcance: <ruta/spec> | Complejidad: <baja|media|alta>
Modelo recomendado: <BAJO|MEDIO|ALTO>
Fases pendientes: <fase:nivel, ...>
Motivos: <1-3 razones verificables>
Antes de continuar: cambia al nivel y responde "listo", o responde "continua con el actual".
```

En `direct`, omite fases, motivos y confirmacion; usa dos o tres lineas.
