# Núcleo breve de skills + referencias — prueba exploratoria

**Terminado: una pareja nueva de TASK-2 Alta, ambas funcionales y con criterios
técnicos consultados. No hubo ahorro global: núcleo/referencias +165,57% tokens
y +83,45% duración en esta ejecución.** La hipótesis de eficiencia no se confirma
en esta muestra; no adoptar este prototipo como optimización demostrada.

Modelo solicitado `openai/gpt-6-luna`, CLI `--variant max`, timeout1800s simétrico.
ID `odd-domain-core-luna-max-v1`. No se reutilizaron cifras de ensayos anteriores.

## 1. Qué se probó y qué se preservó

El mismo procedimiento **ODD ajustado con estándares** en ambos perfiles. Solo
cambia cómo se entrega el contexto de data-api/ui-design:

- Control: SKILL completa original.
- Tratamiento: mismo frontmatter, [núcleo breve](nucleo.md), `implementation.md`
  con secciones técnicas originales, `documentation.md` con flujo documental y
  `original-contract.md` como respaldo íntegro, en el mismo directorio para conservar enlaces.
- Plantillas/referencias originales conservadas. Ninguna sección se resumió ni
  eliminó: [manifest de partición](evidencia/partition-manifest.json) por encabezado
  y SHA256, y reconstrucción literal comprobada por tests.
- Núcleo exige leer implementation ANTES de trabajar; documentación solo con
  intención autorizada y fallback íntegro disponible si hace falta.
- Proyecto, tarea, permisos, referencia y oráculos idénticos para ambos. No se
  añadieron `.navigator`/`.architecture`, subagentes ni recuperación externa. El
  experimento de navegación anterior queda descartado, pero su evidencia se conserva.

## 2. La reducción de texto sí ocurrió

| Fuente experimental, bytes UTF-8 | API/datos | UI/diseño |
|---|---:|---:|
| SKILL original | 12.395 | 11.270 |
| Nuevo núcleo con frontmatter | 1.494 | 1.464 |
| Criterios de implementación | 6.004 | 5.638 |
| Flujo documental diferido | 6.120 | 5.391 |

Núcleo+implementación suman14.600 bytes frente a23.665 originales. Estos son tamaños
de archivos, no tokens estimados. El respaldo original conserva el mismo contenido
completo y no se considera borrado por mover secciones a referencias.

Los criterios incluyen identidad/límites, aplicabilidad/intención, estándares,
fuentes tecnológicas, implementación, índice contextual y reglas; UI también el
checklist visual. Las secciones restantes de estructura/modos/bootstrap/sync quedan
en documentación. Los textos siguen siendo autoridad: la partición no garantiza
que un modelo interprete igual fragmentos entregados en otro orden/contexto.

## 3. El agente sí leyó los criterios

En el tratado se verificó el contenido completo devuelto por read, normalizando
solo numeración de líneas/presentación, no aceptando una mención del archivo:

| Consulta tratada | Observación |
|---|---|
| Core data-api / ui-design | Ambos cargados por contenido |
| implementation data-api | Una lectura completa; evento10 |
| implementation ui-design | Una lectura completa; evento11 |
| Primer cambio de producto | Evento53, después de ambas referencias |
| documentation.md | Cero lecturas en ambos dominios |
| original-contract.md | Cero lecturas en ambos dominios |

El control recibió los criterios en las skills completas antes de modificar.
No se ahorró por omitir estándares ni se penalizó al tratado por usar un fallback:
simplemente no lo necesitó. La exposición por contenido es verificable, pero no
equivale a auditoría exhaustiva de aplicación de todos los estándares.

## 4. Resultado de la única pareja

| Medida | Skills completas | Núcleo + referencias |
|---|---:|---:|
| Conversación terminada y sana | Sí | Sí |
| Oráculos externos | 9/9 | 9/9 |
| catalog restaurado + tests añadidos | Pasa | Pasa |
| Criterios consultados antes de producto | Sí | Sí |
| Tokens comparables | **1.226.103** | 3.256.195 |
| Duración conversacional (s) | **631,329** | 1.158,198 |
| Herramientas | **48** | 77 |
| Eventos de pasos con métricas | **22** | 45 |
| Lecturas completadas | **19** | 20 |
| Búsquedas/listados completados | **2** | 11 |
| Seguimiento ODD creado | Ninguno | odd/tasks/reservation-flow.md |

Incremento observado: **+165,57% tokens y +83,45% tiempo**. El lote tardó1.172,014s
de reloj con coordinación/evaluación. No hubo error API ni timeout. Preparación,
preflights y checks externos están fuera de las conversaciones. Comparables=
input+cache_read+cache_write+output, reasoning separado; no es facturación.

