# Modo: YOLO

Prompt para copiar y ejecutar en la herramienta de IA después de instalar los
agentes y skills del MAS. Se adapta a OpenCode, Claude Code, Copilot, Kiro, Pi y
Antigravity según las capacidades de la versión y variante instaladas; no garantiza
una aplicación completa ni idéntica en todas ellas.

## Prompt

```text
Configura esta herramienta de IA para reducir avisos innecesarios sin saltarte sus controles ni los del MAS.

1. Detecta herramienta, variante (CLI/IDE/app), versión, sistema operativo y perfil activo. Revisa la configuración efectiva de usuario, proyecto, agentes y políticas administradas. Consulta documentación oficial sobre sintaxis y precedencia; no inventes claves, rutas ni modos.

2. Permisos y comandos Bash:
   - Permite por defecto lo que no tenga una restricción explícita; conserva todos los `deny`, gates, límites de rol y confirmaciones necesarias para cambios, borrado, instalación, red, publicación, Git mutante, seguridad y datos sensibles. No actives modos que omitan controles.
   - Si un `bash: "*": "ask"` bloquea verificaciones conocidas de solo lectura, no lo conviertas en `allow` global. Consérvalo como regla de respaldo y añade, solo si la plataforma admite reglas por comando, excepciones limitadas como:
     `git status --short`, `git status --short --branch`, `git diff --check`, `git diff --stat`, sus variantes `--cached`, `test -f <ruta>` y `test ! -e <ruta>`.
   - Pon las excepciones después de la regla general solo si la documentación oficial confirma que la última coincidencia prevalece. Mantén confirmación para comandos no incluidos, redirecciones, instalaciones, pruebas que ejecuten código, `git diff --no-index`, process substitution, envoltorios o sintaxis que no puedas analizar con seguridad. Nunca autorices `bash` completo ni `git *`.
   - Los `git diff -- <rutas>` que muestran contenido también siguen pidiendo permiso salvo que se compruebe una protección efectiva para secretos; no los trates como equivalentes a `--check` o `--stat`.
   - Respeta las instrucciones conversacionales del agente además de los permisos técnicos. En particular, no habilites shell para una operación `inspect` de `code-review` si su contrato la prohíbe.

3. Recursos instalados: detecta las rutas reales de skills, instrucciones, documentación y referencias. Permite solo su lectura/búsqueda sin avisos de directorio externo; conserva el control de lectura de archivos sensibles. No autorices todo HOME ni toda la carpeta de configuración. Esta excepción no debe autoautorizar edición ni shell; si el host no puede separarlos, informa el límite y conserva la confirmación.

4. Revisa otras reglas que interrumpan el flujo solicitado. Para cada una, identifica agente/acción, si bloquea una operación concreta y si esa operación es realmente de solo lectura. Ajusta solo fricciones redundantes y acotadas como las anteriores. Conserva restricciones de edición, delegación, red, secretos, scopes documentales, gates SDD, remediación, commits, push, tags, releases y acciones destructivas cuando protejan responsabilidades o tengan efectos. Si una regla no es claramente innecesaria, consérvala y explica por qué.

5. Aplica los cambios mínimos compatibles en la configuración del usuario y, solo si hace falta, en los agentes pertinentes. Respalda cada archivo, preserva el resto de opciones y del texto, no instales componentes ni eludas políticas administradas. Si la sintaxis no permite una excepción segura, no la sustituyas por acceso total.

6. Valida la sintaxis y la configuración resuelta. Comprueba inocuamente que las rutas de recursos seleccionadas quedan permitidas, otras rutas externas siguen preguntando, los comandos de lectura incluidos en la lista no preguntan y un comando mutante/desconocido sigue en `ask` o `deny`. Informa archivos modificados, cambios automáticos, confirmaciones/prohibiciones conservadas, otras restricciones detectadas, límites, respaldo/restauración y si hay que reiniciar o iniciar sesión nueva. Distingue comprobaciones estáticas de pruebas reales del host.
```

## Límites

- El nombre YOLO identifica este prompt; no activa por sí mismo un modo nativo ni
  concede acceso total. Los permisos de herramientas no aprueban acciones ni gates
  del MAS.
- Solo las verificaciones de lectura incluidas en una allowlist específica pueden
  dejar de preguntar. Los demás `ask` explícitos siguen vigentes. El modo `--auto`
  de OpenCode también autoaprueba los `ask`, por lo que no cumple esta política.
- Las reglas Bash por patrón no son un sandbox y pueden no reconocer comandos
  envueltos, redirecciones u operaciones que oculten rutas. Para esos casos, conserva
  la confirmación; no declares aislamiento efectivo.
- Pi no incorpora un control nativo por acción equivalente. Sin un mecanismo
  efectivo ya instalado, las instrucciones del MAS no equivalen a una restricción
  técnica; debe comunicarse esa limitación sin inventar una configuración.

Referencias: [permisos de OpenCode](https://opencode.ai/docs/permissions/) y
[seguridad de Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md).
