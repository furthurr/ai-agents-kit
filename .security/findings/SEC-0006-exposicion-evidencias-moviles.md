# SEC-0006 — Exposición de información interna en evidencias móviles

- Fecha: 2026-11-10.
- Severidad: alta por exposición de información interna; impacto de credenciales
  reales de Genera no confirmado.
- Estado: árbol anonimizado y referencias locales del historial reescritas con
  autorización explícita; publicación, objetos originales y reflogs pendientes.
  Imágenes revisadas por OCR local con límites, no por inspección visual humana.
  Los candidatos de comprimidos se reclasificaron sin confirmar exposición de
  Genera por esas coincidencias. No declarar resuelto globalmente.
- Referencias: CWE-200, CWE-359; relacionado con MASVS-PRIVACY/STORAGE como
  clasificación temática. No es una evaluación MASVS de las aplicaciones.
- MASWE/MASTG: no se asigna una prueba móvil específica a esta publicación de
  artefactos Git, ni se afirma conformidad de las aplicaciones.

## Evidencia sin valores

Se confirmó información interna Android en
`docs/experimentos/proyectos-arneses-comparativa/genera/README.md` y
`tools/real_android_harness_benchmark.py`, junto con otras herramientas, oráculos,
tareas y resultados. Se encontraron rutas personales y referencias de fuentes
iOS en `docs/experimentos/real-ios-gemini-antigravity-2026-11-09/`.

Se identificaron localmente los commits de incorporación y su relación con la
referencia publicada anterior. Sus identificadores y el mapa de recuperación se
mantienen fuera del contenido versionado para no divulgar nuevos punteros a las
versiones retiradas. Otros nombres históricos solo se localizaron por reflog;
no se ha probado su publicación.

Los siguientes nueve miembros fueron candidatos del análisis inicial. **Se retira
su clasificación como exposición confirmada de Genera**; las ubicaciones se
conservan únicamente para trazabilidad de la corrección:

- `docs/experimentos/archive/odd-batching-luna-max/laboratorio.tar.gz`, miembros
  `invocations/TASK-2-ODD-r2-1.json`, `live/TASK-2-ODD-r2-events.json`,
  `traces/TASK-2-ODD-r2.json`, `transport/TASK-2-ODD-r2.json`.
- `docs/experimentos/archive/odd-estandares-gpt6-luna-max/laboratorio.tar.gz`,
  miembros `invocations/TASK-2-ADJUSTED-r1-1.json`,
  `records/TASK-2-ADJUSTED-r1.json`, `traces/TASK-2-ADJUSTED-r1.json`.
- `docs/experimentos/archive/real-project-gemini-2026-11-05/laboratorio.tar.gz`,
  miembros `build-01.json` y `build-02.json`.

### Corrección tras la revisión previa a reconstruir los comprimidos

La autorización de reconstrucción llevó a decodificar el JSON y comprobar sus
cadenas por líneas lógicas, no por líneas del JSON serializado. Los nueve avisos
mezclaban rutas con palabras de generación de código o verbos españoles. No
contenían los namespaces, nombres de ZIP ni símbolos originales conocidos del
proyecto. La atribución inicial a Genera no estaba sustentada.

Se reexaminaron los 27 comprimidos: 28.053 miembros y 27.810 textos, sin extracción.
Doce coincidencias adicionales en referencias de perfiles son líneas idénticas
al ejemplo de ruta de la documentación canónica de project-navigator. No se
modificaron perfiles ni ninguno de los comprimidos. No quedaron candidatos con
las reglas concretas utilizadas; esto no es una garantía universal de ausencia.

La revisión textual inicial no decodificó 243 PNG de los comprimidos. El
seguimiento posterior sí realizó OCR local, sin extracción; se conserva el límite
de inspección visual humana y el alcance exclusivamente local. Evidencia, ubicaciones,
clasificación y nueve regresiones sintéticas correctas:
[reclasificación de comprimidos](../reviews/genera-archive-reclassification-2026-11-10.json).

## Mitigación autorizada

1. Sustitución local de identificadores por placeholders coherentes; el mapa de
   valores originales no se guarda ni se publica.
2. Redacción de detalles crudos de evidencias JSON con conservación de todos sus
   valores numéricos, booleanos y nulos.
3. Omisión de fragmentos de implementación de los enunciados y señalización del
   cambio de procedencia; archivos y enlaces históricos se conservan.
4. Rutas de fixtures configurables sin seleccionar automáticamente los ZIP de los
   proyectos privados. No se ejecutaron benchmarks ni se procesaron laboratorios
   externos.

Durante el saneamiento inicial del árbol se preservaron el cambio previo en
`docs/experimentos/CONTINUAR-AQUI.md`, los otros proyectos y los perfiles/instrucciones.
En esa primera etapa no hubo commit, push, borrado de archivos, reconstrucción de
ZIP/TAR.GZ, revocación ni reescritura de Git. La aplicación histórica local
autorizada posteriormente se documenta en el seguimiento siguiente.

## Verificación de esta etapa

- 98 archivos existentes anonimizados; 65 JSON conservan exactamente sus 1.338
  valores numéricos, booleanos y nulos frente a `HEAD`.
- 49 pruebas unitarias correctas: 38 del núcleo móvil, 5 del adaptador Android y
  6 de privacidad; solo fixtures sintéticos y operaciones locales.
- `python3 tools/check_mobile_privacy.py`: 87 archivos, cero hallazgos en sus
  reglas acotadas. La comprobación local de los identificadores originales
  conocidos tampoco detecta restos en el alcance no comprimido revisado.
- Sintaxis de ocho archivos Python y `git diff --check` sobre cambios propios
  correctos. Los 27 comprimidos coinciden byte a byte con sus blobs en `HEAD`.
