from fastapi import APIRouter

from apps.users.urls import users_routers
from apps.books.urls import book_router

urls =  APIRouter()

urls.include_router(book_router)
urls.include_router(users_routers)


