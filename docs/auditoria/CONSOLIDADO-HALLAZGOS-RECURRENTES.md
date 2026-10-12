# Consolidado general de hallazgos recurrentes y plan de solución

- **Fecha:** 2026-10-10.
- **Base:** lectura completa de los cinco informes de esta carpeta.
- **Resultado:** 17 temas recurrentes, ordenados por prioridad de atención.
- **Estado actualizado:** tablero de origen más seguimiento de REC-01–REC-05 y REC-09–REC-17; REC-03–REC-05 implementados en el worktree, pendientes de integración/CI remota.
- **Complemento:** [Backlog de hallazgos no recurrentes](BACKLOG-HALLAZGOS-NO-RECURRENTES.md).
- **Ejecución entre sesiones:** [Protocolo de remediación](PROTOCOLO-REMEDIACION.md).
- **Primera sesión:** [Prompt de REC-01](PROMPT-REC-01.md).

## 1. Resumen ejecutivo

**En la línea base, las mayores coincidencias fueron la duplicación de instrucciones (5/5 fuentes), los disparadores de skills demasiado amplios (4/5) y la obligatoriedad o incompatibilidad de alcance de Scalar (4/5).** REC-04 responde a este último retirando Scalar por completo del flujo actual; el tablero conserva la frecuencia histórica de los informes.

Sin embargo, **el orden de trabajo debe comenzar por secretos, permisos efectivos y contratos de alcance**, porque pueden comprometer información o impedir operaciones legítimas. La frecuencia expresa coincidencia documental; no determina por sí sola el impacto.

Conviene conservar la arquitectura `canonical/` → adaptadores → `generated/`, la separación agente/skill, la trazabilidad SDD, la lectura selectiva y la validación no destructiva. La solución consiste en hacer esos controles más consistentes, proporcionales y verificables.

## 2. Fuentes y método

| Clave | Documento | Ámbito declarado |
|---|---|---|
| A | [AUDITORIA-MAS-ANTIGRAVITY.md](AUDITORIA-MAS-ANTIGRAVITY.md) | Kit canónico y distribución multi-host; recomendaciones orientadas a Antigravity. |
| D | [AUDITORIA-MAS-DEEPSEEK.MD](AUDITORIA-MAS-DEEPSEEK.MD) | Fuentes canónicas, adaptadores, herramientas y pruebas; revisión estática. |
| G | [AUDITORIA-MAS-GPT.md](AUDITORIA-MAS-GPT.md) | Kit, contratos, adaptadores y evidencia histórica; sin nuevas ejecuciones de agentes. |
| M | [AUDITORIA-MAS-MIMO.MD](AUDITORIA-MAS-MIMO.MD) | Instalación local de OpenCode y skills globales; no auditó las fuentes canónicas del kit. |
| E | [Estudio-agentes-y-skills-ai-agents-kit.md](Estudio-agentes-y-skills-ai-agents-kit.md) | Kit, herramientas, registros, CI y documentación; revisión estática. |

### Reglas de consolidación

1. Una mención significa **una fuente distinta que identifica sustantivamente el problema**. Resumen, detalle y solución del mismo informe cuentan una sola vez.
2. Se agrupan equivalencias de causa o contrato; los matices conservan su trazabilidad. No se suman las frecuencias de temas relacionados.
3. Las advertencias generales sobre falta de runtime no se cuentan como hallazgo conductual específico. R08 cuenta los dos documentos que lo desarrollan expresamente.
4. Se conservan separados problemas con remedios y criterios de cierre diferentes: duplicación, acrónimos forzados, fragmentación, métricas y presupuestos.
5. Las fuentes no acreditan independencia entre auditorías. El recuento no equivale a cinco experimentos independientes ni a una tasa de fallos.
6. Las referencias `A/D/G/M/E:líneas` apuntan a los **informes originales**, no a líneas actuales de código. Las rutas de producto citadas por ellos deben comprobarse antes de editar.
7. Los IDs `REC-*` son IDs de esta síntesis, no sustituyen deudas o findings existentes. Vincular los registros originales al implementar.

### Criterio de prioridad

Se considera, en este orden: exposición de información o ampliación de permisos; bloqueo o incompatibilidad contractual; integridad de distribución; capacidad de demostrar cumplimiento; mantenibilidad y fricción; medición. La recurrencia ayuda a ordenar dentro de esos grupos. Las prioridades son de atención, no severidades Sonar/OWASP.

## 3. Matriz de recurrencia y orden de importancia

`✓` indica una identificación explícita del tema; `—` no significa que la fuente lo descarte.

