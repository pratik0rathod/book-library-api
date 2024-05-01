from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.base import get_db

from apps.users import function, schema, auth, filters

librarian_router = APIRouter(prefix='/readers', tags=['Librarian'])


@librarian_router.get("/all", response_model=list[schema.RetriveUser])
async def get_all_readers(
        db: Annotated[Session, Depends(get_db)],
        userid: Annotated[auth.get_user, Depends()]):
    return function.get_all_reader(db, int(userid))


@librarian_router.get("/search", response_model=list[schema.RetriveUser])
async def search_reader(
        db: Annotated[Session, Depends(get_db)],
        userid: Annotated[auth.get_user, Depends()],
        filers: Annotated[filters.FilterModelUser,
                          Depends(filters.FilterModelUser)]):
    return function.search_reader(db, int(userid), filers)


@librarian_router.get("/{reader_id}", response_model=schema.RetriveUser)
async def get_a_reader(
        db: Annotated[Session, Depends(get_db)],
        userid: Annotated[auth.get_user, Depends()],
        reader_id: int):
    return function.get_a_reader(db, int(userid), reader_id)


@librarian_router.patch("/{reader_id}/set-status")
async def set_status(
        db: Annotated[Session, Depends(get_db)],
        userid: Annotated[auth.get_user, Depends()],
        reader_id: int, active: bool = True):
    return function.set_status(db, int(userid), reader_id, active)
