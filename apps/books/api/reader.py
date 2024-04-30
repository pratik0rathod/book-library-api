from typing import Annotated
from fastapi import APIRouter,Depends

from apps.users import auth
from apps.books import functions,schema
from sqlalchemy.orm import Session

from database.base import get_db

reader_router =  APIRouter(
    tags=['Reader'] 
)

@reader_router.post('/borrow/{book_id}')
async def borrow_book(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book_id:int):
    return functions.borrow_book(db,user_id,book_id)

@reader_router.post('/return/{book_id}')
async def return_book(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()],book_id:int):
    return functions.return_book(db,user_id,book_id)

@reader_router.get("/books/history",response_model=list[schema.BookTransactionSchema])
async def return_book_history(db:Annotated[Session,Depends(get_db)],user_id:Annotated[auth.get_user,Depends()]):
    return functions.return_book_history(db,user_id)