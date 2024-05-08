# import logging
from functools import reduce
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
# from fastapi_pagination.ext.sqlalchemy import paginate
from pydantic import BaseModel
from sqlalchemy import select, delete, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import nulls_last
from starlette import status

from database.base import Base

# from satori.core import errors
# from satori.core.exceptions import SatoriHTTPException


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# logger = logging.getLogger(__name__)


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
            getattr(self.model, "is_active") == True,
            getattr(self.model, "is_deleted") == False
        )

    async def is_exist(self, db: AsyncSession, **kwargs) -> Optional[ModelType]:
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
                # error_code=getattr(errors, f"{self.model_name.upper()}_ALREADY_EXISTS")
            )
        return True

    async def get(
            self, db: AsyncSession, id: int, raise_exc=True, **kwargs
    ) -> Optional[ModelType]:
        # logger.debug(
        #     f"Reading from %s, id: %s", self.model.__name__, id
        # )
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
                    # error_code=getattr(errors, f"NOT_FOUND")
                )
        return result

    async def filter_by(
            self, db: AsyncSession, is_reversed=False, raise_exc=True, join_tables: list = [],
            is_outer: bool = False, **kwargs
    ) -> Optional[ModelType]:
        # logger.debug(
        #     f"Reading from %s, kwargs: %s", self.model.__name__, kwargs
        # )
        query = await self._active_data(select(self.model))
        for join_table in join_tables:
            query = query.join(join_table,
                               isouter=is_outer)  # if is_outer is true then left join otherwise inner join
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
            join_tables: list = [],
            is_outer: bool = False,
            **kwargs
    ) -> List[ModelType]:
        # logger.debug(f"Reading data from {self.model.__name__}")
        query = await self._active_data(select(self.model))
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
        elif kwargs.get("order_by"):
            order_by = kwargs.get("order_by")
            query = query.order_by(
                nulls_last(desc(order_by) if kwargs.get("direction") == "desc" else order_by)
            )
        else:
            query = query.order_by(desc(getattr(self.model, "id")))
        # logger.debug('Query string: %s', query)

        if pagination:
            pass
            # results = await paginate(db, query)
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
        # obj_in_data = jsonable_encoder(obj_in)
        # logger.info(f'Creating {self.model.__name__} with kwargs: {obj_in}')
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
            # logger.exception(ex.orig.args)
            raise HTTPException(
                detail=str(ex.orig),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # logger.info(f'{self.model.__name__} created, data: {db_obj.__dict__}')
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            autocommit: bool = True
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        # logger.debug(f"Updating {self.model.__name__} with '{obj_in}' data")
        try:
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
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
            # logger.exception(ex.orig.args)
            raise HTTPException(
                detail=str(ex.orig),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        # logger.info(f'{self.model.__name__} updated, data: {db_obj.__dict__}')
        return db_obj

    async def remove(
            self, db: AsyncSession, *, autocommit: bool = True, **kwargs
    ) -> ModelType:
        # logger.debug(f"Deleting from {self.model.__name__}, id: '{id}'")
        query = await self.filter_by(db=db, **kwargs)
        query.is_deleted = True
        await db.commit()
        # logger.info(f'{self.model.__name__} deleted, id: {id}')
        return query

    async def hard_delete(
            self, db: AsyncSession, *, id: int, autocommit: bool = True
    ) -> ModelType:
        # logger.debug(f"Deleting from {self.model.__name__}, id: '{id}'")
        query = delete(self.model).filter(getattr(self.model, "id") == id)
        await db.execute(query)
        await db.commit()
        # logger.info(f'{self.model.__name__} deleted, id: {id}')
        return True

    async def remove_multi(
            self, db: AsyncSession, *, autocommit: bool = True, **kwargs
    ) -> bool:
        # logger.debug(f"Deleting from {self.model.__name__}, kwargs: {kwargs}")
        query = delete(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        # db.commit() if autocommit else db.flush()
        await db.execute(query)
        # logger.info(f'{self.model.__name__} deleted')
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
