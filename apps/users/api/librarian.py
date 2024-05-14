from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio.session import AsyncSession
from database.base import get_async_db

from apps.users import function, schema, auth, filters

librarian_router = APIRouter(prefix='/readers', tags=['Librarian'])


@librarian_router.get("/all", response_model=list[schema.RetriveUser] |dict)
async def get_all_readers(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
):
    return await function.get_all_reader(db=db, user=user)


@librarian_router.get("/search", response_model=list[schema.RetriveUser]|dict)
async def search_reader(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        filers: Annotated[
            filters.FilterModelUser,
            Depends(filters.FilterModelUser)
        ]
):
    return await function.search_reader(
        db=db,
        user=user,
        filers=filers
    )


@librarian_router.get("/{reader_id}", response_model=schema.RetriveUser)
async def get_a_reader(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        reader_id: int
):
    return await function.get_a_reader(
        db=db,
        user=user,
        reader_id=reader_id
    )


@librarian_router.patch("/{reader_id}/set-status")
async def set_status(
        db: Annotated[AsyncSession, Depends(get_async_db)],
        user: Annotated[auth.get_user, Depends()],
        reader_id: int, active: bool = True
):
    return await function.set_status(
        db=db, user=user,
        reader_id=reader_id,
        active=active
    )