| Orden / ID | Tema consolidado | A | D | G | M | E | Fuentes | Atención |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| 1 / REC-01 | Secretos reales permitidos mediante autorización | — | ✓ | ✓ | — | ✓ | 3/5 | Alta |
| 2 / REC-02 | Permisos y límites efectivos inconsistentes | — | ✓ | — | ✓ | ✓ | 3/5 | Alta |
| 3 / REC-03 | Evidencia de `inspect` restringida al alcance documental | — | ✓ | ✓ | — | — | 2/5 | Alta |
| 4 / REC-04 | Scalar obligatorio o fuera del alcance autorizado | ✓ | ✓ | ✓ | — | ✓ | 4/5 | Alta |
| 5 / REC-05 | Preflight que acepta recursos incompletos | — | ✓ | — | — | ✓ | 2/5 | Alta |
| 6 / REC-06 | Render no transaccional | — | ✓ | — | — | ✓ | 2/5 | Media |
| 7 / REC-07 | Importador que sigue symlinks sin controlar destino | — | ✓ | — | — | ✓ | 2/5 | Media |
| 8 / REC-08 | Cumplimiento conductual actual sin evidencia suficiente | — | — | ✓ | — | ✓ | 2/5 | Alta, transversal |
| 9 / REC-09 | Duplicación de identidad, contexto y reglas normativas | ✓ | ✓ | ✓ | ✓ | ✓ | 5/5 | Media |
| 10 / REC-10 | Descripciones amplias y activación solapada | ✓ | ✓ | ✓ | ✓ | — | 4/5 | Media |
| 11 / REC-11 | Tests que fuerzan acrónimos OWASP fuera de seguridad | ✓ | ✓ | — | — | — | 2/5 | Media |
| 12 / REC-12 | Micro-pasos obligatorios para cambios atómicos | ✓ | ✓ | — | — | — | 2/5 | Media |
| 13 / REC-13 | Referencias SDD hiperfragmentadas | ✓ | ✓ | — | — | — | 2/5 | Media |
| 14 / REC-14 | Opciones retiradas y advertencias históricas repetidas | ✓ | ✓ | ✓ | — | — | 3/5 | Media-baja |
| 15 / REC-15 | Conocimiento Git elemental reexplicado | ✓ | ✓ | — | — | — | 2/5 | Media-baja |
| 16 / REC-16 | Métrica de contexto no representativa del flujo | — | ✓ | — | — | ✓ | 2/5 | Media, transversal |
| 17 / REC-17 | Topes de tokens basados en heurísticas rígidas | ✓ | ✓ | — | — | — | 2/5 | Baja |

**Lectura por frecuencia:** REC-09 (5); REC-04 y REC-10 (4); REC-01, REC-02 y REC-14 (3); los restantes (2). La tabla principal está ordenada por importancia de atención, no por frecuencia descendente.

## 4. Fichas de trabajo

Todas las fichas comienzan en **pendiente de verificar vigencia**. Una modificación de texto no basta para declarar resuelto un problema de comportamiento o herramientas.

### REC-01 — Unificar la política de secretos

- **Fuentes:** D AUD-01, líneas 66–78; G H04, 165–197; E EST-001, 194–206.
- **Problema e impacto:** Git permite incluir archivos sensibles con autorización, mientras otras reglas prohíben secretos. Una autorización puede interpretarse como excepción para publicar credenciales.
- **Ámbito:** `canonical/skills/git-commit/SKILL.md`, `release-management`, política general y consumidores.
- **Trabajo:** (1) distinguir nombre sospechoso, configuración pública, placeholder y secreto real; (2) excluir secretos confirmados sin reproducir valores; (3) unificar redacción y opciones de interacción; (4) vincular un control automatizado adecuado al flujo.
- **Cierre:** un fixture sintético con credencial detectable queda fuera del commit aunque se solicite incluirlo; configuraciones públicas no se bloquean solo por nombre; los mensajes no muestran valores sensibles. Reutilizar la deuda existente indicada por G.

### REC-02 — Hacer comprobables permisos y fronteras de confianza

- **Fuentes:** D AUD-02, 82–97; M H8, 167–185; E EST-002, 208–222.
- **Problema e impacto:** el alcance declarado no tiene controles equivalentes entre hosts; la instalación OpenCode añade redundancias y dudas sobre precedencia de patrones.
- **Matiz:** D/E señalan equivalencia multi-host; M señala configuración local. Son variantes de consistencia de permisos, no tres constataciones del mismo fallo runtime.
- **Trabajo:** (1) definir capacidades por agente y modo, diferenciando consulta y remediación autorizada; (2) contrastar semántica vigente de cada host; (3) aplicar restricciones soportadas y retirar redundancias solo cuando la precedencia esté comprobada; (4) documentar controles no soportados y límites de confianza de workspace/web.
- **Cierre:** matriz por host y pruebas inocuas de edición/comandos dentro y fuera de alcance; evidencia de autorizaciones reales. Justificar permisos de red por necesidad del flujo, sin adoptar automáticamente un `ask` universal.

