# MAS — Multi-Agent System

## Nombre oficial

En este proyecto, **MAS** significa **Multi-Agent System** (sistema multiagente).
Es el nombre del sistema formado por los agentes, skills, orquestación, handoffs,
adaptadores y artefactos generados de AI Agents Kit.

`MAS` identifica al sistema y no a una herramienta, proveedor o modelo LLM
concreto. El MAS coordina procedimientos y agentes, pero no selecciona ni cambia
el modelo del host.

## Convención de mensajes

- `MAS:` indica que el comentario o la instrucción se dirige al sistema completo.
- `@<agente>` indica que se dirige a un agente concreto, por ejemplo `@code-review`
  o `@sdd`.
- `MAS + @<agente>` indica una instrucción del sistema que debe ejecutar un agente
  concreto dentro de su alcance.

Ejemplos:

```text
MAS: conserva la trazabilidad entre agentes y no repitas un gate confirmado.
@code-review: solo seguridad; revisa secretos y configuración de red.
MAS + @sdd: convierte este cambio en una spec con trazabilidad completa.
```

Esta convención es **semántica**, no una garantía de sintaxis nativa en cada
host. En Antigravity 2.0, `@<agente>` no está confirmado como invocación: el
mecanismo real de selección de la UI debe registrarse en el
[smoke](antigravity-smoke.md). `sdd` es el identificador nominal que reemplaza
`{{sdd_agent}}`, no un comando. Las skills usan el slash documentado
`/<skill-name>`; `/agents` solo se documenta para el CLI, no se extrapola a 2.0.

`subagent: true` habilita que un rol pueda ser invocado; no autoriza delegación
automática. Se mantienen los handoffs, el alcance explícito, los gates de la
skill y las aprobaciones del usuario. Un padre habilitado por el host puede
probar `invoke_subagent` cuando el usuario lo solicite, pasando contexto y
autorizaciones; los roles del kit no encadenan hijos por iniciativa propia.

## Desambiguación

`MAS` usado solo siempre se refiere al sistema multiagente de este kit. No debe
confundirse con `MASVS`, `MASWE` o `MASTG`, que son nombres propios de estándares y
guías de OWASP Mobile Application Security. Esos identificadores se mantienen
completos y no se abrevian como `MAS`.

## Fuente de verdad

La identidad se documenta aquí y se replica de forma compacta en los agentes y
skills canónicos. `tools/render.py` la propaga a las seis distribuciones: Copilot,
OpenCode, Kiro, Claude Code, Pi y Antigravity. El catálogo mantiene ocho agentes y
diez skills; los artefactos de `generated/` no se editan a mano. Antigravity apunta
inicialmente a 2.0. Los scripts con fixtures tienen evidencia en Linux, macOS y
Windows: **22/22 pruebas nativas por OS**, Python 3.10, en el
[run 37510771502](https://github.com/furthurr/ai-agents-kit/actions/runs/37510771502).
El runtime (descubrimiento 8/10, UI, referencias e `invoke_subagent`) sigue
**PENDIENTE** y el bridge `GEMINI.md` → `AGENTS.md` no está implementado.
No se infiere certificación completa de los seis hosts a partir de este pipeline.
