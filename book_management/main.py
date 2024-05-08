from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from book_management.core.config import settings
from book_management.core.exceptions import ExceptionHandlerMiddleware
from .core.admin import admin
from .urls import urls

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET.get_secret_value()
)

app.add_middleware(ExceptionHandlerMiddleware)

app.include_router(urls)

admin.mount_to(app)
