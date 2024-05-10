from apps.books.models import BookTransaction,Books
from database.crud import CRUDBase
from pydantic import BaseModel

class CRUDBooks(CRUDBase[Books,BaseModel,BaseModel]):
    ...

class CRUDBookTransaction(CRUDBase[BookTransaction,BaseModel,BaseModel]):
    ...
    
book_action = CRUDBooks(Books)
book_transaction_action = CRUDBookTransaction(BookTransaction)
