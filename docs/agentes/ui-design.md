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

## Cómo trabaja

1. Detecta la tecnología y las fuentes visuales reales.
2. Lee `.design/README.md` y los componentes afectados en tareas puntuales.
3. En una primera ejecución presenta un estudio de lo estandarizado y lo pendiente.
4. Espera confirmación antes de generar documentación visual masiva.
5. Actualiza tokens, componentes, deuda y marca de sincronización.

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
- Conserva la identidad existente y no inventa decisiones de diseño.
- Cita la fuente (`archivo:línea`) y no expone secretos, tokens de autenticación ni certificados.
- La extracción inicial requiere estudio, propuesta y confirmación.
