# Flujos existentes — referencias acotadas

## Catálogo y ejemplares
`catalog/urls.py` → vistas genéricas en `catalog/views.py` → Book/BookInstance en
`catalog/models.py` → plantillas `catalog/templates/catalog/`.
Las listas de libros y ejemplares y el detalle bibliográfico usan las clases
BookListView, BookInstanceListView y BookDetailView respectivamente.

## Préstamos y renovación
LoanedBooksByUserListView limita préstamos al usuario; LoanedBooksAllListView exige
`catalog.can_mark_returned`. `renew_book_librarian` exige login y ese permiso, valida
RenewBookForm, actualiza due_back y redirige a `all-borrowed`. Plantilla asociada:
`catalog/templates/catalog/book_renew_librarian.html`.

No asumir que una nueva ruta cubre consumidores existentes: revisar usos reales
de los modelos y funciones que se modifiquen. No se prescribe comportamiento nuevo.
