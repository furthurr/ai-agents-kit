# Tarea 1: Media-Baja — Búsqueda, Filtrado y Normalización de Prospectos (iOS)

**Identificador:** `GIOS-SEARCH-PROSPECTS`  
**Complejidad:** Media-Baja  
**Capa Afectada:** `FixtureProject/FixtureProject/Domain/` y `FixtureProject/FixtureProject/Data/`

---

## Contexto y Requerimiento de Negocio

En el módulo de Cartera de Prospectos de iOS CRM, los ejecutivos requieren buscar prospectos en memoria de forma reactiva y determinista. La búsqueda debe tolerar acentos, variaciones de mayúsculas/minúsculas y espacios accidentales al inicio o fin.

## Alcance Técnico Requerido

### 1. Modelo de Dominio
En `FixtureProject/FixtureProject/Domain/Entities/`:
Asegurar la entidad `ProspectoItem`:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


### 2. Caso de Uso de Búsqueda y Normalización
Crear en `FixtureProject/FixtureProject/Domain/UseCases/SearchProspectsUseCase.swift`:
> Fragmento de implementación original omitido. Usar únicamente fixtures sintéticos.


**Reglas de normalización y filtrado:**
1. **Normalización del Query:**
   - Aplicar `trimmingCharacters(in: .whitespacesAndNewlines)`.
   - Si la consulta normalizada está vacía (`isEmpty`), retornar la lista completa de prospectos sin filtrar.
   - Eliminar acentos y diacríticos (`folding(options: .diacriticInsensitive, locale: .current)` o similar).
   - Comparación insensible a mayúsculas/minúsculas (`caseInsensitive`).
2. **Criterios de Coincidencia:**
   - Un prospecto coincide si el término normalizado está contenido en:
     * Nombre completo (`"\(nombre) \(apellidoPaterno) \(apellidoMaterno)"`)
     * O en el `rfc` (normalizado sin guiones ni espacios).
3. **Ordenamiento:**
    - Retornar los resultados ordenados alfabéticamente por `apellidoPaterno`, luego `apellidoMaterno`, luego `nombre`, ignorando mayúsculas y diacríticos en esas claves.

---

## Verificación Requerida
- Crear suite de pruebas unitarias en `FixtureProject/FixtureProject Tests/Domain/SearchProspectsUseCaseTests.swift`.
- Las pruebas deben verificar: coincidencia exacta, coincidencia parcial, insensibilidad a acentos/diacríticos ("José" encuentra "Jose"), espacios en blanco y query vacío.
