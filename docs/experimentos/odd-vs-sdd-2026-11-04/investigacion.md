# Investigación de fuentes — ODD y SDD

Fecha: 2026-11-04. [Protocolo](protocolo.md).

## Fuentes fijadas

Gentle AI: commit `3ea08cdfbdce671053c82377a4365915799abe57`, fechado
2026-11-03T20:08:58Z, resuelto mediante API GitHub antes de diseñar el tratamiento.
Se estudia ese commit de main, no se atribuye todo su contenido a una release.

- [Protocolo ejecutable y Task Size](https://github.com/Gentleman-Programming/gentle-ai/blob/3ea08cdfbdce671053c82377a4365915799abe57/internal/components/agentguidance/routing.go).
- [Secciones compartidas](https://github.com/Gentleman-Programming/gentle-ai/blob/3ea08cdfbdce671053c82377a4365915799abe57/internal/assets/skills/_shared/odd-orchestrator-sections.md).
- [Orquestador OpenCode](https://github.com/Gentleman-Programming/gentle-ai/blob/3ea08cdfbdce671053c82377a4365915799abe57/internal/assets/opencode/orchestrator.md).
- [Guía de disparadores](https://github.com/Gentleman-Programming/gentle-ai/blob/3ea08cdfbdce671053c82377a4365915799abe57/docs/trigger-rules.md).
- [README y benchmarks publicados](https://github.com/Gentleman-Programming/gentle-ai/blob/3ea08cdfbdce671053c82377a4365915799abe57/README.md).

MAS: baseline `f3b58d58e0fd690d31c99131bbe5c85bc8ea2fcd`. Fuentes locales:
[agente SDD](../../../canonical/agents/sdd.md),
[skill SDD](../../../canonical/skills/sdd-spec/SKILL.md),
[profundidad](../../../canonical/skills/sdd-spec/references/scope-depth.md),
[testing](../../../canonical/skills/sdd-spec/references/testing.md) y
[Tiny](../../../canonical/skills/sdd-spec/references/tiny.md).
La ejecución carga los derivados OpenCode reproducibles de estas fuentes.

## Hallazgos contrastados

| Eje | MAS SDD | Gentle AI ODD |
|---|---|---|
| Entrada | Selección explícita de SDD | Flujo por defecto de cada petición |
| Cambio pequeño | Direct sin spec, con guardas de riesgo | Small sin documento, por comprensión, riesgo y reanudabilidad |
| Documento breve | Tiny: spec vivo y Gates 3/4 | Documento solo si falla reanudación desde petición + diff |
| Trabajo más amplio | Lite: Quick Plan y verificación, sin Gates 1–4 | Registro Specs/Tasks/Log, espejo Engram y commits por unidades |
| Pruebas | Adaptativas; regresión en bugs, focalizadas en features | Test-first aplicable por defecto y diferencial de comandos compartidos |
| Requisitos | Comportamientos verificables; EARS donde exige el modo | Requisitos y ejemplos literales, handoff por referencia |
| Delegación | SDD conserva ejecución, skills de dominio bajo demanda | Explorer por presupuesto, writer por motivo, verificador por riesgo nombrado |
| Memoria | Artefactos y estado/gates locales | Documento local y espejo Engram, reconciliación al reanudar |
| Revisión nativa | Controles MAS, sin recibos de Gentle AI | RDD separado del flujo, on por defecto y opt-out |
| Correcciones | Evidencia e integridad antes de cerrar | Correcciones acotadas; prueba agotada requiere decisión |

El README externo aporta benchmarks de Gentle Shell, algunos n=1 y con modelos,
fixtures y harness distintos. Son antecedentes del autor, no resultados contra
nuestro MAS. La retirada del SDD de Gentle AI desde v4.0.0 tampoco prueba que
nuestro SDD actual sea peor: este ya incluye Direct, Tiny y Lite.

## Hipótesis y alcance aprobado

El usuario eligió **ODD adaptado dentro del mismo MAS**, frente a comparar los
ecosistemas completos. Hipótesis: menor ceremonia y lectura pueden ahorrar
recursos; requisitos literales y test-first podrían evitar omisiones/regresiones.
Contrahipótesis: el SDD proporcional ya cubre esos problemas; menos documentos o
turnos podrían reducir recuperación o evidencia sin aportar calidad.

La adaptación elimina espejo Engram, RDD, commits implícitos y topología nativa;
por ello sus resultados solo se pueden atribuir al paquete de instrucciones
adaptado. No separan el efecto de cada regla ni permiten recomendar Gentle AI
completo. La igualdad de permisos tampoco garantiza igualdad de conducta:
se comprueban cargas, secuencias y artefactos reales.

Como en [Ponytail](../ponytail-2026-11-04/README.md), no se incorpora una regla
activa al MAS antes de observar evidencia. Esta vez se conservan también las
entradas reproducibles del experimento, no solo una síntesis de agregados.
