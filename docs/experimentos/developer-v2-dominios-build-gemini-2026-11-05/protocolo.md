# V2 candidato2 con consultas selectivas + build nativo — nueva cohorte

ID: v2-domains-build-v1-20261105. Modelo único solicitado:
`google/antigravity-gemini-3.8-flash`. No actualizar configuración persistente ni
agentes canónicos/instalados. No mezclar datos con cohortes previas.

## Objetivos

1. Asegurar consultas pertinentes de data-api/ui-design sin rutinas ajenas al dominio.
2. Comprobar que el cierre documental es independiente de esas cargas.
3. Comparar tarea Alta con Developer actual, ODD histórico, V2 candidato2 y build nativo.

V2 candidato2 solo aclara selección/carga de skills y cierre documental del candidato1.
No incorpora detalles específicos de reservas, soluciones ni oráculos.

## Comparación principal: doce celdas

TASK-2 literal del LocalLibrary documentado y commit previo. Mismo baseline, nueve
oráculos externos, SQLite en disco y >=43 tests originales restaurados en copia aparte.
Revalidar referencia antes de congelar. Tres repeticiones nuevas por brazo, hasta cuatro
procesos concurrentes, orden rotado entre repeticiones. 600s por llamada, steps60
configurado y máximo6 llamadas por celda; no afirmar hard cap de eventos SDK.

Developer/ODD conservan fuentes y sustituciones de nombres. V2 candidato2 tiene una
sola skill primaria. Skills de dominio idénticas normalizadas entre brazos.

Build usa `--agent build` real: comprobar `native:true`, ausencia de prompt sustituido
y no inyectar metodología MAS ni exigir skill primaria. Solo se igualan modelo,
temperatura, presupuesto y permisos del laboratorio. Se ofrecen skills de dominio
opcionales, pero se deniegan Developer/ODD/SDD y otras metodologías. No es un LLM
«sin instrucciones»: permanecen instrucciones nativas de OpenCode/proveedor y host.

Única diferencia de petición entre brazos: los especializados cargan su skill primaria;
build no recibe esa orden. No cambiar requisitos ni inyectarle un procedimiento propio.
El simulador responde únicamente un plan pedido antes de mutar producto, sin conceder
otro alcance. No se contesta feedback oculto ni se reintentan fallos selectivamente.

Aceptación funcional y carga correcta se informan por separado. En TASK-2 V2 debe
cargar ambas skills por contenido, sin bootstrap documental ni artefactos canónicos
no solicitados. Contar cargas, referencias, lecturas, seguimiento, herramientas,
pruebas y coste; cargar una skill no certifica aplicar todos sus estándares.

## Cinco comprobaciones focalizadas adicionales de V2

Sesión nueva por caso, no agregadas a las doce celdas ni a sus métricas:
- PLAN backend/API: cargar solo data-api, cero cambios.
- PLAN visual/CSS: cargar solo ui-design, cero cambios.
- PLAN función pura: ninguna skill de dominio, cero cambios.
- Cambio de saludo con documentación de uso canónica previa que queda obsoleta:
  implementar/probar, señalar ruta+motivo y proponer documentation-orchestrator;
  no actualizar documentación sin autorización ni bootstrap.
- Añadir test del saludo actual sin cambio funcional ni documental: ninguna carga
  de dominio ni recomendación documental innecesaria; código/docs originales intactos.

Las fixtures simples declaran la documentación de uso y su entrada para hacer
observable el cierre, no para imponer una metodología. No se exige al modelo una
lista de skills en la petición: se verifican llamadas y contenido de herramientas.
PLAN tiene shell/escritura deshabilitados por igual dentro de esos tres casos.
El cierre de las fixtures se revisa semánticamente; regex no certifica intención.
Una pasada focalizada no demuestra fiabilidad universal ni reemplaza el flujo real
de documentación tras selección manual del agente responsable.

## Evidencia y reglas de interpretación

Preflight real por cada brazo: prompt/identidad resuelta, lectura, edición y unittest;
en especializados contenido de skill primaria, en build identidad nativa en lugar
de fingir una carga inexistente. Congelar perfiles, candidato, scripts, fixtures,
contratos, baseline y oráculos ANTES de comprobaciones focalizadas y tareas.
No retocar candidato tras observar resultados. Todos los intentos en raíces exclusivas.

Error API/timeout/carga primaria o identidad incorrecta detiene nuevos bloques; fallos
funcionales o de selección se conservan. No comparar solo éxitos, no mezclar cohortes.
Tokens=input+cache_read+cache_write+output; reasoning aparte. Tiempo sumado no es
wall-clock ni espera humana; preparación y comprobaciones separadas. Coste host no
es factura. Caché y host no completamente herméticos, permisos no son sandbox OS.

Para considerar corregido el comportamiento en esta muestra: V2 debe consultar ambas
skills en3/3 celdas Alta y acertar los cinco casos focalizados, sin ingeniería/documentos
ajenos al alcance. Para eficiencia descriptiva frente a cada control: 3/3 funcionales,
ahorro agregado >=10% tokens, tiempo no peor en más de10% y ahorro tokens en>=2/3
repeticiones. Reportar si no cumple sin cambiar umbrales. No instalar/promover por
una sola tarea, ni equiparar igual tasa funcional con equivalencia integral de agentes.
