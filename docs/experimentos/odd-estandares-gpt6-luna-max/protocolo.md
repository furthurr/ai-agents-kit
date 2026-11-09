# ODD histórico vs ODD ajustado — GPT-6 Luna max

Nueva cohorte independiente: modelo `openai/gpt-6-luna`, variante CLI `max` en
TODAS las invocaciones, dos brazos y tres repeticiones nuevas por brazo. Mismo
baseline LocalLibrary TASK-2, documentos, pruebas externas y prompts de ODD que
`odd-estandares-gemini-2026-11-05`; mismo timeout 600 s e igual configuración para
ambos brazos. No forzar temperatura: el catálogo del modelo declara que no la admite.
Control/ajuste se diferencian solo por el bloque de estándares ya congelado.

Preflight de cada perfil verifica prompt resuelto, skill por contenido, edición y
unittest con `--model openai/gpt-6-luna --variant max`. Fijar configuración y
comprobar hashes antes/después; no inferir activación max solo por texto del agente.
Tres bloques de dos procesos; detener nuevas repeticiones ante errores del proveedor,
timeout o carga errónea, conservar intentos completos y parciales sin reintentos
selectivos. Evaluar suite original restaurada y nueve oráculos externos, incluyendo
SQLite en disco/concurrencia. No retroalimentar el oráculo al agente.

No mezclar contadores ni porcentajes con Gemini. Reportar input+cache_read+cache_write+
output y reasoning separado, tiempo sumado vs wall-clock y errores; métricas ausentes
son desconocidas. No derivar facturación de coste cero. Observar consulta por contenido,
documentos leídos, artefactos, tests y cierre. Consultas no garantizan estándares ni
descubrimiento documental completo. n=3/un proyecto no prueba generalización.

Los cinco casos focalizados previamente ejecutados con Gemini se referencian, no son
evidencia de este modelo ni se incluyen en sus costes. Sin instalación de agentes,
cambios canónicos, credenciales, commits o publicación. Permisos no son sandbox OS.
