# Requisitos: soporte de Google Antigravity

- **Tipo de trabajo:** feature (precedida por exploración de factibilidad).
- **Modo SDD:** standard
- **Fase:** Requirements
- **Estado:** aprobado
- **Gate:** Gate 1 — aprobado por el usuario mediante «procede» tras la presentación de requisitos
- **Intención autorizada:** solo planificación; no implementar sin autorización posterior.
- **Fecha:** 2026-10-05

## Objetivo y por qué

Incorporar Google Antigravity como sexta distribución del kit MAS para reutilizar
sus especialistas y procedimientos sin duplicar las fuentes canónicas. La primera
entrega apunta a **Antigravity 2.0**, con instalación global de los ocho agentes y
las diez skills del inventario actual. No promete compatibilidad universal con el
CLI ni con el IDE standalone.

## Historias de usuario

- **HU1:** Como usuario de Antigravity 2.0, quiero instalar los agentes y skills
  del kit para usar los mismos procedimientos disponibles en las otras plataformas.
- **HU2:** Como usuario con personalizaciones locales, quiero anticipar las
  operaciones y respaldar los elementos sobrescritos para conservar mi contenido.
- **HU3:** Como mantenedor, quiero generar, validar y probar la nueva distribución
  desde las fuentes comunes para evitar divergencias y regresiones.
- **HU4:** Como usuario, quiero conocer los mecanismos de invocación y límites
  comprobados para no confundir archivos instalados con soporte efectivo del host.

## Requisitos funcionales y criterios EARS

Cada criterio tiene un identificador estable para su trazabilidad posterior.

### R1 — Inventario de plataforma (HU1, HU3)

- **R1.1:** EL SISTEMA DEBERÁ reconocer `antigravity` como plataforma adicional
  conservando las cinco plataformas existentes en el manifiesto.
- **R1.2:** CUANDO se genere la distribución Antigravity EL SISTEMA DEBERÁ
  incluir cada agente y cada skill declarados en el manifiesto canónico.

El inventario actual contiene los agentes `architecture`, `code-review`,
`data-api`, `documentation-orchestrator`, `git-release-manager`,
`project-navigator`, `sdd` y `ui-design`, y las diez skills de
`canonical/manifest.json`. El manifiesto sigue siendo la fuente del inventario.

### R2 — Skills y recursos (HU1, HU3)

- **R2.1:** CUANDO se genere una skill para Antigravity EL SISTEMA DEBERÁ
  producir su directorio con `SKILL.md` y todos sus recursos canónicos asociados.
- **R2.2:** EL SISTEMA DEBERÁ conservar los campos `name` y `description` del
  frontmatter canónico de las skills.
- **R2.3:** SI queda un token de adaptación sin resolver ENTONCES EL SISTEMA
  DEBERÁ rechazar la validación de la distribución.

### R3 — Agentes personalizados nativos (HU1)

- **R3.1:** CUANDO se genere un agente para Antigravity EL SISTEMA DEBERÁ
  producir un archivo `<id>.md` con su cuerpo canónico adaptado y frontmatter YAML.
- **R3.2:** EL SISTEMA DEBERÁ incluir en cada agente los campos `name`,
  `description`, `model`, `subagent`, `mainAgent` y `tools` conforme al esquema
  documentado del host.
- **R3.3:** EL SISTEMA DEBERÁ configurar los ocho agentes con `mainAgent: true`
  para permitir su selección como principales.
- **R3.4:** EL SISTEMA DEBERÁ configurar los ocho agentes con `subagent: true`
  para permitir su invocación como subagentes.
- **R3.5:** EL SISTEMA DEBERÁ usar `model: inherit` como configuración inicial
  de los ocho agentes sin convertir las recomendaciones de nivel LLM del kit en
  cambios automáticos del modelo del host.
- **R3.6:** EL SISTEMA DEBERÁ conservar en la descripción de SDD los términos
  `direct`, `lite`, `standard` y `Quick Plan`, excluyendo los términos `deep` y
  `estricto` de dicha descripción conforme al contrato solicitado.

### R4 — Herramientas y adaptación del host (HU1, HU4)

- **R4.1:** EL SISTEMA DEBERÁ declarar únicamente herramientas cuyos nombres
  estén respaldados por evidencia de la versión objetivo de Antigravity.
- **R4.2:** EL SISTEMA DEBERÁ asignar herramientas por rol coherentes con las
  responsabilidades y prohibiciones del agente canónico.
- **R4.3:** SI un adapter contiene un modelo, tipo de campo o herramienta no
  admitidos por el contrato verificado ENTONCES EL SISTEMA DEBERÁ rechazar su
  validación con un diagnóstico que identifique el agente y el campo.
