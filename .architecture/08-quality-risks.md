# 8. Atributos de calidad y riesgos

Esta vista recoge atributos y riesgos arquitectónicos observables en el código y
la documentación disponible. No es una auditoría de seguridad ni una ejecución
de pruebas.

## Atributos de calidad

| Atributo | Mecanismo observado | Evaluación arquitectónica |
|---|---|---|
| Consistencia de catálogo | Manifest común; validación de listas, adapters y huérfanos. | Fuerte dentro del pipeline local. |
| Reproducibilidad | Render a temporal y comparación de hashes contra `generated/`. | Verificable localmente; depende de ejecutar `validate.py`. |
| Portabilidad | Renderer Python y wrappers por host/OS; diferencias quedan en adapters. | Diseño multi-plataforma; la compatibilidad real requiere comprobar cada host. |
| Robustez de generación | El render normal reemplaza progresivamente cada subárbol de plataforma. | Existe riesgo de salida parcial ante fallo; véase `ARQ-001`. |
| Preservación de datos del usuario | Backups, dry-run, preflight y no borrar artefactos no declarados. | Reduce riesgo de sobrescritura; el preflight posterior informa si el destino queda incompleto. |
| Mantenibilidad | Fuente común y configuración declarativa con utilidades de validación. | Reduce duplicación de prompts, a costa de sostener manifest y adapters coherentes. |

## Riesgos registrados

| ID | Severidad | Riesgo | Mitigación actual | Seguimiento |
|---|---|---|---|---|
| ARQ-001 | Media | El renderer elimina el directorio generado de una plataforma antes de terminar de escribir su reemplazo; un fallo durante el render puede dejar salida parcial o una matriz de plataformas en estados distintos. | `validate.py` puede detectar falta de paridad después; el flujo normal debe validar antes de instalar. | Deuda registrada en [`arch-tech-debt.md`](arch-tech-debt.md). |

## Límites de evaluación

- `validate.py` prueba coherencia estructural y reproducibilidad del repo; no
  prueba el descubrimiento/ejecución en cada aplicación host
  (`../tools/validate.py:219-245`).
- La instalación modifica directorios externos al repo. Los preflight y backups
  son mitigaciones; esta documentación no ejecuta ni verifica instalaciones
  reales (`../docs/instalacion.md:112-139`).
- La aplicación de una solución a `ARQ-001` tendría que definir el comportamiento
  ante interrupción y comprobarlo en los entornos soportados. No se modifica
  código como parte de este bootstrap.
