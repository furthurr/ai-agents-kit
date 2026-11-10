# Tarea 1: Media-Baja — Búsqueda, Filtrado y Normalización de Prospectos (GBA-SEARCH-PROSPECTS)

Implementa directamente el caso de uso `FixtureSource1` y su modelo de resultado en el módulo `:core:domain`.

## Alcance y Autorización
El alcance está plenamente autorizado para implementación y verificación inmediata en esta sesión. Trabaja únicamente en este workspace. No hagas commits, no uses red externa ni crees archivos fuera de las rutas especificadas.

---

## Archivos Exactos a Crear

### 1. Modelo de Salida: `core/domain/src/main/java/mx/com/bancadigital/crm/domain/model/prospect/FixtureSource3.kt`
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


### 2. Caso de Uso: `core/domain/src/main/java/mx/com/bancadigital/crm/domain/use_case/prospect/FixtureSource1.kt`
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


### 3. Reglas de Negocio Requeridas:
1. **Búsqueda por Texto (`query`):**
   - Si `query` es `null`, vacío o solo espacios tras `trim()`, **no** filtra por texto.
   - Si contiene texto, busca como subcadena insensible a mayúsculas/minúsculas y diacríticos/acentos (`Normalizer.normalize(..., Normalizer.Form.NFD)` o similar) en:
     - `razonSocial`
     - `rfc`
     - `nombreEmpleado`
2. **Filtro por Tipo de Cliente (`tipoCliente`):**
   - Si `tipoCliente` no es nulo ni vacío tras `trim()`, filtra coincidencia exacta (ignorando mayúsculas/minúsculas) con `prospect.tipoCliente` o `prospect.idTipoCliente`.
3. **Filtro por Marca de Gestión (`soloGestionados`):**
   - Si `soloGestionados == true`, solo incluye prospectos con `marcaGestion != null`, no vacío y diferente de `"0"`.
4. **Ordenamiento:**
   - La lista `items` resultante debe ordenarse por `razonSocial` ascendente ignorando acentos y mayúsculas.
   - Elementos con `razonSocial` nulo o vacío van al final, ordenados secundariamente por `rfc` ascendente.
5. **Métricas:**
   - `totalCount`: Cantidad de prospectos en `items`.
   - `gestionadosCount`: Cantidad de prospectos en `items` con `marcaGestion` activa (diferente de null, vacío o `"0"`).
6. **Inmutabilidad y Preservación:**
   - No muta la lista original; preserva la suite existente de `:core:domain:test`.

---

## Verificación Requerida
- Crear pruebas unitarias completas en:
  `core/domain/src/test/java/mx/com/bancadigital/crm/domain/use_case/prospect/FixtureSource2.kt`
- Ejecutar verificación: `./gradlew :core:domain:testReleaseUnitTest --console=plain`
- Informar resultados y límites observados.
