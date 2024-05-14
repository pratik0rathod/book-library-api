from fastapi import APIRouter

from apps.books.api import (
    reader,
    routers,
)

book_router = APIRouter()

book_router.include_router(reader.reader_router)
book_router.include_router(routers.books_router)
