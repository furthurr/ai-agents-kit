## Carpeta canónica: `.design/`

Toda la documentación visual vive en una carpeta `.design/` (oculta, estilo
`.github/`). Su **ubicación depende de cuántos proyectos hay** (ver "Ubicación:
uno o varios proyectos"): una `.design/` en la **raíz** si es un solo proyecto, o
**una por proyecto** si hay varios independientes. Créala solo dentro de una
operación documental aprobada.

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
Solo para una operación documental solicitada (o un estudio pedido), NO generes
toda la documentación de golpe. Una consulta puntual y una implementación de
producto siguen las reglas de intención anteriores. Primero:
1. Escanea las fuentes visuales y detecta la tecnología.
2. Entrega un **resumen** de lo que encontraste (qué hay estandarizado, qué no)
   y una **lista de recomendaciones priorizadas** de qué documentar primero.
3. Pregunta al usuario qué quiere generar (todo, o por bloques: colores primero,
   luego tipografía, etc.). **Espera su confirmación** antes de escribir en masa.

### 1. Localizar / crear `.design/`
Si el plan documental aprobado incluye crearla y no existe, créala con la
estructura de arriba y un `README.md` inicial.
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

## Referencias bajo demanda

Las plantillas completas y criterios de clasificación están en
[`references/templates.md`](references/templates.md). Ábrela solo al crear o
actualizar el artefacto correspondiente; no es necesaria para una consulta,
triage o tarea puntual.

