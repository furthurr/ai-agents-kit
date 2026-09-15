# Contexto opcional de Project Navigator

Project Navigator es una ayuda de navegación, no una dependencia de SDD. Este
contrato se aplica antes de consumir `.navigator/`; la autoridad sobre el formato,
bootstrap y update de sus índices sigue perteneciendo a la skill
`project-navigator`.

## Principios

- El código, el steering y los contratos canónicos aplicables son las fuentes de
  verdad. Navigator reduce exploración; no reemplaza su verificación.
- La ausencia, ambigüedad o falta de frescura de Navigator no bloquea SDD.
- SDD no crea ni actualiza `.navigator/` sin petición o aprobación explícita.
- No se invoca ni se cambia automáticamente a otro agente.

## Orden de lectura

En exploración y en cada fase que necesite contexto nuevo:

1. Leer el steering de la plataforma y `.sdd/steering/`.
2. Ejecutar el preflight mínimo de Navigator.
3. Leer solo la capa mínima útil de Navigator.
4. Leer el README de contexto de dominio aplicable y documentación adicional
   estrictamente necesaria.
5. Leer código puntual y pruebas según la fase.

En requisitos, el código es condicional si hace falta aclarar el comportamiento
actual. En diseño, implementación y verificación, confirmar en código real toda
decisión o evidencia relevante. Si Navigator no es confiable, solo aporta pistas
de ubicación y las afirmaciones se validan en fuentes directas.

## Preflight mínimo

1. Resolver la raíz del repositorio o workspace.
2. Localizar candidatos con nombre exacto `.navigator/config.yaml` en la raíz y
   subproyectos conocidos; ignorar backups y nombres parecidos.
3. Seleccionar la instancia única o el `project.root` más específico que contenga
   el alcance consultado. Si varias empatan, clasificar `ambiguo`; no adivinar.
4. Leer el `config.yaml` seleccionado desde filesystem en la petición actual.
5. Resolver los índices junto a ese config, no junto al archivo de código
   consultado. Una capa solo está disponible si está habilitada, existe y es
   legible.
6. Empezar por `ai-context.md` o `module-map.json`; usar símbolos o grafo solo si
   la consulta los necesita y están habilitados.

No volcar índices completos al contexto. Filtrar módulos, símbolos y paths antes
de escalar a código.

## Frescura y confianza

| Estado | Criterio | Uso permitido |
|---|---|---|
| `vigente` | Baseline común verificable, sin cambios relevantes posteriores ni locales | Orientación inicial; confirmar código según la fase |
| `desfasado` | Hay cambios relevantes posteriores al baseline | Solo pistas; confirmar en fuentes directas |
| `no_verificable` | Faltan marcas, Git no permite contraste o los baselines difieren | Solo pistas; no afirmar vigencia |
| `ambiguo` | No se puede elegir una instancia única | Omitir Navigator y continuar |
| `ausente` | No existe una instancia aplicable | Continuar con fuentes directas |

Para declarar `vigente`:

1. Los artefactos consumidos que soporten baseline deben representar el mismo
   `source_commit` completo y verificable.
2. Contrastar cambios entre ese baseline y `HEAD`, además del working tree, para
   las rutas relevantes al alcance.
3. Considerar relevantes el módulo o rutas objeto de la spec, sus contratos,
   steering y manifiestos estructurales aplicables.
4. Si no puede determinarse con seguridad si un cambio afecta al alcance,
   clasificar `no_verificable`; no elevar la confianza por inferencia.
5. `generated_at` solo informa antigüedad y nunca demuestra frescura por sí solo.

Un cambio claramente ajeno al alcance no vuelve desfasado el índice por sí mismo.
Si Navigator cambia durante la sesión, repetir el preflight antes de volver a
basar una fase o decisión en sus artefactos.

## Capas incompletas y degradación

- Capa habilitada pero ausente o ilegible: usar otra capa disponible o fuentes
  directas; no inventar datos indexados.
- Capa deshabilitada: no leerla aunque el archivo exista.
- Config inválido o ilegible: tratar Navigator como `no_verificable` y continuar.
- Instancias empatadas: omitirlas; preguntar solo si el usuario exige usar
  Navigator y la selección resulta necesaria.
- Path indexado inexistente: descartarlo y localizar el código real.

Comunicar solo la limitación relevante, las fuentes realmente usadas y una
confianza breve. No convertir el preflight en un gate adicional.

## Bootstrap o update

Si conviene materializar o refrescar los índices, recomendar Project Navigator y
continuar salvo que el usuario elija detenerse. Ante aceptación, preservar sus
gates, avisos de modelo, exclusiones y alcance de escritura. Retomar SDD después de
que el usuario aporte el resultado o confirme que desea seguir sin actualizar.
