## Coordinación de operaciones independientes

Agrupa en una misma ronda las lecturas, búsquedas, cambios de un comportamiento
coherente y comprobaciones que sean independientes cuando no necesites observar
un resultado intermedio para decidir la siguiente operación. Usa llamadas juntas
o un parche multiarquivo cuando las herramientas lo permitan. No paralelices
escrituras sobre el mismo archivo ni comprobaciones que dependan de una escritura
todavía no terminada. Conserva separados RED, implementación y GREEN.

Esta coordinación no reduce criterios, consultas pertinentes, pruebas, revisión
de consumidores ni cierre documental. No cambia la clasificación del trabajo,
las reglas de seguimiento ODD ni la necesidad de investigar un fallo concreto.
No agrupes operaciones dependientes para aparentar menos pasos.
