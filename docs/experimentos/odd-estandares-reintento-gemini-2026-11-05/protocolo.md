# Reintento completo de ODD con estándares — lote independiente

ID: odd-standards-retry-v1-20261105. Autorización actual del usuario:
«puedes reintentar para terminar la prueba ?».

El lote anterior `odd-standards-v1-20261105` permanece PARCIAL e intacto: cuatro
intentos, un timeout del control original en R2. Este lote NO lo completa ni
reemplaza selectivamente ese fallo. Nueva raíz, nuevos procesos/sesiones y seis
celdas nuevas: ODD original y ODD ajustado por tres repeticiones cada uno.

## Invariantes

Mismo modelo solicitado `google/antigravity-gemini-3.8-flash`, mismo host/plugin,
agentes/skills byte a byte, namespaces, task TASK-2 literal, baseline LocalLibrary,
documentación, referencia y nueve oráculos del lote anterior. Mismos permisos y
temperatura, steps60 configurado,600s por invocación y máximo6 invocaciones por celda.
No aumentar timeout, cambiar el ajuste ni instalar nada para conseguir éxitos.

Verificar inputs congelados del lote parcial antes de copiar. Congelar la nueva raíz
antes de inferencia comparativa y comprobar equivalencia de contenidos/configuración
normalizando solo rutas. Nuevo preflight real por brazo y referencia revalidada.
El wrapper nuevo aporta identidad/procedencia y preparación exclusiva, no cambia
el runner de celdas ni su simulador. Código y freeze anteriores no se editan.

Los cinco checks focalizados de selección/cierre documental ya ejecutados se
referencian con su procedencia; **no se vuelven a ejecutar ni se cuentan como nuevos**.
No forman parte de métricas de las seis celdas. No incorporar datos del lote parcial
como controles de este lote ni agregar cohortes para mejorar porcentajes.

## Ejecución y análisis

Hasta dos procesos concurrentes, original/ajustado en R1/R3 y ajustado/original en R2.
Sesión independiente por celda, sin feedback externo al modelo. Solo aprobación de
plan solicitada antes de código y limitada al alcance original. Todos los fallos se
conservan. Un nuevo timeout/error de proceso, API, configuración o carga detiene
nuevas repeticiones de este lote; no bucle de reintentos hasta lograr verde. Un fallo
funcional ordinario se evalúa y conserva sin cambiar el tratamiento.

Evaluación en copia separada con los43 tests originales restaurados y nueve tests
externos, SQLite en disco y concurrencia real según el oráculo heredado. Comprobar
skills por contenido y orden respecto a escrituras, documentación consultada,
seguimiento, pruebas, cierre y comportamiento fuera de alcance. Una carga no
certifica aplicación exhaustiva de estándares ni riesgo acumulativo eliminado.

Si se completan seis conversaciones saludables, presentar este lote completo por
separado. Si no, declararlo parcial también. Informar explícitamente el timeout
histórico y todos los intentos: no afirmar que nunca hubo fallos por mostrar solo
este reintento. n=3/un proyecto/modelo no prueba significancia. Diferencias<10%
son cercanía descriptiva. No imponer un ahorro obligatorio al ajuste ni ocultar coste.

Tokens=input+cache_read+cache_write+output, reasoning aparte; tiempo sumado no es
wall-clock ni espera humana, checks externos fuera. Cache no equivale a factura.
Permisos no son sandbox OS. No perfiles reales, commits/push, release, cambios
canónicos ni modificaciones del plan Developer del Escritorio.
