# REC-01 — Unificar la política de secretos

- **Modo SDD:** standard.
- **Tipo:** bugfix no trivial de seguridad.
- **Intención:** implementación y verificación.
- **Fase:** 1 — Requirements.
- **Estado:** requisitos satisfechos según Verification; spec cerrada con evidencia conductual real y aprobación del Gate 4.
- **Gate aprobado:** Gate 1 — el usuario respondió «procede» a la solicitud de aprobación de estos requisitos.
- **Gates posteriores:** 2 y 3 aprobados; Gate 4 aprobado explícitamente mediante «Aprobar cierre REC-01» tras presentar evidencia real y suites satisfactorias.
- **Ejecutor:** sesión SDD, coordinadora e implementadora exclusiva de REC-01; sin subagentes escritores.
- **Fecha:** 2026-10-10.
- **Baseline:** `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880`, rama `main`, carpeta original.

## Objetivo y trazabilidad

Eliminar la posibilidad contractual de incluir secretos confirmados mediante
autorización conversacional, conservando la decisión contextual sobre archivos
potencialmente sensibles que no contienen secretos confirmados.

Fuentes de alcance y cierre:
- [Prompt REC-01](../../../docs/auditoria/PROMPT-REC-01.md).
- [Consolidado, sección REC-01](../../../docs/auditoria/CONSOLIDADO-HALLAZGOS-RECURRENTES.md).
- [Protocolo](../../../docs/auditoria/PROTOCOLO-REMEDIACION.md).
- [Registro de sesión](../../../docs/auditoria/seguimiento/REC-01.md).
- [Deuda existente, sección P0.5](../../../docs/mejoras.md).

El alcance y la continuidad en standard se aceptaron con «Procede» después de
explicar la exclusión de lite. Esa aceptación permite formalizar esta fase, no
aprueba sus requisitos ni los gates posteriores.

## Actual — defecto confirmado por inspección

- **A1:** CUANDO se identifica un archivo sensible EL SISTEMA permite incluirlo
  mediante autorización explícita sin distinguir un secreto confirmado de un
  archivo cuyo nombre es sospechoso.
  Evidencia: `canonical/skills/git-commit/SKILL.md:34,83–106`.
- **A2:** CUANDO se prepara el commit de una release EL SISTEMA hereda la
  decisión del Paso 1.5 de Git, aunque el proyecto prohíbe commits de secretos.
  Evidencia: `canonical/skills/release-management/SKILL.md:314–316` y
  `README.md:174`.

Esta evidencia acredita la contradicción textual, no una filtración ni una
ejecución conductual del modelo. No se ha ejecutado todavía un fixture de regresión.

## Esperado — requisitos verificables

### Historia 1 — impedir la publicación de secretos confirmados

Como usuaria del flujo Git/release, quiero que una autorización de publicación
no permita incluir credenciales, para evitar incorporarlas al historial.

- **R1:** CUANDO se confirma un secreto en un archivo propuesto para commit
  EL SISTEMA DEBERÁ excluir ese contenido del conjunto admisible para el commit.
- **R2:** CUANDO se solicita incluir un secreto confirmado EL SISTEMA DEBERÁ
  rechazar esa inclusión aunque la solicitud sea explícita.
- **R3:** CUANDO informa sobre un secreto confirmado EL SISTEMA DEBERÁ indicar
  su ubicación y motivo sin reproducir el valor en mensajes, diagnósticos ni
  evidencia conservada.

### Historia 2 — distinguir indicios de secretos

Como usuaria, quiero que una configuración pública o un placeholder no se
equiparen a una credencial solo por el nombre del archivo.

- **R4:** CUANDO el único indicio es el nombre o extensión de un archivo
  EL SISTEMA DEBERÁ tratarlo como potencialmente sensible, no como secreto confirmado.
- **R5:** CUANDO la revisión acredita configuración pública o placeholders sin
  secretos confirmados EL SISTEMA DEBERÁ permitir la decisión contextual de
  inclusión, manteniendo las autorizaciones independientes del flujo Git/release.
- **R6:** SI la revisión no permite resolver un indicio ENTONCES EL SISTEMA
  DEBERÁ informar que la clasificación sigue pendiente sin presentar ese archivo
  como seguro ni ofrecer una excepción para un secreto confirmado.

### Historia 3 — aplicar y demostrar una política coherente

Como mantenedora del kit, quiero contratos y controles verificables alineados,
para no sustituir comportamiento efectivo por garantías textuales.

- **R7:** EL SISTEMA DEBERÁ aplicar la misma prohibición de inclusión de secretos
  confirmados en Git, release, contratos de seguridad y consumidores directamente afectados.
