# <Nombre del proyecto>

## Proposito
- Que es: <1-3 frases>
- Alcance: <que incluye>
- Fuera de alcance: <que no es / no cubre>

## Stack
- Lenguajes y frameworks: <...>
- Build / monorepo tool: <gradle, npm workspaces, melos, ...>
- Entrypoints: <paths clave, p. ej. app/main.ts, :app>

## Mapa rapido
- `<path o modulo>` → <responsabilidad en una frase>
- `<path o modulo>` → <...>
- (Detalle y dependencias: ver `module-map.json`; no duplicar el JSON aqui)

## Convenciones
- <solo las que afectan a navegar o editar: capas, naming, tests, paquetes>

## Docs y contexto externo
- `README.md` — <nota breve o "presente">
- `AGENTS.md` / `CLAUDE.md` / otras — <presente|ausente; no pegar contenido>
- Carpetas canonicas (`.architecture/`, `.data/`, ...) — <paths si existen>

## Riesgos y restricciones
- <areas delicadas, PII, no tocar sin cuidado>
- Secretos: nunca indexar `.env` ni claves (ver exclude)

## Meta
- Actualizado: <YYYY-MM-DD>
- Source commit: <git rev-parse HEAD; omitir si no hay commit verificable>
- Navigator root: <`.` o subpath del monorepo>
- Generado por: project-navigator bootstrap|update|manual
