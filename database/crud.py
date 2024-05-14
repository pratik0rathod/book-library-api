from functools import reduce
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, delete, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import nulls_last
from starlette import status

from database.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.model_name = reduce(
            lambda x, y: x + ('_' if y.isupper() else '') + y, self.model.__name__
        )
        self.id = "id"

    async def _active_data(self, query):
        return query.filter(
            # getattr(self.model, "is_active") == True,
            # getattr(self.model, "is_deleted") == False
        )

    async def is_exist(self, db: AsyncSession, **kwargs) -> Optional[ModelType] | bool:
        query = select(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                if kwargs.get("updated") and key == self.id:
                    query = query.filter(getattr(self.model, key) != value)
                else:
                    query = query.filter(getattr(self.model, key) == value)
        query = await db.execute(query)
        exists = query.scalars().first()
        if exists:
            raise HTTPException(
                detail=f"{self.model_name.replace('_', ' ')} already exists",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return True

    async def get(
            self, db: AsyncSession, id: int, raise_exc=True, **kwargs
    ) -> Optional[ModelType]:
        query = (await self._active_data(select(self.model))).filter(
            getattr(self.model, self.id) == id
        )
        query = await db.execute(query)
        result = query.scalars().first()
        if not result:
            if raise_exc:
                raise HTTPException(
                    detail=f"{self.model_name.replace('_', ' ')} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                )

        return result

    async def filter_by(
            self, db: AsyncSession, is_reversed=False, raise_exc=True, join_tables: list = [],
            is_outer: bool = False, joined_load=None, **kwargs,

    ) -> Optional[ModelType]:
        query = await self._active_data(select(self.model))
        for join_table in join_tables:
            query = query.join(  # if is_outer is true then left join otherwise inner join
                join_table,
                isouter=is_outer
            )

        for key, value in kwargs.items():
            if hasattr(self.model, key):
                if isinstance(value, list):
                    query = query.filter(getattr(self.model, key).in_(value))
                else:
                    query = query.filter(getattr(self.model, key) == value)
            if key == "inner_filter":
                query = query.filter(value)
        if is_reversed:
            query = query.order_by(desc(getattr(self.model, "id")))

        if joined_load is not None:
            query = query.options(
                joinedload(
                    joined_load
                )
            )

        query = await db.execute(query)
        result = query.scalars().first()
        if not result:
            if raise_exc:
                raise HTTPException(
                    detail=f"{self.model_name.replace('_', ' ')} not found",
                    status_code=status.HTTP_404_NOT_FOUND,
                    # error_code=getattr(errors, f"NOT_FOUND")
                )

        return result

    async def get_multi(
            self,
            db: AsyncSession, *,
            filter_data=None,
            sorting: bool = True,
            filters: bool = True,
            pagination: bool = True,
            join_tables: list = None,
            is_outer: bool = False,
            joined_load=None,
            **kwargs
    ) -> List[ModelType] | Any:

        query = await self._active_data(select(self.model))
        if join_tables is not None:
            for join_table in join_tables:
                query = query.join(join_table, isouter=is_outer)

        for key, value in kwargs.items():
            if hasattr(self.model, key) and value:
                if isinstance(value, list):
                    query = query.filter(getattr(self.model, key).in_(value))
                else:
                    query = query.filter(getattr(self.model, key) == value)
            if key == "inner_filter":
                value = [value] if not isinstance(value, list) else value
                query = query.filter(*value)
        if filters:
            query = filter_data.filter(query)
        if sorting:
            query = filter_data.sort(query)

        # will refactor this and add for more dynamic options
        if joined_load is not None:
            query = query.options(
                joinedload(
                    joined_load
                )
            )

        elif kwargs.get("order_by"):
            order_by = kwargs.get("order_by")
            query = query.order_by(
                nulls_last(desc(order_by) if kwargs.get(
                    "direction") == "desc" else order_by)
            )
        else:
            query = query.order_by(desc(getattr(self.model, "id")))

        if pagination:
            pass
        else:
            pass
        query = await db.execute(query)
        results = query.unique().scalars().all()
        return results

    async def create(
            self, db: AsyncSession, *,
            obj_in: Union[Dict[str, Any], CreateSchemaType],
            autocommit: bool = True,
    ) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            db.add(db_obj)
            if autocommit:
                await db.commit()
                await db.refresh(db_obj)
            else:
                await db.flush()
        except IntegrityError as ex:
            await db.rollback()
            raise HTTPException(
                detail=str(ex.orig),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return obj_in

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            autocommit: bool = True
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            if autocommit:
                await db.commit()
                await db.refresh(db_obj)
            else:
                await db.flush()
        except IntegrityError as ex:
            await db.rollback()
            raise HTTPException(
                detail=str(ex.orig),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return db_obj

    async def remove(
            self, db: AsyncSession, *, autocommit: bool = True, **kwargs
    ) -> ModelType:
        query = await self.filter_by(db=db, **kwargs)
        query.is_deleted = True

        await db.commit()
        return query

    async def hard_delete(
            self, db: AsyncSession, *, id: int, autocommit: bool = True
    ) -> bool | Any:
        query = delete(self.model).filter(getattr(self.model, "id") == id)
        result = await db.execute(query)
        if autocommit:
            await db.commit()
            return True
        return result

    async def remove_multi(
            self, db: AsyncSession, *, autocommit: bool = True, **kwargs
    ) -> bool:
        query = delete(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        await db.execute(query)
        return True

    async def count(self, db, **kwargs):
        query = await self._active_data(select(func.count(self.model.id)))
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                if isinstance(value, list):
                    query = query.filter(getattr(self.model, key).in_(value))
                else:
                    query = query.filter(getattr(self.model, key) == value)
            if key == "inner_filter":
                query = query.filter(*value)
        count = (await db.execute(query)).unique().scalars().first()
        return count
