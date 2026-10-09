# Verificación — Compactación del contexto SDD

- **Modo SDD:** standard
- **Fase:** Verification
- **Estado:** verificación completada; iteración cerrada
- **Gate 1 de compactación:** aprobado
- **Gate 2 de compactación:** aprobado
- **Gate 3 de compactación:** aprobado
- **Reanudación:** autorizada por el usuario («procede»)
- **Gate 4 de compactación:** aprobado por el usuario («procede»)

## 1. Suite y evidencia final

| Comando | Resultado final | Exit |
|---|---|---|
| `python3 -B tools/test_sdd_contract.py` | **483/483** comprobaciones; anclas/rangos, ocho mutantes semánticos, presupuestos por fuente/escenario, doc opcional y paridad seis plataformas. | 0 |
| `python3 -B tools/test_model_recommendations.py` | **5/5** tests; exclusividad, gates y ausencia de referencias obligatorias al respaldo. | 0 |
| `python3 -B tools/validate.py` | Validación correcta: 10 skills, 6 agentes en 6 plataformas; generated reproducible. | 0 |
| `python3 -B tools/check_links.py` | Enlaces correctos; **67 archivos** revisados. | 0 |
| `python3 -B tools/test_integrity.py` | **415/415** checks; incluye validación negativa, enlaces, identidad MAS y contratos core. | 0 |
| `git diff --check` | Sin errores de whitespace en el diff versionado. | 0 |

Una ejecución inicial del check agregado de compatibilidad 10+ resultó en 482/483
por una expectativa textual que no coincidía con el texto semánticamente equivalente.
Se ajustó la aserción (sin cambiar rúbrica/producto) y se repitió SDD contract:
483/483. Este fallo de test se informa, no se oculta como fallo funcional.

No se afirma CI remota, instalación ni smoke en runtime de host. La repetición del
render no era necesaria durante Verification: `validate.py` renderizó en temporal
y comprobó reproducibilidad sin cambiar `generated/`.

## 2. Matriz R01–R28

Abreviaturas: **REF** = `canonical/skills/sdd-spec/references/feature-level.md`;
**SDD** = `tools/test_sdd_contract.py` (483/483); **ROLES** =
`tools/test_model_recommendations.py` (5/5); **VAL** = `tools/validate.py`.
La prueba textual valida el contrato publicado, no garantiza el razonamiento de un LLM.

| Req | Tareas | Check/revisión y evidencia | Estado |
|---|---|---|---|
| R01 | C2.2, C4.2, C5.1 | Alcance pedido vs proyecto completo; REF §Comparación y test de protocolos. | ✅ |
| R02 | C1.1, C2.2, C4.2 | Diez dimensiones explicitadas en REF; SDD inspecciona cada dimensión. | ✅ |
| R03 | C1.1, C2.2, C2.3 | F10 scaffold/sin scaffold y X13+ con soporte distinguido; negativo de reutilización. | ✅ |
| R04 | C1.1, C2.2 | Escala ordinal, sin fórmula/proxies de tamaño/riesgo; mutantes de tabla/rango. | ✅ |
| R05 | C1.1, C2.2, C2.3 | Alcance esencial antes de nota y supuestos; check de no provisional; smoke conserva bloqueo por evidencia ausente. | ✅ |
| R06 | C1.1, C2.2 | F01=1 en perfiles; mutante de referente rechazado. | ✅ |
| R07 | C1.1, C2.2 | X13=10; 10+ distingue superioridad, no cambia ancla X13. | ✅ |
| R08 | C1.1, C2.2 | Perfiles ordinales 1–10 en REF; el 9 se declara interpolación, no benchmark. | ✅ |
| R09 | C1.1, C2.2 | F10=8 con tres métodos y garantías scaffold; contraste sin scaffold. | ✅ |
| R10 | C1.1, C2.2, C2.3 | 10+ requiere saga/compensación/interacciones adicionales; mutante sin dimensiones rechazado. | ✅ |
| R11 | C1.1, C2.2 | REF prohíbe nota >10, suma o señal aislada; ejemplo explica diferencia tras reutilización. | ✅ |
| R12 | C1.1, C2.1–C2.2, C3.2 | Bloque de cuatro campos en REF, agente, skill y plantillas. | ✅ |
| R13 | C1.1, C2.2 | Rangos e iconos, `10+` literal y rechazo de mutantes `11`. | ✅ |
| R14 | C2.1, C2.2 | Solo agente SDD, tiempos por modo, no provisional/no repetir; ROLES. | ✅ |
| R15 | C1.1, C2.2 | REF: entero 1–10 e `exceeds_x13` separado; check semántico final. | ✅ |
| R16 | C1.1, C2.1–C2.2 | Tests de modos/gates/modelos/routing; score no cambia profundidad ni otras políticas. | ✅ |
| R17 | C1.1, C2.2 | Verde no habilita lite; mutante que lo cambia falla; F07 conserva su exclusión. | ✅ |
| R18 | C1.1, C2.2, C2.3 | X13: 10/11, C12 válido, fallo admin_create; no se presenta como superado. | ✅ |
| R19 | C3.2, C4.1–C4.2, C5.1 | Docs activas usan síntesis/enlace; VAL y SDD verifican 6 consumidores. | ✅ |
| R20 | C4.1, C4.3, C5.1 | Solo renderer alteró 24 generated SDD; `git status` preserva cambios preexistentes; adapters/manifest/CI/.gitignore sin diffs. | ✅ |
| R21 | C1.1, C2.2–C2.3 | Referencia contiene regla completa; ejemplo es opcional; tests no importan `.agent-lab`. | ✅ |
| R22 | C1.1–C1.2, C2.3, C4.2, C5.2 | Negativos/anclas/paridad y escenarios E01–E07 pendientes de host declarados. | ✅ |
| R23 | C1.2, C2.1–C2.2, C4.2, C5.1 | Cada uno de agente, skill y rúbrica disminuyó palabras y caracteres vs baseline. | ✅ |
| R24 | C2.1–C2.2, C4.2 | Delegación canónica única; tests confirman formato común, sin duplicar escala completa. | ✅ |
| R25 | C2.3, C3.2, C4.2 | 550 palabras de ejemplos/procedencia fuera del contexto obligatorio; agentes/skill/plantillas no lo refieren. | ✅ |
| R26 | C1.1, C3.1, C4.2, C5.1 | Anclas y contrastes mínimos permanecen en canonical; mutantes y fixture opcional también verificados. | ✅ |
| R27 | C1.2, C4.2, C5.1 | Mismo conteo whitespace/Unicode y tres escenarios; token/costo no afirmado. | ✅ |
| R28 | C4.1, C4.2, C5.1 | Pipeline render/validate correcto; seis plataformas y 24 outputs SDD. | ✅ |

