# ODD ajustado con navegación — una tarea, dos brazos, exploratorio

ID odd-context-routing-luna-max-v1. Se ejecuta TASK-2 Alta UNA vez por brazo:
control=ODD ajustado con estándares ya probado; tratamiento=el mismo ajustado más
ruta-contexto.md. No comparar contra ODD original sin estándares ni mezclar Gemini.
Mismo `openai/gpt-6-luna`, `--variant max`,1800s por llamada, steps60 configurado,
permisos, task literal, modelo de usuario simulado y oráculos. Dos procesos simultáneos.

Ambos reciben EXACTAMENTE el mismo baseline con mapas mínimos preexistentes del
fixture: `.navigator/ai-context.md` y `.architecture/{README.md,flows.md}`. Son
descripciones verificadas de fuentes del baseline; no soluciones, nuevos requisitos
ni oráculos. No se modifican `.navigator/` o `.architecture/` canónicos del kit.
Se añaden las mismas notas a la solución de referencia para revalidarla.

Solo cambia la instrucción de ruta selectiva. Las skills data-api/ui-design conservan
su contenido íntegro y deben seguir consultándose cuando corresponda. No subagentes,
RAG externo ni resumen generativo. No reducir normas para ganar el contador.

Pruebas offline de composición, igualdad del corpus y roles; referencia43+9 y dos
preflights reales antes de congelación. Inputs verificados antes/después de llamadas.
Evaluación en copia con tests originales restaurados y nueve oráculos. No feedback
oculto ni reintentos selectivos. Error de proceso/timeout/API se conserva como parcial.

Observar aceptación global vs oráculos externos, consultas por contenido/orden,
lecturas de mapas y fuentes, búsquedas, volumen de salidas, referencias/seguimiento,
doc-recomendaciones, herramientas/pasos, tokens y duración. Leer mapas no prueba que
se usen correctamente ni que se apliquen todos los estándares. Clasificar mapa vs
archivo de código; no atribuir automáticamente ahorro a menos lecturas.

Tokens=input+cache_read+cache_write+output; reasoning aparte. Métricas desconocidas
no son cero, caché no equivale a factura, suma de tiempo no es wall-clock. Preparación
y preflights separados. Permisos no son sandbox OS. Configurar max no acredita por
sí solo aplicación interna de ese parámetro por el proveedor.

Regla exploratoria: ambos funcionales y nuevas fuentes usadas sin perder las skills,
sin artefactos fuera de alcance; reducción de tokens>=10% y tiempo no peor en más
de10% sería señal favorable, no prueba de causalidad o mejora repetible. Si crece
coste, ambos usan mapas, se omiten fuentes o falla calidad, reportar sin retocar.
Una pareja no permite adoptar/promover ni afirmar ahorro universal.

Conservar evidencia anterior y plan del Escritorio. No instalación, catálogo nuevo,
commits, cambio de agentes canónicos ni ejecución de documentación automática.
