# Prompt para una sesión completamente nueva

Copiar el bloque siguiente en una sesión nueva sobre el mismo checkout o después
de transportar los archivos locales. Preferiblemente seleccionar manualmente el
agente de desarrollo; no se requiere cambiarlo automáticamente ni activar SDD.

```text
Quiero continuar la investigación de una versión de ODD que consulte correctamente
nuestros dominios data-api y ui-design y la documentación pertinente del proyecto,
pero reduzca el consumo TOTAL sin ahorrar por omitir estándares.

Primero lee:
docs/experimentos/continuidad-odd-2026-11-06/CONTINUAR-AQUI.md
docs/experimentos/continuidad-odd-2026-11-06/estado.json
y los tres informes recientes que allí se priorizan. Verifica las afirmaciones
necesarias en JSON, scripts y fuentes directas; no cargues todas las trazas por rutina.

Contexto: ODD con estándares sí consultó dominios y detectó documentación en la
cohorte GPT-6 Luna max completa, con +36,78% tokens agregados frente al original.
No es un coste fijo ni causalmente aislado. Dos optimizaciones recientes NO dieron
ahorro en sus parejas exploratorias: navegación +55,77% tokens; núcleo/referencias
+165,57%. En esta última no se eliminaron normas y se verificó lectura íntegra de
criterios antes del código, pero aumentaron búsquedas/pasos y apareció seguimiento.
No adoptes esas variantes ni concluyas que son inútiles universalmente con n=1.

Esta primera fase debe ser de SOLO LECTURA e investigación acotada con la evidencia
ya existente: analiza dónde crece la conversación (exploración, carga de criterios,
código, tests, correcciones, notas y cierre) y qué causas podemos distinguir de
variabilidad. No almacenes razonamiento privado; usa operaciones observables.

Después resume hechos, incertidumbres y propone el siguiente experimento mínimo
con control, criterios de calidad/fidelidad/eficiencia total, presupuesto y parada.
Espera mi aprobación antes de editar candidatos o ejecutar nuevos modelos.
No hagas otra batería por el mero hecho de recuperar este contexto.

Preserva todos los archivos locales y los lotes, incluidos timeouts/403 y análisis
corregidos. No reintentes selectivamente ni mezcles métricas de modelos/cohortes.
Muchos archivos son untracked y no están en el remoto: si faltan, indícalo, no hagas
reset/clean/bootstrap ni inventes evidencia. Los paquetes por experimento y el
snapshot de continuidad permiten recuperar fuentes; revisar hashes y rutas antes.

El último modelo operativo fue openai/gpt-6-luna con --variant max, timeout1800s
simétrico. Gemini devolvió403; el motivo de cuenta no se confirmó. No cambies modelo,
cuenta o proveedor ni solicites credenciales para sortearlo. Verifica disponibilidad
solo cuando sea necesario para un plan aprobado.

No instales agentes, no modifiques canonical/generated/adaptadores, no hagas
commits/push/releases, no actives SDD ni delegues automáticamente. No sincronices
carpetas documentales. La decisión previa de usar Developer v2 candidato2 con nombre
Developer y deprecar el anterior está documentada, pero NO implementada: esta
investigación ODD no autoriza alterar esa decisión ni ejecutar el plan del Escritorio.

Si para sincronizar índices canónicos hace falta otro rol, prepara contexto y
espera mi selección manual de documentation-orchestrator; no cambies de agente.
```
