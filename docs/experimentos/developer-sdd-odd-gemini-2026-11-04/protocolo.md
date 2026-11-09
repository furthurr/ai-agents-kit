# Protocolo — Developer, SDD y ODD con Gemini

Identificador: `gemini-three-way-v1-20261104`. Fecha de diseño: 2026-11-04.
La congelación efectiva, anterior a las celdas, se guarda en `evidencia/freeze.json`.
No se usa el reporte Gemini anterior como comparación validada.

## Pregunta y alcance

Con el mismo modelo e integración, ¿qué diferencias observables presentan los
tres flujos en calidad, fidelidad metodológica, herramientas, tiempo y tokens?
Se busca orientar la elección según tarea, no demostrar un ganador universal.

Modelo: `google/antigravity-gemini-3.8-flash`. Host: versión real registrada al
congelar. Developer y SDD proceden de los derivados OpenCode actuales del MAS;
ODD es el tratamiento adaptado conservado, sin Engram, RDD ni delegación nativa.
ODD no se implementa ni se registra en el catálogo del kit para este ensayo.

## Tratamientos y control del host

Tres agentes temporales con selección explícita `--agent g3-developer`,
`g3-sdd` y `g3-odd`. Skills y referencias con namespaces propios `g3d-`, `g3s-`
y `g3o-`: no hay colisión con `developer` o `sdd-spec` de la instalación habitual.
Las sustituciones son de identificadores; las reglas fuente se conservan.
[Definición y fuentes](tratamientos.md).

Se conserva la configuración habitual que carga el plugin Antigravity y su
autenticación. No se lee/copia ningún almacén de credenciales ni se exporta la
configuración global. No se usa `--pure` ni se cambia XDG: esos controles impedían
la integración. La configuración experimental se inyecta por proceso, con roles,
prompts, permisos y rutas de skills explícitos, sin cambiar defaults persistentes.

El preflight comprueba por brazo: prompt resuelto, tools disponibles, contenido
íntegro de la skill primaria en la traza, lectura, edición efectiva y unittest.
No se acepta «PREFLIGHT_OK» como prueba si el archivo no cambió o falló la carga.
Un primer preflight falló por patrones de rutas absolutas en reglas que el host
resuelve relativamente; se corrigió antes de las celdas y se repitió en otra raíz.
Ese intento no se agrega a los resultados de tareas. El resto del host/config y
plugin no es un snapshot completamente hermético: se declara ese límite.

Permisos de roles: lectura/búsqueda y edición local; unittest, py_compile,
git status/diff; skills primaria y dominios data-api/ui-design del namespace.
Sin task, question, webfetch o websearch; sin commits, instalaciones ni red del
agente. Permanecen deny de secretos. El límite de directorios externos permite
el fixture y los recursos del perfil. No es sandbox OS: el código Python escrito
por un agente no queda aislado por una instrucción de prompt.

Consulta S10: shell/escritura deshabilitados simétricamente. Plan S09: edición
de Python deshabilitada; las reglas del flujo determinan si produce un documento
formal o plan en respuesta. Los checks externos no son herramientas del agente.

## Escenarios y aceptación fijada

Las tareas originales, archivos, soluciones de referencia y oráculos se conservan
en la congelación/fixtures del experimento. Proceden de declaraciones de
`tools/odd_vs_sdd_experiment.py`, cuyo hash actual se fija; no se llama su runner
ni se modifica su evidencia anterior. S08 recibe una petición neutral de
reanudación y documentos equivalentes por flujo.

| ID | Tipo de trabajo | Aceptación externa común |
|---|---|---|
| S01 | Documento pasivo | Solo corregir la errata exacta, ningún archivo adicional. |
| S02 | Función pura pequeña | Espacios, Unicode, caja y fallback exactos. |
| S03 | Feature con seis reglas | Normalización, orden/deduplicación, límite, errores y no mutación. |
| S04 | Bug monetario | Decimal y HALF_UP al final, negativos y legado. |
| S05 | CLI compartida | Opción local, salidas/errores exactos y comando hermano intacto. |
| S06 | Reglas literales extensas | Doce reglas: mensajes, orden, Unicode y validación de filas ocultas. |
| S07 | Persistencia ante fallo | Validación sin alterar bytes; replace real, error y limpieza. |
| S08 | Reanudación | Preservar T1 y completar T2 reutilizando helper; sesión nueva con estado sembrado. |
| S09 | Solo planificación | Criterios y pruebas propuestas; sin código ni verificación inventada. |
| S10 | Consulta/instrucción incrustada | Diagnóstico de división por cero, cero escrituras y no sentinel. |

Los oráculos se validan sobre baseline y solución antes de inferencia. Se ejecuta
externamente la suite entregada y el código original de tests sobre la solución
final. Un unittest vacío no es éxito funcional. Los archivos iniciales se añaden
al índice de un Git temporal sin commits: git diff sí puede contrastar cambios.
No se toca el índice del repositorio del usuario.

## Selección de profundidad y simulación de usuario

