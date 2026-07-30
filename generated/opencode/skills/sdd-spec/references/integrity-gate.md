# Integrity Gate — SDD

Cargar en **Implementación** y **Fase 4**. Objetivo: integridad > teatro.

## Marcar tareas

- `[x]` **solo si** existe el path del artefacto citado **o** el comando de verificación pasó con log/evidencia.
- Si se omite algo: dejar `[ ]` o usar `[omitido: razón breve]` — **nunca** `[x]` falso.
- Prohibido tests tautológicos: `assert true`, `XCTAssertTrue(true)`, `expect(true).toBe(true)` sin sujeto real.
- Dependencia en manifest/build sin uso en código/tests → quitar o declarar como deuda explícita en `verification.md`.
- Carpetas de tests/generators creadas vacías **no** cuentan como tarea hecha.
- No añadir dependencias de PBT/test sin al menos un test que las use en la misma entrega.

## Antes de GATE 4

1. Recorrer `tasks.md`: cada `[x]` debe mapear a path en disco o evidencia de comando.
2. Construir matriz de `verification.md` con columna **Evidencia** (path o cmd).
3. Self-check de 3–5 RNF críticos del propio spec (búsqueda en código).
4. No cerrar GATE 4 con requisitos sin evidencia o con `[x]` huérfanos.

## Ejemplos de omisión honesta

```markdown
- [omitido: PBT no aplica; sin invariante algebraico]
- [omitido: mock de red aplazado; solo dominio puro en esta wave]
```
