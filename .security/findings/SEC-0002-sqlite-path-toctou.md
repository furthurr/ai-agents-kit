# SEC-0002: TOCTOU entre la inspección de la ruta y apertura SQLite

- Estado: Resuelto en el alcance F07 revisado
- Severidad: 🟡 Media
- Referencia: CWE-367
- Ubicación: `.agent-lab/sdd-escalation/runner/src/lab_runner/storage_rpc.py:97-101,118-119`
- Fecha detección: 2026-10-07

## Descripción del riesgo

El worker ejecuta `lstat` sobre directorio/archivo SQLite para comprobar tipo y
link-count, y después llama `sqlite3.connect(path)`. Como el candidato comparte el
namespace/escritor del contenedor, puede sustituir la ruta entre el check y el open.
Esto puede redirigir la operación de evaluación a un archivo distinto. Se relaciona
con SEC-0001, pero requiere comprobar explícitamente el manejo de symlinks/races aun
cuando la base se mueva a un mediador separado.

## Plan de remediación (micro-pasos)

- [ ] Paso 1: eliminar la posibilidad de que el actor candidato escriba el directorio SQLite; usar ownership/namespace separado como parte de SEC-0001.
- [ ] Paso 2: hacer aperturas resistentes a symlink/sustitución, o encapsular toda operación en un servicio de almacenamiento con ruta/FD poseído por el mediador.
- [ ] Paso 3: probar sustitución concurrente, hard links y rutas precreadas; reauditar el diff final.

## Bitácora

- 2026-10-07: reauditoría final en `../reviews/f07-2026-10-07.md`; aperturas confiables tras quiescencia y ownership protegido, pruebas reales de symlink/hardlink/FIFO/reemplazo y recuperación SQLite. Resolución frente al UID candidato, no frente a root/host confiable comprometido.

- 2026-10-07: verificado por inspección; no se ha intentado una explotación contra F07 real.
- 2026-10-07: fixture confiable reprodujo sustitución por symlink después del check del prototipo y apertura de una DB no asignada (77 frente a 3). Evidencia `results/f07-wave1-boundary.md` en el laboratorio. No se ejecutó un candidato LLM ni se marca remediación completa.
