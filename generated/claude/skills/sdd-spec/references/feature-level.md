# Esfuerzo previsto del LLM — ReserveLab

Solo el agente SDD comunica esta calificación. Cargar `sdd-spec` desde otro agente
no concede permiso para emitirla. Puntúa la feature completa solicitada
(implementación y verificación), no tareas/fases ni el proyecto entero. Bugs,
consultas y exploraciones no puntúan como features por defecto.

## Comparación del esfuerzo

Analiza primero el alcance deseado y su impacto real. Compara el trabajo pedido con
ReserveLab, descontando infraestructura correcta reutilizada y considerando las
garantías pendientes de integración, regresión y verificación. Un stub no resuelve coordinación.
Evalúa: alcance/regresión; reglas/casos límite; estados/integridad; capas/entradas;
persistencia/integraciones; concurrencia/idempotencia; fallos/compensación/recuperación;
migraciones/legado; aislamiento/autorización; pruebas significativas.

La escala ordinal no es una fórmula validada ni predice tokens, tiempo, pasos o costo.
No sumes dimensiones ni puntúes por archivos, líneas o palabras de riesgo. Elige el
perfil conjunto más comparable y explica diferencias. Si falta evidencia esencial,
investiga o pregunta; no muestres puntuación provisional.

## Perfiles comparables

| Nota | Referente | Trabajo pendiente que distingue el perfil |
|---|---|---|
| 1 | F01 | Transformación pura; formato exacto y validación de campos/tipos/límites. |
| 2 | F02 | Predicados combinados, límites inclusivos y orden estable. |
| 3 | F03 | Reglas monetarias ordenadas, redondeo entero y casos extremos. |
| 4 | F04 | Agrupación, conflictos, normalización e idempotencia. |
| 5 | F05–F06 | Persistencia transaccional, rollback y reintentos sobre esquema correcto. |
| 6 | F07 | Escasez, reserve/cancel e integridad entre procesos. |
| 7 | F08–F09 | Recuperación/dedup o convergencia/versiones con auxiliares existentes. |
| 8 | F10 | Saga durable: tres métodos sobre participantes, locks y esquema correctos. |
| 9 | Entre F10 y X13 | Más coordinación por construir que F10; menos interacciones que X13. Interpolación, no benchmark. |
| 10 | X13 | Offline/sync, persistencia, autorización multiusuario, sesión, migración y recuperación combinadas. |

F10 vale **8** para `Saga.submit`, `Saga.step` y `Saga.get`, con participantes,
locking, esquema y validadores proporcionados. X13 vale **10**: hay puertos/IPC/reloj,
pero su coordinación local/remota forma parte del trabajo; no se suma construir C12
ni el evaluador. Los rangos históricos no se convierten matemáticamente.

## Superior a X13

Usa **10+ 🔴** solo si garantías e interacciones pendientes superan claramente X13,
descontando infraestructura reutilizada. Explica dimensiones adicionales: por
ejemplo, mantener X13 y añadir saga externa multirrecurso, compensaciones/fallos no
proporcionados e interacción con permisos, sesión y migración. Volumen o una señal
aislada no bastan; nunca lo expreses como nota 11.

## Formato de salida

```text
Esfuerzo previsto del LLM: <nota e icono>
Atención especial: <complicación concreta, solo si aplica>
Profundidad recomendada: <direct | lite | standard>

¿Continuamos con <recomendada> o prefieres <otra elegible>?
```

Para 10/10+ ofrece dividir en entregas o abordar el conjunto en standard; no
expliques rutinariamente rangos ni exclusiones. No añadas prefacios ceremoniales.
Si ya hay elección explícita compatible, respétala sin repetir la pregunta.

### Registro interno

En la spec, si corresponde, conservar:

```text
Esfuerzo previsto del LLM: <nota e icono>
Referente del laboratorio: <prueba o rango comparable>
Justificación: <2–4 factores; para 10+ explicar qué supera X13>
Supuestos relevantes: <infraestructura o incertidumbres que cambian la nota>
Atención: <normal | reforzada | alta; controles concretos>
Profundidad recomendada / seleccionada: <modos y elección explícita>
```

1–7 inclusive: 🟢 normalmente, o 🟠 con complicaciones concretas controlables;
8–9: 🟠; 10: 🔴; superior a X13: exactamente 10+ 🔴. No uses
0, decimales, rangos ni enteros mayores de 10 como nota. Si se necesita estructura,
conserva el entero 1–10 y un indicador separado `exceeds_x13`; 10+ es valor 10 e
indicador verdadero. Atención es un indicador separado, no otra nota de riesgo.
No cambies datos históricos. Direct no crea archivos solo para este registro.

Emite al terminar definición de alcance e impacto, antes de recomendar profundidad,
independientemente del modo posterior. No muestres puntuación provisional. No repitas
el nivel al cambiar de fase. Si cambia materialmente alcance o impacto, analiza
primero. La nota orienta la recomendación base de `scope-depth.md`, pero no demuestra
elegibilidad ni elige testing, ejecutor, permisos, modelo, gates o resultado funcional.
Verde no habilita lite sin verificar condiciones; naranja no sustituye garantías.

Ejemplo: `Esfuerzo previsto del LLM: 6 🟠`, `Atención especial: reservas simultáneas;
se comprobará la disponibilidad con pruebas concurrentes`, `Profundidad recomendada:
lite`, solo si mecanismo y verificación son adecuados. Si no lo son, aclarar o
recomendar standard. No rebajar la nota al dividir: evaluar cada entrega.

## Contrastes mínimos

| Caso | Nota | Referente | Diferencia que explica el esfuerzo |
|---|---|---|---|
| F10-scaffold | 8 🟠 | F10 | Tres métodos; participantes y locks ya proporcionados; falta coordinar la saga. |
| F10-sin-scaffold | 9 🟠 | Entre F10 y X13 | Mismo alcance funcional, pero hay que construir coordinación/participantes. |
| X13-plus-saga | 10+ 🔴 | Superior a X13 | Saga y compensación externa con interacciones nuevas. |

## Evidencia de X13

Luna/MAX **no superó X13**: 10/11 familias funcionales aprobadas, C12 válido y
fallo `admin_create`. Es un resultado suplementario acotado, no éxito completo ni
frontera universal de capacidad.