### REC-03 — Separar evidencia de lectura y alcance de escritura

- **Fuentes:** D AUD-03, 101–113; G H01, 56–89.
- **Problema e impacto:** `inspect` exige evidencia dentro de `.data/`, `.design/`, etc.; una inspección correcta de código sin esas carpetas puede resultar inválida.
- **Ámbito:** referencias de handoff y `tools/handoff_contract.py`.
- **Trabajo:** definir fuentes de lectura/evidencia pertinentes dentro del proyecto para `inspect`; mantener `write_scope` para entregables de escritura; actualizar documentación y validador juntos.
- **Cierre:** inspeccionar proyectos con y sin documentación, citar código sin crear artefactos y rechazar rutas externas o symlinks que escapen. Una acción de escritura no puede acreditarse solo con evidencia fuera de su alcance autorizado.

### REC-04 — Retirar el visor interactivo de APIs

- **Fuentes:** A Hallazgo 7, 111–116 y 210–217; D AUD-08, 176–186; G H02, 91–124; E §2.1, 119 y EST-006, 266–278.
- **Problema e impacto:** el flujo exigía mantener un lanzador y un visor interactivo que no son contratos de API y añadían herramientas, instrucciones y rutas de escritura adicionales.
- **Decisión de alcance (2026-10-12):** retirar Scalar del producto en vez de mantenerlo como operación optativa. OpenAPI, JSON Schema y el catálogo de endpoints conservan la documentación contractual.
- **Trabajo:** retirar el flujo interactivo, su referencia y pruebas asociadas de `data-api`; actualizar catálogo y distribuciones.
- **Cierre:** ninguna fuente operativa ni distribución genera visor o lanzador; la documentación API conserva OpenAPI o catálogo y sus modelos; el histórico de informes no se reescribe.
- **Efecto sobre alcance:** al retirarse el lanzador no hace falta ampliar el scope documental ni crear artefactos fuera de `.data/`.

### REC-05 — Validar instalaciones completas

- **Fuentes:** D AUD-13, 245–252; E EST-005, 252–264.
- **Problema e impacto:** comprobar únicamente archivos principales deja pasar referencias o recursos ausentes/alterados; los wrappers pueden tener coberturas distintas.
- **Trabajo:** centralizar inventario esperado y hashes; verificar todo el árbol antes de copiar y el destino después; armonizar los wrappers conservando sus garantías de backup y dry-run.
- **Cierre:** recursos faltantes o alterados fallan en cada plataforma; una fuente inválida falla antes de escribir; una copia incompleta nunca declara éxito. Probar en perfiles temporales.

### REC-06 — Publicar renderizados de forma transaccional

- **Fuentes:** D AUD-12, 229–241; E EST-008, 298–308.
- **Problema e impacto:** se elimina la salida válida antes de reconstruirla; una excepción puede dejar resultados parciales o versiones mezcladas.
- **Trabajo:** definir si la unidad de publicación es una plataforma o la matriz completa; renderizar en staging; validar antes de publicar; diseñar recuperación y limpieza. Evaluar garantías reales del sistema de archivos, sin llamar atómico a un simple borrado y copia.
- **Cierre:** fallos controlados antes y durante publicación conservan o recuperan una distribución válida; no se instala contenido parcial; recuperación documentada y probada.

### REC-07 — Controlar enlaces durante importación

- **Fuentes:** D AUD-14, 256–263; E EST-009, 310–322.
- **Problema e impacto:** el importador puede copiar contenido externo al origen autorizado. Las fuentes no demuestran una filtración.
- **Trabajo:** elegir política explícita para enlaces internos y externos; validar rutas resueltas antes de copiar o rechazar enlaces; conservar errores claros y dry-run sin escrituras.
- **Cierre:** fixtures con enlaces externos no importan contenido ajeno; enlaces internos reciben el tratamiento documentado; dry-run no modifica origen ni destino.

### REC-08 — Obtener evidencia conductual actual

- **Fuentes:** G H10, 372–408; E §4, 326–340 y Bloque C, 361–366.
- **Problema e impacto:** propagación textual y fixtures no prueban que el modelo respete routing, herramientas, límites y gates. Los fallos históricos no certifican fallos de la fuente actual.
- **Trabajo:** establecer baseline fechado; repetir R04/R10 y pendientes R06/R07/R11 cuando sea viable; añadir handoffs y gates; registrar host, versión, modelo, fuente exacta, petición, herramientas, cambios y respuesta sanitizada; comparar variantes en sesiones independientes.
- **Cierre:** matriz con PASS/FAIL/bloqueado, evidencia reproducible y límites declarados. Una ejecución incompleta nunca cuenta como éxito; atribuir mejoras solo a dimensiones medidas.
- **Dependencia transversal:** usar estos escenarios para validar REC-02, REC-03, REC-04, REC-09 y REC-10, sin esperar al final de todas las correcciones.

