# GPT-6 Luna / GitHub Copilot — TASK-2 Alta

Estado: cohorte cerrada; resultados publicados.

**0/6 aceptación completa; 3/5 aceptación primaria entre las implementaciones.**
La causa dominante del 0/6 es el contrato extendido `edges5`, que la referencia
criterio calibrado. Ver [tabla](revision/RESULTADOS.md),
[resultados estructurados](revision/resultados.json) y
[nota de interpretación](NOTA-INTERPRETACION.md).

SDD Alta volvió a pausar: recomendó **SDD-Lite** y pidió confirmación antes de
escribir artefactos o código. No se reanudó ni se fabricó aprobación.

Preflight completo antes de inferir: 4/4 tests del adaptador, resolución real de
modelo/agente/skills, igualdad de perfiles y workspace inicial, seis probes
sintéticos de permisos sin modelo, baseline43 y referencia52 en ambas cohortes.
El adaptador usa un `offline` propio porque el motor histórico fija el
identificador de MAI. Entradas congeladas en ambos `freeze.json`.

Seis configuraciones: Build sin/con MAS, Developer instalado, candidato2,
candidato2 reforzado y SDD. Mismo contrato congelado, checkout
`3120b4302bf87a1b8c84d06662c2b8787f7da5f8`, perfiles, oráculos, bordes y límites.
Cinco perfiles en `high/`, SDD separado en `sdd-high/`; copias nuevas, sin
reutilizar soluciones. **No se reanuda el SDD de media-baja**: esta ejecución no
responde a su solicitud de selección de modo.

Modelo `github-copilot/gpt-6-luna`, nativo Copilot, sin variante explícita.
Temperatura no soportada: predeterminado del proveedor. Límites: 1.800 s,
60 pasos y umbral 5 M tokens por invocación. Sin reintentos, inferencias
auxiliares, aprobaciones simuladas ni continuación automática.

Evaluación: originales43 separados, oráculos9, bordes5, conjunta, check de Django,
consistencia de migraciones, alcance y preservación AST. Una pausa de aprobación
se conserva y revisa; no se inventa respuesta.

```sh
python3 -B -m unittest discover -s tools -p 'test_luna6_task2_high.py' -v
python3 -B tools/luna6_task2_high.py check all
```

Al terminar, `revision/RESULTADOS.md` y `revision/resultados.json` contendrán la
tabla, la revisión y los manifiestos; sin inferencia adicional. No repetir
`prepare`/`run`. Sin commits, push ni cambios globales.
