# Referencias — ui-design

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

