# Project Navigator Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `project-navigator` |
| Skill | [`project-navigator`](../../canonical/skills/project-navigator/SKILL.md) |
| Propósito | Navegar e investigar un repositorio usando la capa más barata suficiente |
| Memoria | `.navigator/` |
| Estilo | Divulgación progresiva y respuestas con fuentes |

Project Navigator reduce la reexploración del repositorio. No intenta leerlo todo:
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
@project-navigator ¿Qué es este repositorio y cómo está organizado?
```

```text
@project-navigator ¿Dónde se define el entrypoint y qué módulos dependen de él?
Cita archivo y línea; no leas el repositorio completo.
```

```text
@project-navigator Inicializa los índices del proyecto y presenta primero el
alcance, las fuentes y el presupuesto.
```

## Límites y confirmaciones

- Por defecto es de solo lectura.
- Solo escribe en `.navigator/`; la exportación opt-in a `AGENTS.md` requiere confirmación.
- No implementa features, refactors, tests, CI ni cambios en Git remoto.
- No selecciona ni cambia el modelo del host; solo recomienda un cambio manual si
  el proceso es pesado.
- Si piden código, aporta ubicación o mapa y redirige al agente adecuado.
