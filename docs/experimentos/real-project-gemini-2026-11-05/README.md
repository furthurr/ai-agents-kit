# Developer / SDD / ODD en proyecto existente documentado

**Estado: 27/27 celdas ejecutadas; 18/27 trayectorias con aceptación funcional.**
Fecha de ejecución: 2026-11-05 UTC. Modelo solicitado en todos los brazos:
`google/antigravity-gemini-3.8-flash`, mediante OpenCode 1.18.34 y Antigravity.

## Resultado principal

| Tarea, tres repeticiones por flujo | Developer | SDD | ODD experimental |
|---|---:|---:|---:|
| Media-alta: búsqueda, filtros, paginación UI + JSON | 3/3 | 3/3 | 3/3 |
| Alta: reservas persistidas, idempotencia y concurrencia SQLite | 3/3 | 3/3 | 3/3 |
| Muy alta: sucursales, migración y reanudación con transferencias | 0/3 | 0/3 | 0/3 |
| **Trayectorias completas aceptadas** | **6/9** | **6/9** | **6/9** |

Las nueve celdas de la tarea muy alta conservan el mismo fallo tanto en fase1
como en fase2: el listado heredado de préstamos expone ejemplares de otra sucursal.
El test externo falla en la aserción de ausencia del UUID ajeno en HTML, no por
problemas de importación o instalación. El aislamiento del endpoint nuevo y las
pruebas propias no bastaron para proteger todos los consumidores existentes.

La suite original sigue pasando en los 36 registros de fase. Es una demostración
concreta de que **preservar las pruebas existentes no implica cubrir el nuevo contrato**.

## Consumo observado

Incluye todos los intentos comparativos, también las tareas incorrectas. Excluye
preparación, preflights y evaluación externa.

| Métrica agregada, nueve celdas por flujo | Developer | SDD | ODD |
|---|---:|---:|---:|
| Tokens comparables | 22.675.965 | 27.575.616 | 19.961.035 |
| Duración sumada de conversaciones (s) | 3.680,972 | 3.918,099 | 3.660,262 |
| Llamadas de herramientas | 563 | 537 | 576 |
| Respuestas de usuario simuladas | 0 | 29 | 0 |
| Errores de herramienta registrados | 6 | 5 | 12 |

ODD frente a Developer: **−11,97 % tokens**, **−0,56 % duración**. La diferencia de
tiempo es pequeña; no hay una mejora importante de velocidad. SDD: **+21,61 % tokens**,
**+6,44 % duración**. No mezclar estos porcentajes con cohortes anteriores.

En el estrato fijado por tareas T1+T2, donde todos pasan, ODD suma 9.916.748 tokens
frente a 11.575.025 de Developer: **−14,33 %**, con **−3,19 % tiempo**. No se elimina
T3 de la tabla principal ni se eligen solo éxitos individuales para inventar adopción.
ODD gasta más que Developer en T2 agregada: 6.004.227 frente a 5.501.090 tokens.

Tokens comparables = input + cache-read + cache-write + output; reasoning separado
en JSON. Tokens cacheados no implican igual precio. No hay factura ni ahorro
monetario acreditado. La suma de duraciones no es tiempo de reloj del lote.
Wall-clock comparativo: **4.566,367 s**, incluyendo checks externos y coordinación.

## Proyecto y documentación previa

