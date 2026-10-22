# Propuestas de herramientas futuras

> **Estado:** documento de planificación. Las propuestas de este archivo no están aprobadas para implementación y no describen herramientas disponibles en el MAS.
>
> **Actualizado:** 2026-10-14.

## Propósito de esta carpeta

`docs/tools/` conserva propuestas de herramientas que podrían complementar al MAS en tareas concretas o poco frecuentes. Su finalidad es dejar el problema, el alcance, los riesgos y los criterios de decisión suficientemente claros para poder retomarlos sin volver a descubrir el contexto.

Esta carpeta contiene **planes**, no código ejecutable, instaladores, integraciones activas ni promesas de compatibilidad. Una propuesta solo pasa a implementación después de una decisión explícita y de definir su trabajo técnico.

### Diferencia con `tools/`

El directorio raíz `tools/` contiene scripts y pruebas reales del repositorio, por ejemplo el renderer y el validador. `docs/tools/` es exclusivamente documental. No crear un directorio raíz `TOOLS/`: además de duplicar el propósito de `tools/`, la diferencia de mayúsculas puede causar colisiones en sistemas de archivos habituales de macOS y Windows.

## Criterios para aceptar una propuesta

Antes de convertir una propuesta en implementación, responder y documentar:

1. **Problema concreto:** qué tarea difícil, repetitiva o propensa a error resuelve y quién la necesita.
2. **Evidencia de utilidad:** frecuencia observada, costo actual o impacto de no resolverla. No basta con que la herramienta sea técnicamente posible.
3. **No duplicación:** qué cubren ya las skills, los agentes, las carpetas canónicas y las herramientas de `tools/`.
4. **Alcance tecnológico explícito:** qué aspectos son comunes y cuáles necesitan adaptadores por lenguaje, framework, host o plataforma.
5. **Proporcionalidad:** que el beneficio esperado justifique instalación, configuración, permisos y mantenimiento.
6. **Seguridad y privacidad:** archivos leídos/escritos, información que podría aparecer en resultados, acceso a red, ejecución de comandos y confirmaciones necesarias.
7. **Resultado verificable:** salida comprensible, evidencia rastreable y criterios para medir si la herramienta funcionó.
8. **Modo opcional:** no debe activarse para proyectos o tareas a los que no aplica ni convertirse en un paso obligatorio del MAS sin justificación.

Si la propuesta no tiene un usuario/caso identificable, duplica una skill existente o exige mantener una matriz de soporte desproporcionada, se conserva como idea diferida o se descarta.

## Estado de las propuestas

| ID | Propuesta | Cuándo tendría sentido | Situación frente al MAS | Estado |
|---|---|---|---|---|
| TOOL-001 | Generador de contexto inicial para proyectos | Un equipo necesita preparar instrucciones y contexto de IA en repositorios sin documentación adecuada. | Alto solapamiento con `project-navigator` y `documentation-orchestrator`; primero hay que demostrar qué automatización adicional hace falta. | Candidata; definición pendiente |
| TOOL-002 | Ejecutor de auditorías de dependencias | Se necesita ejecutar varios escáneres existentes y presentar resultados homogéneos para distintos ecosistemas. | La skill `security` ya define auditorías y el registro de dependencias; la posible aportación sería automatizar la ejecución y normalización. | Candidata; definición pendiente |
| TOOL-003 | Auditor de responsividad de interfaces | Un proyecto con UI necesita revisar de forma repetible su comportamiento en distintos tamaños de pantalla o dispositivos. | `.design/` ya cubre documentación visual; un auditor sería condicional a UI y requeriría métodos distintos según plataforma. | Candidata; definición pendiente |

Los IDs son referencias estables para discusión. No indican orden de prioridad ni autorización para construir.

---

## TOOL-001 — Generador de contexto inicial para proyectos

### Resumen

**Problema que se quiere investigar:** en un repositorio nuevo para el MAS, el equipo puede carecer de contexto útil para que un asistente entienda cómo verificar cambios, dónde están las responsabilidades principales y qué instrucciones existentes debe respetar.

**Resultado hipotético:** un informe de descubrimiento y, solo si se autoriza, una propuesta de contexto neutral del proyecto que apunte a fuentes verificables. El generador no debería crear una segunda fuente de verdad ni regenerar automáticamente la documentación de dominios que ya mantienen las skills del MAS.

### Casos de uso posibles

- Preparar el contexto de IA para un repositorio que no tiene instrucciones de proyecto.
- Identificar instrucciones existentes de asistentes y evitar reemplazarlas.
- Presentar stack, puntos de entrada, comandos de verificación detectados y módulos principales con referencias a sus fuentes.
- Orientar al usuario sobre qué documentación existente del MAS conviene inicializar, en lugar de producir una copia paralela.

