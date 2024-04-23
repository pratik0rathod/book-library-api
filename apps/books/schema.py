from pydantic import BaseModel
from datetime import date

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
    