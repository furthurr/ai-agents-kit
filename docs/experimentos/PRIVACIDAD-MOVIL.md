# Privacidad de las evidencias móviles

## Alcance del saneamiento

Los materiales públicos asociados a Genera Android e iOS usan identificadores
sintéticos y evidencias redactadas. El saneamiento se limita a esos proyectos:
no modifica los otros laboratorios, los perfiles ni las instrucciones de agentes.
Los nombres históricos de carpetas e informes se conservan para no romper enlaces.

- Los paquetes de ejemplo Android usan `com.example.mobilefixture`.
- Los nombres de proyecto/módulo Swift y los tipos sustituidos son placeholders,
  no identificadores de una aplicación distribuida.
- Se omitieron fragmentos de implementación de los enunciados y detalles crudos
  de ejecución de los JSON: rutas, comandos, respuestas, errores y huellas del
  proyecto original. Los oráculos conservan contratos de prueba anonimizados;
  no incluyen una copia de la aplicación ni acreditan compatibilidad con ella.
- Se conservaron los valores numéricos, booleanos y nulos de los JSON históricos.
  La anonimización no es una nueva ejecución ni valida de nuevo sus conclusiones.
- Los manifiestos de referencia anteriores a este cambio no describen el árbol
  anonimizado. Las huellas originales sensibles se sustituyen por placeholders;
  no se debe presentar una huella nueva como prueba de una ejecución anterior.

## Uso de los arneses

Los ZIP privados y los laboratorios móviles recientes no forman parte de esta
distribución. No se deben copiar ni publicar automáticamente.

Para una ejecución nueva, proporcionar un fixture sintético y autorizado:

```sh
export MOBILE_BENCHMARK_ANDROID_ARCHIVE=/ruta/a/fixture-android.zip
export MOBILE_BENCHMARK_IOS_ARCHIVE=/ruta/a/fixture-ios.zip
```

Los adaptadores v2 también admiten `--base-zip`. Sus rutas predeterminadas están
bajo `~/.local/share/ai-agents-kit/fixtures/`, sin apuntar a copias de Genera.
Los fixtures deben implementar los contratos de prueba anonimizados. No se ha
ejecutado una aplicación Android/iOS real para comprobarlos durante este saneamiento.

## Pendientes que impiden declarar una publicación saneada

Control local acotado: `python3 tools/check_mobile_privacy.py`. Detecta rutas
personales, paquetes Kotlin ajenos al fixture y ciertos detalles crudos de los
JSON móviles; no sustituye la inspección de comprimidos ni un escáner completo.

**La reescritura local del historial está aplicada, pero no se ha publicado ni
se han eliminado objetos/reflogs antiguos.** La revisión de comprimidos se
corrigió tras descartar coincidencias no vinculadas al proyecto. No publicar el
estado como una purga completa de los datos de Genera.

- Los 27 ZIP/TAR.GZ permanecen intactos. Los nueve avisos inicialmente atribuidos
  a Genera eran falsos positivos de JSON serializado, palabras de generación y
  verbos españoles. Doce coincidencias en perfiles son ejemplos de la referencia
  canónica. No se justificó reconstruir los archivos con esa evidencia. Véase la
  [reclasificación](../../.security/reviews/genera-archive-reclassification-2026-11-10.json).
- Se reescribieron tres commits en `main` y sus referencias locales asociadas,
  manteniendo los otros 29 refs y todos los archivos del árbol de trabajo.
  Los objetos/reflogs antiguos, el servidor remoto, clones, forks y cachés pueden
  conservar versiones previas. La publicación y la purga física son otras decisiones.
- Se eliminó del árbol de trabajo `CONTINUAR-AQUI.md` con autorización del usuario,
  porque su copia local todavía contenía referencias privadas. No se copió a otra
  ruta ni se sustituyó por una copia de sus notas. La eliminación debe registrarse
  en un commit autorizado; no elimina por sí sola objetos o copias anteriores.
- Se completó OCR local de las 244 ubicaciones PNG, correspondientes a dos imágenes
  distintas, sin detectar indicadores conocidos ni credenciales potenciales. No
  hubo envío a servicios externos ni extracción. El OCR no sustituye revisión
  visual humana ni descarta datos ocultos; los blobs sin ruta mantienen su límite.
- No se confirmó una credencial operativa de Genera. Si el responsable identifica
  una, debe revocarla o rotarla; anonimizar sus copias no sustituye esa acción.

Seguimiento: [SEC-0006](../../.security/findings/SEC-0006-exposicion-evidencias-moviles.md).
Aplicación local autorizada y límites:
[plan del historial](../../.security/reviews/genera-history-plan-2026-11-10.md).

## Antes de commit y push

- La nota retirada tiene una exclusión exacta en `.gitignore`; CI ejecuta el
  control móvil y sus pruebas. Las pruebas del arnés requieren `ripgrep`, declarado
  en el job de Ubuntu. No se ejecutan aplicaciones ni modelos reales en esas pruebas.
- Revisar y agregar rutas explícitas, incluida la eliminación de la nota; no
  incluir mapas de recuperación, valores de lease ni clones de ensayo privados.
- Comprobar el índice completo con el control de secretos inmediatamente antes
  de un commit autorizado. Las validaciones no certifican ausencia universal.
- Un commit nuevo no sustituye el historial expuesto. El remoto todavía contiene
  la versión anterior: para publicar el saneamiento se necesita autorización de
  actualización forzada de **solo `main`**, con un lease explícito contra el OID
  remoto verificado. El `origin/main` local ya reescrito no sirve como lease implícito.
- No hacer `pull`, merge del historial antiguo ni `push --mirror`: podrían
  reintroducir datos o modificar referencias fuera del alcance.
- No es necesario borrar todos los commits, tags o ramas: se conservaron los
  benchmarks anonimizando los tres commits afectados. Las referencias anunciadas
  del remoto no justificaron retirar otros tags, ramas o PRs.
- La publicación no elimina automáticamente objetos locales, reflogs, clones,
  forks o vistas en caché. La purga local es otra autorización y no sustituye la
  retirada en GitHub. Coordinar las copias existentes y consultar a GitHub Support
  cuando proceda; su elegibilidad para purgar contenido la determina GitHub.

[Guía oficial de GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
[Verificación del candidato de publicación](../../.security/reviews/genera-publication-readiness-2026-11-10.json).
