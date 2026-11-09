# Análisis: Desventajas de omitir `data-api` y `ui-design` y Causa de Interrupción en Gemini 3.8

Fecha: 2026-11-08.
Contexto: Evaluación comparativa de ODD Original vs. ODD Ajustado con Estándares en LocalLibrary TASK-2.

---

## 1. Desventajas de omitir `data-api` y `ui-design`: ¿Es bueno o malo?

En el diseño arquitectónico del MAS y en la ingeniería de software del repositorio, **omitir estas skills es MALO**.

Aunque en métricas de laboratorio a corto plazo parezca atractivo porque consume menos tokens y termina más rápido, representa un **falso ahorro** (ahorro por degradación de estándares).

### A. Desventajas de no cargar `data-api`
1. **Contratos JSON improvisados:** Sin la skill, el agente estructura respuestas según su propia inercia (ej. variando entre `{ "error": "..." }`, `{ "detail": "..." }` o códigos 200 con cuerpo de fallo).
2. **Códigos de estado HTTP incorrectos:** Tiende a responder con códigos genéricos en lugar de códigos semánticos (`400`, `401`, `404`, `409`, `422`).
3. **Persistencia e idempotencia frágil:** Omite convenciones críticas del proyecto sobre transacciones atómicas, manejo de bloqueos en SQLite/PostgreSQL y claves de idempotencia en cabeceras HTTP.
4. **Ruptura de consumidores:** Otros clientes o módulos que esperan contratos estrictos fallan silenciosamente.

### B. Desventajas de no cargar `ui-design`
1. **Pérdida del Sistema de Diseño (Design System):** Escribe estilos CSS directos en línea o clases arbitrarias, rompiendo la coherencia visual con el resto del proyecto.
2. **Omisión de Accesibilidad (a11y):** Suele omitir atributos `aria-*`, roles semánticos, contraste adecuado y navegación mediante teclado.
3. **Ausencia de estados de interfaz:** Se concentra únicamente en el caso exitoso (*happy path*), ignorando el estado de carga (*loading spinner*), mensajes de error visibles y estados vacíos (*empty state*).
4. **Fragmentación de la experiencia:** La aplicación parece desarrollada por equipos inconexos.

### C. El efecto del oráculo limitado en los benchmarks
Los tests sintéticos (`manage.py test` u oráculos) solo evalúan lo que está explícitamente en sus `asserts`. Si un test solo valida que una reserva devuelva status 201 y guarde en base de datos, un código sin accesibilidad, sin estilos del sistema y con JSON inconsistente pasará en verde. Ahorrar tokens saltándose la calidad no es eficiencia: es generación de deuda técnica.

---

## 2. Diagnóstico de la Interrupción en Gemini 3.8 Flash (Cohorte v1)

En la ejecución del lote `odd-standards-gemini38-v1-20261108`, ambos brazos se interrumpieron por causas distintas:

### A. ODD Histórico (Original R1)
- **Estado real:** **Completó la tarea al 100 %**.
- **Evaluación:** Pasó las 43 pruebas originales de LocalLibrary y los 9 oráculos externos (`functional_pass: True`).
- **Causa de interrupción:** Tardó exactamente **600,183 segundos**. El arnés tenía un límite rígido de 600,000 s (`limit=600`). Por apenas **183 milisegundos**, el supervisor envió señal SIGTERM (`returncode: -15`, `timeout: True`), marcando la celda como fallida por proceso.

### B. ODD Ajustado con Estándares (Ajustado R1)
- **Estado real:** Cargó ambas skills (`data-api` y `ui-design`) antes del primer cambio de código, cumpliendo el estándar.
- **Causa de interrupción:** `APIError: statusCode 400 (Bad Request)` proveniente de GitHub Copilot en el paso 125.
- **Mecanismo del fallo:**
  1. Al cargar las dos skills completas (más de 23.000 caracteres de instrucciones) y ejecutar exploraciones con `glob` que devolvieron árboles enteros de archivos, el contexto base inicial fue muy alto (~20k tokens).
  2. En lugar de implementar directamente, el agente decidió crear un archivo de seguimiento persistente `odd/tasks/reservation.md` y actualizarlo con `todowrite` en cada micro-paso (más de 20 operaciones redundantes de edición/lectura).
  3. En el paso 125 (a los 570 segundos), el prompt acumulado en la conversación alcanzó **100.312 tokens** (`cache_read: 95.756`).
  4. El endpoint de GitHub Copilot para Gemini 3.8 Flash tiene un límite máximo de contexto por petición de ~96k-100k tokens. Al superar este umbral, la API rechazó la solicitud con HTTP 400.

---

## 3. Plan de Solución para el Reintento (Cohorte v2)

1. **Ajuste de Timeout:**
   Elevar el timeout por invocación de 600 s a **1200 s** (20 minutos), replicando el diseño validado en la cohorte `odd-standards-luna-1800` para evitar cortes artificiales por milisegundos en tareas Django completas.
2. **Alineación con el Acuerdo de Continuidad:**
   En `CONTINUAR-AQUI.md` se acordó que en tareas pequeñas/medianas no se deben crear archivos de seguimiento persistente (`odd/tasks/`) si la tarea y el diff bastan para reanudar. Reforzar esta regla en el prompt simétrico para evitar las 20 llamadas redundantes de micro-log que saturaron los 100k tokens.
3. **Concurrencia Controlada:**
   Ejecutar las celdas de forma secuencial (`max_workers=1`) o con aislamiento estricto para evitar contención de red y latencia en las llamadas concurrentes a la API.
