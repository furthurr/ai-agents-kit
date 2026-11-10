# Genera Android/iOS — reescritura local autorizada

**Aplicada localmente el 2026-11-10**, tras autorización explícita del alcance.
`main` local resuelve a `c149aa1`. No hubo commit adicional, push, expiración de
reflogs ni poda/borrado de objetos. La publicación y la purga física siguen fuera
de esta autorización. [Evidencia de aplicación](genera-history-local-application-2026-11-10.json).

**Seguimiento posterior:** el usuario autorizó eliminar la nota local de
continuidad que conservaba referencias privadas. Se retiró del árbol de trabajo
sin copiar su contenido a otro archivo; el índice documental ya no la requiere.
La retirada está pendiente de commit y no altera las verificaciones históricas
de preservación realizadas antes de esa autorización.

## Resultado disponible

La anonimización del árbol actual está implementada. Primero se preparó un ensayo
en un repositorio bare privado y aislado. Tras validarlo y autorizar expresamente
el alcance, se aplicó la reescritura de las referencias locales y se ajustó el
índice sin sobrescribir ningún archivo del árbol de trabajo. El servidor remoto
no se ha contactado ni modificado.

- 101 commits alcanzables examinados; tres commits cambiarían de identificador.
- 173 versiones ruta/blob transformadas en el ensayo.
- Ocho versiones Python comprobaron sintaxis; 128 versiones JSON conservaron sus
  2.238 valores numéricos, booleanos y nulos.
- `git fsck --full --no-reflogs` del ensayo: correcto.
- Comprobación independiente de 2.567 blobs de texto alcanzables y mensajes de
  commits/tags: cero restos de los namespaces y nombres de ZIP privados conocidos.
  No se considera un detector universal de todos los datos sensibles.
- No se invalidaron firmas en el ensayo.
- Los perfiles/instrucciones y los 27 comprimidos permanecieron intactos.

Evidencia pública redactada: [resumen del ensayo](genera-history-preview-2026-11-10.json).
El mapa de objetos original/candidato y la ubicación de la copia de recuperación
solo se conservan en el directorio temporal privado de la sesión. No publicar el
mapa ni el repositorio de ensayo: este todavía contiene objetos originales.

## Alcance aprobado y aplicado

La aplicación local afectó a:

1. `refs/heads/main`.
2. `refs/remotes/origin/main`, exclusivamente como referencia local.
3. La resolución de `refs/remotes/origin/HEAD`, manteniendo su enlace simbólico
   hacia `origin/main`.

Las otras 29 referencias, incluidos los tags y las otras ramas, no cambiaron.
**Cambiar una referencia local `origin/*` no modifica GitHub** ni acredita que su
valor siga reflejando el servidor. El OID remoto observado se mantiene en
metadatos privados para comprobar un lease explícito antes de una publicación
autorizada; no se publica el mapa de objetos retirados.

El alcance de esta puerta no incluye commit adicional de los archivos nuevos,
push, force-push, borrado de archivos, expiración de reflogs ni poda de objetos.

## Preservación comprobada durante la aplicación

- Revalidar que refs, `HEAD`, índice y cambios locales siguen coincidiendo con el
  estado del ensayo; detenerse ante cambios del usuario no contemplados.
- Mantener el contenido del árbol de trabajo, los archivos nuevos y el cambio
  previo en `docs/experimentos/CONTINUAR-AQUI.md`. No ejecutar reset, checkout,
  clean ni otra operación que descarte contenido.
- En el ensayo se anonimizaron las versiones históricas de `CONTINUAR-AQUI.md` y
  se preservó la copia local durante la reescritura. El usuario autorizó después
  su eliminación, descartando también su modificación local. No reintroducir sus
  notas desde snapshots, reflogs o copias privadas; no reproducir sus valores.
- Conservar un mapa privado de recuperación; no crear refs de respaldo que
  pudieran publicarse accidentalmente con contenido original.
- Importar únicamente los objetos necesarios desde el ensayo local y actualizar
  las referencias con comprobación de sus valores previos.
- Ajustar el índice al nuevo árbol sin escribir sobre el árbol de trabajo. Los
  cambios ya incorporados por la reescritura pueden dejar de aparecer en el diff;
  eso no autoriza perder cambios del usuario ni incluir su archivo en un commit.
- Volver a comprobar sintaxis, JSON, métricas, indicadores conocidos, referencias,
  invariantes de los comprimidos y preservación del árbol de trabajo.

## Pendientes distintos de esta puerta

- Los tres commits que ya estaban visibles solo por reflog, las versiones
  anteriores de los tres commits reemplazados y 14 blobs inicialmente sin ruta
  identificada no se han purgado. No se leyó el contenido de esos blobs sin ruta
  para evitar acceder a posibles credenciales protegidas.
- La eliminación de objetos antiguos y reflogs requiere otra autorización
  específica y una política de recuperación privada. Hasta entonces pueden
  seguir existiendo datos anteriores en el almacenamiento local.
- El commit de controles/documentación nueva, la publicación o force-push y la
  coordinación de clones, forks, cachés y proveedores son decisiones separadas.
- No se reejecutaron las aplicaciones ni todos los benchmarks históricos. El
  cambio de identificadores y ejemplos puede afectar a la reproducción de un
  snapshot antiguo; las métricas conservadas no se presentan como ejecuciones nuevas.

## Imágenes y comprimidos

Las 244 ubicaciones PNG contienen dos imágenes distintas. Apple Vision realizó
OCR local mediante memoria/stdin, sin extracción de miembros ni envío a servicios
externos. No detectó indicadores conocidos, credenciales potenciales ni metadatos
GPS/autor con las reglas usadas. No es una revisión visual humana ni una garantía
contra texto ilegible, datos ocultos o formatos de metadatos no cubiertos.

- [OCR local](genera-local-image-ocr-2026-11-10.json).
- [Reclasificación de los comprimidos](genera-archive-reclassification-2026-11-10.json):
  nueve avisos iniciales descartados y doce ejemplos canónicos verificados; los
  27 ZIP/TAR.GZ siguen sin modificaciones.

**No declarar el repositorio libre de información sensible:** permanecen los
objetos/reflogs originales y las copias externas, además de los límites indicados.
La retirada de la nota local está pendiente de commit. No publicar automáticamente el árbol,
el clon de ensayo ni los mapas privados de recuperación.
