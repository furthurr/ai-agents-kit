# Configuración de releases

## Fuente y formato

- La versión canónica vive en `VERSION` como SemVer puro: `MAJOR.MINOR.PATCH`.
- No se usa build number porque MAS no es una aplicación móvil ni un paquete
  publicado por un gestor de dependencias.
- El CHANGELOG canónico vive en `CHANGELOG.md` y antepone cada nueva versión.

## Flujo

1. Revisar los cambios desde el último tag y ejecutar `python3 tools/render.py`.
2. Ejecutar `python3 tools/validate.py` y la suite completa del repositorio.
3. Actualizar `VERSION` y añadir la entrada correspondiente en `CHANGELOG.md`.
4. Crear un commit Conventional Commit de release.
5. Crear el tag anotado `vX.Y.Z` sobre el commit de release.
6. Publicar rama y tag solo después de confirmación explícita.

## Bump SemVer

- `MAJOR`: breaking change o incompatibilidad de contrato.
- `MINOR`: nueva capacidad compatible (`feat`).
- `PATCH`: corrección, documentación, refactor o mantenimiento compatible.

La primera release de este repositorio es `0.1.0`; mientras permanezca en `0.x`,
la compatibilidad todavía no se considera estable.
