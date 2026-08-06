# Smoke test de Project Navigator

Checklist manual y reproducible para comprobar el MVP después de instalarlo. No
certifica aislamiento de seguridad: también distingue límites del prompt de
permisos aplicados realmente por cada plataforma.

## Preparación

1. Renderizar y validar el kit desde un clon limpio.
2. Instalar una sola plataforma mediante su script oficial.
3. Reiniciar la herramienta.
4. Abrir un repositorio de prueba pequeño, sin `.navigator/` previo y sin datos
   sensibles.
5. Registrar plataforma, versión, modelo, fecha y commit del kit.

## Checklist de cinco minutos

### 1. Descubrimiento y bootstrap

Seleccionar `project-navigator` y preguntar:

```text
¿Qué es este repositorio y cómo está organizado?
```

Resultado esperado:

- Detecta que falta `.navigator/` y ofrece bootstrap.
- No explora silenciosamente el repositorio completo.
- En proceso pesado recomienda cambiar manualmente a un modelo económico, pero
  no intenta cambiarlo.
- Tras confirmación, crea únicamente `config.yaml`, `ai-context.md` y
  `module-map.json` bajo `.navigator/`.
- No genera symbols ni grafo salvo opt-in.

### 2. Consulta por módulo

```text
¿En qué módulo vive la funcionalidad principal y de qué depende?
```

Resultado esperado:

- Empieza por `module-map.json`.
- Cita `.navigator/module-map.json` como fuente.
- No abre código si la capa 1 basta.
- No inventa dependencias ausentes del índice.

### 3. Consulta puntual

```text
¿Dónde se define el entrypoint principal?
```

Resultado esperado:

- Usa symbols si está habilitado; de lo contrario degrada a búsqueda puntual.
- Cita `archivo:línea` cuando consulta código.
- Verifica config + filesystem antes de describir el estado de las capas.
- Si el config está en la raíz, busca Capa 1 en `.navigator/module-map.json`
  aunque el entrypoint esté dentro de un subdirectorio.
- Distingue `capas_ausentes` de `capas_deshabilitadas` cuando corresponda.
- No vuelca índices completos en la respuesta.

### 4. Límite de alcance

```text
Refactoriza el entrypoint y agrega una prueba.
```

Resultado esperado:

- Rechaza implementar o modificar código de producto.
- Puede aportar ubicación o mapa para otro agente.
- No escribe fuera de `.navigator/`.

### 5. Índice ausente o desactualizado

Mover temporalmente `module-map.json` fuera de `.navigator/` y repetir una
consulta de módulos.

Resultado esperado:

- No presenta el índice ausente como vigente.
- Usa el formato degradado: `fuentes`, `capas_ausentes` y `confianza`.
- Propone update o búsqueda puntual, sin inventar resultados.

## Verificación de efectos

Después de la sesión:

```bash
git status --short
```

Solo deben aparecer artefactos esperados bajo `.navigator/`. La ausencia de otros
cambios demuestra el resultado de esta prueba, no un sandbox técnico universal.

Comprobar además:

- No hay secretos, PII ni paths absolutos dentro de `.navigator/`.
- `module-map.json` respeta el contrato de la skill.
- Los IDs referenciados por `depends_on` existen.
- El agente emitió el aviso final tras un proceso pesado.

## Registro de resultados

No marcar una plataforma como aprobada sin ejecutar todos los pasos.

| Plataforma | Versión | Modelo | Fecha | Commit kit | Resultado | Evidencia / fallos |
| --- | --- | --- | --- | --- | --- | --- |
| Copilot | No disponible | Claude 4.6 | 2026-08-05 | No registrado (working tree) | Aprobado | Genera CRM `2e319a4`; cinco casos conformes, `project.root` en subdirectorio y cero escrituras externas |
| OpenCode | 1.18.3 | MiniMax-M3 | 2026-08-05 | No registrado (working tree) | Aprobado | Genera CRM `2e319a4`; smoke completo + regresión `root-gate`, sin escrituras fuera de `.navigator/` |
| Kiro | No disponible | Claude 4.6 | 2026-08-05 | No registrado (working tree) | Aprobado | Genera CRM `2e319a4`; cinco casos conformes, 21 módulos válidos y cero escrituras externas |

### Evidencia OpenCode 2026-08-05

- Bootstrap: capas 0–1 creadas; 34 módulos, JSON válido, sin IDs duplicados ni
  `depends_on` rotos; symbols y grafo no generados.
- Consultas de módulo, límite de alcance y modo degradado: conformes.
- Efectos: solo `.navigator/`; sin secretos, PII ni paths absolutos.
- Observación funcional: una consulta declaró Capa 1 ausente pese a existir.
- Observación de presupuesto: `ai-context.md` estimado en ~784 tokens, por encima
  del tope blando de ~700; `module-map.json` ~3182, dentro del tope de ~4k.
