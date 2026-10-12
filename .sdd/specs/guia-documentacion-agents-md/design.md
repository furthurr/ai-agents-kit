# Diseño — Guía documental gestionada en AGENTS.md

- Modo SDD: lite

## Contexto y alcance

La responsabilidad pasa al `documentation-orchestrator`, que ya coordina las operaciones de escritura y sus autorizaciones. `project-navigator` conserva su autoridad sobre `.navigator/`, pero deja de ser un segundo escritor de `AGENTS.md`. La feature afecta únicamente el bloque documental en el archivo raíz de instrucciones.

Las carpetas que describa la guía se detectan en el proyecto real. Puede documentar `.architecture/`, `.navigator/`, `.data/`, `.design/`, `.quality/`, `.security/`, `docs/` y, si están presentes, `.sdd/` o `.release/`, indicando cuando estas últimas pertenecen a otros workflows. No afirma presencia ni contenido sin comprobarlos.

## Solución acotada

1. El orquestador detecta el `AGENTS.md` raíz en el preflight de operaciones con escritura y lo incluye en el plan global aprobado. No crea ni actualiza el archivo antes de esa aprobación.
2. Tras completar las carpetas documentales aprobadas, compone una guía corta con el mapa verificado, puntos de entrada, ownership, reglas de autoridad/frescura y límites de lectura/escritura.
3. Gestiona el área delimitada por `<!-- ai-agents-kit:documentation:start -->` y `<!-- ai-agents-kit:documentation:end -->`:
   - archivo ausente: crea el archivo con un único bloque;
   - archivo existente sin marcadores: añade el bloque sin sustituir el contenido existente;
   - un par válido: reemplaza solo el interior;
   - contenido generado igual: no escribe;
   - marcadores parciales/duplicados o conflicto semántico: bloquea la escritura y pide decisión.
4. Las operaciones `inspect`, `status` y `release-check` siguen siendo de solo lectura. La instalación del kit no modifica instrucciones del proyecto.
5. Navigator deja de exportar directamente a `AGENTS.md`; su bootstrap/update se limita a `.navigator/**` y deriva la guía al orquestador. Cualquier ajuste existente `sources.export_agents_md` se trata como legado inerte: no se elimina ni reescribe configuración del proyecto consumidor.

## Errores y límites

- Los delimitadores no se normalizan ni reparan automáticamente si están incompletos o repetidos.
- Si el `AGENTS.md` raíz es symlink, no regular o ilegible, no seguir ni modificar el destino; reportar el bloqueo.
- La guía no duplica README largos ni especificaciones; apunta a los puntos de entrada reales.
- Instrucciones manuales contradictorias no se resuelven por precedencia inventada: se informa el conflicto y no se escribe el bloque.
- Las pruebas contractuales comprueban que las instrucciones incluyan estas reglas, pero no prueban el comportamiento runtime del LLM.

## Estrategia de pruebas

- Nivel: TDD focalizado para el contrato observable del orquestador y Navigator.
- RED: ampliar `tools/test_documentation_core.py` con las cláusulas exigidas para aprobación, marcadores, preservación, no-op, conflicto, solo lectura y propiedad única; comprobar el fallo antes de cambiar las fuentes canónicas.
- GREEN: actualizar las instrucciones canónicas con el contrato mínimo; comprobar tests focalizados, renderer, paridad generada y enlaces.
- Smoke conversacional de un host real: no disponible en esta ejecución; documentar como limitación, sin afirmar obediencia del LLM.
- PBT: no aplica; no se implementa una transformación de datos ejecutable ni una propiedad algebraica.
