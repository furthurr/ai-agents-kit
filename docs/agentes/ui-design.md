# UI Design Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `ui-design` |
| Skill | [`ui-design`](../../canonical/skills/ui-design/SKILL.md) |
| Propósito | Documentar y estandarizar la apariencia y el sistema visual |
| Memoria | `.design/` |
| Alcance | Colores, tipografía, espaciado, formas, iconos, componentes, temas y UX visual |

UI Design Agent convierte los estilos reales de un proyecto en un sistema visual
reutilizable. Documenta lo que ya está estandarizado y registra como deuda lo que
conviene unificar.

## Cuándo usarlo

- Para extraer o documentar un design system.
- Antes de crear una pantalla o componente visual.
- Para unificar colores, tipografía, spacing, radios, sombras o iconos.
- Para auditar inconsistencias visuales y registrar deuda de UI.
- Después de cambios de tema o componentes.

## Qué skill utiliza

La skill `ui-design` cubre:

- Foundations: colores, tipografía, espaciado, forma/elevación e iconografía.
- Componentes, variantes, estados y tokens que consumen.
- Temas claro/oscuro y accesibilidad visual.
- Nomenclatura conceptual DTCG/W3C en tablas Markdown, sin generar `.tokens.json`.
- Detección adaptada a Compose/XML, SwiftUI/UIKit, Flutter, Web/CSS y React/RN.

## Recomendación de modelo

Las consultas y ajustes visuales puntuales reciben un aviso `BAJO` o `MEDIO` y
pausan antes de trabajar. Extracciones completas, rediseños amplios o varios
sistemas visuales recomiendan `MEDIO` o `ALTO` y también pausan antes del barrido.
«Continúa» reanuda sin declarar modelo; las aprobaciones de propuestas visuales
siguen siendo independientes.

## Cómo trabaja

1. Detecta la tecnología y las fuentes visuales reales.
2. Lee `.design/README.md` y los componentes afectados en tareas puntuales.
3. En una primera ejecución presenta un estudio de lo estandarizado y lo pendiente.
4. Espera confirmación antes de generar documentación visual masiva.
5. Antes de implementar, clasifica la ruta directa o SDD; recomienda SDD para
   rediseños con múltiples pantallas/flujos, nuevos comportamientos o cruce de dominios.
6. El usuario decide si cambia de agente; nunca se crea `.sdd/` automáticamente.
7. Actualiza tokens, componentes, deuda y marca de sincronización.

## Qué produce

```text
.design/
├── README.md
├── foundations/
│   ├── colors.md
│   ├── typography.md
│   ├── spacing.md
│   ├── shape-elevation.md
│   └── iconography.md
├── components.md
└── ui-tech-debt.md
```

## Ejemplos de uso

```text
@ui-design Extrae la paleta y la tipografía actuales. Presenta primero lo que
encontraste y no inventes valores.
```

```text
@ui-design Revisa este componente y registra inconsistencias visuales como deuda;
no modifiques la lógica de negocio.
```

## Límites y confirmaciones

- Solo trabaja sobre lo visual: UI, tokens, componentes, temas y UX visual.
- No documenta ni modifica lógica de negocio, APIs, datos, red, seguridad o infraestructura.
- Si recomienda SDD, cita el hallazgo/componente y se detiene antes del código;
  SDD no amplía el alcance visual de este agente.
- Conserva la identidad existente y no inventa decisiones de diseño.
- Cita la fuente (`archivo:línea`) y no expone secretos, tokens de autenticación ni certificados.
- La extracción inicial requiere estudio, propuesta y confirmación.