### REC-09 — Asignar una fuente responsable por regla

- **Fuentes:** A Hallazgo 1, 42–54; D AUD-05, 131–141; G H06, 228–267; M H3, 69–86 y H6, 132–148; E §2.2, 123–137.
- **Problema e impacto:** identidad, contexto core, profundidad, derivación y aprobaciones se mantienen en varias capas; aumenta la deriva y el contexto redundante.
- **Trabajo:** inventariar reglas repetidas; dejar rol/límites/selección de skill en el agente y procedimiento en la fuente responsable; evaluar fragmentos ensamblados por renderer; conservar controles esenciales y referencias directas; revisar pertinencia del contexto core para Git/release.
- **Diferencia entre propuestas:** M sugiere steering global OpenCode; D/E, fragmentos de render. No son intercambiables: comprobar qué instrucciones carga cada host y mantener artefactos distribuidos utilizables por sí mismos. Consultar contexto no equivale por sí solo a modificar arquitectura.
- **Cierre:** cada regla tiene propietario; cambios no requieren múltiples ediciones normativas; referencias distribuidas válidas; contratos preservados y casos representativos evaluados.
- **Dependencia:** REC-11 antes de quitar texto exigido por tests; FUT-06 si se opta por steering local.

### REC-10 — Precisar cuándo se activa cada skill

- **Fuentes:** A Hallazgo 8, 120–125; D AUD-11, 215–225; G H07, 269–304; M H4, 88–106, H5, 108–130 y H11, 217–233.
- **Problema e impacto:** términos universales y compartidos hacen competir arquitectura, navegación, orquestación y especialistas; Graphify y skills externas añaden solapamientos locales.
- **Trabajo:** redactar operación + objeto + resultado; expresar límites de pares concretos; retirar cuantificadores absolutos; probar consultas positivas, negativas y ambiguas. Revisar las descripciones que ve el selector, no solo el cuerpo.
- **Diferencia entre propuestas:** A/D proponen retirar consultas directas del orquestador, mientras su contrato actual las contempla. Decidir primero qué componente debe ser dueño de esas consultas y conservar o migrar ese comportamiento explícitamente.
- **Cierre:** catálogo sin competencias ambiguas no justificadas; selección observada registrada, incluidos falsos positivos y omisiones. No crear otro router sin evidencia de necesidad.
- **Relacionado:** FUT-08 conserva el defecto específico del campo/comando de Graphify.

### REC-11 — Desacoplar tests de identidad y contenido irrelevante

- **Fuentes:** A Hallazgo 1, 42–54 y Paso 1, 135–144; D AUD-04, 117–127.
- **Problema e impacto:** `test_mas_identity.py` exige MASVS/MASWE/MASTG incluso en Git/UI, forzando advertencias ajenas al dominio.
- **Trabajo:** definir contrato mínimo de identidad; reservar referencias OWASP a dominios pertinentes; actualizar pruebas canónicas y de distribución; retirar frases forzadas de consumidores.
- **Cierre:** archivos ajenos a seguridad pasan sin acrónimos móviles; seguridad conserva referencias pertinentes; las pruebas detectan pérdida de identidad real, no ausencia de una frase arbitraria.

### REC-12 — Ajustar aprobaciones al riesgo de remediación

- **Fuentes:** A Hallazgo 4, 78–86 y Paso 4, 179–187; D AUD-06, 145–155.
- **Problema e impacto:** una regla absoluta exige aprobar cada micro-paso incluso en correcciones localizadas.
- **Trabajo:** definir cambio atómico como localizado, reversible, sin migración ni cambio de contrato; proponer una aprobación del cambio completo y verificar; conservar pasos separados para cambios estructurales o de riesgo elevado.
- **Cierre:** corrección atómica autorizada sin aprobaciones redundantes; cambio estructural mantiene gates necesarios. No extender esta simplificación a commit, push, tags u otras autorizaciones independientes.
- **Matiz:** G H08 mantiene los micro-pasos como requisito explícito y no propone retirarlos indiscriminadamente; cualquier cambio del contrato debe aprobarse y comprobarse.

### REC-13 — Reducir lecturas encadenadas en SDD

- **Fuentes:** A Hallazgo 3, 68–74 y Paso 3, 164–175; D AUD-07, 159–172.
- **Problema e impacto:** cargar o releer referencias que no requiere la decisión actual aumenta lecturas y contexto.
- **Trabajo aplicado:** indicar una carga por necesidad/fase y reutilizar la referencia mientras fuente y alcance no cambien. Se mantuvieron los archivos independientes bajo demanda: una fusión mecánica podría cargar material ajeno al caso y aumentar tokens.
- **Cierre:** la política de lectura selectiva está en la skill; REC-16 debe medir archivos realmente leídos en tareas representativas antes de afirmar que bajaron lecturas/latencia. No se hizo una consolidación sin evidencia de ahorro.
- **Dependencia:** REC-09 y REC-16 para evitar resolver duplicación mediante más lecturas o afirmar ahorros no medidos.

