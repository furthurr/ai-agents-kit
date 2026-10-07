# Contrato compartido de contexto del proyecto

Referencia portable de descubrimiento y consumo, disponible en la skill
`documentation-orchestrator` sin cargar su workflow de mantenimiento. No define
formatos nuevos: [Architecture](../../architecture/SKILL.md) conserva autoridad
sobre `.architecture/` y [Project Navigator](../../project-navigator/SKILL.md)
sobre config, formatos, disponibilidad y capas de `.navigator/`.

## Orden de lectura bajo demanda

1. Leer primero instrucciones del host/proyecto y steering aplicable, incluido
   `.sdd/steering/` cuando corresponda. Código, steering y contratos canónicos
   son autoridad; el contexto core ayuda a localizar y explicar, no los sustituye.
2. Consultar core solo si ayuda al alcance; no cargar carpetas ni índices completos.
3. Para arquitectura, entrar por `.architecture/README.md` y su «Contexto para IA».
   Abrir solo secciones o ADRs relevantes. Contrastar la marca de sincronización
   con Git y cambios estructurales relevantes antes de afirmar vigencia.
4. Para navegación, localizar `.navigator/config.yaml` en raíz/subproyectos
   conocidos, excluyendo backups. Elegir instancia única o `project.root` más
   específico que contenga el alcance; en empate no adivinar. Leer el config en
   esta petición y resolver artefactos junto a él, no junto al código consultado.
   Aplicar [config](../../project-navigator/references/config.md) y
   [capas](../../project-navigator/references/layers.md): una capa debe estar
   habilitada, existir y ser legible. Empezar por `ai-context.md` o
   `module-map.json`; escalar a símbolos/grafo solo si hace falta y están habilitados.
5. Contrastar baseline común verificable (`source_commit` de artefactos consumidos
   que lo soporten) con `HEAD` y working tree, filtrando rutas relevantes,
   contratos, steering y manifiestos. `generated_at` solo informa antigüedad.
   Marcas ausentes/incompatibles o relevancia incierta no demuestran vigencia.
6. Validar en fuentes directas las afirmaciones que sustentan decisiones o
   evidencia según la operación. Un índice desfasado solo aporta pistas;
   descartar paths inexistentes. Si cambia el contexto, repetir el preflight mínimo.

## Degradación sin mantenimiento implícito

| Estado | Evidencia y uso permitido |
| --- | --- |
| `Vigente` | Baseline verificable común, sin cambios relevantes posteriores/locales; orienta, con verificación de decisiones en fuentes directas. |
| `Ausente` | Sin contexto o instancia aplicable; continuar con fuentes directas. |
| `Desfasado` | Cambios relevantes desde baseline; solo pistas y contraste con fuentes directas. |
| `Ambiguo` | Instancias empatadas o propiedad incierta; omitir contexto ambiguo y continuar con fuentes directas. |
| `Ilegible` | Config/capa inaccesible o inválida; usar otra capa válida o fuentes directas. |
| `No verificable` | Marca ausente, incompatible o imposible de contrastar; no afirmar vigencia, usar solo pistas verificadas. |

Una capa deshabilitada no se lee aunque exista. Una capa habilitada ausente o
incompleta no se inventa. La ausencia/desfase por sí sola no bloquea la tarea;
preguntar solo si la selección es indispensable para la petición explícita.
Comunicar la limitación pertinente, fuentes realmente usadas y confianza breve.
Si esta referencia no está disponible, continuar con fuentes directas sin suponer
que el contexto fue validado.

## Lectura y escritura son operaciones distintas

El consumo directo no exige handoff ni cambio de agente. Una consulta no crea ni
actualiza documentación, índices o instrucciones del proyecto; no ejecuta
bootstrap, sync, export ni instalación de herramientas. Recomendar
`documentation-orchestrator` para mantenimiento cuando sea útil, sin invocarlo
automáticamente ni inferir autorización. Allí core se ejecuta localmente con sus
skills separadas y gates; Navigator mantiene export opt-in con confirmación
específica. La recomendación de modelo no autoriza escritura y conserva la política
de avisos vigente. Los demás especialistas mantienen sus contratos de handoff.
