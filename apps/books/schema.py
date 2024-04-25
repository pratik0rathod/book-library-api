from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi_filter.contrib.sqlalchemy import Filter
from apps.books import models

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
 
    
class FilterModelBook(Filter):
    title__like:Optional[str] = None
    author__like:Optional[str] = None
    ratings__gte:Optional[float] = None
    ratings__lte:Optional[float] = None
    is_available:Optional[bool]=None
    
    class Constants(Filter.Constants):
        model = models.Books
        search_field_name = "search"
        search_model_fields = ['title','author','ratings']


    
    
    