### REC-14 — Simplificar compatibilidad histórica

- **Fuentes:** A Hallazgo 5, 90–98; D AUD-09, 190–200; G H06, 236–258.
- **Problema e impacto:** opciones retiradas y prohibiciones históricas se repiten en varias capas.
- **Trabajo:** describir modos vigentes; mantener una única regla breve para solicitudes/specs antiguas; retirar advertencias redundantes solo tras identificar el requisito que protegen.
- **Cierre:** solicitudes vigentes tienen flujo directo; una spec antigua recibe una propuesta de migración correcta; agente/skill/referencias no divergen. G identifica repetición normativa, no recomienda borrar todas las restricciones.

### REC-15 — Podar instrucciones Git elementales

- **Fuentes:** A Hallazgo 2, 58–64 y Paso 2, 148–160; D AUD-10, 204–211.
- **Problema e impacto:** tablas de comandos básicos y tipos de commit añaden contexto sin reglas específicas.
- **Trabajo:** conservar idioma, estilo, ámbito, ticket, agrupación, política de secretos y aprobaciones; reducir tablas genéricas; comprobar que la poda no elimina excepciones del producto.
- **Cierre:** los escenarios de commit conservan formato y controles requeridos; menos contenido genérico sin pérdida funcional.
- **Relacionado:** FUT-17/FUT-18 corrigen problemas específicos de clasificación y detección de cambios incompatibles.

### REC-16 — Medir utilidad y coste por tarea

- **Fuentes:** D AUD-15, 267–276; E §2.3, 139–151.
- **Problema e impacto:** sumar palabras no representa el contexto real ni recursos anidados; no demuestra utilidad del kit.
- **Trabajo:** etiquetar la métrica actual como inventario; medir tareas de consulta, implementación, documentación y Git; registrar archivos leídos, tokens cuando estén disponibles, turnos, tiempo y corrección; comparar baseline con/sin kit en condiciones documentadas.
- **Cierre:** protocolo y resultados por tarea; separar mediciones de estimaciones; si un host no expone tokens, declarar el dato ausente. No reproducir como resultados los ahorros estimados por A, líneas 254–257.

### REC-17 — Sustituir garantías de tokens no instrumentadas

- **Fuentes:** A Hallazgo 6, 102–107 y Paso 6, 200–206; D AUD-15, 269–276.
- **Problema e impacto:** `~4 chars ≈ 1 token` y topes rígidos pueden presentarse como cumplimiento fiable sin medición.
- **Trabajo:** usar pautas de contenido y lectura selectiva; mantener límites medidos solo si existe un mecanismo externo apropiado; distinguir estimación orientativa de garantía.
- **Cierre:** concisión verificable por contenido; métricas con método documentado; sin afirmaciones de autocomputo determinista del modelo.
- **Relacionado:** FUT-04 trata presupuestos de archivos ampliables, un problema distinto del cálculo de tokens.

## 5. Secuencia de ejecución recomendada

| Fase | Acciones | Resultado esperado |
|---|---|---|
| 0 — Baseline | Comprobar vigencia, vincular deudas existentes, preparar REC-08/REC-16 | Saber qué fuente se corrige y cómo comparar resultados. |
| 1 — Confianza y contratos | REC-01 a REC-04; revisar FUT-01 | Política coherente, permisos comprobables y alcances compatibles. |
| 2 — Distribución | REC-05 a REC-07 | Instalación, render e importación resistentes a contenido incompleto o externo. |
| 3 — Simplificación | REC-11 → REC-09; REC-10, REC-12 a REC-15 y REC-17 | Menos duplicación y fricción sin pérdida de requisitos. |
| 4 — Evaluación | Repetir REC-08 y comparar REC-16 tras cada bloque relevante | Evidencia de cierre y mejoras medidas, no inferidas. |

### Verificación técnica al implementar

Seleccionar pruebas relevantes según el cambio. Los informes proponen, entre otras, las siguientes comprobaciones; confirmar su vigencia antes de ejecutarlas:

```bash
python3 -m unittest tools/test_validate.py tools/test_integrity.py tools/test_mas_identity.py tools/test_documentation_core.py tools/test_handoff_contract.py
python3 tools/render.py
python3 tools/validate.py
python3 tools/check_links.py
```

`render.py` escribe artefactos: ejecutarlo como parte de la remediación correspondiente, después de comprobar su estado. Los tests de contrato deben complementarse con pruebas negativas de herramientas y evaluación en host cuando el hallazgo lo requiera.

## 6. Seguimiento y criterio común de cierre