### Cuándo no usarlo

- Para una consulta puntual de arquitectura o de ubicación de código: usar `documentation-orchestrator` en modo `inspect`.
- Para inicializar o actualizar índices de navegación: usar `project-navigator` mediante los flujos documentados.
- Para documentar arquitectura, datos/API, diseño, calidad o seguridad: usar la skill especializada correspondiente.
- Para modificar instrucciones existentes sin revisar su autoría, propiedad y contenido manual.

### Alcance que debería explorarse

**Posible entrada:** ruta raíz o subproyecto objetivo, instrucciones existentes, documentación y manifiestos presentes. La ruta del proyecto y la selección de subproyecto deben quedar claras antes de cualquier escritura.

**Descubrimiento de solo lectura:**

- Detectar proyectos y subproyectos a partir de evidencia encontrada, sin asumir que un monorepo es una única aplicación.
- Inventariar instrucciones para asistentes y documentación contextual existentes.
- Leer manifiestos, configuraciones y scripts existentes para proponer comandos; no inventarlos.
- Identificar puntos de entrada, módulos y fuentes documentales pertinentes con rutas verificables.
- Marcar como desconocido todo lo que no se pueda confirmar.

**Posible salida:** primero un informe revisable. Si el usuario aprueba una operación documental, producir o actualizar únicamente los artefactos elegidos y conservar el contenido preexistente no gestionado por el MAS.

### Límites y protecciones

- No modificar código de producto, pruebas, CI, dependencias ni lockfiles.
- No sobrescribir `AGENTS.md`, `CLAUDE.md`, steering u otras instrucciones personalizadas.
- No declarar que un comando existe sin haber encontrado su fuente.
- No ejecutar build, tests, scripts ni escáneres como efecto implícito del descubrimiento. La ejecución de verificaciones requeriría un alcance y una autorización adecuados.
- No emitir archivos específicos de un host por defecto. El contenido común debe ser neutral; cualquier adaptador por plataforma tendría que ser una decisión aparte.
- No duplicar `.navigator/`, `.architecture/`, `.data/`, `.design/`, `.quality/` o `.security/`.

### Relación con el MAS y pregunta de diseño pendiente

Esta idea es la que más se aproxima al propósito de AI Harness Kit, pero también es la que más se solapa con el MAS actual. Antes de diseñarla se debe comparar, caso por caso, contra:

- [`project-navigator`](../../canonical/skills/project-navigator/SKILL.md): mapa de módulos, símbolos y navegación selectiva.
- [`documentation-orchestrator`](../../canonical/skills/documentation-orchestrator/SKILL.md): estado, bootstrap y sincronización documental con aprobación.
- [`architecture`](../../canonical/skills/architecture/SKILL.md): descubrimiento y documentación arquitectónica.
- [`developer`](../../canonical/skills/developer/SKILL.md): contexto y verificaciones durante una implementación.

**Decisión abierta principal:** ¿existe un paso repetible de análisis/generación que esas skills no cubren y que justifique una herramienta independiente? Si la respuesta es no, no construirla; mejorar el flujo existente solo si se identifica una carencia concreta.

### Criterios mínimos para reconsiderar implementación

- Hay solicitudes repetidas de preparar contexto inicial que actualmente requieren trabajo manual sustancial.
- Se define una salida que no duplique las carpetas ni la autoridad documental existente.
- El descubrimiento produce referencias comprobables y trata instrucciones previas como contenido que debe preservarse.
- Un dry-run sobre repositorios de al menos dos estructuras tecnológicas distintas puede informar sin escribir ni ejecutar comandos de producto.
- La generación, si se aprueba, muestra el plan y el diff antes de escribir y permite omitir cualquier artefacto.

---

## TOOL-002 — Ejecutor de auditorías de dependencias

### Resumen

**Problema que se quiere investigar:** los escáneres de dependencias y sus formatos de salida varían por ecosistema. Puede ser útil una capa opcional que detecte qué escáneres ya están disponibles, ejecute los apropiados bajo autorización y reúna hallazgos comparables.

**Resultado hipotético:** un reporte reproducible de los manifiestos inspeccionados, herramientas y versiones utilizadas, alcance cubierto, hallazgos y limitaciones. No sería un sistema de remediación automática.

### Casos de uso posibles

- Un usuario solicita explícitamente una auditoría de dependencias.
- Un repositorio contiene varios ecosistemas y se necesita identificar qué partes se pudieron escanear.
- Se requiere conservar evidencia de la fecha, el alcance y el resultado de una auditoría autorizada.

### Cuándo no usarlo

