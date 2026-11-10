# Cohorte limpia de ODD con estándares — Gemini 3.8 Flash

ID: odd-standards-gemini38-v1-20261108.
Autorización del usuario:
«intenta terminiar las que nos hacen falta terminar, realizalas con el cli de google que tenemos, pero si crees que sea mejor reiniciarlas adelante. lo que necesito es finalizar esas pruebas y que me des resultados» (Opción 1 confirmada para reiniciar cohorte limpia de 6 celdas).

Los lotes históricos anteriores (`odd-standards-v1-20261105` y `odd-standards-retry-v1-20261105`) permanecen PARCIALES e intactos: conservan sus timeouts, errores 403 y registros. Este lote NO los altera ni reemplaza selectivamente celdas individuales. Nueva raíz de laboratorio, nuevos procesos/sesiones y seis celdas nuevas: ODD original y ODD ajustado con estándares por tres repeticiones cada uno en la tarea Alta (TASK-2 de LocalLibrary).

## Invariantes

- Modelo ejecutado: `github-copilot/gemini-3.8-flash` (Gemini 3.8 Flash, vía proveedor Copilot activo en OpenCode 1.18.34).
- Host y arnés: OpenCode 1.18.34, configurado con aislamiento total, sin skills externas.
- Agentes y skills byte a byte idénticos a los del ensayo anterior, namespaces aislados por brazo (`oa` para ODD original, `ob` para ODD ajustado).
- Tarea TASK-2 literal de LocalLibrary (reservas persistidas UI/API, concurrencia SQLite, errores exactos).
- Baseline idéntico y suite de referencia (43 pruebas originales + 9 externas) pasando antes del freeze.
- Permisos normalizados, temperature 0.2, steps 60, timeout 600 s simétrico por invocación y máximo 6 invocaciones por celda.
- No alterar código del kit canónico, perfiles instalados ni documentación canónica.

## Ejecución y análisis

- Hasta dos procesos concurrentes, original/ajustado en R1/R3 y ajustado/original en R2.
- Sesión independiente por celda, sin feedback externo.
- Solo aprobación de plan solicitada antes de código y limitada al alcance original.
- Criterio de parada: ante cualquier error API/proceso o timeout se detienen nuevas repeticiones y se conserva la evidencia.
- Evaluación en copia separada con la suite de 43 tests originales y 9 externos.
- Comprobación de contenido de skills, orden de carga respecto a escrituras, documentación consultada, seguimiento, pruebas y cierre.
- Presentación de resultados descriptivos independientes de cohortes anteriores, sin sumar métricas entre modelos.
