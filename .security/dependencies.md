# Dependencias — inventario de seguridad

Fecha de comprobación: 2026-10-05. El inventario describe el snapshot local
observado y no usa `HEAD` como baseline.

## JavaScript / npm

- Manifiesto: `.opencode/package.json`.
- Dependencia directa: `@opencode-ai/plugin` `1.18.15`.
- Lockfile: `.opencode/package-lock.json`, lockfileVersion 3; 32 paquetes en el
  grafo (9 opcionales).
- Verificación: `npm audit --package-lock-only --json`; resultado: 0
  vulnerabilidades conocidas (0 info, low, moderate, high y critical).
- Nota de cadena de suministro: el lockfile indica que la dependencia opcional
  `msgpackr-extract` tiene script de instalación; no se ejecutó instalación ni
  script en esta auditoría. El resultado de `npm audit` no acredita la seguridad
  de la cadena de suministro ni de las acciones de CI.

## Python

- Las herramientas revisadas usan la biblioteca estándar. No se encontró un
  manifiesto Python de dependencias de terceros en el inventario consultado.
- La revisión no ejecutó pruebas ni instaló paquetes.

## GitHub Actions

- `.github/workflows/ci.yml` usa `actions/checkout@v4` y
  `actions/setup-python@v5`. Estas referencias no forman parte del grafo npm y no
  fueron evaluadas por `npm audit`.
- El hallazgo asociado está registrado como SEC-0002. No se configuró un SBOM
  para las acciones en esta revisión.
