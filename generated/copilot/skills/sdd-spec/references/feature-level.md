# Calificación de feature

Solo el agente SDD comunica esta calificación. Cargar `sdd-spec` desde otro agente
no concede permiso para emitirla. La puntuación evalúa la feature completa, nunca
una tarea, fase, modelo o proveedor.

## Evidencia y rúbrica ordinal

Analiza primero el alcance deseado y su impacto real en el proyecto. Considera
extensión del alcance, acoplamiento, dificultad técnica, impacto de fallos y
esfuerzo de verificación/reversión. Usa evidencia de módulos, contratos,
integraciones, persistencia y tests; no estimes por cantidad de archivos/líneas,
tiempo o capacidad del modelo.

Selecciona el ancla más alta sustentada por evidencia. Los niveles son ordinales,
no mediciones exactas. Una señal aislada (p. ej. editar un contrato público) no
impone una puntuación alta sin impacto material. Si falta evidencia para definir
alcance/impacto, investiga o pregunta; no muestres puntuación provisional.

| Nivel | Ancla orientativa |
|---|---|
| 1 | Cambio mínimo y localizado, patrón directo, impacto y verificación inmediatos. |
| 2 | Cambio local pequeño con varios casos sencillos y reversión inmediata. |
| 3 | Comportamiento acotado en un componente, con errores y tests conocidos. |
| 4 | Varios componentes de un módulo; coordinación interna limitada. |
| 5 | Feature de un módulo con integración existente y tests no triviales. |
| 6 | Varios módulos con patrones conocidos y dependencias controladas. |
| 7 | Cambio transversal significativo con coordinación amplia, sin condiciones materiales de 8–10. |
| 8 | Impacto transversal y contrato público, integración externa significativa o decisión arquitectónica relevante. |
| 9 | Dificultad elevada con migración compleja, concurrencia, seguridad/privacidad sensible o legado riesgoso, de impacto amplio. |
| 10 | Cambio sistémico crítico: falla/reversión puede comprometer integridad crítica, disponibilidad general o cumplimiento; exige coordinación y verificación excepcionales. |

## Emisión

Publica solo después de cerrar el análisis y definir el alcance deseado:

- `direct`: después de inspeccionar el cambio y antes de editar.
- `lite`: al cerrar Quick Plan, en el resumen del alcance.
- `standard`: al cerrar Requirements, en el resumen junto a Gate 1.

Formato exacto con el entero real calculado:

```text
Nivel de feature: <n> <emoji>
```

El marcador `<n>` se sustituye por el valor asignado, no por un número fijo para
todo el rango: por ejemplo, nivel 7 → `Nivel de feature: 7 🟢`, nivel 8 →
`Nivel de feature: 8 🟠`, nivel 9 → `Nivel de feature: 9 🟠`.

- 1–7 inclusive: 🟢
- 8–9: 🟠
- 10: 🔴

No uses 0, decimales, rangos ni números de ejemplo como puntuación fija. Añade
1–3 motivos concretos y el alcance evaluado en el artefacto de Requirements cuando
exista; la línea visible mantiene el formato exacto anterior. No repitas el nivel
al cambiar de fase ni pidas aprobación de la calificación. Un gate real sigue
requiriendo su propia aprobación.

Si cambia materialmente alcance o impacto, analiza primero la nueva definición y
actualiza el registro con los motivos. No mantengas una puntuación que describa el
alcance anterior.

No puntúes bugs, consultas o exploraciones como features por defecto. No uses la
puntuación para elegir `direct`, `lite` o `standard`, estrategia de testing,
ejecutor, permisos o modelo. La calificación no es una certificación de seguridad,
estimación de tiempo ni autorización para implementar.
