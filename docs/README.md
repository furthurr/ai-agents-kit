# Documentación — AI Agents Kit

Índice de la documentación del kit. El [README raíz](../README.md) es la puerta
de entrada; aquí está el detalle por tema.

| Documento | Para quién | Contenido |
|-----------|------------|-----------|
| [vision.md](vision.md) | Todos | Qué es el kit, problema que resuelve y modelo mental |
| [mas.md](mas.md) | Todos | Identidad de MAS y convención para dirigir mensajes |
| [catalogo.md](catalogo.md) | Usuarios | Skills, agentes y carpetas canónicas |
| [agentes/README.md](agentes/README.md) | Usuarios y contribuidores | Qué hace cada agente, qué skill utiliza y cómo invocarlo |
| [agentes/developer.md](agentes/developer.md) | Usuarios | Ejecución proporcional, verificación, continuidad bajo demanda y cierre documental de Developer |
| [developer-smoke.md](developer-smoke.md) | Usuarios y contribuidores | Escenarios manuales de consulta/PLAN, implementación, refuerzos A/B y aislamiento SDD |
| [instalacion.md](instalacion.md) | Usuarios | Render, validación e instalación por plataforma |
| [extra-tools/modo-autonomo.md](extra-tools/modo-autonomo.md) | Usuarios | Contrato del modo autónomo por host, límites y cómo aplicarlo |
| [extra-tools/prompt-actualizacion-mas-autonomia.md](extra-tools/prompt-actualizacion-mas-autonomia.md) | Usuarios | Prompt listo para copiar: actualizar MAS en las seis plataformas y activar el modo autónomo |
| [compatibilidad-hosts.md](compatibilidad-hosts.md) | Usuarios y contribuidores | Versiones mínimas/validadas, formatos y comportamiento con hosts antiguos |
| [migracion-agentes.md](migracion-agentes.md) | Usuarios y contribuidores | Retirada opt-in, revisión por archivo, respaldo obligatorio, recuperación y smoke pendiente |
| [uso.md](uso.md) | Usuarios | Cómo invocar especialistas y cuándo usar cada uno |
| [navigator-smoke.md](navigator-smoke.md) | Usuarios y contribuidores | Smoke test reproducible del Project Navigator |
| [documentation-orchestrator-smoke.md](documentation-orchestrator-smoke.md) | Usuarios y contribuidores | Smoke test de modos, gates y límites del orquestador |
| [model-recommendations-smoke.md](model-recommendations-smoke.md) | Usuarios y contribuidores | Smoke test histórico y criterios actuales: sin recomendaciones LLM |
| [code-review-smoke.md](code-review-smoke.md) | Usuarios y contribuidores | Revisión de calidad/seguridad, documentación y handoffs acotados |
| [sdd-smoke.md](sdd-smoke.md) | Usuarios y contribuidores | Smoke test de alcance completo, continuidad, gates y testing adaptativo |
| [sdd-effort-examples.md](sdd-effort-examples.md) | Usuarios y contribuidores | Ejemplos de esfuerzo previsto, atención especial y profundidad elegible |
| [desarrollo.md](desarrollo.md) | Contribuidores | Editar `canonical/`, `adapters/` y flujo de trabajo |
| [arquitectura-del-kit.md](arquitectura-del-kit.md) | Contribuidores | Pipeline de render y herramientas |
| [mejoras.md](mejoras.md) | Contribuidores | Backlog priorizado (impacto → esfuerzo) para subir calidad del kit |
| [Índice de experimentos del MAS](experimentos/README.md) | Contribuidores | Catálogo completo de benchmarks, comparativas y resultados empíricos |
| [Continuar experimentos en otra sesión](experimentos/README.md) | Contribuidores | Contexto al día, decisiones pendientes, resultados consolidados y evidencia |
| [ODD con estándares — Gemini 3.8 Flash](experimentos/archive/odd-estandares-gemini-38-v3-2026-11-08/README.md) | Contribuidores | Benchmark de ODD con `data-api`/`ui-design`, balanceo R1+R2 y análisis arquitectónico |
| [Proyecto Real Android CRM — Gemini 3.8](experimentos/real-android-gemini-2026-11-08/README.md) | Contribuidores | Benchmark en proyecto Android real (15 celdas): Developer v1 vs v2 vs v2 reforzado vs Build |
| [Developer vs SDD vs ODD — Gemini](experimentos/archive/developer-sdd-odd-gemini-2026-11-04/README.md) | Contribuidores | Experimento independiente de tres flujos con Gemini: profundidad natural, calidad, herramientas, velocidad y tokens |
| [Developer actual vs compacto — Gemini](experimentos/archive/developer-compacto-gemini-2026-11-04/README.md) | Contribuidores | Prueba del prompt compacto con skill idéntica, control vigente y ODD de referencia |
| [Experimento Ponytail — 2026-11-04](experimentos/archive/ponytail-2026-11-04/README.md) | Contribuidores | Evidencia A/B, protocolo, resultados y decisión de conservar el MAS actual |
| [Experimento ODD vs SDD — 2026-11-04](experimentos/archive/odd-vs-sdd-2026-11-04/README.md) | Contribuidores | Registro histórico: evidencia GPT, suplemento, rectificación de Gemini y límites |
