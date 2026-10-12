# Diseño — F10 Developer Agent Experimental

- Modo SDD: lite
- Alcance: una condición experimental F10 sobre el runner existente
- Estrategia: pruebas focalizadas del perfil/recibo, sandbox, clasificación y flujo;
  regresión de modos existentes; recorrido Docker completo con fixture falso

## Reutilización y composición

- Extender `PilotRequest`, validación CLI, `_prompt` y `run_pilot` para un único
  stage `developer-agent-experimental`, sin alterar las ramas de Lite, Lite2 ni
  no-SDD.
- Añadir un cargador local de perfil que use `tools/render.py` (`shared_substitutions`,
  `substitute`, `frontmatter`) sobre `canonical/agents/developer.md`, las skills
  canónicas Developer y data-api, `adapters/opencode/agents/developer.json` y las
  fuentes compartidas. Empaquetar solo los tres documentos renderizados bajo
  `.agent-profile/` dentro del contenedor de generación. El adaptador aporta la
  identidad/configuración Developer; el permiso efectivo se fija al allowlist
  sandbox actual de cuatro herramientas.
- El prompt completo del agente conserva el texto canónico Developer y añade solo
  la tarea F10 y los límites de experimento. La skill Developer se consulta desde
  `.agent-profile/skills/developer/SKILL.md`; `data-api` queda disponible en
  `.agent-profile/skills/data-api/SKILL.md`. No se añaden instrucciones SDD ni skills
  UI/extra.
- Registrar hashes de bytes canónicos, adaptador, fuentes compartidas, documentos
  renderizados, prompt final y recibo efectivo en artefactos propios del run.

## Resultado y guardas

- El actor conserva el evento `final_answer` sanitizado. Tras congelar el snapshot
  de entrega, un clasificador conservador determina `plan_only` solo ante una
  petición explícita de aprobación sin cambio en `feature.py`; ausencia de código
  con respuesta ambigua queda como `no_delivery`.
- Ambos estados terminales conservan respuesta y hashes, no abren contenedor
  evaluador ni ejecutan criterios F10.
- Con implementación, aplicar `only_target_bodies_changed`, exportar únicamente
  `feature.py`, comprobar que no se creó `.sdd/` en el workspace candidato y evaluar
  en el contenedor F10 ya aislado.
- Mantener el snapshot materializado, herramientas, MCP, sandbox y evaluador Docker
  existentes. El fixture falso escribe la referencia confiable solo por las
  herramientas sandbox; la fuente candidata permanece como datos en el host.

## Evidencia y verificación

- Añadir pruebas para elegibilidad F10 exclusiva, render/resolución/hash de fuentes,
  configuración y recibo Developer, allowlist de cuatro herramientas, aislamiento,
  restricción `.sdd/`, guard AST, texto final y estados `plan_only`/`no_delivery`,
  entrega congelada y ausencia de evaluación cuando no hay código.
- Añadir integración Docker de recorrido completo con actor falso y evaluator F10;
  sus metadatos deben declarar `fake_reference_fixture_used=true`,
  `benchmark_results=false`, `model_calls=0` y `opencode_invocations=0`.
- Registrar resultado por criterio y límites locales en
  `.agent-lab/sdd-escalation/`; distinguir fixture de ejecución LLM.

## Límites de seguridad y datos

- El contenedor de generación recibe solo los cuatro archivos del snapshot público
  y el perfil explícito; no hay bind mounts ni secretos.
- La configuración OpenCode tiene `instructions=[]`, `plugin=[]`, entorno aislado,
  herramientas builtin denegadas y las cuatro herramientas MCP sandbox permitidas.
- El evaluador, referencias y criterios reservados permanecen fuera de la generación.
- El guard AST y el evaluador procesan/ejecutan la entrega dentro de sus fronteras
  existentes; no se importa candidato en host.
- Si una fuente del perfil falta, un token queda sin resolver, una huella no coincide,
  se amplía el permiso o la entrega sale del alcance, el flujo falla cerrado.
