# Diseño — Presentación y validación del alcance completo

Modo SDD: standard
Fase: Design
Estado: aprobado
Gate 2: aprobado por el usuario («procede»)

## Contexto y alcance

Cambio del contrato textual SDD, sin motor runtime ni cuarto modo. Sustituye la
regla local de 1–3 frases y conserva anclas, atención, elegibilidad, routing y gates.
No altera evidencia histórica ni cierra la spec de alcance anterior. La spec de
continuidad cerrada mantiene sus garantías, aplicadas a esta ampliación.

## Responsabilidades

- `canonical/skills/sdd-spec/references/scope-depth.md`: autoridad de contenido
  completo y validación común; incorporar procedimiento compacto sin duplicar rúbrica.
- `references/feature-level.md`: formato de alcance completo seguido de nota,
  atención y recomendación; reemplazar reglas de resumen/deduplicación insuficiente.
- `canonical/agents/sdd.md` y `SKILL.md`: entradas breves de validación de alcance
  antes de modos; compactar texto existente para mantener presupuestos principales.
- `references/spec-continuity.md`: ampliar continuidad cuando cambia alcance,
  conservando versiones, autorización y aprobaciones afectadas, sin reinicio automático.
- `references/integrity-gate.md`: comprobar validación vigente antes de ejecutar
  y correspondencia alcance/requisitos/evidencia antes de cierre.
- Revisar plantillas solo si hay contradicción; no añadir documento obligatorio común.
- `docs/agentes/sdd.md`, `docs/sdd-effort-examples.md`, `docs/sdd-smoke.md` y uso:
  sustituir ejemplos de resumen por presentación completa y decisiones explícitas.
- `tools/test_sdd_contract.py`: sustituir checks del resumen por checks de completitud,
  aprobación, ajustes y continuidad. Conservar negativos/gates/routing/presupuestos.
- `generated/`: regenerar seis plataformas sin edición manual ni adaptadores nuevos.

## Flujo y decisiones

1. Preflight, contexto selectivo y preguntas esenciales, sin prefacio ceremonial.
2. Identificar relación con specs y aclarar dudas esenciales; reutilizar información.
3. Presentar alcance completo con campos pertinentes, sin límite de frases.
4. Para features, publicar nota y atención del alcance mostrado y recomendar modo.
   Bugfix/consulta mantienen su tratamiento, sin nota inventada.
5. Preguntar conjuntamente validación del alcance y elección de modo si faltan ambas.
6. Interpretar respuesta: continuar solo si las decisiones esenciales requeridas
   están resueltas; conservar límites de autorización e intención.
7. Generar artefactos/implementar según modo. Informar diferencias respecto al
   alcance validado antes de ejecutar contenido funcional nuevo.

Consultas informativas sin artefactos ni implementación no adquieren una aprobación
ceremonial. La decisión común aplica al alcance del trabajo que se va a producir.
Elegir especialista sigue siendo decisión independiente: paquete manual y parada,
no ejecución automática ni sustitución de los gates del receptor.

## Contenido completo, no documentación exhaustiva

La presentación denominada `Alcance definido` incluye objetivo/resultado y todos
los comportamientos acordados con reglas/condiciones, criterios verificables,
errores/estados/casos límite identificados, exclusiones, restricciones y supuestos.
Distinguir confirmado de supuesto; usar EARS o formulación igualmente verificable.
Si un campo no aplica, indicarlo cuando evite ambigüedad, sin inventar contenido.

No reducirlo a decisiones principales ni poner un límite de palabras/frases que
omita información. No exponer algoritmos, archivos a editar, arquitectura o pruebas
de implementación como requisitos funcionales. Completo se refiere a lo definido,
no a todos los casos hipotéticos del proyecto. Incertidumbres esenciales se aclaran.

## Respuestas y vigencia

