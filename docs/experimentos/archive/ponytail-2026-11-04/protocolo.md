# Protocolo prerregistrado — síntesis conservada

[Informe y decisión](README.md) · [Resultados](resultados.md)

Identificador: `ponytail-v1-20261104`. Congelación registrada:
**2026-11-04T06:08:32.877144+00:00**, antes de las celdas A/B. Se conservaron
162 hashes de protocolo, harness, fixtures, oráculos e instrucciones, sin cambios
durante la comparación. Este documento es una síntesis posterior, no el archivo
original congelado ni una nueva instrucción de ejecución.

## Tratamientos y aislamiento

- A: baseline limpio `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`.
- B: copia externa de A con las seis reglas descritas en el informe y render oficial.
  No se ajustó B después de observar resultados.
- MAS completo disponible en ambos brazos: cinco agentes, once skills y referencias;
  prompts íntegros y carga normal de skills. Las cargas del rol/dominio se comprobaron
  en las sesenta trazas; el texto experimental de Developer estaba en B y no en A.
- Configuración XDG separada por brazo; instrucciones globales no sensibles iguales;
  `--pure`, sin plugins ni descubrimiento externo de skills/compatibilidad Claude.
  Sesiones y directorios nuevos por celda, sin memoria compartida autorizada.
- Overrides temporales simétricos por rol. En `inspect`, bash/edit/write/task/webfetch
  deshabilitados en configuración resuelta y prueba real. Comparación de hashes de
  archivos antes/después. Developer podía editar el fixture y ejecutar sus checks.
- Sin acceso autorizado a oráculos, otro brazo o red desde las herramientas del agente.
  La inferencia utilizó el proveedor existente OpenAI, con autenticación del host sin
  leer ni copiar credenciales. Solo tareas sintéticas e instrucciones MAS del alcance.
- Estos controles no constituyen un sandbox de sistema operativo para código arbitrario.

## Ejecución

Modelo `openai/gpt-6.1-sol`, OpenCode 1.18.34. Interfaz:
`opencode --pure run --format json --agent … --model … --dir …`.

Filtro: 10 escenarios × 2 brazos × 1 repetición = 20 celdas. Tras pasar el filtro,
completar tres repeticiones: 60 acumuladas. S09 es una celda con dos subcriterios.
Máximo 22 pasos y 180 segundos por celda, cuatro procesos concurrentes, sin reintentos
A/B automáticos. Dos pruebas reales de preflight realizadas por separado.

Orden alternado AB/BA por escenario y repetición; la concurrencia no controla el
orden de finalización. Mismas herramientas, límites, tareas y oportunidades de
autocorrección por rol y brazo. Checks externos al terminar, sin segunda oportunidad
asistida. Conservar fallos, timeouts e incidentes; no seleccionar solo éxitos.

## Escenarios y aceptación

| ID | Caso | Criterios necesarios |
|---|---|---|
| S01 | Helper adecuado | `caption` correcto en vacío/espacios/Unicode; reutiliza helper compatible; sin abstracciones/dependencias nuevas. |
| S02 | Helper incompatible | Conserva caja, colapsa espacios y devuelve fallback vacío; no fuerza helper con pérdida de información. |
| S03 | Dependencia justificada | Carga YAML con alias y multilínea, raíz mapa, errores `ValueError`, rechazo de construcción Python; PyYAML declarada y justificada. |
| S04 | Contrato y consumidores | Retorno dict, presentación, CLI, exportación y fixture coherentes; tests actualizados; declara límites externos. |
| S05 | Recursos y errores | Validación/autorización antes de abrir, cierre una vez en éxito/error/cancelación, error original conservado; no exige context manager. |
| S06 | Frontera arquitectónica | Rechaza negativos, conserva cotización cero/positivos, puerto y separación de dominio; inyección fake funcional. |
| S07 | Review de regresión conectada | Detecta que desempaquetar dict produce claves y una salida incorrecta en consumidor; evidencia, condición y consecuencia. |
| S08 | Defecto independiente | Ningún defecto atribuible al cambio bajo contrato str; comprueba consumidor, no convierte defecto cercano independiente en hallazgo del diff. |
| S09 | Concurrencia y topología | Known: lock de proceso insuficiente con cuatro procesos/dos máquinas/store compartido. Unknown: riesgo condicionado, sin inventar despliegue. Corrección proporcional. |
| S10 | Cambio trivial | Literal «Guardado», prueba pertinente, sin abstracciones/dependencias ni rastreos de componentes ajenos. |

Todas las celdas debían respetar alcance/permisos, conservar checks y no eliminar
ni debilitar tests para aparentar éxito. Complejidad injustificada significa una
dependencia/abstracción innecesaria o duplicación de un helper compatible, no una
preferencia estética. Review conserva criterios de dominio, severidades e IDs.

## Métricas y juicio

Por celda: tests y oráculo externos, archivos cambiados, herramientas, pasos,
inicio/duración, input/output/cache/reasoning y coste expuestos por `step_finish`.
No observable se registra como desconocido. No guardar razonamiento privado;
solo su contador cuando lo exponga el host.

Review: verdaderos positivos (TP), falsos positivos (FP), omisiones (FN), condiciones
y evidencia contra rúbrica. Respuestas con etiquetas de brazo ocultas, ceguera
limitada del coordinador. Developer: revisar también diff y salida, pues pasar tests
es necesario pero insuficiente. No observable esencial impide aceptar.

## Reglas de decisión previas

1. Pasar filtro exige veinte celdas completas/aisladas, sin B incompleto respecto a A,
   daños graves, violaciones de permisos o nuevos FP/FN. No retocar B dentro de v1.
2. Ninguna regresión grave de seguridad/integridad/permisos es compensable. Analizar
   degradaciones por escenario, sin ocultarlas en promedios.
3. Sin tolerancia económica cuantitativa acordada, promover solo por dominancia:
   mejora reproducida de calidad en al menos dos escenarios y dos de tres repeticiones,
   sin degradaciones esenciales ni aumento agregado de tokens, tiempo o coste reportado;
   o calidad equivalente completa y ahorro agregado de tokens y tiempo de al menos 10 %,
   con dirección favorable en al menos dos repeticiones y seis escenarios.
4. El 10 % es un umbral experimental de ahorro, no disposición a pagar sobrecostes.
   Calidad equivalente sin ahorro robusto implica inconcluso/no promover; rechazo
   técnico requiere daño repetido atribuible. Aceptación parcial exige nueva variante
   reducida y reevaluación; no seleccionar retrospectivamente un subconjunto favorable.
