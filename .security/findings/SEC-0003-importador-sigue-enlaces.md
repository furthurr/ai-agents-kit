# SEC-0003: El importador sigue enlaces simbólicos del origen

- Estado: Corrección multiplataforma integrada localmente; CI Windows pendiente
- Severidad: 🟢 Baja
- Referencia: CWE-59 (Improper Link Resolution Before File Access)
- Ubicación: `tools/import_installed.py:32-53`
- Fecha de detección: 2026-10-05

## Descripción del riesgo

El importador recoge entradas del directorio instalado y copia las esperadas con
`shutil.copytree` o `shutil.copy2`, sin excluir enlaces simbólicos ni exigir que
su ruta resuelta permanezca bajo el directorio de origen. El comportamiento por
defecto sigue enlaces. Si una entrada esperada apunta a un archivo o directorio
externo, su contenido podría acabar en la instantánea local `imports/`, que está
ignorada por Git. El riesgo es local y requiere que el directorio instalado
contenga un enlace preparado; no se verificó ninguna instalación de host.

## Impacto, esfuerzo y recomendación

- Impacto potencial: copia local inadvertida de datos que no pertenecen al
  artefacto esperado y posible promoción posterior por revisión humana.
- Esfuerzo estimado: Bajo.
- Recomendación: rechazar enlaces o verificar la ruta resuelta dentro de la raíz
  autorizada antes de copiar; importar solo archivos/directorios regulares.

## Plan de remediación (no ejecutado)

- [x] Definir el comportamiento permitido para enlaces en los orígenes de
  importación.
- [x] Validar las rutas y probar enlaces a destinos internos y
  externos con datos ficticios.

## Bitácora

- 2026-10-14: se rechazan enlaces internos/externos, raíces/padres enlazados,
  puntos de reanálisis y archivos especiales usando los helpers existentes de
  lectura segura. Se valida/lee antes de escribir; `--dry-run` aplica la misma
  política. `python3 -B tools/test_import_installed.py`: 9 tests OK, tras observar
  el fallo del importador anterior ante enlaces preparados. Suite añadida a CI.
  No se inspeccionaron perfiles reales. Se exige árbol estable: no se acredita
  aislamiento contra sustitución concurrente de directorios por otro proceso.
- 2026-10-15: CI remoto de v3.3.0 encontró que Windows normaliza rutas cortas 8.3
  (`RUNNER~1`) a su forma larga. `source_directory` ahora inspecciona el path
  suministrado mediante `safe_directory` en Windows, comprobando symlinks, junctions
  y reparse points sin tratar aliases 8.3 como enlaces. Contrato Windows simulado;
  importador 10/10 y Antigravity 22/22 pasan en macOS. Reejecutar CI Windows antes
  de cerrar la validación multiplataforma.

- 2026-10-05: hallazgo estático registrado; no se ejecutó el importador.
