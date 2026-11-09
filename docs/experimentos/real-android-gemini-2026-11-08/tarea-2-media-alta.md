# Tarea 2: Media-Alta — Remediación QLT-0017 y Gestión de Altas en Conflicto (GBA-BUZON-RETRY-UI)

Implementa directamente la remediación del hallazgo de fiabilidad `QLT-0017` en `AccesoBuzon.kt` y la acción de reintento de altas en `CONFLICTO` en `BuzonSalidaViewModel.kt`.

## Alcance y Autorización
El alcance está plenamente autorizado para implementación y verificación inmediata en esta sesión. Trabaja únicamente en este workspace. No hagas commits, no uses red externa ni crees archivos fuera de las rutas especificadas.

---

## Archivos Exactos a Modificar y Crear

### 1. `app/src/main/java/com/example/mobilefixture/tests1/features/offline/buzon/AccesoBuzon.kt`
1. Modelar un estado sellado en el mismo archivo:
> Fragmento de implementación original omitido; usar fixtures sintéticos.

2. En `AccesoBuzonViewModel`:
   - Exponer `val estadoAcceso: StateFlow<EstadoAccesoBuzon>`
   - Implementar `fun reintentar()` que reejecute `refrescar()`.
   - Si `cola.todas()` arroja una excepción, transicionar `estadoAcceso` a `EstadoAccesoBuzon.Error(e)` y **mantener `hayAltas.value = true`** para que el acceso al Buzón no se oculte ante errores de lectura (remediando QLT-0017).
3. En la función `@Composable fun buzonPendientesVisibles()`:
   - Ante error de lectura, debe retornar un valor no nulo (para que la nube o botón permanezca visible y accesible para el usuario).

### 2. `app/src/main/java/com/example/mobilefixture/tests1/features/offline/buzon/BuzonSalidaViewModel.kt`
1. Agregar la función pública:
> Fragmento de implementación original omitido; usar fixtures sintéticos.

2. Comportamiento:
   - Si la acción existe y está en `EstadoPendiente.CONFLICTO`:
     * Llama al almacén para actualizar su estado a `EstadoPendiente.PENDIENTE` y limpiar `motivoError = null`.
     * Refresca la lista de altas observables del ViewModel.
   - Si la acción no existe o no está en `CONFLICTO`, ignora la operación de manera segura sin lanzar excepciones.

---

## Verificación Requerida
- Modificar o crear pruebas en:
  `app/src/test/java/com/example/mobilefixture/tests1/features/offline/buzon/AccesoBuzonViewModelTest.kt`
- Ejecutar verificación: `./gradlew :app:testDebugUnitTest --tests "com.example.mobilefixture.tests1.features.offline.buzon.*" --console=plain`
- Informar resultados y límites observados.
