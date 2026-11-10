# LocalLibrary — arquitectura observada del baseline

Snapshot descriptivo, no diseño nuevo ni lista de requisitos añadidos.
Fuentes: `catalog/models.py`, `catalog/views.py`, `catalog/urls.py`, plantillas y
`docs/lab-context.md` del baseline documentado.

- Django con vistas servidor y Templates; `catalog.models` usa el ORM.
- `Book` describe una obra; `BookInstance` un ejemplar con UUID, estado, borrower y due_back.
- Rutas y vistas están centralizadas en catalog; las vistas existentes consultan ORM.
- Formularios HTML usan el mecanismo de formularios de Django; auth y permisos se
  aplican mediante decoradores o mixins. No asumir que un permiso global es de otro módulo.
- El baseline usa SQLite local y migraciones Django; el catálogo no usa un framework REST externo.
- Preservar contratos observables existentes y verificar consumidores de fuentes compartidas.
  No crear capas, paquetes o servicios solo porque exista este índice.

## Lectura bajo demanda
- [Flujos existentes: navegación, listados y renovación](flows.md).
- Para campos y restricciones concretos, abrir el modelo relevante en código.
- Para instrucciones de ejecución originales, consultar README del proyecto.

No se declara una ADR nueva ni una solución de concurrencia. Estas notas registran
solo lo que ya existe y no autorizan cambios documentales o de producto.
