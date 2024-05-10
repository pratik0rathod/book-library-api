from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.base import get_db

from apps.users import function, schema, auth

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.post("/register",response_model=schema.RetriveUser)
async def register_user(
        db: Annotated[Session, Depends(get_db)],
        user: schema.UserRegister,
):
    return function.register_user(db=db, user=user)


@user_router.post("/login")
async def login_user(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return function.login_user(db=db, user=user)


@user_router.get("/me", response_model=schema.RetriveUser)
async def get_me(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[auth.get_user, Depends()]
):
    return function.get_me(db=db, user=user)


@user_router.delete("/delete/me")
async def delete_me(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[auth.get_user, Depends()]
):
    return function.delete_me(db=db, user=user)
