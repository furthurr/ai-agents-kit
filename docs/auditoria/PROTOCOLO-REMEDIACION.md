# Protocolo de remediación por hallazgo y entre sesiones

## 1. Punto de entrada

- Recurrentes: [consolidado y tablero REC](CONSOLIDADO-HALLAZGOS-RECURRENTES.md).
- Específicos: [backlog y tablero FUT](BACKLOG-HALLAZGOS-NO-RECURRENTES.md).
- Primera ejecución: [prompt REC-01](PROMPT-REC-01.md).
- Evidencia por sesión: [plantilla](PLANTILLA-RESULTADO.md), guardada en `seguimiento/<ID>.md`.

**Un ID representa un hallazgo, no una autorización para resolver todos los relacionados.** La ficha define objetivo y cierre; verificar su vigencia y adaptar la implementación al código actual.

## 2. Preparación y persistencia

Los dos tableros, este protocolo, la plantilla, el prompt, los cinco informes originales y los registros de seguimiento se mantienen en `docs/auditoria/`, una carpeta disponible para versionado normal. Toda `.agent-lab/` continúa excluida mediante `.gitignore`.

La ubicación permite versionar; **no crea commits ni hace que archivos sin commit aparezcan en otros worktrees**. Antes de trabajo paralelo:

1. Revisar los archivos de preparación y el diff, separándolos de cambios ajenos.
2. Obtener autorización explícita y crear un commit de preparación que incluya los documentos de `docs/auditoria/` y cualquier ajuste pendiente de `.gitignore` pertinente.
3. Registrar ese commit como baseline inicial y crear cada rama/worktree desde él, con autorización y herramientas apropiadas al entorno.
4. Asignar un ID, un responsable, la rama/worktree, baseline y archivos previstos; la coordinadora actualiza el tablero.

Si se empieza antes de ese commit, ejecutar **una sola sesión** en la carpeta que contiene los documentos. Esa sesión puede asumir coordinación e implementación para REC-01; registrar HEAD y archivos sin commit del baseline. No afirmar aislamiento ni iniciar escritores paralelos en esa misma carpeta.

## 3. Roles

### Sesión coordinadora

- Mantiene exclusivamente los tableros y su historial cuando hay paralelismo.
- Reserva el ID y comprueba dependencias/solapamientos antes de asignar.
- Revisa los registros y cambios entregados; integra con autorización del usuario.
- Verifica el resultado integrado y decide el estado según la evidencia.
- Resuelve conflictos de archivos compartidos y planifica la siguiente tanda.

### Sesión implementadora

- Trabaja solo el ID asignado en su carpeta de trabajo.
- Confirma el diagnóstico, baseline y alcance; registra inicio y resultados en su ficha.
- Implementa y verifica; actualiza documentación/deudas existentes directamente afectadas sin abrir registros paralelos innecesarios.
- Entrega archivos modificados, pruebas, pendientes y estado propuesto.
- En paralelo, no modifica tableros generales ni los registros de otra sesión.

Una implementadora solo asume también coordinación si trabaja de forma exclusiva en esa carpeta. Esa condición debe quedar en su ficha.

## 4. Estados y condiciones

| Estado | Cuándo se usa |
|---|---|
| Pendiente | Sin diagnóstico actual confirmado; puede haber prompt/ficha preparados. |
| Confirmado | El problema sigue vigente con evidencia actual y alcance identificado. |
| En curso | Sesión asignada, baseline registrado y corrección iniciada. |
| Corregido en rama | Implementación y comprobaciones disponibles en trabajo aislado; indicar si hay cambios aún sin commit y verificaciones pendientes. No significa integrado. |
| Integrado pendiente de verificación | Cambios presentes en la línea de trabajo coordinada, pero falta verificación integrada o un criterio de cierre. En sesión exclusiva puede usarse para cambios locales sin commit, declarándolo. |
| Cerrado | Todos los criterios de cierre exigidos están acreditados sobre el resultado integrado; baseline final y límites registrados. El estado no implica por sí solo commit, push o release. |
| Bloqueado | Falta autorización, dependencia, herramienta, entorno o decisión necesaria; registrar estado previo y cómo desbloquear. |
| No vigente | La fuente actual demuestra que el problema ya no existe; registrar evidencia, sin atribuir un fix a esta sesión. |