## 5. Por qué menor SKILL no dio menor consumo total

El contenido devuelto por herramientas skill sí bajó de31.324 a11.639 bytes. Tras
sumar12.969 bytes de lecturas técnicas, skill+criterios fue24.608 frente a31.324:
hubo menos contexto directo de dominio en ese subconjunto medido.

Sin embargo, la ejecución tratada siguió una trayectoria más larga:45 vs22 eventos
de paso,11 vs2 búsquedas y un registro ODD que el control no creó. El volumen medido
de salidas read+búsquedas+skills acabó siendo146.667 frente a141.895 bytes. Ese
subconjunto no es todo el contexto, pero muestra que la reducción local no se
convirtió en reducción global de recuperación. El contexto permanece en turnos
posteriores; más pasos importan al sumar input/cache del SDK.

También varió el razonamiento registrado (37.306 vs19.604), las pruebas y decisiones
de implementación. **No se aisló causalmente qué parte genera el incremento**:
el registro no fue una obligación nueva, y el procedimiento ODD principal era el
mismo. Una pareja no prueba que la partición cause siempre sobrecoste; sí impide
vender este prototipo como ahorro validado. No atribuir todo a dos lecturas extra.

## 6. Disciplina y cierre

Ambos identificaron que README no enumera reservas, lo conservaron intacto y
propusieron al usuario una actualización mediante selección manual de
`documentation-orchestrator`. No se ejecutó el orquestador. El tratado no cargó
el flujo documental completo para hacer esa recomendación: el cierre siguió
independiente de leer instrucciones de bootstrap/sync.

No se crearon carpetas canónicas ni mapas, ni se instalaron dependencias/agentes.
El tratado creó una nota ODD; un archivo no prueba por sí solo sobreingeniería,
pero ese seguimiento y sus pasos forman parte del coste y no se excluyen.
Los oráculos no certifican seguridad, diseño visual ni todas las responsabilidades
del MAS. Los criterios están preservados literalmente, no declarados equivalentes
por una simple compresión del texto.

## 7. Decisión recomendada

**No integrar esta partición en producción por motivos de ahorro con la evidencia
actual.** Mantener intactos los agentes/skills instalados y el diseño seleccionado
de Developer. La organización por intención funcionó; la ventaja de consumo no.

Si se quiere continuar investigando, conviene primero obtener más observaciones
comparables o estudiar una recuperación realmente más acotada; no añadir otra
capa o subagente suponiendo que será gratis. No ejecutar otra batería automáticamente.
No mezclar las cifras con navegación, Gemini o el ensayo de tres repeticiones.

## Evidencia

- [Protocolo previo](protocolo.md), [copia congelada](evidencia/protocol.md).
- [Resultado y auditoría de criterios](evidencia/summary-final.json).
- [Partición sin pérdida](evidencia/partition-manifest.json).
- [Core API/datos compilado](evidencia/domain-profiles/data-api/SKILL.md),
  [criterios API](evidencia/domain-profiles/data-api/implementation.md),
  [flujo documental API](evidencia/domain-profiles/data-api/documentation.md).
- [Core visual compilado](evidencia/domain-profiles/ui-design/SKILL.md),
  [criterios visuales](evidencia/domain-profiles/ui-design/implementation.md),
  [flujo documental visual](evidencia/domain-profiles/ui-design/documentation.md).
- [Freeze](evidencia/freeze.json), [preflights](evidencia/preflight.json),
  [referencia43+9](evidencia/reference-proof.json), [contratos](evidencia/cases.json).
- [Tratamientos](evidencia/treatments.json), [lote](evidencia/batch-result.json).
- [Verificaciones](verificaciones.json), [laboratorio](laboratorio.tar.gz),
  [manifest de hashes](preservacion.json).

Código: `tools/odd_domain_core.py`, `tools/odd_domain_core_report.py` y sus pruebas.
La fuente de estándares es la distribución previa congelada, con nombres de perfil
aislados; las fuentes canónicas de skills no se editaron. Los bloques `underlying`
del JSON conservan el esquema heredado de tres repeticiones y controles originales;
para esta pareja usar las etiquetas y estado del nivel superior, esperado2 celdas.

Se preservan entradas, versiones completas de criterios, oráculos, snapshots y
trazas saneadas. Credenciales, venv, Git y bases SQLite no se incluyen. Reproducción
requiere revisar rutas, recrear dependencias/estáticos y usar raíz/congelación nueva.
Permisos del host no son sandbox OS. Sin commits/push ni modificaciones del plan
del Escritorio o documentación canónica del kit.
