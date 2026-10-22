# Modo: YOLO

Prompt para copiar y ejecutar en la herramienta de IA después de instalar los
agentes y skills del MAS. Se adapta a OpenCode, Claude Code, Copilot, Kiro, Pi y
Antigravity según las capacidades de la versión y variante instaladas; no garantiza
una aplicación completa ni idéntica en todas ellas.

## Prompt

```text
Configura esta herramienta de IA para permitir lo no restringido y consultar sus recursos instalados sin avisos externos repetidos.

1. Detecta herramienta, variante (CLI/IDE/app), versión, sistema operativo y perfil activo. Revisa los permisos efectivos de usuario, proyecto, agentes y políticas administradas. Consulta documentación oficial sobre sintaxis y precedencia; no inventes opciones ni extrapoles entre variantes.

2. Autoriza por defecto únicamente lo que no tenga restricciones explícitas. Conserva confirmaciones, prohibiciones, comodines restrictivos, gates y límites del MAS. No uses modos que los ignoren ni desactives protecciones existentes.

3. Única excepción: permite leer y buscar skills, instrucciones, documentación y referencias instaladas del asistente sin el aviso genérico por estar fuera del proyecto. Detecta y limita sus rutas reales; excluye credenciales y datos privados. No autorices todo HOME ni toda la carpeta de configuración. Conserva prohibiciones y confirmaciones específicas de lectura. Esta excepción no debe ampliar escritura ni ejecución; si la herramienta no permite separarlas, conserva el control existente e informa.

4. Aplica directamente los cambios mínimos compatibles en el perfil de usuario y, solo si resulta imprescindible, en los permisos de los agentes. Respalda los archivos modificados, evita duplicar reglas y preserva las demás propiedades e instrucciones. No instales componentes ni eludas archivos protegidos. Para ajustes manuales, indica pasos verificados para la versión instalada.

5. Valida sintaxis y permisos efectivos mediante comprobaciones inocuas. Resume archivos cambiados, qué queda automático, qué exige confirmación, qué está prohibido, limitaciones, cómo revertir y si requiere recarga o nueva sesión. Distingue lo comprobado de lo pendiente.
```

## Límites

- El nombre YOLO identifica este prompt; no activa por sí mismo un modo nativo ni
  concede acceso total. Los permisos de herramientas no aprueban acciones ni gates
  del MAS.
- Los `ask` explícitos seguirán solicitando permiso, salvo la excepción externa
  acotada. El modo `--auto` de OpenCode también autoaprueba los `ask`, por lo que no
  cumple esta política.
- Pi no incorpora un control nativo por acción equivalente. Sin un mecanismo
  efectivo ya instalado, las instrucciones del MAS no equivalen a una restricción
  técnica; debe comunicarse esa limitación sin inventar una configuración.

Referencias: [permisos de OpenCode](https://opencode.ai/docs/permissions/) y
[seguridad de Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md).