No forzar Tiny a todas las features. En SDD, excepto consulta y reanudación,
primero se pide recomendación natural sin artefactos/código, con campo
`Recomendación: Direct|SDD-Tiny|SDD-Lite`. El simulador acepta esa recomendación
elegible, confirma el mismo alcance y selecciona el modo en un turno separado.
No selecciona Standard ni infiere un modo de un score. Si la respuesta no ofrece
recomendación interpretable, se registra incumplimiento, no se inventa una elección.

Tiny: spec antes del código, aprobación explícita Gate 3, implementación/pruebas,
aprobación Gate 4. Lite/Direct no reciben esos gates. S08 conserva Tiny histórico
con Gate 3 aprobado expresamente en la petición, no por existir un archivo.
Developer puede pedir aprobación de un plan; el simulador aprueba solo el alcance
original cuando existe una propuesta y el producto aún no ha cambiado. Lo mismo
aplica a una pausa equivalente de ODD, sin añadirle aprobaciones obligatorias.

Los mensajes del simulador están en el runner congelado. No equivalen a una
revisión humana semántica de cada spec ni miden minutos humanos. No se aprueba una
ampliación, no se responde a decisiones funcionales nuevas y no se reintenta tras
error de proceso. Máximo previsto cuatro invocaciones/celda, incluida conversación
metodológica; 32 pasos y 240 s por invocación. Sesiones únicas por celda, continuadas
solo por su ID para respuestas de usuario. Sin compartir memoria autorizada.

## Ejecución y orden

Filtro: 10 escenarios × 3 brazos × 1 repetición = 30 celdas. Si preflight y controles
son válidos y no hay errores de integración/acceso, ejecutar r2 y r3: 90 acumuladas.
Un fallo funcional ordinario no se elimina ni por sí solo impide replicación.
Errores de API, accesos externos o contaminación de skill en el filtro detienen
la replicación; se informa el límite y no se cambia configuración en medio.

Tres procesos concurrentes como máximo. Orden de presentación contrabalanceado
por escenario/repetición con seis permutaciones fijadas en el runner. La concurrencia
no controla finalización ni caché del proveedor. No sobrescribir directorios o
registros, no reutilizar únicamente éxitos y no repetir celdas fallidas. Cualquier
cambio de entradas exige nueva versión/raíz y conservar el incidente anterior.

## Métricas

Por celda: aceptación funcional, entrega conforme al flujo, carga primaria por
contenido, errores API, timeouts, errores de tools, llamadas malformadas, accesos,
documentos, modo SDD, invocaciones, respuestas de usuario, herramientas y pasos.
Tiempo medido de inicio a fin de la conversación CLI, sin espera humana real;
los checks externos posteriores quedan fuera. Separar mediana por tarea y suma
de duraciones; no llamar a la suma tiempo de reloj del lote.

Tokens: input, cache-read/write, output; total comparable = suma de esos cuatro.
Reasoning se informa aparte; puede estar incluido en output. Coste reportado es
solo lo expuesto por host, no factura. Ausencia de métricas = desconocido, no cero.
Separar éxitos de intentos parciales, sin eliminar los últimos del ledger.

Capturar trazas con allowlist: no contenido de razonamiento privado, headers,
cookies, cuerpos arbitrarios de errores o metadata opaca del proveedor. Conservar
outputs de herramientas sobre datos sintéticos, snapshots, mensajes de usuario y
hashes. El contenido de credenciales no se usa como entrada experimental.

## Juicio y recomendaciones fijados antes de ejecutar

1. Calidad/alcance/integridad primero. Menor coste con entrega incorrecta no es
   una victoria. Informar aceptación funcional y fidelidad por separado.
2. Para proponer preferencia descriptiva en una tarea, exigir 3/3 entregas
   funcionales/conformes del flujo candidato y ausencia de regresiones esenciales.
   Comparar mediana de tokens y duración; si una mejora y otra empeora, trade-off.
3. Una reducción inferior al 10 % se trata como diferencia pequeña, no preferencia
   robusta por eficiencia. Tres repeticiones sintéticas no prueban significancia
   estadística ni generalización a proyectos reales.
4. Si todos pasan, hay efecto techo: no afirmar mejora de calidad por gastar menos.
   El número de documentos o gates no es calidad por sí mismo.
5. Registrar casos donde SDD/Developer/ODD no cumplen su contrato aunque el código
   pase. No atribuir al modelo un error de integración sin evidencia causal.
6. Las recomendaciones combinarán evidencia con el propósito de cada flujo:
   implementación general, especificación explícita o continuidad proporcional.
   No declarar que «SDD siempre es más lento» ni promover ODD globalmente por este lote.
7. Si el lote queda incompleto/no interpretable, cerrar como parcial y no seleccionar
   un subconjunto favorable para aprobar una metodología. No integrar agentes al MAS.

## Límites previstos

Un modelo/host/plugin, escenarios Python sintéticos, estado de recuperación
sembrado y no compactación real, sin UI/API distribuida ni colaboración humana.
Longitud de instrucciones y método varían juntos. La instalación habitual aporta
instrucciones comunes y plugin; no se afirma hermeticidad completa. Los controles
estáticos son distintos de la evidencia runtime de cada celda. La evaluación del
coordinador no es ciega. Se conserva el histórico, no se reparan retrospectivamente
las pruebas Gemini anteriores.
