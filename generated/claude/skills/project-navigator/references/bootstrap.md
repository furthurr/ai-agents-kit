# Bootstrap y update

## Bootstrap asistido (pasos)

1. Verificar autorización de bootstrap.
2. Detectar lenguajes, build system y fuentes externas de contexto (`sources.md`).
3. Detectar ubicación de `.navigator/` (monorepo; ver abajo). Si es ambiguo, **preguntar**.
4. Crear `.navigator/` si no existe.
5. Escribir `config.yaml` mínimo desde `templates/config.template.yaml`.
6. Generar `ai-context.md` breve desde `templates/ai-context.template.md`.
7. Generar `module-map.json` desde `templates/module-map.template.json`; si Git y
   el working tree permiten un baseline verificable, registrar `source_commit`
   tambien en `ai-context.md` y los indices generados.
8. No bloquear si faltan `symbols` o grafo.
9. Respetar `exclude` y no indexar secretos (`config.md`).
10. Ejecutar el gate post-bootstrap descrito abajo; corregir fallos antes de cerrar.
11. Informar: artefactos creados, fuentes externas detectadas, gaps, presupuesto y cómo consultar.

### Lectura para Capa 0 (presupuesto)

- Preferir README + "Contexto para IA" + manifests de build
- Usar pocas fuentes iniciales y ampliar si el alcance lo requiere
- No leer árboles completos
- Repos enormes: acotar `project.root` o pedir subproyecto

### Generación de capas 0–1

**ai-context.md:**

1. Idioma del repo o del usuario
2. No incluir secretos, tokens, connection strings ni PII
3. Referenciar paths de docs largas; no incrustarlas
4. Mapa rápido = resumen; dependencias viven en `module-map.json`
5. Listar fuentes externas detectadas; no sobrescribirlas
6. Revisar que sea breve y no duplique el mapa ni documentos externos

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
6. El contexto es conciso y referencia, no copia, documentación extensa.

Concisión de `ai-context.md`:

- Mantener propósito, stack principal, mapa rápido, fuentes y restricciones.
- Si se vuelve extenso o repetitivo, compactar antes de cerrar.
- Recortar primero dependencias exhaustivas, convenciones de implementación y
  detalles duplicados en `module-map.json` o documentación externa.

Concisión de `module-map.json`:

- Describir responsabilidades en una frase; si el mapa se vuelve extenso,
  reducir granularidad o acotar `project.root`, sin truncar JSON.

Si el gate falla, corregir solo los artefactos de `.navigator/`, repetir las
comprobaciones antes de cerrar.

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
- Preferir regenerar solo capas/módulos afectados
- Actualizar `source_commit` en cada artefacto tocado solo cuando represente un
  baseline Git verificable; no ocultar cambios locales bajo el hash de `HEAD`
- Si el update sería más caro que un bootstrap acotado, proponer bootstrap parcial del `root` y pedir confirmación

## Propiedad de `AGENTS.md`

- Navigator no crea, exporta ni sobrescribe `AGENTS.md`; su escritura se limita a
  `.navigator/**`.
- `documentation-orchestrator` mantiene la guía portable delimitada dentro de un
  plan global de escritura documental aprobado.
- `sources.export_agents_md` se conserva como campo legado ignorado. No se modifica
  la configuración del proyecto consumidor ni se interpreta como autorización.
- `.navigator/ai-context.md` sigue siendo el artefacto canónico de Capa 0.

## Tras bootstrap — mensaje al usuario

Informar de forma breve:

1. Paths creados bajo `.navigator/`
2. Fuentes externas detectadas (sin pegar su contenido)
3. Gaps (symbols/graph off, cobertura parcial)
4. Cómo consultar: preguntas de onboarding → Capa 0; módulos → Capa 1; etc.
