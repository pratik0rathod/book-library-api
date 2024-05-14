from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio.session import AsyncSession
from database.base import get_async_db

from apps.users import function, schema, auth

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.post("/register", response_model=schema.RetriveUser)
async def register_user(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: schema.UserRegister,
):

    return await function.register_user(db=db, user=user)


@user_router.post("/login")
async def login_user(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    return await function.login_user(db=db, user=user)


@user_router.get("/me", response_model=schema.RetriveUser)
async def get_me(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()]
):

    return await function.get_me(db=db, user=user)


@user_router.delete("/delete/me")
async def delete_me(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()]
):

    return await function.delete_me(db=db, user=user)
