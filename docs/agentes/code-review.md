# Code Review Agent

## Resumen

| Campo | Información |
|---|---|
| ID | `code-review` |
| Skills | [`code-quality`](../../canonical/skills/code-quality/SKILL.md) y [`security`](../../canonical/skills/security/SKILL.md), según alcance |
| Propósito | Revisar calidad y seguridad mediante una sola entrada |
| Memoria | `.quality/` con IDs `QLT`; `.security/` con IDs `SEC` |
| Estándares | Sonar/Clean Code para calidad; OWASP/CWE para seguridad |

Sustituye los agentes anteriores, no sus skills. Una revisión completa aplica
ambos procedimientos en la misma sesión; una petición específica o ID de finding
selecciona solo su dominio. No mezcla escalas de severidad ni migra registros.

## Cómo trabaja

1. Clasifica proyecto, archivos/módulos, dominios e intención. Una revisión puntual
   no se expande a todo el repositorio ni a otro dominio sin autorización.
2. Recomienda `BAJO`, `MEDIO` o `ALTO` y pausa. «Continúa» reanuda sin declarar el
   modelo; no repite el preflight al cargar la segunda skill si ya estaba cubierto.
3. Carga solo los procedimientos necesarios y cita evidencia verificable.
4. Consulta/`inspect`: no escribe findings, cachés ni marcas de sincronización.
5. Auditar y documentar, inicializar o sincronizar: registra todos los hallazgos
   verificados del alcance, agrupando ocurrencias de una misma causa, sin volver
   a elegir severidades. Pregunta ante ambigüedad, ampliaciones, sobrescritura
   manual o recursos insuficientes para completar la operación.
6. Entrega resumen con dominio, ID, severidad original, referencia, ubicación,
   estado y limitaciones. No declara métricas que no haya podido medir.

Seguridad también considera configuración, auth, red, permisos, almacenamiento
y dependencias cuando el alcance lo requiere. Si una revisión de solo calidad
detecta un riesgo, informa y ofrece ampliar; no escribe en el dominio no autorizado.

## Ejemplos

```text
@code-review Solo calidad: revisa la complejidad del módulo de pagos.
Responde en el chat sin escribir archivos.
```

```text
@code-review Solo seguridad: audita y documenta el almacenamiento y TLS.
```

```text
@code-review Haz una revisión completa de calidad y seguridad de autenticación
y documenta los hallazgos verificados. No modifiques código de producto.
```

```text
@code-review Continúa con SEC-0001: explica el riesgo y propone el primer
micro-paso. Espera mi autorización antes de modificar código.
```

En Pi, usa `/code-review <tarea>`. Las invocaciones de skill `/security` o
`/code-quality` siguen disponibles donde las soporte el host.

## Handoff y correcciones

El orquestador puede derivar con `target: code-review` y `scope: [.quality/]`,
`[.security/]` o `[.quality/, .security/]`. La escritura respeta la misma selección;
`inspect` exige `write_scope: none`. Un resultado conjunto de escritura acredita
ambos dominios antes de declararse entregado. `gate_state` no autoriza por sí solo.

Auditar/documentar no autoriza remediar: se aprueba el primer micro-paso y cada
siguiente. Un cambio que requiere requisitos, diseño o coordinación amplia se
recomienda a SDD, sin cambiar automáticamente de agente. Los hallazgos se verifican
antes de marcarse resueltos. Nunca se documentan secretos o valores reales de PII.

Para actualizar instalaciones anteriores consulta
[la guía de migración de agentes](../instalacion.md#actualizar-a-code-review).
Los tests estáticos del kit verifican contratos; el comportamiento del host se
comprueba con [los escenarios smoke](../code-review-smoke.md).
