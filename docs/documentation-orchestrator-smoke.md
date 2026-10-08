# Smoke test de Documentation Orchestrator

Validación manual mínima del agente y la skill en cualquiera de las plataformas
soportadas. Ejecuta las pruebas en un repositorio desechable o con cambios bajo
control; algunos escenarios escriben documentación tras varios gates.

## Precondiciones

1. Ejecuta `python3 tools/render.py` y `python3 tools/validate.py` en este kit.
2. Instala o copia los artefactos generados de la plataforma de prueba.
3. Reinicia la herramienta para cargar agente y skill.
4. Selecciona `documentation-orchestrator`.

## 1. Preflight informativo en status

Prompt:

```text
Comprueba si la documentación está actualizada.
```

Esperado:

- Detecta `status` y comienza con un preflight superficial.
- No recomienda nivel, modelo ni proveedor LLM.
- Completa la inspección e informe en el mismo turno.
- No escribe archivos.

Debe completar el inventario sin escribir ni exigir `continúa con el actual`.

## 2. Bootstrap core

Prompt:

```text
Inicializa la documentación core del proyecto.
```

Esperado:

- Selecciona únicamente `.navigator/` y `.architecture/`.
- No recomienda nivel, modelo ni proveedor LLM.
- Presenta el plan global y espera su aprobación de escritura.
- Conserva los gates de Project Navigator y Architecture.
- Ejecuta ambas skills separadas localmente, sin handoff a agentes retirados.
- No crea `.data/`, `.design/`, `.quality/` ni `.security/`.

## 3. Sync existing con Quality

Prepara un repo que tenga `.navigator/`, `.architecture/` y `.quality/`, pero no
`.data/` ni `.design/`. Prompt:

```text
Actualiza las carpetas documentales que ya tenemos.
```

Esperado:

- Detecta `sync-existing`.
- Selecciona solo las tres carpetas existentes.
- Recomienda las ausentes aplicables sin crearlas.
- Reutiliza el plan autorizado para registrar findings de calidad verificados,
  sin pedir otro filtro de severidad; no remedia código ni agrega seguridad ausente.
- Actualiza Navigator al final si corresponde.

## 4. Alias y cambio de alcance

Prompt:

```text
Ejecuta sync-check.
```

Esperado: interpreta `status`, no `release-check`, no recomienda modelos y completa
la inspección e informe.

En la siguiente petición, cambia el alcance:

```text
Mejor actualiza solo arquitectura y seguridad.
```

Esperado: recalcula como `sync-domain`, no recomienda modelos y presenta el plan.
Espera la aprobación de escritura o una decisión real pendiente; una autorización
anterior no cubre una ampliación.

## 5. Release check

Prompt:

```text
Comprueba si el proyecto está listo para una release.
```

Esperado:

- Selecciona `release-check` sin recomendar nivel o modelo LLM.
- En el mismo turno lee documentación y findings existentes y entrega el informe.
- No reescanea código, no genera changelog, no versiona y no crea tags.
- Devuelve `APTO`, `APTO CON ADVERTENCIAS` o `NO APTO` con evidencia.
- Un finding `Crítica` de Security o `Blocker` de Quality produce `NO APTO`.
- Cualquier core distinto de `Vigente` o cambio local relevante produce `NO APTO`.
- Un Navigator legado sin `source_commit` queda `No verificable` hasta ejecutar
  un update que establezca un baseline Git limpio.

## 6. Límites

Solicita una feature, un bugfix, una release y Graphify. El agente debe redirigir
respectivamente a SDD, Git & Release Manager o Graphify sin modificar `.sdd/`,
`.release/`, `graphify-out/` ni código de producto.

## 7. Handoff productor–receptor

Después del análisis inicial y del plan, solicita explícitamente continuar
con el agente Code Review real para una inspección documental de solo seguridad.

Esperado en el orquestador:

- Emite `## Handoff` con `target: code-review`, `scope: [.security/]`, `action: inspect`,
  `write_scope: none`, `requires_confirmation: false` y `status: pending`.
- Incluye `handoff_id`, `project_root` y referencias existentes relativas.
- No ejecuta la inspección localmente y marca el dominio pendiente.

Copia el bloque a Code Review. Esperado en el receptor:

- Rechaza un bloque con target distinto, ruta absoluta/`..`, acción desconocida o
  escritura incoherente.
- No interpreta `gate_state` como aprobación de sus gates.
- Para un bloque válido, ejecuta solo su alcance y devuelve `## Handoff Result`
  con el mismo `handoff_id`, `status`, `evidence` y `result_summary`.
