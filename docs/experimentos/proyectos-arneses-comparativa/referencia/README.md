# Referencia y base comparativa

> **Evidencia anonimizada:** identificadores y fragmentos originales han sido sustituidos u omitidos. Las métricas son históricas; no acreditan una ejecución nueva sobre los fixtures. Véase [alcance y límites](../../PRIVACIDAD-MOVIL.md).

Esta carpeta fija la base exacta usada por el experimento. No duplica el árbol
de trabajo porque el repositorio ya está versionado en Git; en su lugar registra
la identidad verificable de cada insumo.

## Contenido

| Archivo | Qué fija |
|---|---|
| `repo-head.txt` | Commit del MAS usado (`1b52c73`). |
| `repo-status.txt` | Estado del árbol al iniciar el experimento. |
| `repo-sha256.txt` | SHA-256 de los 1.193 archivos versionados del repositorio. |
| `inputs-sha256.txt` | SHA-256 del ZIP de Genera Android, la tarea histórica, el oráculo histórico y las fuentes de `v2_reforzado`. |
| `genera-sha256.txt` | SHA-256 de la tarea y el oráculo adaptados a Genera. |
| `resultados-sha256.txt` | SHA-256 de los documentos finales, `resultados.json` y el runner. |
| `incidente-permission.md` | Diagnóstico y corrección del incidente de la regla comodín con gentle-ai. |
| `lab-size.txt` | Tamaño de cada componente del laboratorio temporal. |

## Nota sobre la base

El ZIP histórico `mobile-android.zip` referenciado por
`inputs-sha256.txt` ya no está en disco. La base efectiva de esta ronda es
`mobile-android.zip`, también registrada en
`inputs-sha256.txt`. La adaptación se documenta en
[../genera/README.md](../genera/README.md).

## Copias de trabajo

Las copias aisladas del proyecto Android viven en la carpeta temporal del
sistema, junto a los demás proyectos de experimentos:

```
…/T/opencode/proyectos-arneses-comparativa/
  _sources/        clones de los cinco arneses
  _bin/            gentle-ai y Bun locales
  task_1/
    runs/<arnés>/      copia limpia del proyecto por brazo
    profiles/<arnés>/  HOME/XDG/OPENCODE_CONFIG_DIR aislados
    evidence/          run, eval, install y preflight por brazo
    install-logs/      salida de cada instalador
```

## Cómo verificar

```bash
shasum -a 256 ~/.local/share/ai-agents-kit/fixtures/mobile-android.zip
# compara el resultado con la primera línea de inputs-sha256.txt
shasum -a 256 -c docs/experimentos/proyectos-arneses-comparativa/referencia/resultados-sha256.txt
git rev-parse HEAD   # debe coincidir con repo-head.txt
```
