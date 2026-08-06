# Bootstrap y update

## Avisos de modelo (obligatorios en procesos pesados)

Aplica a bootstrap, update pesado, indexado y navegación reiterada de varias capas.

**Antes:**

```text
Antes de continuar con project-navigator, te recomiendo cambiar manualmente
el modelo de esta sesion a uno pequeno/rapido/economico (menor costo y
latencia para indexar y navegar).

No cambio el modelo por ti. Cuando lo hayas cambiado (o si prefieres seguir
con el actual), confirmalo y sigo.
```

Esperar confirmación o "sigo con el actual". Nunca seleccionar ni forzar el modelo.

**Después:**

```text
project-navigator termino.

Ya puedes cambiar manualmente el modelo a uno enfocado en tu siguiente tarea
(p. ej. coding agentic para implementar, o razonamiento fuerte para disenar).
No lo cambio por ti.
```

## Bootstrap asistido (pasos)

1. Aviso de modelo pequeño (arriba).
2. Detectar lenguajes, build system y fuentes externas de contexto (`sources.md`).
3. Detectar ubicación de `.navigator/` (monorepo; ver abajo). Si es ambiguo, **preguntar**.
4. Crear `.navigator/` si no existe.
5. Escribir `config.yaml` mínimo desde `templates/config.template.yaml`.
6. Generar `ai-context.md` (~500 tokens) desde `templates/ai-context.template.md`.
7. Generar `module-map.json` desde `templates/module-map.template.json`.
8. No bloquear si faltan `symbols` o grafo.
9. Respetar `exclude` y no indexar secretos (`config.md`).
10. Ejecutar el gate post-bootstrap descrito abajo; corregir fallos antes de cerrar.
11. Informar: artefactos creados, fuentes externas detectadas, gaps, presupuesto y cómo consultar.
12. Aviso final de modelo.

### Lectura para Capa 0 (presupuesto)

- Preferir README + "Contexto para IA" + manifests de build
- Máx. ~3–5 docs cortos de entrada
- No leer árboles completos
- Total sesión bootstrap tipica: objetivo < ~30–50k tokens in+out
- Repos enormes: acotar `project.root` o pedir subproyecto

### Generación de capas 0–1

**ai-context.md:**

1. Idioma del repo o del usuario
2. No incluir secretos, tokens, connection strings ni PII
3. Referenciar paths de docs largas; no incrustarlas
4. Mapa rápido = resumen; dependencias viven en `module-map.json`
5. Listar fuentes externas detectadas; no sobrescribirlas
6. Si supera ~700 tokens: ejecutar una pasada de compactación antes de cerrar

**module-map.json:**

1. `id` único y estable entre updates
2. Todo `depends_on` apunta a un `id` existente
3. Unidades de primer nivel / features detectables
4. No listar `node_modules`, build outputs ni paths excluidos
5. Si no hay dependencias claras: `depends_on: []` (no inventar)
6. `root` coincide con el subárbol de esta instancia `.navigator/`

### Gate post-bootstrap

No declarar el bootstrap terminado hasta verificar:

1. Existen `config.yaml`, `ai-context.md` y `module-map.json` bajo la instancia
   `.navigator/` correcta.
2. `module-map.json` es JSON válido y cumple `schemas.md`: IDs únicos,
   `depends_on` resolubles, `root` alineado y paths relativos.
3. Las capas 2–3 no se generaron sin opt-in.
4. Ningún artefacto contiene secretos, PII ni paths absolutos de la máquina.
5. El estado de capas coincide con `config.yaml` y el filesystem.
6. Se estimó el tamaño con `caracteres / 4` y se registró el resultado.

Presupuesto de `ai-context.md`:

- Objetivo: ~500 tokens; tope blando: ~700.
- Si supera 700, compactar al menos una vez antes de informar el resultado.
- Recortar primero dependencias exhaustivas, convenciones de implementación y
  detalles duplicados en `module-map.json` o documentación externa.
- Preservar propósito, stack principal, mapa rápido, fuentes y restricciones.
- No cerrar por encima de 700 sin explicar la causa y obtener aceptación
  explícita del usuario para conservar la excepción.

Presupuesto de `module-map.json`:

- Objetivo: ~1–2k tokens; tope blando: ~4k.
- Si supera 4k, reducir granularidad o acotar `project.root`; no truncar JSON.

Si el gate falla, corregir solo los artefactos de `.navigator/`, repetir las
comprobaciones y después emitir el aviso final de modelo.

### Symbols (opt-in en bootstrap)

- Solo si `layers.symbols: true` o el usuario lo pide
- Subconjunto útil (públicos / entrypoints); cobertura total no es meta del MVP
- Si no hay confianza en `file`+`line`, omitir el símbolo

### Graph (opt-in)

- Fuera del presupuesto MVP core
- No bloquear bootstrap; provider externo si se habilita después

## Monorepo y ubicación de `.navigator/`

Misma lógica que la skill `architecture` del kit.

Escanear raíz y subcarpetas de primer nivel (y contenedores `apps/`, `packages/`,
`services/`) buscando marcadores: `settings.gradle(.kts)`, `build.gradle`,
`package.json`, `pubspec.yaml`, `Cargo.toml`, `go.mod`, `*.xcodeproj` /
`*.xcworkspace`, `Podfile`, `pyproject.toml`, etc.

| Situación | Dónde crear `.navigator/` |
| --- | --- |
| Un solo producto o **agregador en la raíz** | **Una** en la **raíz del repo** |
| Varios productos/apps **independientes** sin agregador | **Una por subproyecto** |
| Flutter / React Native / KMP con marcador en raíz | **Una en la raíz** |
| Escaneo **ambiguo** | **Preguntar** antes de escribir |

Reglas:

1. Nunca mezclar productos independientes en el mismo `module-map.json`
2. Cada `.navigator/` indexa solo su subárbol (`config.project.root`)
3. En multi-navigator, cada uno tiene su `ai-context.md` y `module-map.json`
4. Consultas: usar el `.navigator/` del subproyecto en contexto; si hay varios y no está claro, preguntar
5. Los índices siempre se resuelven junto al `config.yaml` seleccionado;
   `project.root` delimita código, no cambia la ubicación física de los índices
6. Ignorar backups como `.navigatorBack/`; solo `.navigator/config.yaml` define
   una instancia válida

## Update on_request

- Solo cuando el usuario lo pida o acepte tras detectar desfase
- Actualizar capas afectadas; no regenerar todo por defecto
- Si `ai-context.md` tiene edición manual evidente: preguntar antes de sobrescribir o fusionar conservando notas del usuario
- Mantener `exclude` y política de secretos
- Avisos de modelo antes/después si el update es pesado
- Preferir regenerar solo capas/módulos afectados
- Si el update sería más caro que un bootstrap acotado, proponer bootstrap parcial del `root` y pedir confirmación

## Export opt-in a `AGENTS.md`

- Solo si el usuario lo confirma (`sources.export_agents_md` o petición explícita)
- Resumen compatible; no sobrescribir `AGENTS.md` existente sin confirmación
- No es el artefacto canónico (eso es `.navigator/ai-context.md`)

## Tras bootstrap — mensaje al usuario

Informar de forma breve:

1. Paths creados bajo `.navigator/`
2. Fuentes externas detectadas (sin pegar su contenido)
3. Gaps (symbols/graph off, cobertura parcial)
4. Cómo consultar: preguntas de onboarding → Capa 0; módulos → Capa 1; etc.
