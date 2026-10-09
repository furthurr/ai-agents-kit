# Requisitos — Presentación y validación del alcance completo

Modo SDD: standard
Fase: Requirements
Estado: aprobado
Gate 1: aprobado por el usuario («procede»)
Intención: implementación tras aprobar los gates correspondientes

## Objetivo y relación con acuerdos existentes

Permitir al usuario verificar que SDD entendió íntegramente el alcance funcional
antes de producir artefactos o implementar, sin recortar información a un resumen.

Amplía `sdd/alcance-calificacion-y-seleccion`: su Req 1.3 evita preguntas repetidas
cuando la petición ya es clara; la propuesta conserva esa protección, pero añade
validación explícita del alcance completo si aún no existe para esa versión.
Elegir profundidad por sí solo no valida el contenido del alcance.

Sustituye la regla de resumen de 1–3 frases implementada después del commit
`14ce018`, todavía sin commit, por presentación completa y aprobación previa.
Conserva el resto de cambios locales. No reescribe evidencias anteriores ni cierra
el Gate 4 pendiente de la spec de alcance; tampoco reabre la spec de continuidad
cerrada, cuyas protecciones siguen vigentes.

## Calificación de este cambio

- Esfuerzo previsto del LLM: 4 🟢
- Referente del laboratorio: F04, comparación ordinal de conflictos y normalización.
- Justificación: coordina validación de alcance con selección y gates; elimina
  contradicciones de presentación; reutiliza referencias y renderer; requiere
  regresiones de aprobación, cambios y reanudación sin aumentar ceremonia por fase.
- Supuestos relevantes: contrato textual sin motor runtime; pruebas estáticas no
  certifican comprensión funcional del agente en un host real.

## Historia 1 — Alcance completo visible

- Req 1.1: CUANDO quede definido el alcance de una solicitud nueva, EL SISTEMA
  DEBERÁ presentar al usuario el alcance funcional completo antes de generar
  artefactos de esa solicitud o implementar.
- Req 1.2: CUANDO presente el alcance, EL SISTEMA DEBERÁ incluir objetivo, resultado
  esperado y todos los comportamientos acordados con sus reglas y condiciones.
- Req 1.3: CUANDO presente comportamientos incluidos, EL SISTEMA DEBERÁ acompañarlos
  de criterios de aceptación verificables y cubrir errores, casos límite y estados
  relevantes identificados durante la definición.
- Req 1.4: CUANDO presente el alcance, EL SISTEMA DEBERÁ mostrar exclusiones,
  restricciones y supuestos relevantes, distinguiendo lo confirmado de lo supuesto.
- Req 1.5: CUANDO organice la presentación, EL SISTEMA DEBERÁ evitar omitir detalles
  funcionales para cumplir límites de frases, palabras o longitud de respuesta.
- Req 1.6: CUANDO presente el alcance, EL SISTEMA DEBERÁ conservar la separación
  del qué/porqué frente al cómo, sin inventar requisitos o decisiones de implementación.
- Req 1.7: SI falta una decisión esencial, ENTONCES EL SISTEMA DEBERÁ aclararla
  antes de presentar el alcance como listo para validación o calificar una feature.

## Historia 2 — Validación y elección

- Req 2.1: CUANDO presente un alcance aún no validado, EL SISTEMA DEBERÁ esperar
  aprobación explícita o ajustes antes de continuar con artefactos o implementación.
- Req 2.2: CUANDO la selección de profundidad también esté pendiente, EL SISTEMA
  DEBERÁ combinar validación del alcance y elección de modo en una sola interacción,
  sin tratar la nota como otra aprobación.
- Req 2.3: SI el usuario elige únicamente profundidad o ejecutor, ENTONCES EL
  SISTEMA DEBERÁ resolver la validación del alcance pendiente sin inferir aprobación.
- Req 2.4: CUANDO exista validación explícita previa del mismo alcance completo y
  siga vigente, EL SISTEMA DEBERÁ reutilizarla sin repetir presentación ni pregunta.
- Req 2.5: CUANDO publique una calificación de feature, EL SISTEMA DEBERÁ hacerlo
  después de mostrar su alcance completo vigente, incluidas notas 10 y 10+.
