# Tarea 3: Alta — Deduplicación Atómica, Concurrencia y Cifrado en Cola Offline (iOS)

**Identificador:** `GIOS-QUEUE-CONCURRENCY-CIPHER`  
**Complejidad:** Alta  
**Capa Afectada:** `FixtureProject/FixtureProject/Presentacion/Features/Chat/` (o capa de persistencia Data)

---

## Contexto y Requerimiento de Negocio

La cola offline de acciones pendientes de iOS CRM (`FixtureComponent1`) debe ser resistente ante múltiples llamadas concurrentes generadas por procesos en segundo plano o el motor de sincronización. Además, debe implementar deduplicación atómica de operaciones idempotentes y proteger la confidencialidad de los payloads sensibles mediante cifrado AES-GCM (CryptoKit).

## Alcance Técnico Requerido

### 1. Inserción Idempotente y Deduplicación
En `FixtureComponent1.swift`:
Implementar la función pública:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


**Comportamiento de deduplicación:**
- Deduplica lógicamente por la tupla `(action, entityName, payload)` contra acciones en estado no terminal (`.pending` o `.sending`).
- Si ya existe una acción no terminal con los mismos valores:
  * **No duplicar ni sobreescribir** el elemento en la cola.
  * Retornar el `id` (UUID) de la acción existente.
- Si no existe:
  * Cifrar el campo sensible `payload` utilizando `CryptoKit` (`AES.GCM`) o clave simétrica AES-256.
  * Persistir la nueva acción y retornar su `action.id`.

### 2. Concurrencia y Exclusión Mutua Atómica
- La ejecución debe ser estrictamente segura ante ejecuciones concurrentes simultáneas (`thread-safe`), empleando un `NSLock`, `NSRecursiveLock` o aislamiento mediante `actor` de Swift.
- Evitar condiciones de carrera (*race conditions*) cuando 10 o más corrutinas/hilos llamen a `enqueueIdempotente` al mismo milisegundo.

### 3. Cifrado y Descifrado Transparente
- Al persistir, el `payload` debe almacenarse cifrado en Base64 con AES-256-GCM.
- Al invocar `loadAll()` o `loadPending()`, los payloads deben descifrarse automáticamente y devolverse en texto plano a los consumidores de la aplicación.

---

## Verificación Requerida
- Crear suite de pruebas unitarias en `FixtureProject/FixtureProject Tests/App/ViewModels/FixtureComponent2ConcurrencyTests.swift`.
- Las pruebas deben verificar:
  1. **Idempotencia:** dos llamadas con el mismo payload devuelven el mismo UUID y el tamaño de la cola no aumenta.
  2. **Diferenciación:** si el estado es `.completed`, una nueva llamada sí debe crear una nueva acción.
  3. **Concurrencia real:** disparar 20 tareas concurrentes con `TaskGroup` o `DispatchQueue.concurrentPerform`; la cola debe contener exactamente 1 elemento y todas las tareas deben recibir el mismo UUID.
  4. **Cifrado observable:** verificar que los datos en `UserDefaults` crudo contienen el payload cifrado (no en texto plano).