- No comunica recomendaciones de modelo. Conserva decisiones y gates reales.

Devuelve el resultado al orquestador. Esperado: verifica la evidencia antes de
marcar el dominio completado. Repite al menos una vez con `action: sync` y
confirma que pide aprobación de escritura y no duplica la acción.
Si la misma escritura ya está autorizada en esa sesión, no vuelve a preguntar;
`gate_state` copiado por sí solo no acredita autorización. Para ambos dominios,
usa `scope: [.quality/, .security/]` y exige evidencia de cada dominio al sincronizar.

## 8. Inspect core y selección bajo demanda

En un fixture solicita por separado:

```text
@documentation-orchestrator inspect: explica las capas y localiza un ADR. Solo lectura.
@documentation-orchestrator inspect: localiza el entrypoint y sus dependencias. Solo lectura.
```

Esperado: elige `architecture` o `project-navigator` según la pregunta; si necesita
ambas, las usa secuencialmente. No carga todas las skills, no genera handoff core
ni estado `delivered`, no crea/actualiza índices, documentos ni instrucciones del
proyecto. Cita fuentes, confianza y límites; responder no acredita sincronización.
`status` conserva inventario/frescura y no se confunde con investigación `inspect`.

## 9. Consumo directo y degradación

Repite consultas core desde documentación y desde otro agente vigente (por
ejemplo SDD), con fixtures de contexto **vigente, ausente, desfasado, ambiguo,
ilegible y sin baseline verificable**. Arquitectura entra por README/Contexto
para IA; Navigator resuelve config/instancia y empieza por capas mínimas.
Esperado: consumo directo selectivo, sin handoff obligatorio para leer; código,
steering y contratos confirman decisiones. Índices viejos solo orientan; ante
fallos se usan fuentes directas y se comunica el límite. No hay bootstrap/sync
automático ni escrituras del consumidor.

## 10. Petición mixta y exportación

```text
Explica las capas ahora y actualiza después los índices; no he aprobado escrituras.
```

Esperado: atiende lectura separable, propone mantenimiento y espera aprobación
aplicable antes de escribir. Solicitar exportación de Navigator a `AGENTS.md`
conserva confirmación específica; una consulta, handoff antiguo o `gate_state` no
autoriza exportar ni sobrescribir.

## 11. IDs retirados y conservación

Presenta una solicitud o handoff cuyo target sea `architecture` o
`project-navigator` a un agente vigente. Esperado: diagnóstico de receptor
retirado y orientación a `documentation-orchestrator`; no reescribe/ejecuta el
handoff ni transfiere autorización. Un host que no resuelva la mención antigua
requiere selección manual, sin prometer routing nativo.
Verifica catálogo de seis agentes y diez skills y ambas carpetas separadas.
La [migración del instalador](migracion-agentes.md) tiene sus propios fixtures;
no se ejecuta desde documentación ni se borran skills/contexto.

## Registro core pendiente

| Escenario | Resultado | Evidencia requerida |
|---|---|---|
| Inspect arquitectura / navegación | PENDIENTE | Skill cargada, fuentes, respuesta, snapshot pre/post idéntico |
| Core local bootstrap/sync | PENDIENTE | Plan, aprobación, skills/gates y rutas modificadas |
| Consumo directo y seis estados de contexto | PENDIENTE | Estado/baseline, capas y fuentes directas por fixture |
| Mixta / exportación | PENDIENTE | Lectura atendida y ausencia de escritura sin gate |
| Targets retirados / otros targets conservados | PENDIENTE | Diagnóstico sin ejecución; handoffs vigentes válidos |
| Catálogo y conservación | PENDIENTE | 6 agentes, 10 skills, carpetas y formatos intactos |

Por ejecución registrar plataforma, versión/build, OS, modelo, fecha/responsable,
commit del kit, fixture/autorización, prompt, recursos cargados, snapshots,
resultado observado y bloqueos: **PENDIENTE**. Los escenarios core nuevos no han
sido ejecutados en runtime LLM; evidencia histórica y tests estáticos no los aprueban.

## Criterio de cierre actualizado

La prueba pasa si todos los modos aplican preflight sin recomendaciones LLM; las
escrituras conservan aprobación del plan global, las skills especialistas conservan
autoridad y no aparece una carpeta `.documentation/`. El handoff pasa solo si productor y receptor
cumplen el contrato, no duplican la acción y preservan los gates.

Escenarios del contrato nuevo definidos, no ejecutados en hosts. Registra evidencia
observada por plataforma; el preflight o los tests textuales no acreditan ejecución
conversacional. Los permisos del host y la validación técnica de evidencia siguen vigentes.
