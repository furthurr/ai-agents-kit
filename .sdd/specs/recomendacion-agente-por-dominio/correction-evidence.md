# Corrección R01 — Evidencia y límites

Modo SDD: standard
Fase: Implementación correctiva
Estado: corrección implementada — pendiente de nueva Verification
Gate: Gates 1–3 aprobados; Gate 4 pendiente
Autorización: «procede» a diagnóstico/corrección, seguido de reanudación del preflight.

## Diagnóstico y decisión acotada

La traza inicial demuestra un intento de edición sin carga de `sdd-spec` ni lectura
de la política. La definición del agente remitía al detalle «para recomendar»,
pero carecía de una condición explícita de no escritura mientras faltara elección.
Además, seleccionar SDD podía confundirse con preferencia de continuar aquí.
Esto sustenta reforzar la precedencia, no confirma una causa raíz única del LLM.

Prueba de control: agente temporal `routing-probe` solicitaba responder una cadena
sin herramientas en el fixture anterior. `opencode run --agent routing-probe --pure
--format json ...` terminó con exit 1 y HTTP 403, sin texto ni herramientas. No
permitió comprobar la entrega efectiva del prompt por esa vía; no se infiere un
fallo del renderer ni se elude la restricción. La repetición normal con el agente
SDD corregido sí respondió, por lo que tampoco se afirma que todo el host esté bloqueado.

Decisión: condición visible al comienzo del agente, carga de skill/referencia antes
de escribir y aclaración de selección activa versus preferencia explícita. No se
añade hook, agente, permiso nuevo ni clasificador runtime. La barrera sigue siendo
una instrucción: no es un aislamiento técnico impuesto por el kit.

## Artefactos y RED/GREEN

- `canonical/agents/sdd.md`: `Control previo a cualquier escritura` antes de las
  reglas generales; no usar edit/write/apply_patch/comandos de escritura mientras
  falte elección esencial. Contenido core ajeno preservado.
- `canonical/skills/sdd-spec/SKILL.md`: condición antes de la primera modificación,
  sin confundir descubrimiento con carga de skill.
- `canonical/skills/sdd-spec/references/agent-routing.md`: elegir el agente SDD no
  rechaza automáticamente al especialista; decisión precede al intento de edición.
- `tools/test_sdd_contract.py`: `test_agent_routing_write_barrier` y seis checks
  adicionales de propagación de la condición.

Regresión contractual:

```sh
python3 -B -c 'import tools.test_sdd_contract as t; t.test_agent_routing_write_barrier(); print(f"{t.PASSED}/{t.PASSED + t.FAILED} comprobaciones correctas"); raise SystemExit(bool(t.FAILED))'
```

RED: exit 1, **0/15**, por ausencia de condición y precedencia explícitas.
GREEN con política/integración: exit 0, **66/66** (51 previos + 15 nuevos).
Propagación antes de render: exit 1, **30/42**, faltan las seis condiciones y las
seis referencias actualizadas. GREEN acumulado tras publicar: exit 0, **108/108**.

## Render selectivo por cambios concurrentes

Otra tarea modificó fuentes core y Navigator durante esta sesión. No se regeneró
todo `generated/` sobre esos cambios ajenos. Se usó `tools/render.py --output`
en staging temporal y se publicaron solo 18 assets: agente SDD, su SKILL.md y
agent-routing.md en seis plataformas. Script temporal `routing-render-selected.py`;
staging `routing-render-d6sgdceh`. Comprobó que los tres archivos fuente y los targets
no cambiaran durante el render antes de copiar. No alteró renderer ni adaptadores.

## Repetición real R01 — PASS

Fixture nuevo: `routing-smoke-0tnpexyv`, HOME/XDG aislados, OpenCode 1.18.34,
sin credenciales copiadas, sin cambio de modelo ni perfil global. Fuente: working
tree actualizado, que también conserva contexto core concurrente. No se atribuye
el cambio de comportamiento exclusivamente a una frase ni se certifica determinismo.

Mismo prompt y comando del R01 original, sin revelar el resultado esperado.
Exit 0, sin timeout ni stderr. Secuencia observable:

1. Localiza contexto/archivo y **carga skill `sdd-spec`**.
2. Lee `button.css` y **agent-routing.md** del fixture.
3. Emite texto con `ID recomendado: ui-design`, justificación de dominio y límites.
4. Pregunta: «¿Quieres seleccionar manualmente ui-design o continuar con SDD
   (modo direct) y hacerlo aquí?».
