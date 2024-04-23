from typing import Annotated,Any

from fastapi import APIRouter,Depends
from apps.books import functions
from sqlalchemy.orm import Session

from apps.users import auth
from apps.books import schema
from database.base import get_db

books_router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@books_router.get("/all")
async def get_all_books(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()]):
 
    return functions.get_all_books(db,user_id)
 
@books_router.get("/get/{book_id}")
async def get_a_book(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book_id:int):
    return functions.get_a_book(db,user_id,book_id)
 
@books_router.post("/create")
async def create_book_item(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book:schema.BooksSchema):
    return functions.create_book_item(db,user_id,book)
    
@books_router.put("/edit/{book_id}")
async def edit_book_item(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book_id:int,book:schema.BooksSchema):
    return functions.edit_book_item(db,user_id,book_id,book)

@books_router.delete("/delete/{book_id}")
async def delete_book_item(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book_id:int):
    return functions.delete_book_item(db,user_id,book_id)