- **R8:** EL SISTEMA DEBERÁ disponer de un control automatizado pertinente y
  ejecutable sobre fixtures sintéticos que rechace la credencial detectable del
  caso de prueba y acepte sus contrastes públicos o con placeholders.
- **R9:** SI el control requerido no puede completar su evaluación ENTONCES
  EL SISTEMA DEBERÁ informar el fallo sin declarar aprobada la comprobación de secretos.
- **R10:** EL SISTEMA DEBERÁ documentar el alcance y límites del control sin
  afirmar detección universal ni equivalencia entre pruebas del control y runtime del host.

## Inalterado — garantías de no regresión

- **I1:** EL SISTEMA DEBERÁ SEGUIR requiriendo autorización explícita para commit,
  push, tag, release y demás escrituras que la requieran en sus contratos.
- **I2:** EL SISTEMA DEBERÁ SEGUIR preservando trabajo ajeno y sin modificar la
  configuración global durante esta remediación.
- **I3:** EL SISTEMA DEBERÁ SEGUIR modificando fuentes canónicas y regenerando
  `generated/` mediante el renderer, sin ediciones manuales de distribuciones.
- **I4:** EL SISTEMA DEBERÁ SEGUIR registrando cada criterio de cierre con evidencia
  observada, conservando REC-01 abierto cuando falte algún criterio exigido.

## Aceptación, errores y casos límite

| Caso | Resultado exigido | Requisitos |
|---|---|---|
| Credencial sintética detectable con solicitud explícita de inclusión | Exclusión/rechazo acreditado sin commit real | R1, R2, R8 |
| Mismo fixture en archivo de nombre normal | No depender exclusivamente del nombre sospechoso | R1, R4, R8 |
| Configuración pública en archivo de nombre sospechoso | No clasificarla como secreto por nombre; conservar decisión contextual | R4, R5 |
| Placeholders en archivo de nombre sospechoso | No clasificarlos como credenciales reales por nombre | R4, R5 |
| Indicio no resuelto o evaluación fallida | Estado pendiente/fallo, nunca aprobación inventada | R6, R9 |
| Diagnósticos y evidencias del fixture sensible | Ausencia del valor del fixture en todas las salidas conservadas | R3 |
| Git, release y consumidores distribuidos | Política coherente y autorizaciones independientes preservadas | R7, I1, I3 |
| Evidencia parcial, incluida imposibilidad de runtime en host | Límites y siguiente acción registrados; no cerrar REC-01 | R10, I4 |

Los tests de presencia de frases pueden comprobar propagación de contratos, pero
no acreditan el comportamiento runtime de Git/release en un host. El diseño
delimitará las verificaciones ejecutables y la evidencia conductual necesaria;
si no puede obtenerse, el hallazgo permanecerá abierto.

## Alcance y exclusiones

- Archivos principales: `canonical/skills/git-commit/`,
  `canonical/skills/release-management/`, consumidores de seguridad/Git directamente
  afectados, documentación y controles de `tools/`/CI que la evidencia justifique.
- Distribuciones: únicamente las generadas como consecuencia de fuentes modificadas.
- Registros: `docs/auditoria/seguimiento/REC-01.md` y exclusivamente la fila REC-01
  y sus entradas históricas en el consolidado.
- Vincular la deuda P0.5 sin cerrar sus elementos ajenos a REC-01.
- No resolver REC-02, REC-15, FUT-17/18, ni construir una plataforma general de escaneo.
- No trabajar en `.docs/`, no instalar globalmente y no ejecutar commits, push,
  tags ni release. Las pruebas usarán exclusivamente fixtures sintéticos.

## Supuestos y limitaciones observadas

- No se encontró una spec previa dedicada a esta política en la búsqueda de
  `requirements.md`/`bugfix.md`; otras specs mencionan confidencialidad genérica
  o fixtures de laboratorio y no constituyen continuidad de REC-01.
- Navigator y arquitectura no contienen un baseline Git verificable; se usaron
  solo como orientación y las afirmaciones del diagnóstico se contrastaron en fuentes.
- `.security/README.md` describe F07, no una auditoría de esta política.
- La terminal antes detectada en `.docs/` ya no aparece en la comprobación de
  procesos de esta reanudación. No se detectó otra sesión escritora; observar
  procesos y cwd es una comprobación puntual, no un mecanismo de exclusión mutua.
- Los tableros muestran REC-02, REC-15 y FUT-17/18 pendientes y sin asignación.
  Cualquier nueva asignación o escritura concurrente obliga a coordinar antes de editar.

## Cierre

Gates 1–4 aprobados. Implementación, pruebas y evidencia conductual real registradas en
[verification.md](verification.md). Spec cerrada tras aprobación explícita del Gate 4.