La **sesión coordinadora** mantiene este tablero y su historial. Cada sesión implementadora registra su trabajo en `seguimiento/<ID>.md`; así pueden trabajar en paralelo sin editar el mismo tablero. En ejecución de una sola sesión, esa sesión puede asumir explícitamente ambos roles.

Estados y reglas de transición: [Protocolo de remediación](PROTOCOLO-REMEDIACION.md). Secuencia habitual: **pendiente → confirmado → en curso → corregido en rama → integrado pendiente de verificación → cerrado**. También se admiten **bloqueado** y **no vigente**, con evidencia y explicación. `Pendiente` incluye comprobar vigencia.

### Tablero individual

`—` significa sin asignar o sin evidencia todavía. Preparar una ficha o un prompt no reserva el hallazgo ni inicia su implementación. La coordinadora completa responsable, rama/worktree y baseline al asignarlo.

| ID | Estado | Responsable / rama | Última actualización | Evidencia | Próxima acción |
|---|---|---|---|---|---|
| REC-01 | Cerrado | Coordinación / `main` `5dba871`; fix `9e0696e` | 2026-10-11 | [Ficha](seguimiento/REC-01.md), [reporte real](seguimiento/REC-01-live.json) — scanner 1/0, rechazo de excepción, contraste público/placeholder, sin exposición; suites/CI acreditadas y Gate 4 aprobado | Conservar evidencia; ajuste del harness y cierre sin commit nuevo. No certificación universal. |
| REC-02 | Cerrado; validación runtime complementaria abierta | Coordinación / `main` `5dba871`; fix `9e0696e`; origen `remediation/rec-02` | 2026-10-11 | [Ficha](seguimiento/REC-02.md), [reporte real](seguimiento/REC-02-live.json) — matriz multi-host, controles aplicables, límites explícitos, OpenCode/Pi y CI acreditados | Remanentes de hosts/variantes en [VER-REC-02](seguimiento/VER-REC-02.md); no bloquean REC-03 ni otros hallazgos independientes. |
| REC-03 | Integrado pendiente de verificación | Coordinación / `main`, baseline `43fd2dc` + trabajo local | 2026-10-12 | [Ficha](seguimiento/REC-03.md): inspect acepta evidencia de código dentro del proyecto aunque falten carpetas de findings; escrituras siguen limitadas al scope; 37 tests pasan | Revisión final integrada y conservar smoke runtime como cobertura complementaria de REC-08. |
| REC-04 | Integrado pendiente de verificación | Coordinación / `main`, baseline `43fd2dc` + trabajo local | 2026-10-12 | [Ficha](seguimiento/REC-04.md): flujo Scalar retirado de `data-api`, catálogo actualizado y seis distribuciones sin visor; integridad 416/416 | Revisión final integrada; conservar informes originales como historia. |
| REC-05 | Integrado pendiente de verificación | Coordinación / `main`, baseline `43fd2dc` + trabajo local | 2026-10-12 | [Ficha](seguimiento/REC-05.md): preflight compara archivos esperados y hashes con render canónico; source y postflight verificados; Bash wrappers 250/250, Antigravity 22/22 | Revisión final integrada y CI remota/runner Windows tras publicación. |
| REC-06 | Pendiente | — | 2026-10-10 | — | Definir unidad de publicación y recuperación. |
| REC-07 | Pendiente | — | 2026-10-10 | — | Confirmar comportamiento del importador. |
| REC-08 | Pendiente | — | 2026-10-10 | — | Preparar baseline y escenarios por host. |
| REC-09 | Cerrado | Coordinación / `main`; seis distribuciones | 2026-10-11 | Fragmentos MAS/contexto centrales, aplicación pertinente y Git/release excluido del contexto ajeno; identidad y contratos verificadas | Ninguno de la remediación; measurement real continúa en REC-16. |
| REC-10 | Implementado; evaluación runtime pendiente | Coordinación / `main`; descriptores en seis hosts | 2026-10-11 | Descripciones con operación/objeto/límite; Graphify local acotado | Medir activaciones positivas y falsas por host; follow-up de REC-08. |
| REC-11 | Cerrado | Coordinación / `main`; seis distribuciones | 2026-10-11 | Identidad compartida y test desacoplado; `test_mas_identity.py` 235/235 | Ninguno del contrato; runtime de triggers va en REC-08/REC-10. |
| REC-12 | Implementado; smoke conversacional pendiente | Coordinación / `main`; seis distribuciones | 2026-10-11 | Corrección atómica: diff completo/una aprobación; estructural: micro-pasos; contract 7/7 | No medir turnos ahorrados hasta probar con agente; autorizaciones Git/release independientes permanecen. |
| REC-13 | Política de carga implementada; medición pendiente | Coordinación / `main`; seis distribuciones | 2026-10-11 | SDD carga solo la referencia/fragmento necesario una vez y lo reutiliza; referencias permanecen bajo demanda | Medir lecturas reales con REC-16; no fusionar módulos si aumenta la carga parcial. |
| REC-14 | Cerrado | Coordinación / `main`; seis distribuciones | 2026-10-11 | Compatibilidad histórica condensada y fuente responsable única; SDD 613/613 | Ninguno de la poda; decisiones históricas preservadas. |
| REC-15 | Cerrado | Coordinación / `main`; seis distribuciones | 2026-10-11 | Tablas/comandos/troubleshooting genéricos retirados; `test_secret_policy.py` 26/26 y suite CI local | Ninguno de la poda; FUT-17/18 siguen como mejoras funcionales distintas. |
| REC-16 | Parcial; medición source-volume implementada | Coordinación / `main` | 2026-10-11 | Flujos generados OpenCode: Git −493 palabras/−3.390 B; SDD scope −276 palabras/−2.147 B frente a HEAD | Estos son bytes/palabras, no tokens ni usage; tokens, turnos/tiempo/éxito requieren medición real del host. |
| REC-17 | Cerrado | Coordinación / `main`; seis distribuciones | 2026-10-11 | Fórmula caracteres→tokens y topes no instrumentados retirados; Navigator conciso por contenido | Ninguno de heurísticas; los límites instrumentados se documentan con método. |

