# Prompt para iniciar REC-01

Copiar el bloque siguiente en una sesión nueva abierta en este repositorio o en el worktree asignado. El prompt autoriza trabajar el fix, no acciones Git ni instalaciones globales. Para iniciar varios implementadores, preparar antes el baseline y aislamiento indicados en el protocolo.

```text
Implementa el hallazgo REC-01 — Unificar la política de secretos — de este repositorio ai-agents-kit.

Lee primero:
1. docs/auditoria/CONSOLIDADO-HALLAZGOS-RECURRENTES.md (ficha REC-01 y seguimiento).
2. docs/auditoria/PROTOCOLO-REMEDIACION.md.
3. docs/auditoria/seguimiento/REC-01.md.
4. Las instrucciones del proyecto y los contratos/skills aplicables a esta remediación.

Si los documentos no están en tu worktree, pide el baseline de preparación; no inventes su contenido. Si trabajas en la carpeta original antes de ese commit, comprueba que eres la única sesión escritora y asume también la coordinación de REC-01. En worktree paralelo actúa como implementadora y deja los tableros generales a la coordinadora.

OBJETIVO
Eliminar la contradicción por la cual Git/release permiten incluir secretos reales mediante autorización conversacional, mientras la política general lo prohíbe. Distinguir nombres sospechosos, configuraciones públicas, placeholders y secretos reales, sin mostrar valores sensibles.

INICIO
- Revisa Git, registra HEAD, rama/worktree y cambios previos sin commit; preserva trabajo ajeno.
- Confirma el problema en fuentes actuales y vincula la deuda ya existente, especialmente docs/mejoras.md y consumidores pertinentes. Las líneas de los informes son históricas.
- Delimita los archivos y verificaciones. Ámbito esperado: canonical/skills/git-commit/, canonical/skills/release-management/, contratos de seguridad y documentación/pruebas que realmente consuman esta política. Ajusta ese ámbito con evidencia, no por suposición.
- Revisa si REC-02, REC-15 o FUT-17/18 están asignados y comparte archivos con ellos. Coordina cualquier solapamiento antes de editarlo. No resuelvas esos otros hallazgos como parte de este fix.
- Si sigue vigente, registra confirmado/en curso en la ficha de sesión y, si asumes coordinación exclusiva, también en la fila REC-01 y el historial del consolidado. Si ya no existe, entrega evidencia de no vigencia.

IMPLEMENTACIÓN
1. Establece una regla coherente: un secreto real confirmado queda excluido y la autorización del usuario no convierte su publicación en una opción válida. Informar ubicación y motivo sin reproducir el valor.
2. Conserva una decisión contextual para archivos potencialmente sensibles sin secreto confirmado. Un nombre como .env no basta para equiparar configuración pública o placeholders con credenciales reales.
3. Elimina opciones contradictorias y actualiza consumidores directamente afectados. Conserva autorizaciones de commit/push/release y demás controles independientes.
4. Reutiliza controles automatizados existentes cuando aporten verificación real; si falta un control necesario, incorpora el mínimo proporcional y documenta sus límites. No afirmes detección universal ni expandas el trabajo a una plataforma general de escaneo.
5. Modifica fuentes canónicas y herramientas responsables; genera distribuciones mediante el renderer cuando corresponda. No edites generated/ manualmente ni instales los cambios en configuraciones globales.

VERIFICACIÓN
- Usa exclusivamente fixtures sintéticos, nunca credenciales reales.
- Verifica el caso de secreto detectable con solicitud de inclusión: no debe quedar autorizado para el commit; no realices commits reales durante esta prueba.
- Verifica configuración pública y placeholders: no deben clasificarse como secretos solo por nombre.
- Verifica que diagnósticos y resultados no reproducen valores del fixture sensible.
- Comprueba coherencia Git/release/seguridad y consumidores pertinentes, con pruebas negativas significativas. Los tests de presencia de frases no acreditan comportamiento runtime.
- Ejecuta pruebas relevantes y, si modificas fuentes distribuidas, render/validate y enlaces cuando corresponda. Registra comandos y resultados observados.
- Si algún criterio de la ficha requiere comportamiento en host y no puedes ejecutarlo, documenta exactamente lo pendiente y conserva el hallazgo abierto; no sustituyas esa evidencia por una garantía textual.

REGISTRO Y ENTREGA
- Completa docs/auditoria/seguimiento/REC-01.md: diagnóstico actual, baseline, archivos, decisiones, deuda vinculada, pruebas, cada criterio de cierre, pendientes y estado propuesto.
- Si eres implementadora paralela, no edites los dos tableros generales. Entrega la ficha a la coordinadora para integración y actualización de estado/historial.
- Si eres coordinadora e implementadora exclusiva, actualiza únicamente REC-01 y su historial en el consolidado. Marca cerrado solo si todos los criterios están acreditados sobre el resultado integrado en esta carpeta; si falta evidencia, usa integrado pendiente de verificación o bloqueado, con causa. Declara cambios sin commit.
- No hagas commit, push, tags, release o instalaciones globales sin autorización explícita.
- Tu respuesta final debe incluir: qué corregiste, archivos afectados, pruebas/resultados, estado de REC-01, evidencia y pendientes.

Continúa hasta completar la implementación y la verificación posible. Si un contrato aplicable exige aprobación o falta una decisión indispensable, explica el punto concreto y solicita esa decisión siguiendo el protocolo.
```
