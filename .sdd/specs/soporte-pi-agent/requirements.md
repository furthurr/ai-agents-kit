# Requisitos: soporte de Pi Agent

- **Modo SDD:** standard
- **Fase:** Requirements
- **Estado:** aprobado
- **Gate:** Gate 1 — aprobado

## Historia de usuario

Como usuario de Pi, quiero instalar las skills y los agentes canónicos del kit
MAS en mi directorio personal de Pi, para invocarlos desde sus comandos y
conservar una única fuente de verdad en `canonical/`.

## Requisitos funcionales (EARS)

### R1 — Plataforma Pi en el inventario

**CUANDO** Pi esté declarada como plataforma en `canonical/manifest.json`,
**EL SISTEMA DEBERÁ** generar una salida Pi para cada skill y cada agente que
figure en el inventario, sin editar las fuentes canónicas ni afectar las otras
plataformas.

### R2 — Skills nativas de Pi

**CUANDO** se rendericen las skills para Pi, **EL SISTEMA DEBERÁ** producir una
carpeta por skill con su `SKILL.md` y los recursos de apoyo canónicos, incluidos
`references/` y `technologies/` cuando existan.

**EL SISTEMA DEBERÁ** conservar `name` y `description` en el frontmatter de cada
`SKILL.md`, aplicar las sustituciones propias de Pi y fallar si queda un token
`{{...}}` sin resolver.

### R3 — Agentes invocables como prompt templates

**CUANDO** se renderice un agente canónico para Pi, **EL SISTEMA DEBERÁ** producir
una plantilla Markdown invocable como `/<id>`, con el contenido del agente,
frontmatter `description` y un indicador de argumentos apropiado.

**CUANDO** el usuario invoque una plantilla con una tarea, **EL SISTEMA DEBERÁ**
incluir esos argumentos en el prompt renderizado para que la tarea llegue al
agente.

**EL SISTEMA DEBERÁ** adaptar las referencias entre agentes y rutas de steering a
la convención de Pi y fallar si quedan tokens de plataforma sin resolver.

### R4 — Instalación en el directorio personal de Pi

**CUANDO** se instale el kit para Pi, **EL SISTEMA DEBERÁ** copiar las skills a
`<agent-dir>/skills/` y las plantillas de agente a `<agent-dir>/prompts/`.

**EL SISTEMA DEBERÁ** usar `PI_CODING_AGENT_DIR` cuando esté definido y, en caso
contrario, el directorio predeterminado `~/.pi/agent` (o su equivalente bajo
`USERPROFILE` en Windows).

### R5 — Protección de instalaciones existentes

**MIENTRAS** el instalador esté en modo `--dry-run` / `-DryRun`, **EL SISTEMA
DEBERÁ** mostrar las rutas y operaciones previstas sin crear ni modificar
archivos.

**CUANDO** una instalación vaya a sobrescribir artefactos existentes y no se haya
solicitado omitir el backup, **EL SISTEMA DEBERÁ** respaldarlos antes de copiar.
**EL SISTEMA NO DEBERÁ** borrar recursos de Pi que no pertenezcan al kit.

### R6 — Verificación e importación

**CUANDO** falte una skill o plantilla declarada en la salida generada o en el
destino instalado, **EL SISTEMA DEBERÁ** informar el artefacto ausente y no
declarar la instalación completa.

**CUANDO** se importe una instalación local de Pi, **EL SISTEMA DEBERÁ** copiar
solo los artefactos del kit a `imports/pi/` para revisión, sin modificar
`canonical/` ni `adapters/`.

### R7 — Límites de comportamiento documentados

**EL SISTEMA DEBERÁ** documentar que las plantillas de agente de Pi son comandos
de prompt dentro de la sesión activa: no crean subagentes aislados ni aplican
permisos distintos por agente. Los handoffs entre especialistas de esta versión
serán manuales.

## Requisitos de calidad

### R8 — Reproducibilidad y compatibilidad

**CUANDO** se ejecute el render y la validación, **EL SISTEMA DEBERÁ** producir
artefactos Pi reproducibles desde `canonical/` y `adapters/pi/`, y pasar las
pruebas de integridad, instalación, enlaces y contratos afectadas por la nueva
plataforma.

### R9 — Documentación de uso

**EL SISTEMA DEBERÁ** documentar las rutas de instalación, los comandos de
agentes (`/<id>`), la activación de skills (`/skill:<id>`), la recarga de recursos
de Pi y los límites establecidos en R7.

## Alcance acordado y exclusiones

- Incluye skills nativas y nueve agentes exportados como prompt templates.
- La instalación inicial será global, en el directorio personal de Pi; no incluye
  instalación por proyecto en `.pi/`.
- No incluye una extensión Pi para delegación automática, aislamiento de contexto
  o permisos por rol.
- Se mantienen los flujos y gates definidos en el contenido canónico como
  instrucciones del agente; esta integración no los convierte en controles de
  seguridad del sistema operativo.

## Supuestos

- Pi descubre las skills desde `<agent-dir>/skills/` y las plantillas desde
  `<agent-dir>/prompts/`, según su configuración oficial.
- El manifiesto canónico sigue siendo la fuente del conjunto de skills, agentes y
  plataformas.
- La integración debe funcionar aunque el ejecutable Pi no esté instalado en el
  entorno de CI; su descubrimiento real se comprueba con un smoke test manual.
