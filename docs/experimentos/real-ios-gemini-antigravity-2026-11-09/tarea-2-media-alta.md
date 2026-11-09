# Tarea 2: Media-Alta — Remediación QLT-0017 y Gestión de Altas en Conflicto (iOS)

**Identificador:** `GIOS-BUZON-RETRY-UI`  
**Complejidad:** Media-Alta  
**Capa Afectada:** `FixtureProject/FixtureProject/Presentacion/` (SwiftUI / ViewModels)

---

## Contexto y Hallazgo de Calidad (QLT-0017)

En la aplicación móvil iOS, el acceso al buzón offline de altas pendientes no debe ocultarse si ocurre un error de lectura o si existen altas rechazadas en conflicto con el servidor. Ocultar el botón ante un fallo bloquea al ejecutivo impidiéndole revisar o reintentar sus operaciones.

## Alcance Técnico Requerido

### 1. Modelo de Estado de Acceso al Buzón
En `FixtureProject/FixtureProject/Presentacion/Features/Chat/EstadoAccesoBuzon.swift` (o ubicación análoga en Presentacion):
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


### 2. ViewModel de Buzón (`BuzonSalidaViewModel`)
En `FixtureProject/FixtureProject/Presentacion/Features/Chat/BuzonSalidaViewModel.swift`:
Implementar o extender el ViewModel observable:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


---

## Verificación Requerida
- Crear suite de pruebas unitarias en `FixtureProject/FixtureProject Tests/Presentacion/BuzonSalidaViewModelTests.swift`.
- Las pruebas deben verificar:
  1. Estado inicial y transición a disponible con conteo de altas.
  2. Cumplimiento de QLT-0017: `estadoAcceso.tieneAltasVisibles == true` ante estado `.error`.
  3. `reintentarAltaEnConflicto`: cambia una acción de `.failed` a `.pending` y refresca.
  4. ID inexistente o estado no fallido no muta la cola ni lanza excepciones.
