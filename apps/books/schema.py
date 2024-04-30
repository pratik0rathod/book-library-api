from pydantic import BaseModel
from datetime import date,datetime

class BooksSchema(BaseModel):
    
    title:str
    author:str
    isbn:str
    genre:str
    synopsis:str 
    genre:list[str] 
    is_available:bool
    publication_date: date
    ratings:float
    
class BooksSchemaExtra(BooksSchema):
    id:int
    added_by:int
    created_on:datetime
    last_updated:datetime


class BookInTransaction(BaseModel):
    title:str
    author:str
    genre:list[str]
    
class BookTransactionSchema(BaseModel):
    id:int
    borrow_date:date
    due_date:date
    return_date: date 
    book:BookInTransaction    
 
    

    
    
    