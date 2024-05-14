from fastapi import APIRouter

from apps.books.urls import book_router
from apps.users.urls import users_routers

urls = APIRouter()

urls.include_router(users_routers)
urls.include_router(book_router)
