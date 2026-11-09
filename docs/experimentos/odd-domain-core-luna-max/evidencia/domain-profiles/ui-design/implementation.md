

# Skill: UI Design (documentación visual estandarizada)

## Identidad del MAS

MAS significa **Multi-Agent System**; `MAS:` se dirige al kit y `@<agente>` a un rol concreto.


Esta skill es la **referencia canónica** para documentar, estandarizar y desarrollar
lo visual de un proyecto, sin importar la tecnología (Android/Compose/XML, iOS/
SwiftUI/UIKit, Flutter, Web/CSS, React, etc.). `ob-developer` la usa para criterios
visuales de implementación y `ob-documentation-orchestrator` para trabajo documental.
La skill mantiene autoridad sobre sus estándares visuales.

> **Regla de dominio:** esta skill define criterios para lo **visual** (UI). El
> flujo documental no modifica lógica de negocio, APIs, datos, red, seguridad ni
> infraestructura. Cuando `ob-developer` la use en una feature multicapa, este límite
> delimita los criterios visuales, no el alcance integral de Developer; para las
> demás capas aplica el plan global y las fuentes pertinentes.

## Cuándo usar esta skill

- Documentar el sistema de diseño: colores, tipografía, espaciado, formas,
  sombras/elevación, íconos y componentes.
- Antes de trabajar cualquier pantalla o componente visual (leer primero
  `.design/` para reutilizar lo estandarizado).
- Auditar la UI y registrar **deuda técnica** (colores hardcodeados, tamaños
  mágicos, inconsistencias, duplicados, falta de estandarización).
- Sincronizar la documentación tras cambios de diseño en el repositorio.

## Elegir el flujo según la intención

- **Consulta sin persistencia:** responde con las fuentes existentes. No crees
  `.design/`, archivos ni índices, y no inicies un inventario documental completo
  por una pregunta sobre un token, componente o patrón visual.
- **Implementación de producto:** Developer coordina la implementación completa;
  esta skill aporta criterios visuales bajo demanda. No inicialices ni sincronices
  `.design/` como efecto de implementar una pantalla o componente.
- **Documentación con persistencia:** trabaja en `.design/` solo cuando el usuario
  solicite documentar, inicializar, sincronizar o registrar hallazgos. Una auditoría
  puede limitarse a informar sin escribir. Si falta `.design/`, presenta primero el
  estudio y el alcance propuesto; espera su aprobación antes de crearla.

## Detección de tecnología (dónde viven los tokens)

Antes de documentar, detecta la tecnología y localiza las fuentes de verdad
visuales:

| Tecnología | Dónde buscar lo visual |
|------------|------------------------|
| Android + Jetpack Compose | `**/theme/**`, `Color.kt`, `Theme.kt`, `Type.kt`, `Shape.kt`, módulos `designsystem`/`ui`, `@Composable` de componentes |
| Android + XML | `res/values/colors.xml`, `dimens.xml`, `styles.xml`, `themes.xml`, `font/`, `drawable/` |
| iOS SwiftUI/UIKit | `Assets.xcassets` (colorset), `Color`/`UIColor` extensions, `Font`, design system framework |
| Flutter | `ThemeData`, `ColorScheme`, `TextTheme`, `theme/`, widgets de design system |
| Web / CSS / SCSS | `:root` custom properties, `tokens.*`, `variables.scss`, `theme.*` |
| React / RN | `theme.ts`, `tokens.ts`, styled-components/Tailwind config, librería de componentes |

Si la tecnología no está en la tabla, infiere las fuentes visuales por patrones
de nombres (color, theme, font, style, spacing, component) y documenta igual.

## Uso durante implementación de producto

`ob-developer` resuelve requisitos visuales ambiguos, rediseños de múltiples pantallas
o flujos, nuevos estados/comportamientos, cambios reutilizables de impacto amplio y
coordinación entre UI y otras capas mediante su modo PLAN. Esta skill no recomienda
ni inicia SDD, no crea `.sdd/` y no detiene un cambio multicapa. Implementa UI conforme
al plan global aprobado, reutiliza patrones existentes y verifica estados y
accesibilidad pertinentes.

Durante una implementación de producto, no ejecutes el bootstrap/sync completo de
`.design/` salvo que el usuario lo solicite como parte del alcance. Al cierre,
Developer evalúa si `.design/` quedó desactualizada y ofrece la actualización
documental correspondiente.

## Qué documentar (checklist visual)

- **Colores:** paleta base, colores semánticos (primario, error, éxito, etc.),
  temas claro/oscuro, opacidades. Hex + nombre + uso.
- **Tipografía:** familias/fuentes, escala de tamaños, pesos, alturas de línea,
  letter-spacing, estilos de texto nombrados (título, cuerpo, caption…).
- **Espaciado:** escala de spacing/padding/margin y dimensiones estándar.
- **Formas y elevación:** radios de esquina, bordes, sombras, niveles de
  elevación.
- **Iconografía y assets:** set de íconos, tamaños, formato, nomenclatura.
- **Componentes:** catálogo con propósito, variantes, estados (normal, disabled,
  pressed, error…), y tokens que consume cada componente.

## Índice de contexto para otros agentes

`.design/README.md` incluye una sección **"Contexto para IA"**: resumen denso del
stack visual, dónde viven los tokens, temas y estado de estandarización. Es el
punto de entrada que otros agentes leen para orientarse antes de tocar UI.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- En trabajo documental, limita las escrituras a UI; en implementación con Developer,
  aplica estos criterios visuales sin restringir el alcance integral autorizado.
- No expongas secretos, tokens de auth ni certificados.
- Cita `archivo:línea` como fuente de verdad; no inventes valores.
- Documenta lo estandarizado Y lo estandarizable (marca lo segundo como deuda).
- git solo de lectura.
