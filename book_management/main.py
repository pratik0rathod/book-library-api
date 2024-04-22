from fastapi import FastAPI 
from .urls import urls
from .core.admin import admin
from starlette.middleware.sessions import SessionMiddleware
from config import db_settings
app = FastAPI()


app.add_middleware(SessionMiddleware,secret_key= db_settings.SESSION_SECRET.get_secret_value())

app.include_router(urls)

admin.mount_to(app)
