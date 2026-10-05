# SEC-0003: El importador sigue enlaces simbólicos del origen

- Estado: Pendiente
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

- [ ] Definir el comportamiento permitido para enlaces en los orígenes de
  importación.
- [ ] Validar las rutas resueltas y probar enlaces a destinos internos y
  externos con datos ficticios.

## Bitácora

- 2026-10-05: hallazgo estático registrado; no se ejecutó el importador.
