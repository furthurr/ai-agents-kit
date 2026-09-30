# Referencias — code-quality

## Plantillas

### `README.md`
```markdown
# Calidad de código — <Proyecto>

Estado canónico de la calidad. Léelo antes de auditar o remediar.

## Estado de sincronización
- Lenguajes detectados: <p. ej. Kotlin, Swift>
- Último commit documentado: `<hash>` (o fecha si no hay git)
- Última actualización: <YYYY-MM-DD>

## Contexto para IA (resumen denso)
- Stack y build: <lenguajes, gestor de build, framework de test>
- Quality gate: <passed/failed y condiciones clave>
- Métricas actuales: <cobertura, duplicación, complejidad>
- Hallazgos abiertos: <nº por severidad; enlace a quality-tech-debt.md>
- Reglas Sonar de referencia: <familias/lenguajes en standards/>

## Índice
- Tablero de hallazgos: `quality-tech-debt.md`
- Detalle por hallazgo: `findings/`
- Métricas: `metrics.md`
- Reglas cacheadas: `standards/`
```

### `findings/QLT-NNNN-titulo.md`
```markdown
# QLT-NNNN: <título>

- Estado: Pendiente | En progreso | Resuelto
- Severidad: 🔴 Blocker / 🟠 High / 🟡 Medium / 🟢 Low
- Regla Sonar: `kotlin:SXXXX` · Cualidad: Maintainability | Reliability
- Ubicación: `archivo:línea`
- Fecha detección: <YYYY-MM-DD>

## Descripción
<qué regla se incumple y por qué importa>

## Plan de remediación (micro-pasos)
- [ ] Paso 1: <...>
- [ ] Paso 2: <...>

## Bitácora
- <YYYY-MM-DD> Paso 1 aplicado: <qué cambió y por qué>
```

### `quality-tech-debt.md` (tablero maestro)
```markdown
# Calidad — Tablero de hallazgos

| ID | Severidad | Regla | Cualidad | Hallazgo | Ubicación | Estado |
|----|-----------|-------|----------|----------|-----------|--------|
| QLT-0001 | 🟠 | kotlin:S3776 | Maintainability | Complejidad cognitiva alta | `archivo:línea` | Pendiente |
```

### `metrics.md`
```markdown
# Métricas de calidad
- Cobertura de pruebas: <%> (fuente: JaCoCo/…)
- Duplicación: <%>
- Complejidad: <resumen>
- Deuda técnica estimada: <tiempo>
- Quality gate: <passed/failed y condiciones>
```

