# Guía de la skill project-navigator

## Resumen

| Campo | Información |
|---|---|
| Entrada responsable | `documentation-orchestrator` (agente) |
| Skill | [`project-navigator`](../../canonical/skills/project-navigator/SKILL.md) |
| Propósito | Navegar e investigar un repositorio usando la capa más barata suficiente |
| Memoria | `.navigator/` |
| Estilo | Divulgación progresiva y respuestas con fuentes |

La skill Project Navigator, ejecutada localmente por Documentation Orchestrator,
reduce la reexploración del repositorio. No intenta leerlo todo:
elige la mínima capa que puede responder la pregunta y cita el índice o el código.

## Cuándo usarlo

- Para saber qué es un repositorio y cómo está organizado.
- Para localizar módulos, dependencias o un símbolo.
- Para estimar el impacto de cambiar algo.
- Antes de una feature o refactor cuando falta un mapa del proyecto.
- Para crear o actualizar índices de `.navigator/` bajo petición explícita.

## Capas de navegación

| Pregunta | Capa inicial | Si no basta |
|---|---|---|
| Propósito y organización | 0 `ai-context.md` | Capa 1 |
| Módulos y dependencias | 1 `module-map.json` | Capa 2 o 4 |
| Símbolos y firmas | 2 `symbols.json` | Capa 4 |
| Relaciones e impacto | 3 grafo, si está habilitado | Capa 1 + código puntual |
| Detalle de implementación | 4, código puntual | — |

## Cómo trabaja

1. Clasifica la petición como consulta, bootstrap/update o fuera de alcance.
2. En cada consulta comprueba el `config.yaml` y que los índices existan realmente.
3. Elige una o dos capas suficientes, sin volcar índices completos.
4. Responde de forma concisa citando fuentes y rangos de líneas.
5. Si falta una capa, distingue `capas_ausentes` de `capas_deshabilitadas` y reduce
   la confianza.

El bootstrap crea como mínimo:

```text
.navigator/
├── config.yaml
├── ai-context.md
└── module-map.json
```

`symbols.json` y `graph/` son opt-in. `cache/` no se versiona.

## Ejemplos de uso

```text
@documentation-orchestrator inspect: ¿Qué es este repositorio y cómo está organizado?
```

```text
@documentation-orchestrator inspect: ¿Dónde se define el entrypoint y qué módulos dependen de él?
Cita archivo y línea; no leas el repositorio completo.
```

```text
@documentation-orchestrator bootstrap-core: inicializa el core y presenta primero
el alcance, las fuentes, el presupuesto y el plan de escritura.
```

```text
@documentation-orchestrator sync-domain project-navigator: actualiza solo los índices existentes.
Presenta las capas afectadas y conserva las autorizaciones de escritura/exportación.
```

`inspect` no crea ni actualiza índices. Si faltan, están desfasados, no son
verificables o hay varias instancias ambiguas, usa fuentes directas y comunica
los límites. No obliga a bootstrap ni crea handoff core. La skill se conserva
separada de `architecture`; `@project-navigator` es un agente retirado sin alias.
Para instalaciones anteriores, consulta [migración segura](../migracion-agentes.md).

## Límites y confirmaciones

- Por defecto es de solo lectura.
- Solo escribe en `.navigator/`; la exportación opt-in a `AGENTS.md` requiere confirmación.
- No implementa features, refactors, tests, CI ni cambios en Git remoto.
- No selecciona ni cambia el modelo del host; solo recomienda un cambio manual si
  el proceso es pesado. Los avisos previo y final son informativos: continúa el
  trabajo autorizado en el mismo turno sin exigir «continúa» ni confirmar el modelo.
  No repite un aviso ya comunicado para el mismo alcance, incluido el orquestado.
  Crear, actualizar, exportar o sobrescribir índices conserva su autorización efectiva.
- Si piden código, aporta ubicación o mapa y redirige al agente adecuado.
