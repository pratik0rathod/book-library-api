from fastapi import FastAPI 
from .urls import urls

app = FastAPI()

app.include_router(urls)

