# Paquete de conservación para otra sesión

Entrada funcional: [CONTINUAR-AQUI.md](../CONTINUAR-AQUI.md). Este paquete solo
preserva datos; no representa otra ejecución, validación del modelo o cambio de
decisión experimental. Los originales y sus JSON/congelaciones no se reescribieron.

## Qué se guardó

Se recuperaron **798 archivos internos en siete ZIP**, 3.844.181 bytes comprimidos
(aproximadamente 3,84 MB), más una copia exacta del plan ODD v1.1 del Escritorio.
Se verificó SHA-256 del archivo comprimido, cada miembro descomprimido y el plan.
No hubo miembros faltantes/excluidos de la selección ni discrepancias con hashes
de procedencia conocidos. Eso acredita la copia, no certificación independiente
de la calidad experimental o ausencia de todo dato sensible imaginable.

| Archivo | Contenido / alcance |
|---|---|
| [odd-sdd-gpt-trazas.zip](anexos/odd-sdd-gpt-trazas.zip) | Las 60 trazas GPT v2 ya saneadas, incluidos fallos de cuota; hashes contrastados con procedencia. |
| [odd-sdd-suplemento-trazas.zip](anexos/odd-sdd-suplemento-trazas.zip) | Seis trazas del suplemento separado, sin fusionar con el lote original. |
| [gemini-tres-flujos-trazas.zip](anexos/gemini-tres-flujos-trazas.zip) | Noventa trazas Developer/SDD/ODD; mismas que respaldan el reporte validado. |
| [developer-compacto-trazas.zip](anexos/developer-compacto-trazas.zip) | Noventa trazas A/B/C; conserva los casos costosos, no solo éxitos elegidos. |
| [ponytail-recuperado.zip](anexos/ponytail-recuperado.zip) | Originales seleccionados, ledger, métricas, protocolo, scripts, parche, fixtures/oráculos, evidencia y workspaces sintéticos finales recuperables. |
| [herramientas-actuales.zip](anexos/herramientas-actuales.zip) | Snapshot de once herramientas actuales de experimentación/preservación; no confundir con un runner histórico congelado distinto. |
| [gemini-exploratorio-no-validado.zip](anexos/gemini-exploratorio-no-validado.zip) | Resumen y registros finales del Gemini exploratorio, expresamente no válidos como A/B. |

[preservacion.json](preservacion.json) contiene el inventario exacto, tamaños,
SHA-256 de archivos y miembros, raíces originales y referencias a los manifests
históricos. Las rutas absolutas de origen son procedencia, no dependencias para
leer esta copia. Los cuatro paquetes de trazas posteriores a Ponytail contienen
246 archivos contrastados con sus hashes existentes. Los cinco hashes originales
publicados en el registro Ponytail también coinciden con los archivos recuperados.

## Plan y decisiones

[plan-odd-v1.1.md](plan-odd-v1.1.md) es copia **byte a byte** de
`~/Desktop/plan-crear-agente-odd-mas-2026-11-04.md` al preparar esta continuidad.
El original no se editó. Mantiene `.odd/`, registro solo cuando hace falta y
sin issues/tickets en v1, pero describe la propuesta anterior de un agente separado.
No incorpora como decisión la posterior sugerencia de evolucionar Developer hacia
ODD, que el usuario aún no eligió. Algunos apartados históricos de evidencia son
anteriores a los ensayos nuevos; leer primero el contexto actualizado enlazado.

## Privacidad y límites de conservación

Solo se seleccionaron archivos sintéticos, documentos y herramientas explícitos.
No se copiaron auth/config globales, credenciales, bases de sesiones del host,
directorios `isolated/` de autenticación, caches, `.git` ni snapshots completos
del entorno. Se verifican nombres/rutas y se rechazan claves estructuradas de
transporte API, tokens de acceso, firmas opacas y contenido de razonamiento
privado; contadores numéricos reasoning sí se conservan.

Los intentos Gemini sobrescritos nunca se guardaron completos: no pueden
recuperarse ni certificarse ahora. El runner GPT v2 exacto con hash 633eb3… no
se reconstruyó: el snapshot actual es la versión modificada documentada en
reproducción. No se afirma que estos ZIP basten para replicar servicios, plugins,
caché, cuotas o entornos completos. Las advertencias históricas sobre trazas
temporales describen el estado original; esta copia posterior reduce esa
dependencia para los archivos que constan en el manifest, no inventa los faltantes.

## Cómo comprobarlo sin inferencia ni extracción

Desde la raíz del repositorio:

```text
python3 tools/preserve_experiment_context.py verify
```

No volver a ejecutar `capture` sobre este paquete: se niega a sobrescribirlo.
`verify` no llama a proveedores, no ejecuta el código archivado y no necesita
credenciales. Los ZIP no deben ejecutarse automáticamente: contienen herramientas
históricas que pueden iniciar inferencia o tener límites ya rectificados.

El paquete está guardado en este checkout, **sin commit ni push**. Para otra
máquina/worktree hay que copiarlo junto con los registros/herramientas o autorizar
su versionado. No se instaló ODD, no se compactó Developer activo ni se cambiaron
fuentes canónicas del MAS al preparar esta conservación.

## Verificación de este punto de continuidad

- `python3 tools/preserve_experiment_context.py verify`: siete ZIP y 798 hashes
  internos correctos; copia del plan intacta.
- SHA-256 del plan original y copia:
  `3280bf7a0f17b3c907302629d4d4a8d63e3f88c7cde99c56fc27af8badc349ef`.
- `python3 tools/check_links.py`: 120 Markdown correctos.
- `python3 tools/validate.py`: 11 skills, 5 agentes y 6 plataformas correctos.
- Sintaxis de la herramienta de preservación y `git diff --check`: correctos.
- Sin nuevas llamadas a modelos, ejecución del código archivado, cambios de
  agente activo, instalación, commit o push para generar este paquete.
