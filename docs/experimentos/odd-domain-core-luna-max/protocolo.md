# Skills núcleo + referencias — una tarea y una pareja exploratoria

ID odd-domain-core-luna-max-v1. Control: ODD ajustado con estándares + data-api y
ui-design completas. Tratamiento: MISMO agente/skill ODD ajustado + esas mismas
skills de dominio descompuestas en núcleo breve y referencias bajo demanda.
No se usa ODD+navegación selectiva ni se añaden mapas al baseline.

Modelo `openai/gpt-6-luna`, CLI `--variant max`, timeout1800s y steps60 configurados
iguales. TASK-2 Alta literal, mismo LocalLibrary documentado, nueve oráculos externos
y43 pruebas originales restauradas. Una ejecución nueva por brazo, dos simultáneas.

## Partición sin eliminar estándares

No modificar skills canónicas/instaladas. En el perfil experimental tratado:
- Mantener frontmatter/nombre de cada skill y sus referencias existentes.
- Sustituir cuerpo SKILL por nucleo.md, que exige leer implementation.md ANTES de
  trabajar el dominio. No basta con cargar una skill vacía o resumida.
- implementation.md conserva literalmente las secciones pertinentes del original:
  identidad/límites, aplicabilidad/intención, estándares, fuentes tecnológicas,
  uso de implementación, índice contextual y reglas. UI incluye el checklist visual.
- documentation.md conserva las secciones complementarias de estructuras, modos,
  bootstrap/sincronización y plantillas. No cargarla por rutina en implementación.
- original-contract.md conserva el archivo original íntegro, byte a byte, con
  enlaces relativos válidos. Usarlo si hay dudas, sin prohibirlo para ganar el test.
- Todas las secciones originales se asignan y trazan por encabezado/hash. Se puede
  reconstruir el original sin omitir ni reescribir reglas. No afirmar equivalencia
  semántica perfecta: cambia la entrega del contexto y el modelo puede interpretar distinto.

Ambos reciben mismos requisitos, código y documentación. No añadir instrucciones
específicas de reservas/SQLite ni soluciones al núcleo. Separar los flujos no implica
que la documentación de producto no importe ni se omita su detección al cierre.

## Verificación y análisis

Preflight real por ambos perfiles: prompt resuelto, carga primaria, edición y unittest;
referencia43+9 y pruebas offline de partición/composición/configuración. Congelar
fuentes, perfiles, corpus y oráculos antes de las dos celdas. No retocar tras ver datos.
Preservar errores/timeouts y snapshots; sin retry selectivo ni feedback de oráculos.

Evaluar funcionalidad y por separado: carga íntegra de cores, lectura de ambas
referencias técnicas por contenido y antes del primer cambio de producto (o fallback
al contrato íntegro), reglas omitidas, consumidores, consultas documentales, flujo
documental innecesario, seguimiento, herramientas, pasos, tokens, bytes y tiempo.
Leer referencias no certifica aplicar exhaustivamente cada estándar. Si no se leen
los criterios, no aceptar menor consumo como mejora aunque pasen oráculos.

Señal favorable exploratoria: ambos funcionales, criterios técnicos consultados,
sin bootstrap/artefactos ajenos, ahorro tokens>=10% y tiempo no peor en más de10%.
Una pareja no prueba causalidad ni generalización. Informar fallback/documentación
leída sin seleccionarlos fuera del coste. La comparación es nueva, no mezclar con
ODD original sin estándares, pruebas de navegación o cohortes previas.

Tokens=input+cache_read+cache_write+output, reasoning aparte. Bytes no son tokens
estimados; no calcular factura del coste host. Conversación sumada no es wall-clock;
preparación/preflights/checks externos fuera. Permisos no son sandbox OS. Sin instalar,
modificar fuentes canónicas o plan del Escritorio, commits, publicación ni subagentes.
