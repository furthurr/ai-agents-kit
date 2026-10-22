# Modo: Autónomo

Prompts de configuración persistente para ejecutar una vez después de instalar
los agentes y skills del MAS. Copia **solo el bloque de tu plataforma**: cada
prompt es completo e independiente.

El objetivo es completar las tareas sin aprobaciones técnicas repetitivas,
conservando las decisiones de alcance, los límites de rol y la protección de
credenciales. Este documento sustituye el prompt YOLO anterior por variantes
autónomas optimizadas para cada host.

## Elegir el prompt

| Host | Prompt independiente | Qué debe configurar |
|---|---|---|
| OpenCode | [OpenCode](#opencode) | Permisos efectivos globales, del proyecto y de los agentes; instrucciones persistentes. |
| Claude Code | [Claude Code](#claude-code) | Settings de permisos, restricciones de subagentes e instrucciones persistentes; políticas administradas vigentes. |
| GitHub Copilot | [GitHub Copilot](#github-copilot) | Ajustes propios de IDE, CLI o cloud; las herramientas declaradas no equivalen a autoaprobación. |
| Kiro | [Kiro](#kiro) | Configuración específica de la versión y variante; sin trasladar reglas de IDE a CLI por analogía. |
| Antigravity | [Antigravity](#antigravity) | Políticas de ejecución y revisión disponibles en la superficie instalada y permisos heredados. |
| Pi | [Pi](#pi) | Instrucciones persistentes, herramientas de la sesión y extensiones que puedan solicitar aprobación. |

El alcance real depende de la versión, variante y políticas del entorno. Ninguna
fila garantiza ausencia total de avisos: el prompt correspondiente debe verificar
lo que puede configurar y comunicar los límites encontrados.

## OpenCode

```text
Configura OpenCode de forma persistente para completar mis tareas sin aprobaciones técnicas repetitivas.

1. Detecta versión, variante, perfil y configuración efectiva de usuario, proyecto, agentes y políticas administradas. Consulta la documentación oficial de permisos y precedencia. Respalda cada archivo antes de modificarlo y conserva las opciones ajenas a este cambio.
2. Configura `allow` para lectura, búsqueda, edición, shell (también tests, variables de entorno, redirecciones y comandos compuestos), red, delegación permitida por el rol y directorios externos necesarios. Revisa tanto `permission` global como los bloques de agentes instalados: sus `ask` pueden prevalecer sobre el global. Respeta el orden de coincidencia documentado y conserva los `deny` de secretos, límites de rol y políticas administradas. No confundas permitir shell con proteger secretos frente a ese shell; informa los límites reales.
3. Guarda en las instrucciones persistentes aplicables: decide los pasos, ejecuta, verifica y corrige hasta completar lo pedido. La petición autoriza los pasos técnicos necesarios dentro de su alcance; elimina reconfirmaciones locales redundantes, sin ampliar responsabilidades del agente. Commit, push, tags, releases y publicación solo si forman parte de lo solicitado. Pregunta únicamente por ambigüedad o decisiones de alcance, incluida una acción destructiva o irreversible no prevista. Si el rol prohíbe algo, informa el límite sin pedir permiso para infringirlo y continúa con lo permitido.
4. Valida sintaxis y permisos resueltos por agente; prueba inocuamente lectura, edición temporal y ejecución de un test mínimo. Comprueba las prohibiciones sin abrir secretos ni ejecutar operaciones peligrosas. Distingue pruebas reales de revisión estática. Informa cambios, respaldos, restauración, límites y reinicio o sesión nueva necesarios. Advierte si actualizar el MAS puede reponer los permisos anteriores.
```

## Claude Code

```text
Configura Claude Code de forma persistente para completar mis tareas sin aprobaciones técnicas repetitivas.

1. Detecta versión, CLI o integración IDE, perfil y settings efectivos de usuario, proyecto y ámbito local, además de subagentes, hooks y políticas administradas. Consulta la documentación oficial sobre permisos y precedencia. Respalda los archivos que cambies y conserva las demás opciones.
2. Usa las reglas de permisos admitidas para autorizar lectura, búsqueda, edición, Bash (incluidos tests y comandos compuestos), red, delegación compatible con el rol y directorios necesarios. Revisa restricciones específicas de subagentes y hooks que generen avisos. No confundas `tools` con permisos ni un modo de aceptar ediciones con permiso para ejecutar Bash. No uses bypassPermissions ni desactives controles administrados. Conserva los bloqueos de secretos y de rol; si las reglas o los hooks impiden eliminar algún aviso, explica el límite sin prometer autonomía total ni retirar controles a ciegas.
3. Persiste en las instrucciones aplicables: planifica, ejecuta, verifica y corrige hasta terminar. Considera autorizados los pasos técnicos necesarios dentro de lo pedido; elimina reconfirmaciones locales redundantes sin ampliar el rol. Commit, push, tags, releases y publicación requieren estar incluidos en la petición. Pregunta solo por ambigüedad o decisiones de alcance, incluidas acciones destructivas o irreversibles no previstas. Si el rol impide una acción, informa el límite y sigue con lo permitido, sin pedir permiso para infringirlo.
4. Valida settings y reglas resueltas; prueba lectura, edición temporal y un test mínimo sin efectos externos. Verifica bloqueos sin leer credenciales y aclara que permitir Bash no lo convierte en un sandbox. Reporta cambios, respaldos, restauración, avisos que persisten y recarga o sesión nueva necesaria; distingue comprobación estática de prueba real.
```

## GitHub Copilot

```text
Configura GitHub Copilot de forma persistente para completar mis tareas sin aprobaciones técnicas repetitivas.

1. Identifica la superficie exacta: extensión IDE y editor, CLI o agente cloud; detecta versión, perfil, instrucciones, agentes personalizados y políticas de organización. Consulta la documentación oficial específica de esa superficie; no traslades ajustes entre IDE, CLI y cloud. Respalda los archivos que modifiques.
2. Configura las aprobaciones de herramientas, terminal, edición, red y delegación usando solo mecanismos documentados de esa variante. Revisa los permisos del host además de `tools` de cada agente: declarar herramientas no las autoaprueba. Autoriza las operaciones necesarias, incluidos tests y comandos compuestos, conservando secretos, límites de rol y políticas administradas. No uses una autorización indiscriminada que anule esas prohibiciones. Si una opción solo existe en la interfaz o depende de la organización o del entorno cloud, describe el paso exacto pendiente sin inventar settings ni afirmar que quedó aplicado.
3. Guarda en las instrucciones persistentes admitidas: decide los pasos, ejecuta, verifica y corrige hasta completar lo pedido, sin reconfirmar operaciones técnicas ya incluidas. No amplíes el rol; commit, push, tags, releases y publicación solo cuando estén solicitados. Pregunta únicamente por ambigüedad o decisiones de alcance, incluidas acciones destructivas o irreversibles no previstas. Cuando el rol prohíba una acción, informa el límite y continúa con lo permitido, sin pedir permiso para saltarlo.
4. Comprueba la configuración efectiva con lectura, edición temporal y un test mínimo inocuo; revisa bloqueos sin abrir secretos. Distingue permisos de herramientas de restricciones del terminal o sandbox. Informa cambios, respaldos, restauración, confirmaciones que conserva el host y recarga o sesión nueva necesaria; separa validación estática de pruebas reales.
```

## Kiro

```text
Configura Kiro de forma persistente para completar mis tareas sin aprobaciones técnicas repetitivas.

1. Detecta si es IDE o CLI, versión, perfil, agentes, steering y políticas administradas. Consulta la documentación oficial correspondiente: no supongas que un formato de reglas del IDE funciona en la CLI ni que todas las versiones comparten esquema. Respalda los archivos que cambies.
2. Ajusta los mecanismos documentados de confianza y permisos de esa variante para lectura, búsqueda, edición, shell (tests, variables de entorno y comandos compuestos incluidos), red, delegación compatible con el rol y rutas necesarias. En esquemas que resuelvan deny > ask > allow, un allow posterior no anula un deny: modifica únicamente los ask redundantes y usa exclusiones solo si el esquema instalado las admite. Conserva secretos, límites de rol y políticas administradas; no conviertas en confiable un conjunto de herramientas que anule esas protecciones. Si el formato del MAS es incompatible con la versión instalada, informa la incompatibilidad y aplica solo lo oficialmente soportado.
3. Persiste en el steering o instrucciones apropiadas: decide, ejecuta, verifica y corrige hasta terminar. La petición autoriza los pasos técnicos necesarios dentro de su alcance; elimina reconfirmaciones locales redundantes sin ampliar el rol. Commit, push, tags, releases y publicación solo si fueron solicitados. Pregunta solo por ambigüedad o decisiones de alcance, incluidas acciones destructivas o irreversibles no previstas. Si el rol impide algo, informa el límite y sigue con lo permitido, sin pedir autorización para infringirlo.
4. Valida con el esquema o mecanismo real de esa versión y pruebas inocuas de lectura, edición temporal y ejecución de un test mínimo. Comprueba prohibiciones sin abrir secretos. Informa cambios, respaldos, restauración, límites efectivos y reinicio o sesión nueva necesarios; no presentes validación de formato como prueba de ejecución del host.
```

## Antigravity

```text
Configura Antigravity de forma persistente para completar mis tareas sin aprobaciones técnicas repetitivas.

1. Detecta variante y versión instaladas, perfil, agentes, instrucciones, políticas de terminal y revisión, permisos del workspace y controles heredados del padre o de la organización. Consulta documentación oficial de esa superficie. Respalda archivos antes de cambiarlos; no inventes claves, scopes ni rutas.
2. Ajusta las políticas de ejecución y revisión realmente disponibles para permitir lectura, búsqueda, edición, terminal (tests y comandos compuestos incluidos), red y delegación compatible con el rol. Revisa herramientas del agente y aprobaciones del host por separado: una lista de tools no configura el sandbox ni los permisos heredados. Usa `commandExecutionPolicy` solo si la versión lo documenta y verifica su efecto. Conserva secretos, límites de rol y políticas administradas. Si un ajuste requiere la interfaz, el padre o administración, informa el paso exacto pendiente y lo que sigue preguntando; no declares que cambiaste controles inaccesibles.
3. Guarda en las instrucciones persistentes admitidas: decide los pasos, ejecuta, verifica y corrige hasta completar lo pedido, sin reconfirmar acciones técnicas ya previstas. No amplíes el rol; commit, push, tags, releases y publicación solo si están solicitados. Pregunta únicamente por ambigüedad o decisiones de alcance, incluidas acciones destructivas o irreversibles no previstas. Si el rol prohíbe algo, informa el límite y continúa con lo permitido, sin pedir permiso para infringirlo.
4. Valida con lectura, edición temporal y un test mínimo inocuo; comprueba prohibiciones sin abrir secretos. Distingue configuración escrita, ajustes observados en la interfaz y pruebas reales del agente. Reporta cambios, respaldos, restauración, límites heredados y reinicio o sesión nueva necesarios.
```

## Pi

```text
Configura Pi de forma persistente para completar mis tareas sin interrupciones técnicas repetitivas.

1. Detecta versión, perfil, instrucciones globales y del proyecto, plantillas del MAS, herramientas activas, extensiones y harness que puedan solicitar aprobación. Consulta la documentación oficial y respalda los archivos que cambies. No inventes un sistema nativo de permisos por acción: las plantillas por sí solas no lo crean.
2. Habilita mediante mecanismos documentados las herramientas necesarias para leer, buscar, editar, ejecutar shell y tests, consultar red o delegar cuando existan y el rol lo permita. Si una extensión o el harness genera avisos, revisa su configuración y elimina solo aprobaciones técnicas redundantes, conservando secretos, límites de rol y políticas administradas. No instales extensiones para eludir controles. Si no existe protección técnica de secretos o restricciones por rol, decláralo: una instrucción no bloquea al proceso ni contiene el shell.
3. Persiste en las instrucciones aplicables: decide los pasos, ejecuta, verifica y corrige hasta terminar cada tarea; no reconfirmes operaciones técnicas necesarias dentro de lo pedido. No amplíes el rol; commit, push, tags, releases y publicación solo cuando estén solicitados. Pregunta únicamente por ambigüedad o decisiones de alcance, incluidas acciones destructivas o irreversibles no previstas. Si la naturaleza del agente impide algo, informa el límite y sigue con lo permitido, sin pedir permiso para infringirlo. No leas ni expongas secretos o credenciales.
4. Prueba inocuamente lectura, edición temporal y un test mínimo. Verifica qué avisos provienen de extensiones y cuáles son preguntas del modelo; no afirmes aislamiento de subagentes ni bloqueos técnicos inexistentes. Reporta archivos cambiados, respaldos, restauración, herramientas disponibles, límites y recarga o sesión nueva necesaria; distingue revisión estática de pruebas reales.
```

## Límites comunes

- Son prompts de configuración, no un modo nativo ni una garantía de autonomía
  idéntica entre herramientas. Las políticas administradas mantienen su autoridad.
- Permitir shell ampliamente no garantiza proteger secretos mediante reglas de
  lectura de otra herramienta. Deben comunicarse las protecciones efectivas y sus
  límites; no se acredita un sandbox por configurar patrones.
- La autonomía se limita a lo pedido. Las decisiones de alcance siguen siendo
  interactivas y las prohibiciones propias de cada rol permanecen vigentes.
- Las instrucciones persistentes deben conciliarse con las skills y agentes
  locales: cambiar permisos técnicos por sí solo no elimina sus preguntas. Una
  actualización del MAS puede reponer instrucciones o permisos anteriores.
- Cada aplicación debe dejar respaldo, forma de restauración y evidencia de lo
  comprobado. Las pruebas deben usar archivos temporales y código inocuo, nunca
  credenciales ni operaciones destructivas o publicación real.

## Referencias

- [Capacidades y permisos del MAS](../permisos-hosts.md).
- [Permisos de OpenCode](https://opencode.ai/docs/permissions/).
- [Permisos de Claude Code](https://code.claude.com/docs/en/permissions).
- [Documentación de GitHub Copilot](https://docs.github.com/en/copilot).
- [Documentación de Kiro](https://kiro.dev/docs/).
- [Documentación de Antigravity](https://antigravity.google/docs).
- [Seguridad de Pi](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md).
