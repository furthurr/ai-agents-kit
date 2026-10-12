# Tareas — F10 Developer Agent Experimental

- Modo SDD: lite
- Plan: Quick Plan en una pasada; sin Gates 1–3

1. Implementar perfil Developer renderizado desde fuentes canónicas/adaptador y
   registro de hashes/sustituciones; empaquetar agent/skills en el contenedor F10.
2. Añadir configuración/recibo OpenCode Developer y prompt que preserva el método
   Developer, el acceso consultable a `data-api` y las cuatro herramientas existentes.
3. Añadir clasificación de resultado con respuesta final preservada, `plan_only` y
   `no_delivery`; impedir evaluación funcional sin implementación.
4. Reutilizar guard AST, exportación de primera entrega y evaluador separado F10 para
   implementación; comprobar ausencia de `.sdd/` candidato y registrar evidencia.
5. Añadir pruebas focalizadas y dry-run Docker completo con actor falso explícito.
6. Ejecutar suite pertinente, `compileall`, revisar límites/evidencia y
   `git diff --check`; documentar verificación compacta.

Orden: 1 → 2 → 3 → 4 → 5 → 6. No se inicia una ejecución con modelo.
