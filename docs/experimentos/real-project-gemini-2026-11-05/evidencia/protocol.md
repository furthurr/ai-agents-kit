# LocalLibrary existente y documentado — protocolo previo a inferencia comparativa

ID: real-project-gemini-v1-20261104. Modelo solicitado único:
`google/antigravity-gemini-3.8-flash`, OpenCode 1.18.34 con plugin Antigravity habitual.
Autorización: usuario aprobó tres tareas, tres flujos y tres repeticiones sobre
proyecto real con documentación previa. No instalación global, commits ni promoción.

## Proyecto y tratamientos

MDN `django-locallibrary-tutorial`, commit
`3120b4302bf87a1b8c84d06662c2b8787f7da5f8`, CC0-1.0. Es una aplicación tutorial
existente, no una aplicación de producción ni una empresa real. Se conservan README,
guías de contribución/revisión/seguridad y 43 tests originales. `docs/lab-context.md`
es complemento fáctico generado con Gemini y revisado contra código. No contiene
soluciones. No se contrasta documentación presente contra documentación ausente:
se observa el comportamiento de los tres flujos con la misma documentación.

Developer y SDD: cuerpos completos de agentes y skills derivados actuales del kit,
con sustituciones de identificadores verificadas byte a byte. No Developer compacto.
ODD: cuerpo histórico del tratamiento B, solo namespaces de skills de dominio;
no se implementa ni evalúa la propuesta v1.1. No expandir las siglas por inferencia.
Perfiles activos `profiles-v2/`; `profiles/` es borrador no utilizado.

## Tareas, orden y límites

`cases.json` fija literalmente contratos, modelos públicos y respuestas:
T1 búsqueda/filtros/paginación UI+JSON; T2 reserva persistida idempotente y concurrente;
T3 sucursales con migración/aislamiento, después cambio autorizado de transferencias.
Cada celda parte del mismo baseline y no recibe soluciones ni tests externos.

27 celdas previstas: tarea × brazo × repetición. T3 tiene dos fases en cada celda,
por lo que una batería completa genera 36 registros de fase, no 36 tareas independientes.
Cada repetición se ejecuta por separado: T1, T2, T3; para cada tarea tres brazos
concurrentes como máximo. Orden de envío rotado por índice tarea+repetición:
Developer/SDD/ODD, SDD/ODD/Developer, ODD/Developer/SDD. No controla finalización ni caché.

600s e igual máximo60 pasos por invocación; máximo6 invocaciones por fase. El
simulador solo envía selección/aprobaciones descritas abajo: no rellena el presupuesto
con continuaciones ni feedback oculto si un modelo termina incompleto. No se limita
memoria RAM del proceso. Dependencias preinstaladas y Python virtualenv común.

R1 es filtro: si procesos, skills y acceso son válidos, continuar R2 y R3 aun con
fallos funcionales. Error API, timeout, configuración/carga incorrecta o excepción del
arnés detiene nuevos bloques/repeticiones, no mata celdas ya en curso. Conservar todo;
no repetir éxitos/fallos ni arreglar arnés tras freeze y seguir la misma cohorte.
Defecto de código entregado (tests rojos) es resultado, no error de integración por sí solo.

## Conversaciones y reanudación

SDD recomienda profundidad natural Direct/Tiny/Lite; el simulador selecciona en
otro turno únicamente si no escribió antes. Tiny recibe Gate3 solo si existe spec
y producto sin modificar; Gate4 solo si se observó test verde posterior a código.
Lite y Direct no reciben gates Tiny. Developer/ODD reciben aprobación de plan solo
si la piden antes de mutar producto. No equivalen a revisión humana semántica completa.
Una pregunta funcional nueva no se contesta inventando opciones; el caso queda sin
esa aprobación y se evalúa el estado alcanzado. Los parsers mecánicos pueden omitir
pausas redactadas de otra forma: reportarlo como límite, no decisión humana real.

T3 fase2 abre proceso sin `--session`, con disco/artefactos propios de fase1 y petición
original completa más cambio predefinido. No se inyecta seguimiento artificial. Se
mantiene modo SDD que el simulador seleccionó en fase1, sin heredar Gate3 para el
cambio material. Las respuestas de aprobaciones dentro de cada fase sí continúan
su sesión. No es prueba de compactación interna del proveedor ni continuidad de meses.

## Verificación y evidencia

Preflight real por brazo: prompt resuelto, tools, carga primaria por contenido,
lectura, edición READY→DONE y unittest ejecutado con resultado OK. Preflight/preparación
se informan aparte, no sumados al coste comparativo de tareas.
Congelación previa: código del arnés/tests/transporte, perfiles, baseline, contratos,
oráculos, referencias y procedencia/dependencias registradas. Verificar antes y después
de cada llamada. Los artefactos staticfiles derivados se excluyen del hash fuente;
se parte de la misma generación inicial y se conservan sus fuentes.

Evaluación en copia separada, restaurando archivos de tests originales; suite original
>=43 tests y suite externa con conteo esperado, exit0 para aceptar. Los tests aportados
por el agente también pueden ejecutarse, pero no sustituyen oráculos. Oráculos ajenos
al alcance del agente, nunca feedback entre fases. SQLite de evaluación en archivo
único por fase con conexiones/hilos independientes; T2 repite barrera tres veces.
MigrationExecutor verifica upgrade desde estado legacy a hojas finales. Cualquier
skip de upgrade adicional se informa, no equivale a evidencia verde de esa garantía.
Validar referencias frente a baseline y solución antes de freeze; no certificar
comportamiento solo por importar modelos ni porque el agente diga «terminado».

Guardar traza saneada al finalizar cada invocación, mensajes simulados, registros
inmutables por fase, hashes, evaluaciones y árboles finales. No razonamiento privado,
headers/credenciales ni payloads opacos de errores API. Captura no es streaming durable
por evento: si el recolector muere a mitad de una invocación, hay límite de evidencia.

## Permisos y límites de interpretación

Denegar secretos, delegación y herramientas de red; shell allowlist pruebas/Django y
git de lectura. Skills primaria y dominio con namespace. Edición fuera de celda y
oráculos/referencias/perfiles prohibida por alcance y límites externos del host.
Read general permite rutas relativas del host; external_directory restringe raíces.
No es aislamiento OS: código Python generado puede eludir límites textuales o de
herramienta. Auditar trazas; no acreditar sandbox universal ni control de red kernel.

Calidad funcional, fidelidad del flujo, omisiones y documentación consultada se
informan separadas. Tokens comparables=input+cache_read+cache_write+output; reasoning
aparte. Métricas ausentes desconocidas. Duración sumada de conversaciones no es wall
clock; los checks externos quedan fuera. Coste host no es factura. Sin significancia,
equivalencia universal ni promoción automática. No mezclar esta cohorte con anteriores.
Comparar coste entre soluciones correctas y mostrar también TODOS los intentos:
una solución incompleta barata no gana. Auditoría por criterios antes de recomendar.
