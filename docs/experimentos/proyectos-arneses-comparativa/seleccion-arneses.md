# Selección de los cinco arneses

## Criterio

Se buscaron proyectos que resuelvan **la misma capa que el MAS**: distribuir
instrucciones, agentes y skills a un host de codificación. Se excluyeron por
esta ronda los proyectos centrados en SDD (se probarán después) y los runtimes
de orquestación pura (`claude-flow`, `openrig`, `munder-difflin`,
`claude-task-master`).

## Los cinco

| # | Proyecto | Por qué entra | Solapamiento con el MAS |
|---|---|---|---|
| 1 | **wshobson/agents** | Única paridad 1:1: fuente Markdown canónica, adapters, generadores, validación y CI con CLIs reales | Arquitectura, distribución y evals |
| 2 | **obra/superpowers** | Orquestación subagent-driven con bootstrap de sesión y 15 skills; instalación oficial para OpenCode | Disparo automático de skills y subagentes |
| 3 | **affaan-m/ECC** | Multi-harness, 26 agentes, 134 skills, tools propias, memoria/instincts | Catálogo, comandos y empaquetado |
| 4 | **gentle-ai** | Instalador que configura OpenCode, orquestador y skills; backup/rollback | Experiencia de instalación y orquestación |
| 5 | **garrytan/gstack** | 62 skills de rol con comandos y contratos de evidencia | Empaquetado por rol |

## Brazo adicional: SDD (MAS)

No es un arnés externo. Se añadió el agente `sdd` y la skill `sdd-spec` del MAS
para medir el coste de la metodología Spec-Driven Development (SDD-Tiny) sobre la
misma tarea, el mismo modelo y las mismas pruebas. Su resultado se reporta aparte
de los cinco arneses externos.

## Agentes SDD-like de los arneses

- **superpowers**: ejecutado como `superpowers-sdd` con `writing-plans` y
  `subagent-driven-development`.
- **ECC**: ejecutado como `ecc-plan` con el subagente `planner` y revisión con
  `code-reviewer`.
- **gstack**, **wshobson** y **gentle-ai**: medidos con su agente por defecto;
  no se añadió un sub-brazo SDD.

## Proyectos SDD externos

- **cc-sdd** (`npx cc-sdd --opencode-skills`): ejecutado; genera
  `.kiro/specs/<feature>/` con un piloto que obliga a crear el spec antes del
  código.
- **OpenSpec** (`openspec init --tools opencode`): ejecutado; genera
  `openspec/changes/<cambio>/`.
- **Spec Kit** (`specify init . --integration opencode`): ejecutado; genera
  `specs/<feature>/{spec,plan,tasks}.md`.

## Descartados para esta ronda

- **claude-flow**, **openrig**, **munder-difflin**, **claude-task-master**:
  runtime/orquestación, no distribución de instrucciones.
- **agentic-awesome-skills**: catálogo/descubrimiento; suplente si un arnés no
  fuera ejecutable. No fue necesario.
- **anthropics/skills**, **openai/skills**, **github/awesome-copilot**:
  referencias de formato y canal, no competidores.
