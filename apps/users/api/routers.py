from typing import Annotated


from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.base import get_db

from apps.users import function,schema

user_router  = APIRouter(prefix='/user',tags=['User'])

@user_router.get("/")
async def get(db:Annotated[Session,Depends(get_db)]):
    return {"message":"please wait under developement"}

@user_router.post("/register")
async def register_user(db:Annotated[Session,Depends(get_db)],user:schema.UserRegister):
    return function.register_user(db,user)

@user_router.post("/login")
async def login_user(db:Annotated[Session,Depends(get_db)],user:Annotated[OAuth2PasswordRequestForm,Depends()]):
    return function.login_user(db,user)


@user_router.get("/me")
async def get_me():
    return function.get_me()
    