from apps.books import models as book_model

from starlette_admin.contrib.sqla.ext.pydantic import ModelView


class BookView(ModelView):
    exclude_fields_from_edit = [
        book_model.Books.created_on,
        book_model.Books.last_updated,
    ]

    exclude_fields_from_create = [
        book_model.Books.created_on,
        book_model.Books.last_updated,
    ]


class BookTranscationView(ModelView):
    exclude_fields_from_edit = [
        book_model.BookTransaction.created_on,
        book_model.BookTransaction.last_updated
    ]

    exclude_fields_from_create = [
        book_model.BookTransaction.created_on,
        book_model.BookTransaction.last_updated,
        book_model.BookTransaction.due_date,
        book_model.BookTransaction.borrow_date,
    ]
