# MAI-Code-1.1-Flash — LocalLibrary

**12 invocaciones iniciales terminadas. Aceptación completa: 2/6 en media-baja,
0/6 en alta.** No todas produjeron una entrega: Developer alta pidió aprobación
de plan y SDD alta se bloqueó intentando acceder a la ruta equivocada.

Ver las [dos tablas y revisión de resultados](revision-posterior/RESULTADOS.md)
y los [resultados estructurados revisados](revision-posterior/resultados-revisados.json).

Ver [protocolo](protocolo.md). Se ejecutaron doce trayectorias iniciales: seis
configuraciones para LL-SEARCH y seis para TASK-2 Alta. No se reanudaron pausas,
no se inventaron aprobaciones ni se repararon soluciones por feedback externo.

Las exportaciones iniciales de `low/`, `high/`, `sdd-low/` y `sdd-high/` se
preservan intactas. La revisión posterior corrige dos limitaciones del estado
automático: Build con MAS agotó 60 pasos en ambas tareas pese a `stop_reason=null`,
y SDD alta no estaba esperando un gate SDD sino bloqueado por confusión de ruta.
Los 2.361 miembros de los cuatro archivos se verificaron por SHA256.

Modelo `github-copilot/mai-code-1.1-flash`, sin variante explícita. Temperatura
no soportada por el catálogo, se usa el predeterminado del proveedor.

Fuentes nuevas: `tools/mai_flash_benchmark.py`,
`tools/test_mai_flash_benchmark.py` y `tools/mai_flash_report.py`. Las cohortes
anteriores se conservan intactas. La revisión posterior es offline, sin inferencia.

Total observado: **12.108.960 tokens comparables**, **2.169,457 s** de conversación
y **425 pasos**. n=1; no equivale a factura ni demuestra superioridad universal.
Hubo fricción de permisos y confusión entre la ruta del Python compartido y el
workspace; esa limitación experimental está documentada, no corregida a mitad
del ensayo. Fidelidad procedural completa no certificada.

Verificación sin inferencia:

```sh
python3 -B -m unittest discover -s tools -p 'test_mai_flash*.py' -v
python3 -B tools/mai_flash_benchmark.py check all
```

No repetir `prepare` ni `run`: los marcadores de invocación son exclusivos.
Tampoco repetir el exportador de revisión: sus archivos son append-only.
Ver [registro de verificación](VERIFICACION.md) para comandos y límites del cierre.
