# 7. Conceptos transversales

## Fuente única e inventario

`canonical/manifest.json` enumera skills, agentes y plataformas. Renderer,
validador, preflight e importer usan ese inventario para evitar listas
independientes (`../canonical/manifest.json:1-31`; `../tools/validate.py:45-58`;
`../tools/install_preflight.py:50-70`).

## Separación de fuentes y salidas

- `canonical/`: comportamiento y texto comunes.
- `adapters/`: diferencias de host.
- `generated/`: salida derivada; no editar manualmente.
- `scripts/`: operaciones de usuario sobre los directorios de host.

La separación y prohibición de editar salida se documentan en
`../docs/arquitectura-del-kit.md:34-43` y `../docs/instalacion.md:3-5`.

## Adaptación y contratos de contenido

- Tokens en el contenido común se sustituyen según `platform.json` y overrides
  por skill/agente. Un token sin resolver provoca error
  (`../tools/render.py:66-71, 81-108`).
- El nombre de salida de agente se valida como ruta relativa segura antes de
  escribir (`../tools/render.py:24-35, 99-108`).
- El validador comprueba inventario, adapters obligatorios, duplicados,
  referencias de plataforma y tokens declarados/no usados
  (`../tools/validate.py:45-123, 151-197`).
- No se sustituyen tokens dentro de `references/`; el validador evita que estos
  lleguen sin resolver al host (`../tools/validate.py:183-197`).

## Consistencia y diagnóstico

- La validación de paridad renderiza en un temporal y compara SHA-256; no
  reemplaza `generated/` (`../tools/validate.py:200-216`).
- El preflight detiene una instalación si el origen/destino no contiene el
  inventario esperado (`../tools/install_preflight.py:74-96, 99-137`).
- El renderer reporta errores de lectura, JSON y tokens por stderr y termina con
  código de error (`../tools/render.py:131-136`).

## Preservación de contenido local

El flujo de instalación respalda lo existente salvo que se pida `--force`,
ofrece `--dry-run` y no elimina elementos extra del destino. La importación
filtra por manifest y deja la promoción bajo control humano
(`../docs/instalacion.md:53-60, 112-139, 184-189`).

## Configuración sensible y lenguaje

- `imports/` está ignorado por Git porque puede incluir configuración local;
  no copiar secretos, tokens ni credenciales a fuentes o documentación
  (`../.gitignore:21-23`; `../docs/instalacion.md:262-265, 277-283`).
- El idioma por defecto de prompts y docs del kit es español
  (`../docs/desarrollo.md:129-136`).
- Los límites de permisos que declaran los adapters son específicos de cada
  cliente; no sustituyen los permisos de sesión ni garantizan aislamiento
  (`../docs/arquitectura-del-kit.md:166-181`).
