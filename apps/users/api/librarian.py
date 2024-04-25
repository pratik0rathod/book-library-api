from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.base import get_db

from apps.users import function,schema,auth

from apps.books.api.routers import books_router_common

librarian_router  = APIRouter(prefix='/readers',tags=['Librarian'])

librarian_router.include_router(books_router_common)

@librarian_router.get("/all",response_model=list[schema.RetriveUser])
async def get_all_readers(db:Annotated[Session,Depends(get_db)],userid:Annotated[auth.get_user,Depends()]):
    return function.get_all_reader(db,int(userid))

@librarian_router.get("/{reader_id}",response_model=schema.RetriveUser)
async def get_a_reader(db:Annotated[Session,Depends(get_db)],userid:Annotated[auth.get_user,Depends()],reader_id:int):
    return function.get_a_reader(db,int(userid),reader_id)

@librarian_router.patch("/{reader_id}/set-status")
async def set_status(db:Annotated[Session,Depends(get_db)],userid:Annotated[auth.get_user,Depends()],reader_id:int,active:bool= True):
    return function.set_status(db,int(userid),reader_id,active)

