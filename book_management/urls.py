from fastapi import APIRouter

from apps.users.api.routers import user_router
from apps.users.api.librarian import librarian_router
from apps.books.api.routers import books_router
from apps.books.api.reader import reader_router

urls =  APIRouter()

urls.include_router(user_router)
urls.include_router(books_router)
urls.include_router(reader_router)
urls.include_router(librarian_router)