- Req 2.6: CUANDO el trabajo sea bugfix o consulta sin nota de feature, EL SISTEMA
  DEBERÁ mantener el tratamiento propio sin inventar una calificación.

## Historia 3 — Ajustes y versiones de alcance

- Req 3.1: CUANDO el usuario agregue, elimine o corrija parte del alcance, EL SISTEMA
  DEBERÁ incorporar el cambio y presentar el alcance completo actualizado antes
  de solicitar validación, no solamente el fragmento modificado.
- Req 3.2: CUANDO cambie el alcance pendiente, EL SISTEMA DEBERÁ impedir que la
  aprobación de una versión anterior se utilice como aprobación del nuevo contenido.
- Req 3.3: CUANDO cambie materialmente el alcance, EL SISTEMA DEBERÁ reevaluar
  esfuerzo, elegibilidad, autorización y ejecutor pertinentes sin repetir notas por fase.
- Req 3.4: CUANDO se evalúe una entrega incremental diferente, EL SISTEMA DEBERÁ
  presentar su alcance completo y dependencias relevantes y resolver su validación.

## Historia 4 — Integración con modos y specs existentes

- Req 4.1: CUANDO el alcance validado sea direct y exista autorización para
  implementar, EL SISTEMA DEBERÁ continuar sin spec formal ni Quick Plan, con pruebas
  proporcionales y evidencia breve.
- Req 4.2: CUANDO el alcance validado sea lite, EL SISTEMA DEBERÁ producir Quick Plan
  en una pasada sin otra aprobación rutinaria de requirements, design o tasks.
- Req 4.3: CUANDO el alcance validado sea standard, EL SISTEMA DEBERÁ formalizar los
  requisitos y conservar Gate 1; validar alcance no aprueba los requisitos formales.
- Req 4.4: CUANDO la formalización introduzca diferencias funcionales respecto al
  alcance validado, EL SISTEMA DEBERÁ exponerlas sin implementarlas silenciosamente.
- Req 4.5: CUANDO continúe una spec existente, EL SISTEMA DEBERÁ conservar decisiones
  vigentes y gates; no reiniciar validación sin cambio ni utilizar direct para evadirlos.
- Req 4.6: CUANDO se trate de una enmienda, EL SISTEMA DEBERÁ aplicar continuidad,
  preservar historia y revisar aprobaciones afectadas sin sobrescribir evidencia anterior.
- Req 4.7: CUANDO el usuario elija un especialista, EL SISTEMA DEBERÁ conservar el
  contexto y decisiones al transferir manualmente, sin ejecutar automáticamente la actividad.
- Req 4.8: CUANDO la intención sea solo planificación, EL SISTEMA DEBERÁ abstenerse
  de implementar aunque alcance y profundidad estén aceptados.

## Contexto, documentación y límites

- Mantener exactamente tres profundidades. Validar alcance es una decisión común
  pendiente, no un cuarto modo ni Gates 1–4 adicionales de lite.
- Alcance completo significa todos los comportamientos definidos, no documentación
  exhaustiva del proyecto ni inventario de casos hipotéticos ajenos a la petición.
- No crear un archivo obligatorio para la etapa común ni cargar specs completas
  sin relación relevante. Mantener lectura selectiva y presupuestos del prompt.
- La respuesta al usuario puede ser más extensa que 1–3 frases: no prometer igual
  consumo de tokens ni reducir completitud para cumplir cuotas de contexto.
- Actualizar referencias, documentación, pruebas y seis distribuciones; retirar
  instrucciones operativas contradictorias de resumen breve sin alterar historia.
- No instalar globalmente ni hacer commit, push, bump, tag o release en este alcance.

## Verificación prevista

Regresiones de alcance completo, confirmación combinada, selección sin validación,
ajustes que requieren presentación completa nueva, validación vigente reutilizable,
direct sin spec, Quick Plan después de validación, Gate 1 standard conservado,
entregas 10/10+ y continuidad sin invalidar evidencia histórica. Smoke runtime
se documenta como pendiente si no se ejecuta; checks textuales no prueban comprensión LLM.
