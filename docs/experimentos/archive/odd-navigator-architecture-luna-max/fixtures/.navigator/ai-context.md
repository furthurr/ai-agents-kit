# LocalLibrary — mapa de fuentes del baseline

Snapshot descriptivo del commit `3120b4302bf87a1b8c84d06662c2b8787f7da5f8`.
No es una aprobación de cambios ni una solución para tareas nuevas. Contrastar con disco.

## Localización por área
- Inventario y catálogo: `catalog/models.py` (Book, BookInstance, Author, Genre, Language).
- Evolución de esquema: `catalog/migrations/`; revisar hojas existentes antes de añadir.
- Rutas: `locallibrary/urls.py` monta `catalog/urls.py` bajo `/catalog/`.
- Vistas/listados y operaciones existentes: `catalog/views.py`.
- Formularios: `catalog/forms.py` (RenewBookForm); renovación: renew_book_librarian en views.
- Plantilla compartida: `catalog/templates/base_generic.html`.
- Detalle bibliográfico/ejemplares: `catalog/templates/catalog/book_detail.html`.
- Estilos locales: `catalog/static/css/styles.css`; la plantilla compartida usa Bootstrap.
- Pruebas originales: `catalog/tests/test_models.py`, `test_forms.py`, `test_views.py`.
- Guía de uso: `README.md`; contexto técnico del baseline: `docs/lab-context.md`.
- Restricciones y flujos observados: [índice arquitectónico](../.architecture/README.md).

## Consulta y comprobación
El baseline tiene43 tests; runner de aplicación: intérprete Python disponible +
`manage.py test catalog`. No se detectan `.data/` ni `.design/` en este snapshot:
usar estándares de dominio y fuentes directas, sin crear esas carpetas por consultarlas.
Este mapa no sustituye revisar consumidores cuando se modifique un helper compartido.
