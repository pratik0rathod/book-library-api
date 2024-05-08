from apps.books.admin.view import BookTransactionView, BookView
from apps.books.models import Books, BookTransaction
from apps.books.schema import BooksSchema, BookTransactionSchema

book_view = BookView(
    model=Books,
    label="Books",
    icon="fa fa-book",
    pydantic_model=BooksSchema
)

book_transaction_view = BookTransactionView(
    model=BookTransaction,
    label="Borrow History",
    icon="fa fa-history",
    pydantic_model=BookTransactionSchema
)
