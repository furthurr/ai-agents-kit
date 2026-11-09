# Agrupación de operaciones independientes — protocolo previo

ID: odd-batching-luna-max-v1. Autorizado por el usuario después de la investigación
de solo lectura. Hipótesis: menos rondas independientes puede reducir consumo total
manteniendo consultas, estándares y verificación, sin comprimir skills.

## Diseño congelado

- Control: ODD con estándares de la cohorte GPT completa, skills completas.
- Tratamiento: mismo control normalizado + agrupacion.md, sin otros cambios.
- Dos parejas NUEVAS, orden de envío control/tratamiento y tratamiento/control;
  dos procesos concurrentes como en los ensayos anteriores. Sin controles históricos.
- TASK-2 literal, baseline documentado LocalLibrary idéntico, sin mapas añadidos.
- openai/gpt-6-luna --variant max, OpenCode 1.18.34 observado; sin temperatura.
- No modificar criterios, clasificación, notas, permisos ni pruebas según el brazo.
- No subagentes, red de producto, instalación, migración Developer ni fuentes canónicas.

## Presupuesto y parada

Máximo cuatro invocaciones principales (una por conversación), sin preflights LLM,
sondeos de disponibilidad ni aprobaciones simuladas adicionales. Si el agente pide
otra aprobación, queda incompleto: no se envía una segunda llamada.
Timeout simétrico de 1800 s y steps 60. Se observa el flujo JSON en vivo; parada al
primer límite de paso con >=5.000.000 tokens comparables por conversación, o 60 pasos.
Presupuesto nominal agregado 20.000.000; el paso que cruza el umbral puede excederlo.
Registrar sobrepaso y consumo parcial observado. Pasos/counters ausentes desconocidos.
403/error API, timeout, métricas incompletas o fallo del arnés detienen nuevas celdas
y cancelan la conversación concurrente si aún sigue activa. Conservar intentos,
snapshots, errores saneados y métricas disponibles. Sin retry selectivo.
No ampliar lote ni retocar tratamiento tras observar resultados.

## Aceptación

- 9 oráculos externos y suite catalog con originales restaurados + tests añadidos.
- Diagnóstico separado de los 43 originales en la copia de evaluación.
- ODD y ambas skills cargados por contenido, dominios antes del primer producto.
- Fuentes documentales pertinentes contrastadas con código; ausencias declaradas.
- Evidencia de aplicación de contratos, persistencia/idempotencia/concurrencia,
  UI/CSRF/estados, patrones y consumidores pertinentes. La lectura no basta.
- README desactualizado detectado, propuesta explícita de selección manual de
  documentation-orchestrator, sin editar documentación canónica ni bootstrap.
- Sin feedback de los oráculos para corregir la solución.
- RED se audita semánticamente: un fallo de importación no certifica ejecución de
  las reglas. Informar límite, no reclasificarlo automáticamente como TDD completo.

## Métricas e interpretación

Input + cache_read + cache_write + output; reasoning numérico separado, sin texto
privado. No inferir factura a partir de coste host cero. Medir duración conversacional,
wall-clock y preparación/evaluación aparte. Contar búsquedas/lecturas, criterios,
escrituras producto/tests/notas (parches mixtos con etiquetas múltiples), pruebas,
correcciones observables, seguimiento, cierre y agrupación por ronda. Bytes no tokens.
Las ventanas de pasos no imputan causalmente el consumo a la herramienta emitida.

Señal exploratoria favorable: todas las conversaciones funcionales y fieles,
>=10% ahorro agregado, ahorro en ambas parejas, tiempo agregado <=+10%, y reducción
observable de rondas independientes. Si no se aplica agrupación, el mecanismo queda
sin probar. Dos parejas no justifican producción ni equivalencia integral.

## Integridad

Congelar corpus, perfiles, arnés, presupuesto y protocolo tras checks offline y
referencia 43+9. Preflight offline se etiqueta como tal, nunca como inferencia real.
Preservar evidencia nueva fuera de raíces históricas y exportarla al checkout.
Los resultados de Gemini/403 y demás ensayos permanecen separados e intactos.
