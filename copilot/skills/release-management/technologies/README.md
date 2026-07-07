# Perfiles de tecnología (caché de auto-extensión)

Esta carpeta almacena los **perfiles de release** generados por la
auto-extensión de la skill `release-management` (Paso 1.5). Cada archivo
`<slug>.md` describe cómo versionar, taggear y generar el CHANGELOG de una
tecnología **no** cubierta de fábrica (Android/iOS/Flutter).

Al detectar una tecnología nueva, la skill:
1. Busca aquí un perfil existente y vigente; si lo hay, lo reutiliza.
2. Si no existe, investiga las convenciones en la web (docs oficiales).
3. Genera el perfil con la plantilla estándar y, tras confirmación del usuario,
   lo guarda aquí para reutilizarlo en cualquier proyecto.

## Convención

- Nombre: `<slug>.md` en minúsculas (p. ej. `node.md`, `rust.md`, `dotnet.md`).
- Contenido: señales de detección, archivo(s) y clave de versión, formato,
  reglas de bump, herramienta CLI, convención de tag, CHANGELOG, notas y fuentes.

> No incluyas secretos ni credenciales en los perfiles.