- El hash del cambio previo, los perfiles/instrucciones, el índice y `HEAD` se
  mantienen. No se revisó visualmente la interfaz ni se ejecutaron apps reales.

Evidencia y lista de archivos: [verificación local](../reviews/genera-mobile-tree-2026-11-10.json).

### Seguimiento: OCR y ensayo histórico aislado

- 244 ubicaciones PNG corresponden a dos imágenes únicas. El OCR local Apple
  Vision pasó una prueba sintética y no detectó indicadores conocidos ni
  credenciales potenciales en las imágenes. No se emitieron textos reconocidos ni
  se modificaron imágenes. No sustituye una inspección visual ni detecta todos
  los datos ocultos. [Evidencia](../reviews/genera-local-image-ocr-2026-11-10.json).
- Ensayo histórico sobre 101 commits: tres commits y tres referencias efectivas
  cambiarían, con 173 versiones ruta/blob transformadas. Comprobados sintaxis de
  ocho versiones Python, 128 versiones JSON y conservación de 2.238 valores
  numéricos/booleanos/nulos. Integridad Git correcta; cero firmas invalidadas.
- Validación independiente de 2.567 blobs de texto alcanzables y mensajes de
  commits/tags sin restos de los namespaces/nombres de ZIP privados conocidos.
  La comprobación inicial detectó una referencia en un snapshot histórico de
  `CONTINUAR-AQUI.md`; se corrigió únicamente en los blobs del ensayo y se volvió
  a validar. El archivo local del usuario permanece intacto y no debe publicarse
  automáticamente: todavía contiene referencias a ZIP privados.
- Después del ensayo se autorizó y aplicó la reescritura local de los tres commits
  y las referencias indicadas. El nuevo `main` local es `c149aa1`. Se ajustó solo
  el índice; se verificó la conservación de bytes/modos de los 1.223 archivos
  presentes, incluido el cambio previo del usuario. Las otras 29 refs no cambiaron.
- Se volvió a comprobar el grafo alcanzable del repositorio original: 2.567 blobs
  de texto y mensajes de commits/tags sin los indicadores concretos buscados.
  Integridad Git correcta. Sin commit adicional, push, expiración de reflogs ni
  eliminación de objetos. GitHub no se ha modificado.
- Al terminar esa etapa, los objetos/reflogs antiguos, la nota local preservada
  y las copias externas seguían fuera de una purga. La retirada posterior de la
  nota se describe a continuación; los mapas y clones privados no deben publicarse.
- [Plan aplicado y límites](../reviews/genera-history-plan-2026-11-10.md) y
  [evidencia de aplicación](../reviews/genera-history-local-application-2026-11-10.json).

### Seguimiento posterior: retirada de la nota local

El usuario autorizó eliminar `docs/experimentos/CONTINUAR-AQUI.md` si seguía
exponiendo datos del proyecto. Se comprobó, sin mostrar valores, que la copia
local aún contenía referencias a ZIP privados. Se eliminó ese archivo, incluido
su cambio local previo, y se actualizó el índice de experimentos para usar los
informes existentes y la guía de privacidad. No se guardó una copia de las notas.

La utilidad `tools/preserve_odd_continuity.py` usa otro archivo homónimo dentro de
un directorio de continuidad proporcionado como argumento, no la nota eliminada;
no se modificó ni se eliminaron sus snapshots. Las referencias en manifiestos e
informes históricos se conservan como evidencia, no como enlaces de navegación.

La autorización anterior de conservar la nota se mantuvo durante la reescritura;
su posterior eliminación está autorizada separadamente y pendiente de commit.
No se modificaron refs, perfiles, instrucciones, comprimidos ni se realizó push o
purga. [Evidencia](../reviews/genera-continuity-removal-2026-11-10.json).

### Preparación de publicación

Se añadieron una exclusión exacta de la nota retirada, el control móvil y sus
regresiones a CI, declarando `ripgrep` como dependencia de esas pruebas. También
se corrigieron exclusivamente enlaces rotos de documentos movidos a `archive/`
o de la nota ausente; no se cambiaron los datos ni los perfiles de los otros
experimentos. Los manifiestos históricos no describen el árbol actualizado.

La consulta anónima del remoto confirmó que su `main` sigue conteniendo las
versiones originales. Se verificó la ascendencia de las referencias anunciadas,
incluidas las dos puntas de PR inicialmente desconocidas, sin descargar código
ni usar credenciales. No se justificó eliminar tags ni otras ramas. El historial
reescrito requerirá una publicación autorizada de `main` con lease explícito;
no hacer merge/pull del historial retirado ni usar un push indiscriminado.

Verificaciones del candidato y límites:
[preparación de publicación](../reviews/genera-publication-readiness-2026-11-10.json).

## Límites y siguiente etapa

La auditoría local recorrió 1.214 archivos versionados, 104 commits incluyendo
reflogs, 2.651 blobs con ruta y 27 comprimidos. No se inspeccionaron visualmente
244 PNG ni se leyó el contenido de 14 blobs sin ruta, para no acceder a posibles
credenciales protegidas. No se consultaron servicios externos ni se verificaron
forks, clones, cachés o artefactos remotos.

No corresponde reconstruir los tres TAR.GZ basándose en los avisos descartados.
La publicación, la expiración de reflogs y la eliminación física de objetos
siguen requiriendo decisiones separadas del responsable. Una purga local no
garantiza retirar copias externas.
Si se descubre una credencial real de Genera, su rotación/revocación corresponde
al responsable.

Guía de publicación: [privacidad móvil](../../docs/experimentos/PRIVACIDAD-MOVIL.md).
