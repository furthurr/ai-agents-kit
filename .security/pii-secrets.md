# Inventario de PII y secretos

| Dato | Tipo | Dónde aparece | Cifrado | Almacenamiento | Notas |
|------|------|---------------|---------|----------------|-------|
| Identidad y contacto público del autor | Dato personal de contacto | `README.md:117-122` | No aplica; publicado intencionalmente | README versionado | No se reproducen los valores en este inventario. |
| Contenido de configuración importado desde hosts | Puede contener instrucciones, datos sensibles o credenciales del usuario | `imports/` se ignora en Git (`.gitignore:21-22`) | Desconocido | Copia local ignorada | No se inspeccionó el contenido de importaciones locales; evitar promoverlas sin revisión. |
| Secretos tipo token/clave conocidos | No detectados por la búsqueda estática de formatos comunes | Repositorio inspeccionado | No aplica | No se observó una ubicación | La búsqueda incluyó cabeceras PEM y formatos comunes de tokens; no es un escáner exhaustivo de secretos ni detecta todas las credenciales posibles. `.sdd/` se excluyó de esa búsqueda. |

No se inventariaron credenciales presentes en las instalaciones de los hosts,
variables de entorno ni archivos locales fuera del repositorio.
