# Replicación LocalLibrary con MAI-Code-1.1-Flash

## Alcance congelado antes de inferir

Dos tareas independientes: LL-SEARCH (media-baja) y TASK-2 (alta). Cada una parte
del checkout `3120b4302bf87a1b8c84d06662c2b8787f7da5f8`, nunca de una solución de
otro participante. Se reutilizan los contratos, oráculos, fixtures MAS y snapshots

Por tarea: Build sin MAS, Build con MAS, Developer instalado, candidato2,
candidato2 con dos refuerzos y SDD. Cinco perfiles automáticos en una cohorte y
SDD en otra, para conservar su revisión manual y evitar una aprobación inventada.
Orden de ejecución: low, high, sdd-low, sdd-high. Una repetición por celda.

## Modelo y diferencias inevitables

- ID exacto: `github-copilot/mai-code-1.1-flash`, proveedor nativo GitHub Copilot.
- El endpoint efectivo y las capacidades se conservan en `offline.json`.
- No se redefine el transporte ni se leen/copían credenciales. No OpenRouter.
- Sin variante explícita; se conserva el predeterminado del proveedor.
- Cambian proveedor, tokenizer, contexto, caché y latencia: no es una comparación
  controlada de pesos del modelo ni una equivalencia de factura.

## Límites y operación

Por invocación: 1.800 s, 60 pasos, umbral de 5.000.000 tokens comparables. El
umbral se comprueba al finalizar cada paso y puede sobrepasarse en el último.
Sin reintentos del operador, correctores, inferencias auxiliares ni auto-resume.
Título explícito para evitar la inferencia automática de título. Una condición
de parada del arnés detiene el resto de esa cohorte; no se oculta su parcialidad.
Los retries internos del proveedor no son observables de forma independiente.

Si SDD pide elección de modo, alcance o aprobación, se conserva literalmente y
no se traslada a MAI. Una pausa real no es un fallo de implementación.

## Evaluación

- Media-baja: originales 43, conjunta = 43 + 13 oráculos + tests propios.
- Alta: originales 43, oráculos 9, bordes 5, conjunta = 43 + 9 + tests propios;
  bordes por separado, check Django y migraciones consistentes.
- AST de métodos originales preservado; conteo de métodos de tests nuevos.
- Aceptación funcional separada de entrega de pruebas y fidelidad procedural.
- Sin reparación de participantes por feedback de evaluación.
- Mismas denegaciones, allowlists y límites de herramientas que sus snapshots.
  Es aislamiento de herramientas, no sandbox del sistema operativo.

Se conservan configuración, freeze, fuentes, prompts, trazas sanitizadas, entrega
y resultados. No se exporta razonamiento privado ni transporte raw, credenciales,
hosts, bases SQLite, dependencias instaladas o estáticos generados.

## Preflight e incidencias offline

Los cuatro tests focalizados del adaptador pasaron antes de preparar. Por cohorte
se verificaron igualdad de workspace inicial/perfiles, resolución real del modelo
y agente, skills aisladas y herramientas con servidor localhost guionado, sin
modelo. Originales43 y referencia56/52 pasan antes de congelar.

El comando `offline all` alcanzó el timeout de 120 s de la herramienta durante
el probe de sdd-high. Las tres cohortes previas ya estaban congeladas. El probe
interrumpido se preservó; sdd-high completó el preflight en
`runtime-probes-recovery`, con timeout del operador de 300 s. Cero inferencias
en ambos probes, sin reiniciar ninguna ejecución del modelo.

## Interpretación

n=1, orden fijo, cohortes posteriores y capacidades distintas. No concluir
superioridad universal, causalidad ni significación estadística. Más tests no
demuestran por sí solos mayor calidad. Tokens de preparación/investigador son
desconocidos, no cero; no se suman al rendimiento del participante.

No commits, push, instalación global ni cambios a canonical/generated/adapters.