- **R4.4:** EL SISTEMA DEBERÁ adaptar las referencias a SDD sin presentar
  `@sdd` como una invocación nativa mientras no exista evidencia que la acredite.
- **R4.5:** EL SISTEMA DEBERÁ identificar `GEMINI.md`, `AGENTS.md` y
  `.agents/rules/*.md` como fuentes de steering soportadas, sin crear ni
  sobrescribir reglas globales del usuario durante la instalación.

Las prohibiciones de los prompts y una lista de tools no constituyen por sí
solas aislamiento de permisos por carpeta o comando. No se añade delegación
automática: se conserva el protocolo de handoff canónico.

### R5 — Instalación global multiplataforma (HU1, HU2)

- **R5.1:** CUANDO se ejecute la instalación para Antigravity EL SISTEMA DEBERÁ
  instalar las skills en `~/.gemini/config/skills/<id>/`.
- **R5.2:** CUANDO se ejecute la instalación para Antigravity EL SISTEMA DEBERÁ
  instalar los agentes en `~/.gemini/config/agents/<id>.md`.
- **R5.3:** EL SISTEMA DEBERÁ ofrecer instaladores Bash para macOS/Linux y
  PowerShell para Windows con opciones equivalentes de simulación y omisión del
  backup (`--dry-run`/`-DryRun` y `--force`/`-Force`, según la convención del kit).
- **R5.4:** SI el preflight detecta un artefacto declarado ausente en las fuentes
  de instalación ENTONCES EL SISTEMA DEBERÁ finalizar con código distinto de cero
  antes de copiar artefactos al destino.
- **R5.5:** SI la copia o la verificación final falla ENTONCES EL SISTEMA DEBERÁ
  finalizar con código distinto de cero sin declarar completa la instalación.

En Windows, `~` representa el directorio personal que resuelva el instalador,
no una ruta literal con ese carácter.

### R6 — Protección del contenido existente (HU2)

- **R6.1:** MIENTRAS esté activo el modo de simulación EL SISTEMA DEBERÁ mostrar
  las operaciones previstas sin crear ni modificar artefactos o backups.
- **R6.2:** CUANDO se sobrescriba un elemento existente sin solicitar omitir el
  backup EL SISTEMA DEBERÁ respaldar ese elemento antes de sustituirlo en
  `~/.antigravity-kit-backup/<timestamp>/`.
- **R6.3:** MIENTRAS esté activa la opción de omitir el backup EL SISTEMA DEBERÁ
  realizar la instalación sin crear dicho respaldo automático.
- **R6.4:** EL SISTEMA DEBERÁ preservar los elementos del usuario ajenos al
  inventario del kit en los destinos de instalación.
- **R6.5:** EL SISTEMA DEBERÁ preservar credenciales, settings y otros archivos
  ajenos a los destinos declarados de skills y agentes.

### R7 — Exportación de personalizaciones (HU2, HU3)

- **R7.1:** CUANDO se ejecute el script de backup/importación EL SISTEMA DEBERÁ
  exportar los elementos instalados declarados por el kit a
  `imports/antigravity/<timestamp>/`.
- **R7.2:** EL SISTEMA DEBERÁ conservar las fuentes canónicas y los adapters
  durante la exportación de personalizaciones.
- **R7.3:** EL SISTEMA DEBERÁ ofrecer la exportación tanto en Bash como en
  PowerShell y propagar los errores mediante códigos de salida distintos de cero.

Esta exportación es distinta del respaldo automático previo a sobrescribir.

## Requisitos de calidad y evidencia

### R8 — Fuente única, reproducibilidad y no regresión (HU3)

- **R8.1:** EL SISTEMA DEBERÁ mantener el contenido compartido exclusivamente
  en `canonical/` y las diferencias de Antigravity en su adapter de plataforma.
- **R8.2:** CUANDO se regenere la distribución EL SISTEMA DEBERÁ producir
  artefactos reproducibles desde las fuentes, sin modificaciones manuales en
  `generated/`.
- **R8.3:** EL SISTEMA DEBERÁ conservar la validez de los contratos y pruebas
  de las plataformas existentes al incorporar Antigravity.
- **R8.4:** EL SISTEMA DEBERÁ incluir Antigravity en las pruebas de instalación
  y en los inventarios de integridad que enumeran plataformas explícitamente.
- **R8.5:** EL SISTEMA DEBERÁ aportar evidencia de ejecución de los scripts
  PowerShell en Windows, además de las pruebas de instaladores Bash.

### R9 — Documentación e invocación verificable (HU4)

- **R9.1:** EL SISTEMA DEBERÁ documentar el catálogo actualizado de seis
  plataformas, sus rutas y comandos de instalación e importación.