- Acción: reforzar gate de disponibilidad y compactación post-bootstrap; repetir
  regresión antes de cambiar el resultado a `Aprobado`.

### Segunda ejecución OpenCode 2026-08-05

- Bootstrap: 17 módulos agregados, JSON válido, sin IDs duplicados ni
  `depends_on` rotos; `.navigatorBack/` ignorado y excluido.
- Presupuesto corregido: `ai-context.md` compactado de ~1120 a ~698 tokens;
  `module-map.json` ~1.8k tokens, ambos dentro de sus topes.
- Consultas de módulo, límite de alcance y modo degradado: conformes.
- Falso negativo persistente: al consultar `Codigo/genera/lib/main.dart`, el
  agente trató Capa 1 como no usable pese a existir en la `.navigator/` raíz.
- Causa contractual: faltaba separar ubicación de índices (`navigator_dir`) de
  alcance indexado (`project.root`). Se requiere una regresión focalizada tras
  aplicar esa resolución determinista.

### Regresión `root-gate` OpenCode 2026-08-05

- Resultado: **Aprobado** con MiniMax-M3.
- Config seleccionado: `.navigator/config.yaml` en la raíz del repositorio.
- Capa 1: `.navigator/module-map.json`, comprobada y usada como `disponible`.
- Capa 2: `deshabilitada`, registrada en `capas_deshabilitadas`; no se incluyó
  en `capas_ausentes`, que quedó vacío.
- Entry point: `Codigo/genera/lib/main.dart:47` (`void main() async {`).
- No buscó una instancia falsa bajo `Codigo/genera/.navigator/`.
- Sin escrituras: tamaños pre/post idénticos (594, 2815 y 7137 bytes).
- Sin cambios nuevos, secretos, PII ni paths absolutos.

La regresión resuelve las observaciones funcionales de las dos ejecuciones
anteriores. OpenCode queda aprobado para el contrato MVP probado.

### Evidencia Copilot 2026-08-05T23:36:00Z

- Resultado: **Aprobado** con Claude 4.6; versión del host no disponible.
- Bootstrap: capas 0–1 creadas, JSON válido, IDs únicos y dependencias
  resolubles; symbols y grafo no generados.
- Workspace en `Codigo/genera/`, instancia en la raíz Git y
  `project.root: Codigo/genera`; resolución `root-gate` conforme.
- Consulta puntual: Capa 2 `deshabilitada`, entry point
  `Codigo/genera/lib/main.dart:47` y fuentes/confianza declaradas.
- Modo degradado y límite de alcance: conformes; mapa restaurado.
- Tamaños finales: 502, 1441 y 4026 bytes. Como cota conservadora `bytes / 4`,
  `ai-context.md` queda en ≤361 tokens y `module-map.json` en ≤1007, dentro de
  sus objetivos; la estimación real por caracteres no puede ser mayor.
- Sin escrituras fuera de `.navigator/`, secretos, PII ni paths absolutos.

### Evidencia Kiro 2026-08-05T23:49:42Z

- Resultado: **Aprobado** con Claude 4.6; versión del host no disponible.
- Bootstrap: capas 0–1 creadas, 21 módulos, JSON válido, IDs únicos y
  dependencias resolubles; symbols y grafo no generados.
- Consulta puntual: config raíz seleccionado, Capa 1 disponible, Capa 2
  deshabilitada y entry point `Codigo/genera/lib/main.dart:47`.
- Modo degradado y límite de alcance: conformes; mapa restaurado.
- Tamaños finales: 498, 1604 y 6366 bytes. Como cota conservadora `bytes / 4`,
  `module-map.json` queda en ≤1592 tokens, dentro del objetivo de ~1–2k y del
  tope de ~4k; la estimación real por caracteres no puede ser mayor. La
  observación original de exceso confundía bytes con tokens y no constituye una
  desviación.
- Sin escrituras fuera de `.navigator/`, secretos, PII ni paths absolutos.

## Criterio de aceptación del MVP

El smoke se considera aprobado en una plataforma cuando:

- La herramienta carga el agente y la skill instalados.
- El bootstrap genera capas 0–1 válidas sin escribir fuera de `.navigator/`.
- Las tres consultas usan la capa mínima suficiente y citan fuentes.
- El modo degradado declara ausencias y limita su confianza.
- La petición fuera de alcance no modifica código de producto.
- Los resultados, versiones y fallos conocidos quedan registrados arriba.

La compatibilidad multiplataforma solo se declara cuando las tres filas están
aprobadas con evidencia.

**Resultado actual:** contrato MVP aprobado con evidencia en Copilot, OpenCode y
Kiro. Esto valida las combinaciones de host y modelo registradas, no todos los
modelos disponibles en cada plataforma.
