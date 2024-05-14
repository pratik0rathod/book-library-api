from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from apps.books import functions,schema
from apps.users import auth
from database.base import get_async_db

reader_router = APIRouter(
    tags=['Reader']
)


@reader_router.post('/borrow/{book_id}')
async def borrow_book(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book_id: int
):
    return await functions.borrow_book(db, user=user, book_id=book_id)


@reader_router.post('/return/{book_id}')
async def return_book(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book_id: int
):
    return await functions.return_book(db, user=user, book_id=book_id)


@reader_router.get(
    "/books/history",
    response_model=list[schema.BookTransactionSchema]
)
async def return_book_history(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()]
):
    return await functions.return_book_history(db, user=user)

