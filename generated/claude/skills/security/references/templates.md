# Referencias — security

## Plantillas

### `README.md`
```markdown
# Seguridad — <Proyecto>

Estado canónico de seguridad. Léelo antes de auditar o remediar.

## Estado de sincronización
- Plataforma/tecnología: <p. ej. Android, iOS, Flutter>
- Estándar aplicado: <MASVS/MASWE/Top 10 | ASVS | …>
- Último commit documentado: `<hash>` (o fecha si no hay git)
- Última actualización: <YYYY-MM-DD>

## Contexto para IA (resumen denso)
- Perfil de riesgo: <qué maneja la app: PII, pagos, auth…>
- Superficie sensible: <almacenamiento, red/TLS, auth, permisos>
- PII/secretos: <existencia y dónde; sin valores — ver pii-secrets.md>
- Hallazgos abiertos: <nº por severidad; enlace a security-tech-debt.md>
- Dependencias vulnerables: <resumen; ver dependencies.md>

## Índice
- Tablero de hallazgos: `security-tech-debt.md`
- Detalle por hallazgo: `findings/`
- PII y secretos: `pii-secrets.md`
- Dependencias: `dependencies.md`
- Estándares cacheados: `standards/`
```

### `findings/SEC-NNNN-titulo.md`
```markdown
# SEC-NNNN: <título>

- Estado: Pendiente | En progreso | Resuelto
- Severidad: 🔴/🟠/🟡/🟢
- Referencia: MASVS-<GRUPO> · MASWE-XXXX · CWE-XXX · (Mobile Top 10 Mx)
- Ubicación: `archivo:línea`
- Fecha detección: <YYYY-MM-DD>

## Descripción del riesgo
<qué es y por qué importa>

## Plan de remediación (micro-pasos)
- [ ] Paso 1: <...>
- [ ] Paso 2: <...>

## Bitácora
- <YYYY-MM-DD> Paso 1 aplicado: <qué cambió y por qué>
```

### `security-tech-debt.md` (tablero maestro)
```markdown
# Seguridad — Tablero de hallazgos

| ID | Severidad | Hallazgo | Ref (MASVS/CWE) | Ubicación | Estado |
|----|-----------|----------|-----------------|-----------|--------|
| SEC-0001 | 🔴 | Tráfico en claro | MASVS-NETWORK / CWE-319 | `archivo:línea` | Pendiente |
```

### `pii-secrets.md`
```markdown
| Dato | Tipo | Dónde aparece | Cifrado | Almacenamiento | Notas |
|------|------|---------------|---------|----------------|-------|
```
> Solo existencia y ubicación; **nunca** valores, tokens ni certificados.

