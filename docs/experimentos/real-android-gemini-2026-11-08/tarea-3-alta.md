# Tarea 3: Alta — Deduplicación Atómica, Cifrado por Campo y Concurrencia en Cola Offline (GBA-QUEUE-CONCURRENCY-CIPHER)

Implementa garantías de deduplicación atómica, cifrado por campo obligatorio y recuperación de candados huérfanos en `OfflineQueueStore.kt`.

## Alcance y Autorización
El alcance está plenamente autorizado para implementación y verificación inmediata en esta sesión. Trabaja únicamente en este workspace. No hagas commits, no uses red externa ni crees archivos fuera de las rutas especificadas.

---

## Archivos Exactos a Modificar y Crear

### 1. `core/data/src/main/java/com/example/mobilefixture/data/local/offline/OfflineQueueStore.kt`
1. Agregar e implementar el método de inserción idempotente con exclusión mutua / transacción:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.

   - Deduplicación lógica por `(idEjecutivo, rfc, tipoDeAlta)`.
   - Si ya existe una acción no terminal (`PENDIENTE` o `ENVIANDO`) con la misma clave `(idEjecutivo, rfc, tipoDeAlta)`, no duplica ni sobreescribe: retorna el `idLocal` de la acción existente. Distintos tipos de alta son acciones independientes.
   - Si no existe: cifra `idEjecutivo`, `payload` y `rfc` con `WrappedKeyCipher` e inserta la nueva entidad, retornando `accion.idLocal`.
   - Ejecución atómica y segura ante múltiples corutinas simultáneas (usando un `Mutex` o bloque transaccional).
2. Agregar e implementar el método de recuperación de bloqueos:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.

   - Busca acciones con estado exactamente `EstadoPendiente.ENVIANDO` cuyo `actualizadoEn < (ahora - timeoutMillis)`.
   - Transiciona su estado a `EstadoPendiente.PENDIENTE` y actualiza `actualizadoEn = ahora`.
   - **Regla de seguridad:** NUNCA altera acciones en estado `AMBIGUO` ni `CONFLICTO`.
   - Retorna la cantidad de acciones recuperadas.
3. Preservar intactos los métodos existentes de `OfflineQueueStore` y su suite de pruebas.

---

## Verificación Requerida
- Crear pruebas unitarias y de concurrencia en:
  `core/data/src/test/java/com/example/mobilefixture/data/local/offline/OfflineQueueStoreConcurrencyTest.kt`
- Ejecutar verificación: `./gradlew :core:data:testReleaseUnitTest --console=plain`
- Informar resultados y límites observados.
