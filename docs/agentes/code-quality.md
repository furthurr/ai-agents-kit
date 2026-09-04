# Code Quality Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `code-quality` |
| Skill | [`code-quality`](../../canonical/skills/code-quality/SKILL.md) |
| Propósito | Auditar y mejorar mantenibilidad, fiabilidad y prácticas de código |
| Memoria | `.quality/` |
| Base | Taxonomía Clean Code y reglas públicas de SonarQube |

Este agente ayuda a convertir problemas de calidad en hallazgos priorizados,
trazables y continuables entre sesiones. Su foco incluye complejidad, duplicación,

## Cuándo usarlo

- Para revisar code smells, complejidad o duplicación.
- Para analizar cobertura y calidad de pruebas.
- Para priorizar deuda técnica de mantenibilidad o fiabilidad.
- Para hacer un refactor seguro y localizado.
- Para consultar o continuar hallazgos documentados en `.quality/`.

Si aparece una vulnerabilidad o un riesgo de seguridad, lo registra como nota y lo
deriva al Security Agent. No es el agente para UI, APIs, releases o features.

## Qué skill utiliza

La skill `code-quality` usa:

- Tipos de issue de Sonar: `Bug`, `Code Smell` y `Security Hotspot`.
- Severidades `Blocker`, `High`, `Medium` y `Low/Info`.
- Reglas identificadas por lenguaje, por ejemplo `kotlin:SXXXX` o `dart:SXXXX`.
- Métricas de cobertura, duplicación, complejidad, deuda estimada y quality gate.
- Reglas públicas cacheadas bajo `.quality/standards/` cuando hace falta consultar
  el detalle de un lenguaje.

## Cómo trabaja

1. Clasifica la solicitud y delimita el código relevante.
2. Lee el estado de `.quality/` si existe; si no, realiza una auditoría inicial en
   solo lectura.
3. Presenta hallazgos con severidad, regla, ubicación, impacto y esfuerzo.
4. Espera confirmación del alcance antes de persistir una auditoría masiva.
5. Para remediar, trabaja un hallazgo y un micro-paso cada vez.
6. Actualiza el finding y el tablero, dejando una bitácora para reanudarlo.

## Qué produce

```text
.quality/
├── README.md
├── findings/QLT-0001-*.md
├── quality-tech-debt.md
├── metrics.md
└── standards/
```

El README contiene contexto para IA, estado de sincronización, lenguajes y
quality gate. Cada finding conserva estado `Pendiente`, `En progreso` o `Resuelto`.

## Ejemplos de uso

```text
@code-quality Revisa la complejidad del módulo de pagos y presenta primero los
hallazgos priorizados. No hagas cambios todavía.
```

```text
@code-quality Continúa con el finding QLT-0001, proponiendo un solo micro-paso.
```

## Límites y confirmaciones

- La auditoría inicial es de solo lectura.
- Requiere confirmación del alcance antes de crear muchos findings.
- La remediación se hace un micro-paso a la vez y espera confirmación.
- No corrige seguridad; deriva al Security Agent.
- No implementa features ni trabaja UI, datos, releases o Git remoto.
- Nunca expone secretos ni tokens; usa placeholders y citas `archivo:línea`.