- **R9.2:** EL SISTEMA DEBERÁ documentar la selección de agentes, la activación
  de skills y la recarga de recursos mediante mecanismos comprobados de la
  superficie objetivo, sin prometer `@<agente>` sin evidencia.
- **R9.3:** EL SISTEMA DEBERÁ documentar la diferencia entre Antigravity 2.0,
  CLI e IDE y limitar las garantías de soporte a las superficies verificadas.
- **R9.4:** EL SISTEMA DEBERÁ documentar cómo recuperar el contenido respaldado
  y los límites de restauración, sin prometer rollback transaccional automático.

### R10 — Comprobación en el host (HU1, HU4)

- **R10.1:** CUANDO se evalúe el soporte runtime EL SISTEMA DEBERÁ registrar
  la versión y superficie de Antigravity usadas en la comprobación.
- **R10.2:** EL SISTEMA DEBERÁ aportar evidencia del descubrimiento de los ocho
  agentes y las diez skills en Antigravity 2.0.
- **R10.3:** EL SISTEMA DEBERÁ aportar evidencia de que un agente seleccionado
  puede cargar su skill y un recurso de referencia asociado.
- **R10.4:** EL SISTEMA DEBERÁ aportar evidencia de una invocación de subagente
  con herramientas válidas y contexto explícito del alcance autorizado.
- **R10.5:** SI no se dispone de acceso al host ENTONCES EL SISTEMA DEBERÁ
  registrar la comprobación runtime como pendiente y no declarar soporte completo
  basándose únicamente en validación estática o instalación de archivos.

## Condiciones de aceptación y estrategia de pruebas

No se han ejecutado estos comandos en Requirements. Para una implementación
posterior se propone TDD focalizado para validación y comportamiento nuevo de los
instaladores; caracterización de los comportamientos existentes que se reutilicen.
La prueba en el host complementa la suite, no la sustituye.

La verificación automatizada deberá incluir los comandos del prompt original:

```bash
python3 tools/render.py
python3 tools/validate.py
python3 tools/test_integrity.py
python3 tools/test_validate.py
python3 tools/test_model_recommendations.py
python3 tools/test_sdd_contract.py
python3 tools/test_code_review_contract.py
python3 tools/test_handoff_contract.py
python3 tools/test_mas_identity.py
python3 tools/check_links.py
python3 tools/test_links.py
```

Se añade `python3 tools/test_install.py`, pruebas negativas del contrato
Antigravity y ejecución real de PowerShell en Windows. Cada resultado deberá
registrar comando, código de salida y entorno; ningún check pendiente se contará
como aprobado. Los fallos preexistentes deben distinguirse de las regresiones.

## Exclusiones

- Instalación por repositorio o en múltiples destinos alternativos.
- Garantía de soporte completo del CLI o del IDE standalone en esta primera entrega.
- Duplicación de agentes como nuevas skills o workflows.
- Orquestación automática avanzada, worktrees y mensajería asíncrona entre agentes.
- Instalación del producto Antigravity, autenticación o gestión de credenciales.
- Cambios de modelos, permisos globales o políticas de autoejecución del host.
- Refactor transversal o rollback transaccional de los instaladores existentes.
- Correcciones ajenas a esta integración en el working tree del usuario.

## Supuestos y decisiones pendientes

- La documentación oficial consultada respalda las rutas y el esquema de agentes
  de Antigravity 2.0; no es evidencia de una instalación local funcional.
- El catálogo exacto de herramientas por rol, el acceso a skills y la versión
  mínima soportada deberán resolverse durante Design, con evidencia del host o
  de su referencia oficial. No se fijan nombres tentativos como contrato probado.
- Se propone `model: inherit` en lugar de asignaciones fijas `flash`/`pro`.
- El análisis anterior no estableció baseline de tests. El repositorio tiene
  cambios locales previos, incluidos canonical, adapters, docs, tests y generated;
  deberán preservarse y releerse antes de diseñar o implementar sobre ellos.
- La autorización actual es de planificación. La aprobación de Requirements no
  autoriza por sí misma implementación, commit, push ni instalación en el HOME real.

## Fuentes

- Inventario: `canonical/manifest.json`.
- Arquitectura: `.architecture/README.md` y `docs/arquitectura-del-kit.md`.
- Contratos del kit: `docs/desarrollo.md`, `docs/instalacion.md`, `docs/mas.md`
  y las pruebas de distribución existentes.
- [Agent skills de Antigravity](https://antigravity.google/docs/skills/).
- [Agentes y subagentes personalizados](https://antigravity.google/docs/subagents/).
- [Reglas de Antigravity](https://antigravity.google/docs/rules/).

## Gate 1

Aprobado por el usuario mediante «procede» tras la presentación de Requirements.
La aprobación autoriza Design, no implementación ni instalación en el HOME real.
