# Security Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `security` |
| Skill | [`security`](../../canonical/skills/security/SKILL.md) |
| Propósito | Auditar, documentar y remediar riesgos de seguridad paso a paso |
| Memoria | `.security/` |
| Estándares | OWASP MASVS, MASWE, MASTG, Mobile Top 10 y CWE |

Security Agent mantiene una memoria de riesgos priorizados y evidencia verificable.
Su foco incluye autenticación, red/TLS, secretos, almacenamiento, permisos,

## Cuándo usarlo

- Para una auditoría de seguridad móvil o de otra tecnología.
- Para revisar secretos, PII, cifrado, TLS, auth o permisos.
- Para analizar dependencias vulnerables o hardening.
- Para continuar un finding existente con micro-pasos.

En Android, iOS y Flutter dispone de checklist móvil precargado. En otras
tecnologías busca el estándar correspondiente y lo cachea sin usar herramientas
propietarias.

## Qué skill utiliza

La skill relaciona cada hallazgo con:

- Grupos MASVS: `STORAGE`, `CRYPTO`, `AUTH`, `NETWORK`, `PLATFORM`, `CODE`,
  `RESILIENCE` y `PRIVACY`.
- Debilidades MASWE y pruebas MASTG.
- Mobile Top 10 y un identificador CWE.

## Cómo trabaja

1. Clasifica plataforma, tecnología y superficie de riesgo.
2. Lee `.security/` si existe; si no, realiza una auditoría inicial en solo lectura.
3. Presenta hallazgos con severidad, referencia, ubicación e impacto.
4. Espera confirmación del alcance antes de persistir muchos findings.
5. Remedia un hallazgo mediante un solo micro-paso por turno.
6. Actualiza estado, bitácora, tablero y marca de sincronización.

## Qué produce

```text
.security/
├── README.md
├── findings/SEC-0001-*.md
├── security-tech-debt.md
├── pii-secrets.md
├── dependencies.md
└── standards/
```

`pii-secrets.md` registra existencia y ubicación, nunca los valores. Los hallazgos
usan estados `Pendiente`, `En progreso` y `Resuelto`.

## Ejemplos de uso

```text
@security Audita el almacenamiento y la red. Presenta primero los hallazgos
priorizados y no escribas todavía.
```

```text
@security Continúa con SEC-0001, explica el riesgo y propone solo el paso 1 de 3.
```

## Límites y seguridad

- La auditoría es de solo lectura hasta confirmar el alcance documental.
- Cada remediación necesita confirmación antes del siguiente micro-paso.
- No expone secretos, tokens, certificados ni PII real.
- No implementa features ni resuelve calidad, UI, datos o releases ajenos a seguridad.
- Cita `archivo:línea` y deriva cambios fuera de su dominio al especialista correcto.
