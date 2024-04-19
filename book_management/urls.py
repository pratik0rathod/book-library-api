from fastapi import APIRouter

from . import user_router
from . import books_router

urls =  APIRouter()

urls.include_router(user_router)
urls.include_router(books_router)