No sustituir una verificación conductual por un test de presencia de frases. Distinguir los criterios originales del hallazgo de cobertura adicional deseable: si los criterios exigen runtime en una superficie, el cierre sigue pendiente; si exigen matriz, límites explícitos y controles soportados, pero cierto runtime no está disponible, cerrar solo al acreditar esos criterios y registrar la cobertura adicional como follow-up separado, visible y no bloqueante. Nunca declarar PASS en hosts no ejecutados ni borrar sus limitaciones. Los hallazgos independientes pueden avanzar mientras exista ese follow-up.

## 5. Paralelismo y archivos compartidos

- Usar worktrees/ramas separados para sesiones implementadoras paralelas. Si el entorno usa worktrees administrados, usar su gestor correspondiente.
- La asignación incluye archivos previstos y recursos externos: dos worktrees no aíslan modificaciones de `~/.config/opencode/` ni otras rutas globales.
- No instalar, ejecutar o cambiar configuración global desde dos sesiones al mismo tiempo. Las pruebas de instalación deben usar perfiles temporales cuando sea posible.
- Generar `generated/` desde las fuentes y adaptadores del worktree propio; no editar distribuciones manualmente. La coordinadora vuelve a renderizar/verificar después de integrar cuando proceda.
- Si surge un archivo compartido, comunicarlo y acordar propietario/secuencia antes de editarlo; no ampliar la reserva silenciosamente.
- Los cambios globales o instalaciones requieren alcance explícito independiente del fix del repositorio.

### Tandas orientativas

| Tanda | Trabajo propuesto | Condición |
|---|---|---|
| Primera | REC-01 y REC-02 | Revisar primero consumidores y tests compartidos. Empezar REC-01 solo mientras no haya baseline de preparación en Git. |
| Contratos | REC-03 → REC-04; FUT-01 coordinado | Comparten handoff y selección de intención. |
| Distribución | REC-05, REC-06 y REC-07 | Paralelismo solo con archivos/tests compartidos delimitados; integración verificada. |
| Simplificación | REC-11 → REC-09 → REC-13 | Mantener contrato de identidad y medir lecturas. REC-14/15 pueden solaparse con esos cambios. |
| Evidencia | REC-08 y REC-16 | Preparar protocolo al inicio; registrar la fuente exacta evaluada y repetir tras cambios relevantes. |

Estas tandas son propuestas, no reservas activas ni una declaración de independencia ya comprobada.

## 6. Flujo de una sesión

1. Leer ficha, protocolo, instrucciones del proyecto y registros existentes.
2. Inspeccionar estado de Git; no sobreescribir trabajo ajeno. Registrar baseline y si hay cambios sin commit.
3. Confirmar vigencia con referencias actuales. Si no existe, entregar evidencia de no vigencia.
4. Definir archivos, pruebas, dependencias y recursos externos; comunicar solapamientos.
5. Registrar diagnóstico y paso a en curso. Implementar el cambio mínimo completo siguiendo contratos vigentes y gates aplicables.
6. Ejecutar pruebas significativas; comprobar consumidores y distribución cuando corresponda.
7. Completar `seguimiento/<ID>.md` con resultados reales, incluyendo fallos/bloqueos.
8. Entregar resultado. La coordinadora actualiza fila e historial, integra con autorización y verifica antes de cerrar.

No hacer commit, push, tags, release o instalaciones globales sin autorización explícita. Una sesión puede entregar un fix y evidencia sin commit, pero debe declararlo para que la integración sea inequívoca.

## 7. Registro de evidencia e integración

Cada ficha debe identificar baseline, archivos afectados, registros de deuda, pruebas y resultado; nunca incluir credenciales reales, respuestas sin sanitizar o dumps completos de configuración local. Las evidencias voluminosas pueden referenciar un artefacto sanitizado mediante ruta estable y procedencia.

Durante trabajo paralelo, el tablero visible en el worktree implementador puede ser una instantánea: su ficha es la entrega local; el estado global autoritativo es el de la coordinadora. Evitar copiar una tabla antigua sobre estados más recientes.

Al integrar, la coordinadora:

1. Lee el diff completo, el registro y los criterios originales.
2. Resuelve conflictos preservando cambios de otras sesiones.
3. Comprueba fuentes/distribuciones y ejecuta verificaciones relevantes sobre el conjunto.
4. Actualiza el tablero y añade una fila histórica con fecha, estado, evidencia y pendientes.
5. Registra integración y cierre en la ficha; si quedan criterios pendientes, conserva el estado abierto.

Los informes originales se conservan como diagnóstico histórico. No reescribir sus hallazgos para aparentar que nunca existieron.
