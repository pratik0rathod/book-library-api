from fastapi import APIRouter

from apps.users.api.librarian import librarian_router
from apps.users.api.routers import user_router

users_routers = APIRouter()

users_routers.include_router(user_router)
users_routers.include_router(librarian_router)
