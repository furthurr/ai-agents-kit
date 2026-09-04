# Revisión post-implementación — orquestacion-handoff-canonical

Fecha: 2026-09-03
Estado: revisión inicial superada por la segunda auditoría; ver
`review-v2.md` para el dictamen vigente.

## Veredicto

**Suma, con matices.** El núcleo (contrato portable + test + coste acotado) es
sólido y coherente con la arquitectura del kit. Pero hay un riesgo real de
**redundancia semántica** y dos defectos menores de especificación que conviene
corregir antes de promocionar el handoff como flujo principal.

## Lo que está bien (suma)

1. **Portabilidad real**: bloque Markdown, sin APIs de subagentes; coherente con
   `docs/arquitectura-del-kit.md:208-225`.
2. **Coste acotado y medido**: +60 palabras siempre cargadas, +308 bajo demanda
   (archivo nuevo). Cumple RNF-1.
3. **Sin tocar `render.py` ni `validate.py`**: el contrato en `references/` se
   propaga solo (`shutil.copytree`).
4. **Test de contrato en CI**: `test_handoff_contract.py` 27/27, integrado en
   `ci.yml`.
5. **Exclusiones correctas**: git/release, remediación, implementación, Graphify.

## Hallazgos (resta o riesgo)

### H1 — Redundancia semántica (el más importante)

El orquestador **ya ejecuta** el trabajo cargando las skills secuencialmente
(`SKILL.md` paso 4). El handoff se emite **además**, lo que puede percibirse como
duplicación: ¿por qué entregar contexto al especialista si el orquestador ya hizo
el trabajo?

El valor real del handoff es distinto y **no está explicado**: permite invocar al
**especialista real** (con su propio rol y permisos de frontmatter) en lugar de
que el orquestador lo "impersonifique" cargando su skill. Sin esa aclaración, el
handoff parece ruido.

**Recomendación:** añadir al contrato una frase de propósito: *"el handoff se
emite cuando el trabajo debe continuar en el agente especialista real (con sus
permisos propios), no cuando el orquestador lo ejecuta él mismo"*. O, si se
prefiere, emitir el handoff **en lugar de** ejecutar, cuando el usuario lo pida.

### H2 — Campo `mode` ambiguo

El handoff usa `mode` con valores de **orquestador** (`status`, `sync-domain`),
pero el destino es un **especialista** que no tiene esos modos (security tiene
Fase A/B; architecture tiene lite/full). El campo queda sub-especificado.

**Recomendación:** renombrar a `action`/`intent` con valores de especialista
(`auditar`, `documentar`, `sincronizar`, `remediar`), o eliminarlo y dejar que el
`target` + `scope` definan la intención.

### H3 — Ubicación del paso 8

El paso 8 ("al cerrar cada dominio") está **después** del paso 7 ("cierre
global"). Hay tensión entre "por dominio" y "cierre global".

**Recomendación:** mover la emisión al paso 4 (ejecución secuencial por dominio),
o reescribir el paso 8 como "al cierre, si procede, emite los handoffs de los
dominios coordinados".

### H4 — `scope` vs `write_scope` redundantes

Para un especialista, `scope` y `write_scope` suelen coincidir (ej. `.security/`).
La distinción solo aporta si `scope` incluye lectura más allá de `write_scope`.
Defendible, pero añade fricción.

**Recomendación:** documentar un ejemplo donde difieran, o fusionar en un solo
campo `scope` con sub-campo de escritura.

### H5 — Validación solo estática

El test valida **estructura** (los campos existen como texto), no **comportamiento**
(el orquestador emitiendo bien el handoff en las 3 plataformas). Aceptable para
este incremento, pero es una limitación.

**Recomendación:** smoke manual (`docs/orchestration-smoke.md`) como siguiente paso.

### H6 — `docs/agentes/` mezclado con trabajo previo

Edité un archivo no commiteado del usuario. No es un fallo, pero conviene
separarlo en el commit.

## Conclusión

- **No cometimos un error de integridad**: render, validate y las 3 suites pasan;
  el coste está medido y aprobado.
- **Sí hay un defecto de diseño** (H1) que puede hacer que el handoff reste en
  lugar de sumar si no se aclara su propósito, y dos defectos menores (H2, H3).
- **Acción recomendada:** un pase corto de ajuste (H1–H3) antes de promocionar el
  handoff como flujo principal; H4–H6 son opcionales o de documentación.