### Historial de cambios de estado

Añadir una fila por transición; no reemplazar el diagnóstico ni las fuentes históricas. Registrar inicio y cierre mediante estas filas y detallar pruebas/archivos en la ficha de sesión enlazada.

| Fecha | ID | Transición | Responsable / baseline / rama | Resumen y evidencia | Pendientes |
|---|---|---|---|---|---|
| 2026-10-10 | REC-01 a REC-17 | Inicialización → Pendiente | Preparación documental; sin rama de remediación | Tablero individual y protocolo creados. Ningún fix ejecutado. | Asignación, vigencia y verificación. |
| 2026-10-10 | REC-01 | Pendiente → Confirmado | Sesión SDD coordinadora e implementadora exclusiva / `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880` / `main` | Contradicción Git/release vigente; deuda P0.5 vinculada; [ficha](seguimiento/REC-01.md) con baseline, comprobación puntual de sesiones y requisitos propuestos. Cambios documentales sin commit; ningún fix aplicado. | Gate 1 y fases posteriores; todos los criterios conductuales abiertos. |
| 2026-10-10 | REC-01 | Confirmado → Confirmado; avance SDD | Sesión SDD exclusiva / `03f30be` / `main` | Gate 1 aprobado; diseño propuesto y verificaciones de baseline en [ficha](seguimiento/REC-01.md). Sin implementación ni commit. | Gate 2, Tasks/Gate 3 y verificación conductual; no cerrado. |
| 2026-10-10 | REC-01 | Confirmado → Confirmado; avance SDD | Sesión SDD exclusiva / `03f30be` / `main` | Gate 2 aprobado; Tasks propuesto con ocho tareas secuenciales y trazabilidad, según [ficha](seguimiento/REC-01.md). Sin fix ni commit. | Gate 3 para iniciar implementación; verificación y cierre pendientes. |
| 2026-10-11 | REC-01 | Confirmado → En curso | Sesión SDD exclusiva / `03f30be` / `main` | Gate 3 aprobado; baseline/exclusividad y ausencia de reservas solapadas revalidados. Inicia implementación, sin commit. | Pruebas significativas, distribución y evidencia conductual antes de cierre. |
| 2026-10-11 | REC-01 | En curso → Integrado pendiente de verificación | Sesión SDD exclusiva / HEAD `03f30befca829daa2c2a3c6cd47c2dc4fe5b4880` + cambios sin commit / `main` | Política/control/CI/docs y seis distribuciones integrados localmente; 26 tests REC-01 y suites pertinentes verdes. [Ficha](seguimiento/REC-01.md) y Verification identifican evidencias y hashes. | Decisión conductual del host no acreditada: intento sin proveedor/autenticación disponible y segundo timeout 90 s; no cerrar. |
| 2026-10-11 | REC-02 | En curso → Integrado pendiente de verificación | Sesión coordinadora / HEAD base `03f30be` + cambios locales / `main`; origen `remediation/rec-02` | Delta selectivo integrado, artefactos regenerados, suites locales y pruebas de host OpenCode/Pi; [ficha](seguimiento/REC-02.md) registra evidencias y limitaciones. | Runtime Kiro V3/otros hosts, evidencia con LLM y consentimiento humano, CI remoto; no cerrar. |
| 2026-10-11 | REC-01 / REC-02 | Mismo estado; integración Git y CI remota acreditadas en revisión posterior | `main` `5dba87197a64fcc9e026a344236d5da02793b4cf`; fix `9e0696e131dd7f105b450cd1bb108acd3ac816b2` | 14 hashes originales coincidentes; suites directas y validate correctos; [CI actual SUCCESS](https://github.com/furthurr/ai-agents-kit/actions/runs/38190590672); controles OpenCode/Pi revalidados. Actualización documental, sin modificación de producto. | Conducta REC-01 y Gate 4; runtime/consentimiento/hosts pendientes de REC-02. No cerrados; no inferir PASS de Kiro ni de un LLM a partir del harness. |
| 2026-10-11 | REC-01 | Integrado pendiente de verificación → Cerrado | Coordinadora; `5dba871` + mejora del probe/evidencia locales | Prueba real aislada revisada: skill local cargada, scanner 1/0, decisión correcta, no exposición ni cambios de fixtures/índice/refs. Usuario aprueba Gate 4 explícitamente. Spec y P0.5 política actualizados. | Sin criterios originales de cierre pendientes; cambios finales sin commit nuevo. |
| 2026-10-11 | REC-02 | Integrado pendiente de verificación → Bloqueado | Coordinadora; host OpenCode 1.18.34, modelo real y proyecto temporal | Inspect sin escritura ignora instrucción embebida; petición fuera de alcance rechazada; apply_patch legítimo con autorización humana y remediación preservada. Rechazo/delegación quedan parcialmente ejecutados y no se cuentan como PASS de respuesta final. | Faltan runtime de Kiro V3 y otras superficies/variantes. No se reduce alcance ni se cierra con solo OpenCode. |
| 2026-10-11 | REC-02 | Bloqueado para cierre → Cerrado; validación complementaria separada | Coordinación / `main` `5dba871`; reporte OpenCode real, Pi, matriz oficial por host y CI | Criterios originales satisfechos: matriz y semántica por host, controles soportados aplicados, límites no soportados expresos, runtime representativo OpenCode/Pi, aprobación humana observada, integración y CI. No se afirma paridad ni enforcement en hosts no ejecutados. | Follow-up [VER-REC-02](seguimiento/VER-REC-02.md): Kiro V3 y otros runtimes, delegación/web y respuesta final tras rechazo. No es dependencia de REC-03. |
| 2026-10-11 | REC-09 a REC-17; FUT-02/04/05/08/11/14 | Pendiente → Implementación local; FUT-14 No vigente | Coordinación / `main`; canonical, adapters, tooling y configuración OpenCode local | Fragmentos compartidos, triggers acotados, aprobaciones proporcionales, carga SDD selectiva, poda Git, medición de texto por flujo y presupuestos cualitativos; pruebas focales en [registro](seguimiento/OPTIMIZACION-CONTEXTO.md). | Render de `generated/` pendiente mientras se coordinan cambios concurrentes de Navigator/contexto; tokens reales/turnos y activación multi-host quedan pendientes donde se indica. |
| 2026-10-12 | REC-03 | Pendiente → Integrado pendiente de verificación | Sesión exclusiva en `main`; HEAD `43fd2dc` y cambios locales de Developer conservados | El validador separa lectura de escritura: inspect puede citar código del proyecto sin carpetas documentales; symlinks externos se rechazan; evidencia de escritura sigue dentro del scope. `tools/test_handoff_contract.py` 37/37. | Sin commit ni CI remota todavía; smoke de host no se afirma y queda como cobertura REC-08. |
| 2026-10-12 | REC-04 | Pendiente → Integrado pendiente de verificación | Sesión exclusiva en `main`; HEAD `43fd2dc` y cambios locales de Developer conservados | Se retiró el visor/lanzador Scalar de `data-api`, se mantiene OpenAPI/JSON Schema/catálogo y se regeneraron seis plataformas; `test_integrity.py` 416/416. | Sin commit ni CI remota; preservar informes históricos y no reinstalar la opción. |
| 2026-10-12 | REC-05 | Pendiente → Integrado pendiente de verificación | Sesión exclusiva en `main`; HEAD `43fd2dc` y cambios locales de Developer conservados | Preflight renderiza fuentes a un temporal y compara rutas/hash de archivos esperados antes de copiar; postflight verifica hash del destino. Pruebas: wrappers Bash 250/250, Antigravity 22/22, retirados 26/26; PowerShell con paridad estática. | Sin commit ni CI remota; verificación nativa Windows de instaladores fuera de Antigravity sigue pendiente. |

### Cierre

Para cerrar: identificar baseline; aplicar cambio autorizado; preservar requisitos pertinentes; ejecutar la verificación de la ficha; registrar evidencia y limitaciones; integrar los cambios y verificar el resultado integrado; actualizar consumidores y distribución cuando corresponda. **Un fix aislado o tests textuales no acreditan por sí solos todos los criterios conductuales.** Si falta una verificación exigida, mantenerla explícitamente pendiente y no cerrar el hallazgo.
