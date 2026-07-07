---
name: ui-design
description: >-
  Documenta y estandariza TODO lo visual de cualquier proyecto (agnóstica a la
  tecnología). Extrae fuentes, colores, tamaños, espaciados, formas, sombras,
  íconos y componentes hacia una carpeta canónica `.design/`. Mantiene la
  documentación sincronizada leyendo el historial de git de forma incremental y
  lleva un registro de "deuda técnica de UI" priorizado por severidad. Úsala al
  trabajar cualquier aspecto visual: diseño, UI, design system, tokens, colores,
  tipografía, componentes, temas claro/oscuro, estilos o auditoría visual.
---

# Skill: UI Design (documentación visual estandarizada)

Esta skill es la **referencia canónica** para documentar y estandarizar todo lo
visual de un proyecto, sin importar la tecnología (Android/Compose/XML, iOS/
SwiftUI/UIKit, Flutter, Web/CSS, React, etc.). Complementa al agente `UI Design
Agent`. Si el agente y esta skill divergen, **manda esta skill**.

> **Regla de alcance (inviolable):** esta skill trabaja SOLO sobre lo **visual**
> (UI). No documenta ni modifica lógica de negocio, APIs, datos, red, seguridad
> ni infraestructura. Si aparece una petición fuera de UI, decláralo y detente.

## Cuándo usar esta skill

- Documentar el sistema de diseño: colores, tipografía, espaciado, formas,
  sombras/elevación, íconos y componentes.
- Antes de trabajar cualquier pantalla o componente visual (leer primero
  `.design/` para reutilizar lo estandarizado).
- Auditar la UI y registrar **deuda técnica** (colores hardcodeados, tamaños
  mágicos, inconsistencias, duplicados, falta de estandarización).
- Sincronizar la documentación tras cambios de diseño en el repositorio.

## Carpeta canónica: `.design/`