- Durante cada implementación ordinaria o por el mero hecho de detectar un manifiesto.
- Para reemplazar las auditorías manuales de seguridad o declarar que un proyecto completo está seguro.
- Para corregir versiones o regenerar lockfiles.
- Si no se conoce el alcance, no está disponible una herramienta apropiada o la ejecución requiere una acción no autorizada.

### Alcance que debería explorarse

**Detección:** reconocer manifiestos y lockfiles presentes, resolver directorios de monorepo y agrupar resultados por subproyecto. Mantener una matriz explícita de ecosistemas soportados; cualquier tecnología fuera de ella debe quedar como no cubierta, no como aprobada.

**Selección de escáner:** priorizar comandos ya disponibles en el entorno o herramientas ya adoptadas por el proyecto. No instalar paquetes ni plugins automáticamente. Si una comprobación consulta servicios externos o bases de datos, indicarlo antes y obtener autorización para esa ejecución.

**Normalización posible:** registrar ecosistema, subproyecto, manifiestos/lockfiles examinados, herramienta y versión, fecha, estado de ejecución, vulnerabilidad/aviso, paquete y versión afectados, severidad según la fuente, referencia externa, y limitaciones del análisis.

**Destino posible:** entregar un informe de solo lectura. Si el usuario pide persistirlo, actualizar el dominio `.security/` mediante su procedimiento aprobado; no crear un tablero alternativo.

### Límites y protecciones

- Solo diagnóstico. No instalar, actualizar, eliminar ni fijar dependencias.
- No modificar manifiestos ni lockfiles.
- No ejecutar código descargado o scripts de instalación como parte de la auditoría.
- Tratar el acceso a red como una decisión explícita; ofrecer resultado limitado/offline cuando sea posible.
- Diferenciar claramente `sin vulnerabilidades detectadas`, `escaneo parcial`, `herramienta no disponible`, `error de escaneo` y `no ejecutado`.
- No afirmar cobertura total ni ausencia universal de vulnerabilidades.
- No registrar secretos, credenciales, rutas personales ni contenido sensible en reportes.
- Mantener la remediación dentro del flujo autorizado de la skill `security`.

### Relación con el MAS y pregunta de diseño pendiente

La skill [`security`](../../canonical/skills/security/SKILL.md) ya cubre auditoría y documentación de vulnerabilidades de dependencias en `.security/dependencies.md`. La herramienta propuesta solo se justificaría si la ejecución repetida y la normalización de resultados son una necesidad real no resuelta por ese procedimiento.

**Decisiones abiertas:**

- ¿Se requiere un ejecutor nuevo o basta con documentar cómo invocar los escáneres existentes bajo demanda?
- ¿Qué ecosistemas tienen demanda suficiente para soporte inicial?
- ¿Conviene producir Markdown únicamente, un formato de intercambio además de Markdown, o ambos?
- ¿Cómo distinguir resultados de fuentes distintas sin ocultar sus niveles de severidad originales?

### Criterios mínimos para reconsiderar implementación

- La auditoría de dependencias se solicita de forma recurrente en repositorios con más de un ecosistema o escáner.
- La matriz inicial de soporte se limita a ecosistemas efectivamente usados; cada uno tiene fixtures seguros.
- Las pruebas confirman que ninguna ejecución modifica manifiestos, lockfiles o el árbol de trabajo.
- Las ejecuciones offline, parciales, fallidas y con avisos quedan diferenciadas en la salida.
- El usuario puede revisar el comando, el alcance y cualquier uso de red antes de ejecutar.
- El reporte puede incorporarse al flujo `.security/` sin crear una fuente de verdad paralela.

---

## TOOL-003 — Auditor de responsividad de interfaces

### Resumen

**Problema que se quiere investigar:** una interfaz puede funcionar en el dispositivo o tamaño de pantalla habitual y fallar en otros: desbordamiento, controles difíciles de usar, contenido oculto o composiciones que no se adaptan.

**Resultado hipotético:** un conjunto acotado de hallazgos reproducibles para una interfaz y una matriz declarada de tamaños/dispositivos. El reporte no equivaldría a certificar toda la accesibilidad o calidad visual del producto.

### Casos de uso posibles

- El usuario solicita una auditoría de una interfaz existente.
- Se necesita comprobar una pantalla o flujo antes de una release.
- El equipo reporta un defecto reproducible que aparece solo en cierto tamaño, orientación o dispositivo.

### Cuándo no usarlo

- En proyectos sin interfaz visual.
- En tareas de backend, datos o scripts que no alteren una UI.
- Para cada cambio visual pequeño si los checks existentes cubren el riesgo.
- Para sustituir pruebas funcionales, validación de accesibilidad o pruebas de usuarios.