## 3. Eficiencia medida

Comparación con baseline registrado en Requirements, usando palabras por `split()`
y caracteres Unicode. Sin tokenizer: estos no son tokens ni facturación.

| Fuente | Antes | Después | Reducción |
|---|---:|---:|---:|
| Agente SDD | 1.066 palabras / 7.580 caracteres | 975 / 6.957 | 91 / 623 |
| Skill SDD | 2.357 / 16.378 | 2.216 / 15.394 | 141 / 984 |
| Referencia de scoring | 1.774 / 12.303 | 662 / 4.610 | 1.112 / 7.693 |
| Plantillas | 863 / 5.722 | 863 / 5.722 | 0 / 0 |

| Escenario | Ahorro | Lectura |
|---|---:|---|
| Agente + skill | 232 palabras / 1.607 caracteres (**6,8 % / 6,7 %**) | Inicio |
| Agente + skill + referencia | 1.344 / 9.300 (**25,9 % / 25,6 %**) | Evaluación de esfuerzo |
| Anterior + plantillas | 1.344 / 9.300 (**22,2 % / 22,2 %**) | Planificación que consulta plantillas |

El respaldo opcional mide 550 palabras / 3.797 caracteres y no se suma a ningún
escenario obligatorio. El ahorro cuenta una reducción real de instrucciones, no
solo un traslado a una nueva lectura.

## 4. Invariantes, RNF y quality bar

| Invariante | Evidencia | Estado |
|---|---|---|
| F01=1, X13=10 y rangos históricos intactos | SDD anclas/negativos; no cambios a catálogo/veredictos | ✅ |
| Notas 1–10/10+, iconos y exceso explicado | REF y negativos; 483/483 | ✅ |
| Verde no habilita lite/gates | Caso F07 standard y tests de modos/gates | ✅ |
| Canonical define; generated reproduce | VAL, byte-parity y 6 plataformas | ✅ |
| Historia, cambios ajenos y globals preservados | diff/status de rutas pertinentes; sin instalación global | ✅ |

| RNF | Evidencia | Estado |
|---|---|---|
| RNF-1 autosuficiencia | Rúbrica operativa no depende de docs opcionales ni `.agent-lab` | ✅ |
| RNF-2 paridad | 483 SDD checks y validate en seis hosts | ✅ |
| RNF-3 políticas intactas | Suites de roles/modos/gates y diff acotado | ✅ |
| RNF-4 preservación | Estado local ajeno conservado; `.gitignore`/historias intactos | ✅ |
| RNF-5 Python stdlib / compatibilidad 3.10 | Sin deps nuevas; inspección de sintaxis; suites corrieron bajo Python 3.12.4, no bajo 3.10 | ✅ inspección; ejecución 3.10 no acreditada |
| RNF-6 reducción sin nueva lectura obligatoria | Budgets y auditoría de referencias más medición | ✅ |

Quality bar: solo prompts/docs/tests, sin lógica de negocio, I/O runtime,
persistencia, DI, singletons o nuevas dependencias. Helpers de pruebas pequeños;
sin catch vacío ni scorer. PBT correctamente omitido: la escala ordinal no posee
propiedad algebraica que lo justifique.

Auditoría de tasks: C1.1–C4.3 tienen artefactos y GREEN/render medidos en
`implementation-evidence.md`; C5.1 corresponde a los comandos de este documento;
C5.2 es esta matriz. No queda `[x]` huérfano.

## 5. Límites y Gate 4

- E01–E07 no se ejecutaron en hosts reales. No se afirma comportamiento de modelos.
- No se hizo CI remota, instalación global ni prueba runtime de las plataformas.
- Suite local: Python 3.12.4; no se afirma ejecución nativa Python 3.10.
- No se cambiaron configuraciones OpenCode cargadas ni se instaló generated.
- No hubo campañas/re-evaluaciones ReserveLab, Docker, llamadas de modelo, commit,
  push o release.
- El cambio de test R15 tras detectar el literal falseado quedó validado con
  483/483; no hubo corrección funcional adicional en Verification.

**Cierre:** aprobado por el usuario («procede»). Los límites y escenarios manuales
no ejecutados permanecen documentados; no bloquean el cierre acordado.