Toda la documentación visual vive en una carpeta `.design/` (oculta, estilo
`.github/`). Su **ubicación depende de cuántos proyectos hay** (ver "Ubicación:
uno o varios proyectos"): una `.design/` en la **raíz** si es un solo proyecto, o
**una por proyecto** si hay varios independientes. Si no existe, **créala**.

```
.design/
├── README.md                      # Índice + Estado de sincronización + Contexto para IA
├── foundations/
│   ├── colors.md                  # Paleta, colores semánticos, temas claro/oscuro
│   ├── typography.md              # Fuentes, tamaños, pesos, alturas de línea, estilos
│   ├── spacing.md                 # Escala de espaciado y dimensiones
│   ├── shape-elevation.md         # Esquinas/radios, bordes, sombras, elevación
│   └── iconography.md             # Íconos y assets visuales
├── components.md                  # Catálogo de componentes visuales
└── ui-tech-debt.md                # Deuda técnica de UI priorizada
```

> **Nota sobre tokens:** se documentan en **Markdown legible** (tablas). Como
> referencia conceptual de categorías se usa la nomenclatura del estándar
> **DTCG/W3C** (color, dimension, fontFamily, fontWeight, typography, shadow,
> border, spacing), pero NO se generan archivos `.tokens.json`.

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

## Ubicación: uno o varios proyectos

Antes de crear `.design/`, determina si el workspace tiene **uno o varios
proyectos independientes** (busca marcadores en carpetas distintas:
`settings.gradle(.kts)`/`build.gradle`, `*.xcodeproj`/`Podfile`, `pubspec.yaml`,
`package.json`):

- ⚠️ **Excepción Flutter / React Native / KMP:** si en la **raíz** hay
  `pubspec.yaml` (Flutter) o `package.json` con `react-native`, las carpetas
  `android/` e `ios/` son **plataformas del mismo proyecto**, NO proyectos
  independientes → usa **UN solo `.design/` en la raíz**.
- **Un solo producto multi-módulo** (p. ej. una app Android con módulos
  `core`, `feature/*`): usa **UN solo `.design/` en la raíz** y, si hay estilos
  por módulo, crea una sub-sección por módulo dentro de cada archivo (p. ej. en
  `colors.md`: `## <módulo>`).
- **Varios proyectos/apps independientes** en carpetas separadas (p. ej. una app
  Android y una app iOS, cada una en su carpeta): crea **una `.design/` dentro de
  cada proyecto** (`<proyecto>/.design/`). **No** las mezcles en una sola carpeta
  de la raíz, porque suelen tener design systems distintos.
- Si dudas si el diseño es compartido o independiente, **pregunta** al usuario
  antes de escribir.

## Flujo de trabajo

### 0. Estudio y propuesta (antes de escribir en masa)
Al invocarse por primera vez en un proyecto (o cuando el usuario pida un
estudio), NO generes toda la documentación de golpe. Primero:
1. Escanea las fuentes visuales y detecta la tecnología.
2. Entrega un **resumen** de lo que encontraste (qué hay estandarizado, qué no)
   y una **lista de recomendaciones priorizadas** de qué documentar primero.
3. Pregunta al usuario qué quiere generar (todo, o por bloques: colores primero,
   luego tipografía, etc.). **Espera su confirmación** antes de escribir en masa.

### 1. Localizar / crear `.design/`
Si no existe, créala con la estructura de arriba y un `README.md` inicial.
`.design/` **se versiona con el repositorio** (es documentación). No coloques
dentro binarios pesados ni copias de assets: referencia su ruta original.

### 2. Leer el estado de sincronización
En `.design/README.md` hay una sección **"Estado de sincronización"** con el
último commit documentado (hash + fecha) y la tecnología detectada. Léela.

### 3. Revisar el historial de git (incremental)
- Si HAY marca de commit: revisa solo lo nuevo relacionado con UI:
  `git log <hash>..HEAD --name-only` y filtra por rutas visuales (color, theme,
  font, style, dimen, shape, component, drawable, assets, res/values, etc.).
  También `git diff <hash>..HEAD -- <rutas UI>` para ver los cambios concretos.
- Si NO hay marca (primera vez): haz un **barrido completo** de las fuentes
  visuales del proyecto.
- **Sin git** (no es repositorio o no hay commits): omite el diff, haz barrido
  completo y usa la **fecha** como marca de sincronización en lugar del hash.
- Solo comandos de git de **lectura** (`git log`, `git diff`, `git show`).

### 4. Extraer y actualizar la documentación
Actualiza los `.md` afectados con lo estandarizado en el código Y lo que se
puede estandarizar aunque aún no lo esté (deja constancia de ambos). Cita
siempre `archivo:línea` de la fuente de verdad. No inventes valores.

### 5. Registrar deuda técnica de UI
Actualiza `ui-tech-debt.md` con hallazgos priorizados por severidad (ver
plantilla). Del más delicado al menos importante.

### 6. Actualizar la marca de sincronización
Escribe en `.design/README.md` el hash de `HEAD` y la fecha actual como último
commit documentado.

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

## Plantillas

### `README.md`
```markdown
# Sistema de diseño — <Proyecto>

Documentación canónica de todo lo visual. Léela antes de trabajar cualquier
aspecto de UI.

## Estado de sincronización
- Tecnología detectada: <p. ej. Android + Jetpack Compose>
- Último commit documentado: `<hash>` (o fecha si no hay git)
- Última actualización: <YYYY-MM-DD>

## Contexto para IA (resumen denso)
- Stack visual: <p. ej. Jetpack Compose + Material 3>
- Dónde viven los tokens: <mapa carpeta/archivo → categoría visual>
- Temas: <claro/oscuro; cómo se selecciona>
- Convenciones clave: <nombres de tokens, escala de spacing, tipografía base>
- Estado de estandarización: <qué está tokenizado y qué sigue hardcodeado>

## Índice
- Fundamentos: colores, tipografía, espaciado, formas/elevación, iconografía
- Componentes: catálogo visual
- Deuda técnica de UI

## Cómo se mantiene
La skill `ui-design` revisa el historial de git desde el último commit
documentado y actualiza esta carpeta cuando detecta cambios de diseño.
```

### `foundations/colors.md`
```markdown
# Colores

Fuente de verdad: `<archivo:línea>`

## Paleta base
| Nombre | Hex | Uso |
|--------|-----|-----|

## Colores semánticos
| Token | Claro | Oscuro | Uso |
|-------|-------|--------|-----|

## Notas de estandarización
- <colores duplicados / candidatos a token / hardcodeados detectados>
```

### `foundations/typography.md`
```markdown
# Tipografía

Fuente de verdad: `<archivo:línea>`

## Fuentes
| Familia | Pesos disponibles | Uso |
|---------|-------------------|-----|

## Estilos de texto
| Estilo | Tamaño | Peso | Altura de línea | Uso |
|--------|--------|------|-----------------|-----|
```

### `components.md`
```markdown
# Componentes

Catálogo de componentes visuales.

## <Componente>
- Propósito: <para qué sirve>
- Variantes: <primaria, secundaria, …>
- Estados: <normal, disabled, pressed, error, loading…>
- Tokens que consume: <color, tipografía, spacing, forma/elevación>
- Fuente de verdad: `<archivo:línea>`
```

### `ui-tech-debt.md`
```markdown
# Deuda técnica de UI

Ordenada de mayor a menor severidad. Trabaja de arriba hacia abajo.

## 🔴 Crítica
| # | Hallazgo | Ubicación (archivo:línea) | Impacto | Esfuerzo | Recomendación |
|---|----------|---------------------------|---------|----------|---------------|

## 🟠 Alta
| # | Hallazgo | Ubicación | Impacto | Esfuerzo | Recomendación |
|---|----------|-----------|---------|----------|---------------|

## 🟡 Media
| # | Hallazgo | Ubicación | Impacto | Esfuerzo | Recomendación |
|---|----------|-----------|---------|----------|---------------|

## 🟢 Baja
| # | Hallazgo | Ubicación | Impacto | Esfuerzo | Recomendación |
|---|----------|-----------|---------|----------|---------------|
```

## Criterios para clasificar deuda técnica

- **🔴 Crítica:** rompe consistencia global o accesibilidad (contraste
  insuficiente, colores hardcodeados en muchos lugares, tamaños de fuente fijos
  que ignoran accesibilidad). Para contraste usa el criterio **WCAG 2.1 AA**:
  mínimo **4.5:1** para texto normal y **3:1** para texto grande (≥18pt o ≥14pt
  en negrita) y componentes/íconos.
- **🟠 Alta:** inconsistencias notorias entre pantallas, componentes duplicados,
  valores mágicos repetidos que deberían ser tokens.
- **🟡 Media:** falta de nombres semánticos, tokens definidos pero poco usados,
  pequeñas divergencias de espaciado.
- **🟢 Baja:** mejoras cosméticas, documentación faltante, oportunidades de
  refactor menor.

Cada hallazgo debe indicar **impacto** (qué mejora) y **esfuerzo** estimado.

## Reglas

- Comunícate en español por defecto; si el usuario escribe en otro idioma o lo
  pide, adáptate. Sé claro y conciso.
- Solo UI: nunca documentes ni toques lógica de negocio, APIs, datos o red.
- No expongas secretos, tokens de auth ni certificados.
- Cita `archivo:línea` como fuente de verdad; no inventes valores.
- Documenta lo estandarizado Y lo estandarizable (marca lo segundo como deuda).
- git solo de lectura.
