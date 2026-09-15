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
- `@<agente>` indica que se dirige a un agente concreto, por ejemplo `@security`
  o `@sdd`.
- `MAS + @<agente>` indica una instrucción del sistema que debe ejecutar un agente
  concreto dentro de su alcance.

Ejemplos:

```text
MAS: conserva la trazabilidad entre agentes y no repitas un gate confirmado.
@security: revisa únicamente secretos y configuración de red.
MAS + @sdd: convierte este cambio en una spec con trazabilidad completa.
```

## Desambiguación

`MAS` usado solo siempre se refiere al sistema multiagente de este kit. No debe
confundirse con `MASVS`, `MASWE` o `MASTG`, que son nombres propios de estándares y
guías de OWASP Mobile Application Security. Esos identificadores se mantienen
completos y no se abrevian como `MAS`.

## Fuente de verdad

La identidad se documenta aquí y se replica de forma compacta en los agentes y
skills canónicos. `tools/render.py` la propaga a Copilot, OpenCode, Kiro y Claude
Code; los artefactos de `generated/` no se editan a mano.
