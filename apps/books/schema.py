from pydantic import BaseModel

class BooksSchema(BaseModel):
    
    title:str
    author:str
    publication_date:str 
    ratings:str