5. No hay llamada edit/write, comando de escritura ni subagente; CSS conserva
   `.button { color: #333333; }`.

Extractos relevantes de la respuesta:

> Decisión de ejecutor pendiente (requisito previo a escribir)
>
> El cambio afecta solo a apariencia [...] conserva eventos y datos, no toca lógica,
> APIs ni persistencia — dentro de los límites de ui-design.
>
> Según la política de enrutado, no debo editar hasta que elijas el ejecutor.

SHA-256 de referencia copiada:
`e7a067bc880e266e0756d85474fcebe0059e080436f8f4fecfbbd95744c28a3d`, idéntica
al generado. Debug confirmó diez skills del kit más la skill incorporada del host.
Logs del fixture: artifacts/R01.stdout, R01.stderr, agent.stdout, skills.stdout,
summary.json. Esta nota conserva resultado y secuencia sin depender solo del temporal.

PASS se limita a routing de R01. El preflight se emitió después de lecturas en esa
respuesta; no se certifica cumplimiento del resto del flujo SDD ni se corrige esa
política ajena dentro de este incremento. R02–R11 siguen sin ejecutar; R12 parcial.

## Checks actuales y brechas

- Contratos específicos de routing, incluida corrección: **108/108**, exit 0.
- Contrato SDD completo: **459/465**, exit 1. Los seis fallos observados son paridad
  de navigator-context.md entre canonical y generated, por cambios concurrentes
  ajenos a routing. No se restauraron ni regeneraron esas fuentes por cuenta propia.
- `tools/validate.py`: exit 1 por falta de paridad global de canonical/generated.
  No se anuncia validación global verde con esas modificaciones en curso.
- `tools/check_links.py`: exit 0, **73 archivos**; `git diff --check`: exit 0.
- measure_context: agentes **4,389**, skills **18,478**, referencias **15,366** palabras.
  Estos totales incluyen cambios core de otra tarea; no se atribuye todo el delta
  a la corrección de routing.

Pendiente: nueva Verification después de la reanudación, coordinar paridad global
con la tarea core y completar smoke. No cerrar Gate 4 ni marcar 4.2 completa por
haber obtenido un PASS de R01. Nivel recomendado para Verification: MEDIO.

## Refuerzo autorizado tras R04/R10

El usuario autorizó «procede con eso» para corregir la lista de candidatos y la
continuidad al elegir especialista, y para repetir escenarios bloqueados.

- `agent-routing.md` declara lista cerrada `ui-design`/`data-api`; al aclarar no
  enumera otros agentes. Dominios externos/mixtos permanecen en SDD.
- Elegir explícitamente al especialista produce el contexto manual y detiene SDD
  para esa actividad, aunque la solicitud original pidiera implementar. Solo una
  nueva elección explícita de SDD autoriza reanudar la misma implementación.
- `sdd.md` y `sdd-spec/SKILL.md` incorporan las mismas condiciones; test contractual
  cubre whitelist, parada y propagación.
- RED/GREEN focal: **91/91** tras render selectivo. Las suites actuales: SDD **505/505**,
  handoff **34/34**, recomendaciones de modelo **437/437**, links **4/4**, checker
  **71 archivos**, validator **10 skills/6 agentes/6 plataformas**, diff check verde.
- `measure_context.py`: agentes **3,793**, skills **18,533**, referencias **15,507**
  palabras; los cambios concurrentes del core impiden atribuir todo el delta a routing.
- Render mediante `tools/render.py --output` en staging, publicación selectiva de
  18 assets SDD en seis plataformas. Staging: `routing-render-lyf8_82p`; no se tocaron
  otros destinos generados ni adaptadores.

Los intentos runtime posteriores, con shell deshabilitado para evitar bloqueos de
permiso, recibieron HTTP 403 `FreeTierError` del proveedor antes de respuesta
(`routing-final-ary6ox3t`). No se cambió proveedor/modelo, no se copiaron credenciales
y no se eludió el rechazo. R04/R10 y los retries de R06/R07/R11 quedan bloqueados
tras la corrección: evidencia contractual verde, pero **sin PASS conversacional nuevo**.
Gate 4 permanece pendiente.
