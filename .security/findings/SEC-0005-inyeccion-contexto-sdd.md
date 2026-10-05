# SEC-0005: Instrucciones del workspace entran en contexto SDD con herramientas de escritura/ejecución

- Estado: Pendiente
- Severidad: 🟡 Media
- Referencia: OWASP LLM01:2025 (Prompt Injection) · LLM06:2025 (Excessive Agency) · CWE-1427 · CWE-250
- Ubicación: `canonical/agents/sdd.md:62-70`; `canonical/skills/sdd-spec/SKILL.md:177-182`; `generated/copilot/agents/sdd.agent.md:5-10,74-83`; `generated/claude/agents/sdd.md:5-14,80-90`; `generated/kiro/agents/sdd.md:3-7,8-44,108-117`
- Fecha de detección: 2026-10-05

## Descripción del riesgo

El flujo SDD indica al agente leer archivos de instrucciones y steering del
workspace (por ejemplo, `AGENTS.md`, instrucciones del host y `.sdd/steering/`).
Los artefactos generados conceden además capacidades de edición/escritura y
ejecución (`execute`, `Bash` o `shell`, según la plataforma). Las reglas de gates
y confirmación están expresadas principalmente en lenguaje natural; el contenido
no especifica una frontera explícita que haga tratar las instrucciones del
workspace como datos no confiables ni vincula cada acción de alto impacto con
una autorización aplicada en el límite de la herramienta.

Un workspace de terceros o comprometido podría incluir instrucciones indirectas
que intenten desviar la tarea hacia cambios o comandos no solicitados. El impacto
depende de la política efectiva del host y de si requiere aprobación para cada
operación; esa configuración no se inspeccionó ni se hizo una prueba dinámica.

## Impacto, esfuerzo y recomendación

- Impacto potencial: cambios no autorizados, ejecución de comandos o acceso a
  datos disponibles para el agente, si una instrucción manipulada logra dirigir
  las herramientas.
- Esfuerzo estimado: Medio.
- Recomendación: definir límites explícitos de confianza para archivos del
  workspace, mantener separadas las directivas autorizadas y el contenido que
  solo debe analizarse, y aplicar en el host controles por acción para escritura
  y shell. Validar con pruebas inocuas en cada adaptador/plataforma.

## Plan de remediación (no ejecutado)

- [ ] Revisar el tratamiento de `AGENTS.md`, steering y contenido del workspace;
  especificar qué fuentes se consideran configuración confiable y cuáles datos.
- [ ] Verificar que los permisos efectivos restrinjan escritura/ejecución al
  alcance autorizado y requieran aprobación de la acción concreta.
- [ ] Probar prompt injection indirecta con fixtures inocuos y herramientas
  instrumentadas en los hosts admitidos.

## Bitácora

- 2026-10-05: hallazgo diferencial aprobado y registrado. No se modificaron los
  agentes ni sus adaptadores.
