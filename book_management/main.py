from fastapi import FastAPI 
from .urls import urls
from .core.admin import admin
app = FastAPI()

app.include_router(urls)

admin.mount_to(app)
