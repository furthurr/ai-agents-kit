# Integrity Gate — SDD

Cargar en **Implementación** y **Fase 4**. Objetivo: integridad > teatro.

## Marcar tareas

- `[x]` **solo si** existe el path del artefacto citado **o** el comando de verificación pasó con log/evidencia.
- Si se omite algo: dejar `[ ]` o usar `[omitido: razón breve]` — **nunca** `[x]` falso.
- Prohibido tests tautológicos: `assert true`, `XCTAssertTrue(true)`, `expect(true).toBe(true)` sin sujeto real.
- Dependencia en manifest/build sin uso en código/tests → quitar o declarar como deuda explícita en `verification.md`.
- Carpetas de tests/generators creadas vacías **no** cuentan como tarea hecha.
- No añadir dependencias de PBT/test sin al menos un test que las use en la misma entrega.
- TDD focalizado exige evidencia del RED esperado y del GREEN. Sin RED observado,
  etiquetar honestamente como caracterización o cobertura retroactiva. TDD estricto
  es una opción retirada y no puede marcarse como estrategia vigente.

## Estado de fase y transición

- Toda spec nueva `standard` declara en cada artefacto `Modo SDD`, `Fase`,
  `Estado` y el gate pendiente o aprobado que corresponda.
- La reanudación determina la próxima operación por esos marcadores; no inferirá
  aprobación solo por la existencia del archivo. Si faltan o se contradicen, pedir
  aclaración antes de continuar.
- El resumen de transición se presenta junto al gate actual, pero no crea un gate
  nuevo. Para iniciar la próxima fase, espera solo la aprobación del gate SDD real
  que corresponda. Si no hay gate intermedio
  (Implementación → Verification), continúa con Verification en el mismo turno.
- Un cambio de alcance o riesgo invalida la evaluación previa: reevalúa el trabajo
  autorizado. Si falta autorización para el alcance nuevo, pregunta por ella.
  Si el cambio requiere reclasificar el modo SDD, solicita aprobación de ese cambio
  de flujo.

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

## Atención y entregas

- Los controles de atención definidos en diseño/tareas requieren evidencia de la
  garantía real antes del cierre: transacciones, concurrencia, idempotencia o
  recuperación según aplique. Un mock que oculta el mecanismo no es evidencia.
- Comprobar integración entre entregas y requisitos transversales antes de cerrar
  el conjunto. Cerrar entregas parciales no demuestra garantías de extremo a extremo.
- Direct conserva criterios y evidencia breve en conversación, sin verification.md.
- Seleccionar profundidad no aprueba gates ni amplía alcance. Respetar elección
  pendiente, autorización e intención antes de ejecutar su flujo.

## Enmiendas y vigencia

- Antes de ejecutar, verificar validación explícita vigente del alcance completo,
  elección, autorización y gates. Elegir modo/ejecutor no acredita aceptación del
  alcance; una aprobación anterior no cubre contenido nuevo. Aplicar scope-depth.md.
- Contrastar requisitos formalizados con alcance validado; diferencias funcionales
  requieren exponer el cambio y resolver aprobación, no ejecutarlas silenciosamente.
- Una enmienda identifica requisito, dependencias y aprobaciones afectadas según
  `spec-continuity.md`; no evade gates ni autoridad de la spec por su nota baja.
- Marcar pendiente de revalidación solo tareas/evidencias afectadas. La evidencia
  anterior permanece histórica, no acredita el comportamiento modificado.
- Conservar historia de cierre y acuerdos sustituidos; no desmarcar tareas ajenas
  ni sobrescribir un cierre como si el requisito nuevo siempre hubiera existido.

## Ejemplos de omisión honesta

```markdown
- [omitido: PBT no aplica; sin invariante algebraico]
- [omitido: mock de red aplazado; solo dominio puro en esta wave]
```
