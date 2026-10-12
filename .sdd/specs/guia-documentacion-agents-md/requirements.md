# Requisitos — Guía documental gestionada en AGENTS.md

- Modo SDD: lite
- Trabajo: feature
- Intención: implementación

## Calificación de feature

- Esfuerzo previsto del LLM: 4 🟠
- Referente del laboratorio: F04
- Justificación: El cambio coordina el contrato de escritura entre el orquestador y Navigator y debe preservar contenido manual con comportamiento idempotente. Reutiliza los gates, renderer y pruebas contractuales existentes; no introduce servicio, parser, almacenamiento o migración.
- Supuestos relevantes: La escritura en proyectos consumidores la ejecutan las instrucciones del orquestador dentro del plan documental aprobado; los checks del kit validan el contrato estático, no garantizan por sí solos la conducta runtime de un LLM.
- Alcance evaluado: Crear o mantener un bloque delimitado de guía portable en el AGENTS.md raíz durante operaciones autorizadas de escritura documental; retirar la exportación directa competidora de Navigator.
- Atención: reforzada; preservar el contenido externo del usuario y detenerse ante delimitadores ambiguos o conflictos.
- Profundidad recomendada / seleccionada: lite
- Entrega: primera entrega limitada a AGENTS.md raíz; detección y referencias en archivos de instrucciones de otros hosts quedan fuera.

## Historia 1: Orientar a cualquier asistente sobre la documentación del proyecto

Como equipo del proyecto, queremos una guía portable en `AGENTS.md` para que una IA sin el MAS entienda qué documentación existe, cómo consultarla y cómo mantenerla.

### Criterios (EARS)

- Req 1.1: CUANDO una operación de documentación autorizada cree o actualice documentación EL SISTEMA DEBERÁ incluir en el plan global la creación o actualización del bloque documental de `AGENTS.md` raíz.
- Req 1.2: CUANDO se apruebe una operación de escritura y no exista `AGENTS.md` raíz EL SISTEMA DEBERÁ crear el archivo con una guía breve basada solo en estructura y documentación verificadas del proyecto.
- Req 1.3: CUANDO `AGENTS.md` exista sin bloque gestionado EL SISTEMA DEBERÁ añadir un único bloque delimitado y preservar el contenido preexistente.
- Req 1.4: CUANDO `AGENTS.md` contenga exactamente un par de delimitadores gestionados EL SISTEMA DEBERÁ actualizar solo el contenido entre ellos y preservar todo el texto exterior.
- Req 1.5: CUANDO una actualización no cambie el contenido de la guía EL SISTEMA DEBERÁ dejar `AGENTS.md` sin cambios.
- Req 1.6: SI `AGENTS.md` contiene delimitadores ausentes, duplicados o mal formados, o instrucciones incompatibles con la guía, ENTONCES EL SISTEMA DEBERÁ detener esa escritura, informar el conflicto y solicitar una decisión sin sobrescribir el archivo.
- Req 1.7: SI `AGENTS.md` es un enlace simbólico, no es un archivo regular o no se puede leer, ENTONCES EL SISTEMA DEBERÁ detener la escritura sin seguir el enlace ni sobrescribir el destino.
- Req 1.8: CUANDO se genere la guía EL SISTEMA DEBERÁ describir solo carpetas documentales verificadas, su propósito, su punto de entrada y su responsable; deberá distinguir fuentes de verdad de índices auxiliares y explicar cómo trabajar con la documentación sin depender del MAS.
- Req 1.9: CUANDO se ejecute `inspect`, `status` o `release-check` EL SISTEMA DEBERÁ mantener esas operaciones en solo lectura y no crear ni actualizar `AGENTS.md`.
- Req 1.10: CUANDO Navigator inicialice o actualice `.navigator/` EL SISTEMA DEBERÁ abstenerse de exportar o sobrescribir `AGENTS.md` directamente y remitir esa responsabilidad al orquestador documental.

## Exclusiones

- No detectar, crear ni actualizar `CLAUDE.md`, `GEMINI.md`, Copilot u otros archivos de instrucciones de host.
- No instalar el kit en proyectos externos ni ejecutar su workflow documental durante la implementación de esta feature.
- No cambiar el formato ni la disponibilidad de `.navigator/` o de otras carpetas documentales.
- No afirmar que los checks estáticos prueban la obediencia runtime del LLM.