| Respuesta/contexto | Decisión |
|---|---|
| «Sí, ese es el alcance; continúa con lite» | Validación y elección explícitas, continuar si está autorizado. |
| «Usa lite», sin validación previa | Solo modo elegido; aclarar aceptación del alcance pendiente. |
| «El alcance es correcto», modo pendiente | Conservar validación y resolver solo elección. |
| «Agrega X» / «quita Y» / corrección | Incorporar ajuste, presentar alcance completo actualizado y volver a validar. |
| Validación previa explícita del mismo alcance completo | Reutilizar sin repetición si fuentes/alcance siguen vigentes. |
| Solo hubo resumen breve | No acredita presentación ni validación completas. |
| Nueva entrega o alcance modificado | Validar la versión/entrega nueva; no heredar aprobación incompatible. |
| Reanudación sin cambio con gates aprobados | Conservar decisiones, sin reiniciar aprobación común por rutina. |

No inferir aprobación por archivos o nombre de modo. Una respuesta breve «procede»
puede resolver una pregunta inequívoca que pide ambas decisiones; si el contexto
no distingue aprobación o selección, aclarar únicamente lo pendiente.
No repetir nota por cambios no materiales; reevaluarla si cambia impacto relevante.
Tras ajustes se presenta el conjunto completo, no solo el delta; historia puede
registrar delta para trazabilidad sin usarlo como sustituto de validación visible.

## Integración por profundidad

- Direct: tras validación/selección e implementación autorizada, cambio y pruebas
  proporcionales; sin archivos formales de spec ni Quick Plan.
- Lite: tras esas decisiones, Quick Plan en una pasada, sin pausa rutinaria de
  requisitos/diseño/tareas ni Gates 1–4. Cierre con verificación compacta real.
- Standard: requisitos formalizados conservan Gate 1, después Gates 2–4. Validar
  alcance no aprueba el documento ni los gates pendientes. Señalar precisiones
  funcionales nuevas; no introducirlas como si estuvieran acordadas.
- Specs existentes: aplicar continuidad y revisar solo decisiones afectadas. No
  forzar direct por nota baja ni desmarcar indiscriminadamente tareas/evidencias.

La validación común es una decisión esencial previa, no un gate numerado nuevo.
Planificación aceptada no autoriza código; elegir modo/ejecutor no amplía permisos.

## Pruebas y errores

TDD focalizado: tests nuevos deben fallar por ausencia de contenido/aprobación
obligatorios; implementar contrato mínimo y observar GREEN. Cambiar aserciones
retiradas (1–3 frases) sin perder cobertura de posición de nota o no repetición.
Cubrir campos completos, espera previa, respuesta solo modo, validación vigente,
ajustes con conjunto completo, 10/10+, nueva entrega, direct/lite/standard y continuidad.
Negativos: recortar a resumen, omitir validación, validar por selección, presentar
solo delta o tratar alcance común como Gate 1 aprobado.
No simular comprensión LLM mediante reglas deterministas; checks son del contrato.

Ejecutar render, suite SDD, modelo/handoff, validate, enlaces y diff --check. Mantener
escenarios runtime pendientes si no se ejecutan; añadirlos al smoke como expectativas.
Errores/ambigüedades no permiten ejecutar contenido pendiente. Contexto desfasado se
revalida selectivamente. Sin dependencias de testing nuevas ni PBT ceremonial.

## Contexto y RNF

Mantener presupuestos anteriores de agente/skill/plantillas y límites de referencias;
compactar duplicaciones, no omitir información funcional para cumplirlos. Medidas
estáticas no incluyen tamaño variable del alcance mostrado ni tokens reales.
Salida completa puede crecer: no prometer igual consumo ni porcentajes de ahorro.
Sin índices/caché persistentes, nueva carpeta de dominio o instalación global.

- RNF-1: contenido completo y validación vigentes antes del trabajo autorizado.
- RNF-2: presupuestos existentes del prompt/referencias respetados, sin cuotas de salida.
- RNF-3: coherencia y render reproducible en seis distribuciones.
- RNF-4: autorización, intención, elección y gates siguen siendo distinguibles.
- RNF-5: reglas activas de resumen de 1–3 frases retiradas; evidencias históricas conservadas.

Barra de calidad: política separada de renderer/adaptadores, sin infraestructura ni
abstracciones nuevas. DI, UI y persistencia de negocio no aplican. Evidencia honesta,
errores explícitos y pruebas acotadas al contrato; no declarar comprensión runtime.
