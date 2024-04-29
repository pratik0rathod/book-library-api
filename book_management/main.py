from fastapi import FastAPI 
from .urls import urls
from .core.admin import admin
from starlette.middleware.sessions import SessionMiddleware
from book_management.core.config import settings
app = FastAPI()


app.add_middleware(SessionMiddleware,secret_key= settings.SESSION_SECRET.get_secret_value())

app.include_router(urls)

admin.mount_to(app)
