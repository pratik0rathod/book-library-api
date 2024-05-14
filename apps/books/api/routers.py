from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from apps.books import functions
from apps.books import schema, filters
from apps.users import auth
from database.base import get_async_db

books_router = APIRouter(
    prefix="/books",
    tags=["Librarian"],
)


@books_router.get("/count")
async def count_all_books(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()]
):
    return await functions.count_books(db=db, user=user)


@books_router.get(
    "/all",
    response_model=list[schema.BooksSchemaExtra] | list[schema.BooksSchema])
async def get_all_books(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()]
):
    return await functions.get_all_books(db=db, user=user)


@books_router.get(
    "/get/{book_id}",
    response_model=schema.BooksSchemaExtra | schema.BooksSchema
)
async def get_a_book(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book_id: int
):
    return await functions.get_a_book(db=db, user=user, book_id=book_id)


@books_router.get(
    "/search",
    response_model=list[schema.BooksSchemaExtra] | list[schema.BooksSchema]
)
async def search_book(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        search: Annotated[filters.FilterModelBook,
        Depends(filters.FilterModelBook)]
):
    return await functions.search_book(db, user=user, search=search)


@books_router.post("/create")
async def create_book_item(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book: schema.BooksSchema
):
    return await functions.create_book_item(db, user=user, book=book)


@books_router.put("/edit/{book_id}")
async def edit_book_item(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book_id: int, book: schema.BooksSchema
):
    return await functions.edit_book_item(db, user=user, book_id=book_id, book=book)


@books_router.delete("/delete/{book_id}")
async def delete_book_item(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        book_id: int
):
    return await functions.delete_book_item(db, user=user, book_id=book_id)
