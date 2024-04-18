from fastapi import APIRouter

from . import user_router

urls =  APIRouter()

urls.include_router(user_router)

