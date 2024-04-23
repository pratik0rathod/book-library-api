from pydantic import BaseModel
from datetime import date

class BooksSchema(BaseModel):
    
    title:str
    author:str
    isbn:str
    publication_date: date
    ratings:float
    