### Alcance que debería explorarse

La revisión puede considerar, según la plataforma y con evidencia disponible:

- Desbordamiento o contenido recortado en los tamaños seleccionados.
- Adaptación de layout, contenido y navegación entre tamaños/orientaciones.
- Uso de unidades o restricciones rígidas que impidan la adaptación.
- Tamaño y separación de controles interactivos cuando la plataforma permita medirlos.
- Viewport y recursos visuales adaptativos en proyectos web.
- Diferencias de densidad, escala de texto o área segura en interfaces nativas, si pueden observarse con herramientas ya disponibles.

El método de comprobación queda pendiente de diseño: análisis estático, ejecución de la aplicación, captura de pantalla, inspección manual guiada o combinación. No asumir que un solo método funciona para web, Android, iOS, Flutter y otras interfaces.

**Entrada posible:** pantalla/flujo objetivo, plataforma, tamaños u orientaciones solicitados y, si hay ejecución, datos de prueba no sensibles y un entorno autorizado.

**Salida posible:** hallazgos priorizados con pantalla/tamaño reproducible, evidencia, fuente o componente implicado cuando sea localizable y sugerencia de corrección. Persistirlos en `.design/` solo si el usuario solicita documentación y aprueba el alcance.

### Límites y protecciones

- Activación optativa y solo cuando se detecte o solicite una interfaz.
- No lanzar emuladores, navegadores, servidores ni comandos del proyecto sin verificar el comando y el alcance de ejecución.
- No instalar dependencias ni modificar código de UI.
- No usar cuentas o datos productivos; proteger capturas y artefactos que puedan contener PII.
- Distinguir observaciones estáticas de resultados observados durante ejecución.
- Indicar tamaños, dispositivos, versiones y áreas que no se probaron.
- No declarar conformidad completa con WCAG u otro estándar a partir de una muestra parcial.
- No fijar requisitos exclusivos de web como si aplicaran a interfaces móviles nativas.

### Relación con el MAS y pregunta de diseño pendiente

La skill [`ui-design`](../../canonical/skills/ui-design/SKILL.md) documenta sistemas visuales y deuda de UI de forma agnóstica a tecnología. Developer ya contempla los riesgos responsive pertinentes a una implementación. El auditor propuesto tendría que aportar una verificación repetible de escenarios/tamaños, no duplicar el catálogo visual ni convertirse en un chequeo permanente para todos los repositorios.

**Decisiones abiertas:**

- ¿Se necesita un script/herramienta ejecutable o basta un protocolo de auditoría dentro de `ui-design`?
- ¿Qué plataforma tiene evidencia y demanda suficientes para una primera versión?
- ¿Qué tamaños/dispositivos deben ser configurables y quién mantiene esa matriz?
- ¿Qué puede probarse de forma determinista sin instalar herramientas adicionales?
- ¿Cómo se controlan y retienen capturas que pudieran contener información sensible?

### Criterios mínimos para reconsiderar implementación

- Hay solicitudes repetidas de auditorías responsive con escenarios reproducibles.
- El alcance inicial se limita a una plataforma/interfaz validada y define cómo ampliar cobertura sin anunciar soporte no comprobado.
- Los hallazgos tienen evidencia que otra persona puede reproducir en el mismo entorno.
- Las pruebas de la herramienta no requieren datos productivos ni cambios en el proyecto auditado.
- El resultado complementa `.design/` y las pruebas existentes, y declara sus límites de cobertura.

---

## Cómo retomar una propuesta

Para convertir cualquiera de estas entradas en trabajo activo:

1. Confirmar el problema y recopilar ejemplos de uso real.
2. Revisar de nuevo las skills, scripts y backlog vigentes para detectar cambios o solapamientos nuevos.
3. Resolver las preguntas abiertas de la ficha y acordar alcance, exclusiones, plataformas y propietario de mantenimiento.
4. Definir criterios de aceptación verificables, tratamiento de errores, permisos, datos y dependencias.
5. Si se aprueba la construcción, planificarla con el flujo de desarrollo/SDD adecuado y preparar pruebas proporcionadas al riesgo.
6. Implementar en `tools/` únicamente si el resultado realmente necesita código; mantener la documentación de decisión aquí.
7. Actualizar esta ficha con el estado, la evidencia y los límites reales; no marcar soporte por la mera existencia de un prototipo.

## Registro de decisiones

| Fecha | ID | Decisión | Evidencia / responsable |
|---|---|---|---|
| 2026-10-14 | TOOL-001–003 | Incorporadas como propuestas para evaluación futura; no aprobadas para implementación. | Comparación documental con AI Harness Kit y las skills actuales del MAS. |
