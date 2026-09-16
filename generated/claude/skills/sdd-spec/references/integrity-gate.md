# Integrity Gate — SDD

Cargar en **Implementación** y **Fase 4**. Objetivo: integridad > teatro.

## Marcar tareas

- `[x]` **solo si** existe el path del artefacto citado **o** el comando de verificación pasó con log/evidencia.
- Si se omite algo: dejar `[ ]` o usar `[omitido: razón breve]` — **nunca** `[x]` falso.
- Prohibido tests tautológicos: `assert true`, `XCTAssertTrue(true)`, `expect(true).toBe(true)` sin sujeto real.
- Dependencia en manifest/build sin uso en código/tests → quitar o declarar como deuda explícita en `verification.md`.
- Carpetas de tests/generators creadas vacías **no** cuentan como tarea hecha.
- No añadir dependencias de PBT/test sin al menos un test que las use en la misma entrega.
- TDD focalizado/estricto exige evidencia del RED esperado y del GREEN. Sin RED
  observado, etiquetar honestamente como caracterización o cobertura retroactiva.

## Estado de fase y transición

- Toda spec nueva `standard` o `deep` declara en cada artefacto `Modo SDD`, `Fase`,
  `Estado` y el gate pendiente o aprobado que corresponda.
- La reanudación determina la próxima operación por esos marcadores; no inferirá
  aprobación solo por la existencia del archivo. Si faltan o se contradicen, pedir
  aclaración antes de recomendar un nivel.
- La recomendación de la próxima fase se presenta junto al resumen y al gate actual,
  pero no crea un gate nuevo. No repetir la misma recomendación dentro de una fase
  mientras no cambien alcance, riesgo ni nivel requerido.
- Antes de iniciar la próxima fase deben estar confirmadas la aprobación de la fase
  actual y el nivel recomendado o el nivel actual. Un cambio de alcance o riesgo
  invalida el preflight anterior y exige recalcularlo.

## Antes de GATE 4

1. Recorrer `tasks.md`: cada `[x]` debe mapear a path en disco o evidencia de comando.
2. Construir matriz de `verification.md` con columna **Evidencia** (path o cmd).
3. Self-check de 3–5 RNF críticos del propio spec (búsqueda en código).
4. No cerrar GATE 4 con requisitos sin evidencia o con `[x]` huérfanos.
5. Contrastar la estrategia declarada en `design.md` con tareas, tests y evidencia;
   cada excepción conserva su razón y una verificación alternativa.

## Cierre `lite`

`lite` no abre Fase 4 ni Gate 4, pero una implementación no se cierra sin
`verification.md` compacto:

1. Recorrer `tasks.md`; cada `[x]` debe tener artefacto o comando verificable.
2. Registrar RED o baseline, GREEN, suite final y excepciones honestas.
3. Mapear requisito, tarea, test/check, evidencia y estado.
4. Revisar solo los RNF declarados y aplicables; no inventar una cuota.
5. Si solo hubo planificación, no crear evidencia ni marcar implementación hecha.

## Ejemplos de omisión honesta

```markdown
- [omitido: PBT no aplica; sin invariante algebraico]
- [omitido: mock de red aplazado; solo dominio puro en esta wave]
```
