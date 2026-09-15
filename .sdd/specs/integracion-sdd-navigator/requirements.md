# Requisitos — Integración SDD con Project Navigator

## Objetivo

Permitir que SDD aproveche el contexto compacto de Project Navigator cuando sea
confiable, sin convertir `.navigator/` en una dependencia obligatoria ni en una
fuente de verdad superior al código y al steering vigente.

## Alcance

- Descubrimiento y uso selectivo de una instancia aplicable de `.navigator/`.
- Evaluación de disponibilidad y frescura antes de usar sus índices.
- Degradación segura cuando Navigator esté ausente, incompleto, deshabilitado,
  desfasado o no sea verificable.
- Comportamiento consistente del agente y la skill SDD en las plataformas
  generadas por el kit.

## Fuera de alcance

- Ejecutar automáticamente bootstrap o update de Project Navigator.
- Hacer que Project Navigator sea obligatorio para crear o implementar una spec.
- Sustituir la inspección puntual del código durante diseño, implementación o
  verificación.
- Habilitar automáticamente `symbols.json`, grafos o herramientas externas.

## Historias y criterios de aceptación

### Req 1 — Uso opcional del contexto de Navigator

Como usuario de SDD, quiero que el agente aproveche un Navigator aplicable cuando
esté disponible, para reducir la reexploración del repositorio.

1. CUANDO SDD inicie una exploración, requisitos o diseño Y exista una instancia
   aplicable de `.navigator/`, EL SISTEMA DEBERÁ evaluar su disponibilidad y
   frescura antes de usar sus artefactos.
2. CUANDO el contexto y el mapa de módulos estén disponibles y vigentes, EL
   SISTEMA DEBERÁ utilizarlos como orientación inicial y limitar la lectura
   posterior a las fuentes necesarias para la solicitud.
3. EL SISTEMA DEBERÁ tratar `.navigator/` como contexto auxiliar y mantener el
   código, el steering y los contratos canónicos aplicables como fuentes de verdad.

### Req 2 — Degradación segura

Como usuario de SDD, quiero que el flujo continúe aunque Navigator no sea usable,
para no bloquear la especificación ni la implementación.

1. SI no existe una instancia aplicable de `.navigator/`, ENTONCES EL SISTEMA
   DEBERÁ continuar con el flujo selectivo actual mediante documentación y código
   puntual.
2. SI una capa requerida está ausente o deshabilitada, ENTONCES EL SISTEMA DEBERÁ
   utilizar únicamente las capas disponibles o degradar a fuentes directas, sin
   inventar información indexada.
3. SI Navigator está desfasado o su frescura no es verificable, ENTONCES EL
   SISTEMA DEBERÁ validar en fuentes directas toda afirmación relevante para el
   requisito, diseño o tarea actual.
4. SI Navigator no puede utilizarse plenamente, ENTONCES EL SISTEMA DEBERÁ
   comunicar la limitación de forma breve y continuar, salvo que el usuario elija
   detenerse para actualizarlo.

### Req 3 — Control explícito de actualizaciones

Como usuario del kit, quiero conservar el control sobre la escritura de los
índices, para evitar cambios documentales inesperados durante una sesión SDD.

1. CUANDO SDD detecte que Navigator está ausente, incompleto, desfasado o no es
   verificable, EL SISTEMA DEBERÁ poder recomendar bootstrap o update mediante
   Project Navigator.
2. EL SISTEMA NO DEBERÁ crear, actualizar ni sobrescribir `.navigator/` sin una
   petición o aprobación explícita del usuario.
3. CUANDO el usuario decida actualizar Navigator, EL SISTEMA DEBERÁ preservar los
   gates, límites y avisos propios de Project Navigator.

### Req 4 — Frescura y cambios locales

Como usuario de SDD, quiero conocer la confianza del contexto usado, para evitar
decisiones basadas en un mapa obsoleto.

1. CUANDO existan marcas verificables de baseline, EL SISTEMA DEBERÁ contrastarlas
   con el estado Git aplicable y con los cambios locales relevantes al alcance.
2. SI hay cambios relevantes posteriores al baseline de Navigator, ENTONCES EL
   SISTEMA DEBERÁ considerarlo desfasado para ese alcance.
3. SI faltan marcas suficientes para demostrar frescura, ENTONCES EL SISTEMA
   DEBERÁ clasificar el contexto como no verificable y no presentarlo como vigente.
4. `generated_at` NO DEBERÁ considerarse por sí solo evidencia suficiente de
   frescura.

### Req 5 — Compatibilidad y coherencia del kit

Como mantenedor del kit, quiero que la integración conserve los contratos de cada
especialista y de todas las plataformas soportadas.

1. EL SISTEMA DEBERÁ mantener separadas las responsabilidades: Navigator navega e
   indexa; SDD especifica, diseña, implementa y verifica tras sus gates.
2. EL SISTEMA DEBERÁ conservar los modos `direct`, `standard`, `deep` y Quick Plan,
   así como sus gates actuales.
3. CUANDO se generen los artefactos por plataforma, EL SISTEMA DEBERÁ reflejar el
   mismo comportamiento canónico de integración sin divergencias materiales.

## Casos límite

- Varias instancias `.navigator/` aplicables o empatadas.
- `config.yaml` ilegible o inválido.
- Capas habilitadas en configuración pero ausentes del filesystem.
- Baselines diferentes entre `ai-context.md`, `module-map.json` e índices opt-in.
- Working tree con cambios locales ajenos o relevantes al alcance SDD.
- Spec limitada a un subproyecto dentro de un monorepo.
- Navigator vigente al inicio que cambia durante la misma sesión.

## Supuestos

- Git puede no estar disponible; en ese caso la frescura puede quedar como no
  verificable sin bloquear SDD.
- La integración prioriza reducción de contexto, no cobertura exhaustiva del repo.
- La selección determinista de instancia y los estados de capa reutilizarán el
  contrato autoritativo de Project Navigator, sin duplicar una definición
  incompatible dentro de SDD.
