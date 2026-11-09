# Paquete de continuidad ODD — 2026-11-06 UTC

**No ejecutar modelos al abrir este paquete.** El usuario pidió pausar y continuar
en una sesión nueva la búsqueda de ODD con consulta de dominios y menor consumo total.

1. [CONTINUAR-AQUI.md](CONTINUAR-AQUI.md): decisiones, cronología, resultados y límites.
2. [PROMPT.md](PROMPT.md): prompt completo para copiar a otra sesión.
3. [estado.json](estado.json): estado estructurado y objetivo actual.
4. [manifest.json](manifest.json): inventario/hash de evidencia, estado Git y verificaciones.
5. [herramientas-y-plan.tar.gz](herramientas-y-plan.tar.gz): snapshot de scripts,
   fuentes de contrato canónicas de referencia y plan previo del Escritorio. Copias
   para recuperación/lectura, NO distribución ni autorización para instalarlas.

Los laboratorios y trazas completas permanecen en los paquetes de cada experimento;
no se duplican aquí todos sus binarios. El manifest verifica sus archivos y los hashes
de los laboratorios contra los registros de preservación existentes. Se documenta
su alcance: no es una nueva auditoría semántica de cada traza histórica.

## Para otra sesión o máquina

- Mismo checkout: leer el punto de continuidad y pegar PROMPT.md.
- Otra máquina/worktree: copiar `docs/experimentos/` completo o el conjunto de cohortes
  citadas más este paquete, junto con los scripts recuperados del snapshot o el checkout
  local completo. Los archivos untracked no están garantizados en el remoto.
- Verificar SHA256 y rutas seguras antes de extraer. No sobrescribir archivos activos
  al restaurar copias históricas. No extraer secretos ni seguir symlinks fuera del destino.
- No depender de temporales: los adapters contienen rutas absolutas que deben revisarse
  antes de cualquier nueva ejecución autorizada. Reconstruir entorno/freeze si procede.

Estos archivos son artefactos del experimento. Los índices canónicos anteriores
no se modificaron desde Developer; su integración queda para selección manual de
`documentation-orchestrator`. No se cambió de agente automáticamente.
