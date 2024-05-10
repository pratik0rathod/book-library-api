from datetime import date, datetime

from pydantic import BaseModel


class BooksSchema(BaseModel):
    title: str
    author: str
    isbn: str
    genre: str
    synopsis: str
    genre: list[str]
    is_available: bool
    publication_date: date
    ratings: float


class AddBookSchema(BooksSchema):
    added_by: int

class BooksSchemaExtra(BooksSchema):
    id: int
    added_by: int
    created_on: datetime
    last_updated: datetime

class BookInTransaction(BaseModel):
    id:int
    title: str
    author: str
    genre: list[str]


class BookTransactionSchema(BaseModel):
    id: int
    borrow_date: date
    due_date: date
    return_date: date
    book: BookInTransaction
