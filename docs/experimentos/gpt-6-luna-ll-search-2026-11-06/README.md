# GPT-6 Luna / GitHub Copilot — prueba media-baja

**Cinco entregas completas aceptadas; SDD pausado para selección de modo.**
Se completaron las seis invocaciones iniciales. SDD no modificó archivos:
recomienda SDD-Tiny y solicita confirmación del alcance y elección del modo.
No es una implementación fallida ni un coste comparable de entrega terminada.

Ver [tabla y resultados](revision/RESULTADOS.md),
[resultados estructurados](revision/resultados.json) y
[revisión manual de la pausa SDD](REVISION-SDD.md).

Preflight completo antes de inferir: 4/4 tests del adaptador, resolución real de
modelo/agente/skills, igualdad de perfiles y workspace inicial, seis probes
sintéticos de permisos sin modelo, baseline43 y referencia56 en ambas cohortes.
Entradas congeladas en sus respectivos `freeze.json`.

Solo LL-SEARCH, seis configuraciones: Build sin/con MAS, Developer instalado,
candidato2, candidato2 reforzado y SDD. Misma tarea, snapshots de perfiles,
checkout `3120b4302bf87a1b8c84d06662c2b8787f7da5f8`, oráculos y límites previos.
Cinco perfiles en `low/` y SDD separado en `sdd-low/`, copias nuevas sin reutilizar
soluciones. **No se ejecuta la tarea alta.**

Modelo `github-copilot/gpt-6-luna`, proveedor nativo Copilot y sin variante
explícita. El catálogo declara temperatura no soportada: predeterminado del
proveedor, no 0,2 garantizado. Límites por invocación: 1.800 s, 60 pasos y umbral
5 M tokens, comprobado al cierre de cada paso. Sin reintentos del operador,
inferencias auxiliares ni aprobaciones simuladas; título explícito.

Se conserva el prompt heredado y su fricción: la ruta del Python compartido no
es el workspace. No se amplían permisos ni se corrigen participantes durante
el ensayo. Las pausas se revisan, no se reanudan automáticamente.

Evaluación: 43 originales separados, 13 oráculos y conjunta de originales +
pruebas propias + oráculos; check Django, alcance y preservación AST de métodos
originales. Aceptación funcional/de pruebas separada de fidelidad procedural.
No es certificación procedural ni comparación causal; n=1.

Fuentes nuevas: `tools/luna6_ll_search.py`, `tools/luna6_ll_search_report.py` y
`tools/test_luna6_ll_search.py`. Reutilizan el recolector y evaluador congelados,

```sh
python3 -B -m unittest discover -s tools -p 'test_luna6_ll_search.py' -v
python3 -B tools/luna6_ll_search.py check all
```

No repetir `prepare` o `run`: marcadores exclusivos, evidencias append-only.
Sin commits/push, instalación global ni cambios canónicos.

`revision/RESULTADOS.md` y `revision/resultados.json` conservan la tabla y las
evaluaciones aisladas de los 13 oráculos, sin inferencia adicional ni modificación
de las entregas. Sus valores false para la evaluación del workspace SDD no
representan una implementación completada: la revisión manual de la pausa manda
para interpretar esa celda, sin sobrescribir el registro automático original.

Los cinco perfiles automáticos pasan 43/43 originales, 13/13 oráculos, conjunta,
check, alcance y preservación AST de métodos originales. Build sin MAS fue el
menor consumo/tiempo entre entregas completas de esta muestra: 268.877 tokens,
79,462 s, 9 tests nuevos y conjunta65. Fidelidad procedural completa no certificada.

Los dos archivos contienen 1.179 miembros verificados por SHA256; la revisión
también verificó su manifiesto suplementario. Total de las seis invocaciones:
4.234.815 tokens comparables, 880,853 s y 117 pasos, incluida la pausa SDD.
