from apps.books.schema import BooksSchema, BookTransactionSchema
from apps.books.models import Books, BookTransaction
from apps.books.admin.view import BookTranscationView, BookView

book_view = BookView(
    model=Books,
    label="Books",
    icon="fa fa-book",
    pydantic_model=BooksSchema
)

book_transcation_view = BookTranscationView(
    model=BookTransaction,
    label="Borrow History",
    icon="fa fa-history",
    pydantic_model=BookTransactionSchema
)
