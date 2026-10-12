# Plantilla de plan de Developer

Usa este formato para PLAN o para un cambio que requiera aprobación. Omite los
apartados no aplicables, pero explica por qué cuando el impacto esperado no sea obvio.

```markdown
## Plan de implementación

### Objetivo
- Resultado que quiere el usuario y quién lo utiliza.
- Comportamiento esperado; criterios de aceptación observables.

### Estado actual y evidencia
- Comportamiento implementado hoy, con rutas y referencias concretas.
- Documentación consultada y su confianza; límites encontrados.

### Alcance
- Incluye: pantallas, reglas de negocio, contratos, datos y módulos afectados.
- Excluye: áreas que no son necesarias para cumplir el objetivo.

### Impacto e implicaciones
- Cambios por capa y dependencias entre ellos.
- Compatibilidad, persistencia/migraciones, UX/accesibilidad, seguridad y rendimiento,
  solo cuando correspondan.
- Riesgos, decisiones pendientes y recomendación con su motivo.

### Secuencia
1. ...
2. ...

### Verificación
- Pruebas y checks esperados; criterio de éxito y limitaciones conocidas.

### Documentación potencialmente afectada
- Rutas candidatas y motivo. La actualización se confirma al revisar el diff final.

¿Apruebas este alcance y plan para comenzar la implementación?
```

## Preguntas esenciales

Pregunta cuando la respuesta del usuario pueda cambiar el comportamiento, los datos,
la compatibilidad, el costo, el riesgo o el alcance. Expón la consecuencia concreta
y, si hay una recomendación, identifícala como tal. No conviertas decisiones internas
reversibles y cubiertas por patrones existentes en preguntas para el usuario.

Ejemplo: «¿Al borrar la cuenta debemos eliminar sus datos o desactivarla? El borrado
afecta datos relacionados y puede ser irreversible; recomiendo desactivación si se
necesita conservar historial».