- Proyecto: [MDN Django LocalLibrary](https://github.com/mdn/django-locallibrary-tutorial).
- Commit verificado en GitHub: `3120b4302bf87a1b8c84d06662c2b8787f7da5f8`.
- Licencia verificada: CC0-1.0. Python 3.12.4, Django 6.1.1, SQLite.
- Se conservaron README, guías de contribución/revisión/seguridad, código y 43 tests
  originales. Gemini preparó un complemento fáctico común `docs/lab-context.md`.
- Se generaron estáticos offline; no se añadieron soluciones a la documentación.
- Cada celda recibió el mismo baseline en una copia independiente.

**Hallazgo documental:** no se observan llamadas directas `read` al README original
ni al complemento `docs/lab-context.md` en ninguno de los tres flujos. Sí aparecen
lecturas de código y, según flujo, referencias metodológicas y seguimiento propio.
Tener documentación disponible no garantiza que se consulte.

Límite del fixture: el `AGENTS.md` de laboratorio no enlazaba el complemento documental
y no se exigió su lectura. Este ensayo observa consulta espontánea, no compara con/sin
documentación ni acredita la integración completa de `.architecture/`, `.navigator/`,
`.data/` o `.design/`. No atribuir causalmente el bug a «no leer documentación»:
el contrato de aislamiento estaba en la petición, y la documentación describía baseline.

## Tratamientos, calidad y límites del simulador

Developer y SDD usan sus agentes completos vigentes y skills con nombres únicos,
verificados byte a byte tras sustitución de identificadores. No Developer compacto.
ODD es **el tratamiento histórico experimental**, no un agente instalado ni toda la
propuesta v1.1. No se ha aprobado reemplazar Developer ni integrar ODD al catálogo.

SDD eligió Tiny en ocho de las nueve decisiones iniciales y Lite en T3-r2. Se conservó
el modo en la reanudación. Se probaron así creación nueva Tiny y una trayectoria Lite,
a diferencia del corpus anterior dominado por Direct.

En **T3-SDD-r2-fase2**, el modelo presentó Quick Plan y pidió confirmar antes de
implementar, aun reconociendo que Lite no requería esos gates. El simulador solo
contemplaba gates Tiny y no respondió esa confirmación adicional. Quedaron cuatro
tests de transferencia fallando además del listado heredado. Se conserva el resultado
sin reintentar; es un **límite de interacción agente/simulador**, no prueba de que SDD
sea incapaz de implementar transferencias. También limita la comparación de coste T3.

Hay una alerta mecánica de cierre/Gate4 prematuro en SDD T3-r3-fase2. Los marcadores
copiados de fase1 pueden afectar ese detector: **no es un finding semántico confirmado**.
Cero alertas mecánicas en otro brazo no certifica fidelidad perfecta; por ejemplo,
Developer implementó sin turnos adicionales de aprobación en esta configuración.

En todas las fases se verificó carga primaria por contenido y proceso saludable.
Sin errores API, timeouts comparativos, accesos externos detectados, skills ajenas ni
llamadas a herramientas prohibidas. Los errores de herramientas conservados no se
confunden con errores API ni con pruebas funcionales rojas.

## Interpretación

1. El proyecto existente fue útil para revelar una omisión de integración compartida
   por los tres flujos, que el corpus pequeño anterior no mostró.
2. ODD mantiene una señal de menor consumo, pero no gana en todas las tareas ni demuestra
   mejor calidad. Igualdad de 6/9 no acredita equivalencia de responsabilidades.
3. Ningún flujo resolvió por completo la tarea muy alta. No promover un agente ni
   retirar otro sobre esta evidencia; importa mejorar cobertura de consumidores.
4. Documentación disponible y documentación realmente utilizada son medidas distintas.
5. Un solo proyecto tutorial, tres repeticiones y un modelo no prueban generalización
   a producción, UI visual real, seguridad exhaustiva ni continuidad prolongada.

No se ajustaron prompts ni entradas después del freeze. No se repararon entregas ni
se comunicaron resultados ocultos a los agentes entre fases. La reanudación fue sesión
nueva real con petición original + cambio + disco propio, no compactación interna.

## Evidencia y reproducción

- [Protocolo congelado](evidencia/protocol.md), [contratos](evidencia/cases.json).
- [Resumen y diagnóstico por celda](evidencia/summary-audit.json).
- [Congelación](evidencia/freeze.json), [preflights reales](evidencia/preflight.json).
- [Procedencia](evidencia/provenance.json), [dependencias](evidencia/dependencies.lock.txt).
- [Validación de oráculos y referencias](evidencia/oracle-validation-v3.json).
- [Incidentes y límites de preparación](evidencia/preparation-review.json).
- [Registro del lote](evidencia/batch-result.json).
- [Comandos y verificaciones de cierre](verificaciones.json).
- [Laboratorio completo preservado](laboratorio.tar.gz) y [hashes](preservacion.json).
- Herramientas nuevas: `tools/real_project_gemini_lab.py`, `tools/real_project_report.py`,
  `tools/preserve_real_project_lab.py`, sus pruebas offline.

El archivo comprimido contiene baseline/original filtrados, documentación, perfiles,
runner y tests del laboratorio, oráculos, referencias, solicitudes, trazas saneadas,
registros, intentos y árboles finales. No incluye virtualenv, credenciales, `.git`,
estáticos derivados ni bases SQLite. La preservación verifica cada miembro por SHA256.
No es una instalación global ni modifica el kit canónico.

Para inspeccionar/revalidar, extraer en una raíz nueva segura y revisar `runner.py`,
`dependencies.lock.txt`, `protocol.md` y `freeze.json`. Recrear venv/estáticos. El runner
conserva una ruta absoluta `REPO` del entorno original: en otra máquina se requiere
adaptación explícita y nueva congelación antes de nuevas inferencias. No sobrescribir
los directorios de ejecución ni reutilizar los probes existentes. Reproducción de
oráculos no promete respuestas idénticas del modelo ni hermeticidad del plugin.

Preparación hecha principalmente con Gemini, revisada y corregida antes del freeze.
Sus borradores e incidentes se conservan separados: primer recolector interrumpido,
dos construcciones y revisión de oráculos con timeout después de escribir validaciones.
El coste total de preparación no es completo/observable por la pérdida del primer
recolector. No se suma a los 70.212.616 tokens comparativos para inventar un total global.

Estado local: evidencia nueva sin commit/push; agentes canónicos/instalados intactos.
El índice general y el punto de continuidad previos no se actualizaron automáticamente.
