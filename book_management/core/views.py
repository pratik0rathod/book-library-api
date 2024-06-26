from typing import Any, Coroutine, Dict

from apps.users.auth import hash_password
from apps.users import models as user_model, crud
from apps.books import models as book_model

from database import base
from fastapi.requests import Request

from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin import PasswordField, RequestAction

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

class UserView(ModelView):

    exclude_fields_from_list = [user_model.Users.password]

    exclude_fields_from_edit = [user_model.Users.created_on,
                                user_model.Users.last_updated,
                                user_model.Users.added_by_admin,
                                ]

    exclude_fields_from_create = [user_model.Users.created_on,
                                  user_model.Users.last_updated,
                                  user_model.Users.added_by_admin,
                                  ]

    exclude_fields_from_detail = [user_model.Users.password]

    # overide the default query
    def get_list_query(self):
        return super().get_list_query().where(user_model.Users.user_type != user_model.UserEnum.ADMIN)

    def get_count_query(self):
        return super().get_count_query().where(user_model.Users.user_type != user_model.UserEnum.ADMIN)

    async def before_create(self, request: Request, data: Dict[str, Any], obj: user_model.Users) -> Coroutine[Any, Any, None]:
        errors: Dict[str, str] = dict()

        with base.session_local() as db:
            if crud.check_username(db, data['username']):
                errors['username'] = 'user with this username is already exist'

            if crud.check_email(db, data['email']):
                errors['email'] = 'user with this email id already exist'

            if len(errors) > 0:
                raise FormValidationError(errors)
        
        data.update({'password': hash_password(data['password'])})

        obj.password = data['password']

        obj.added_by_admin = True
        return super().before_create(request, data, obj)
    
    async def before_edit(self, request: Request, data: Dict[str, Any], obj: user_model.Users) -> Coroutine[Any, Any, None]:
        errors: Dict[str, str] = dict()

        with base.session_local() as db:

            if crud.check_username_update(db, data['username'], obj.id):
                errors['username'] = 'user with this use,rname is already exist'

            if crud.check_email_update(db, data['email'], obj.id):
                errors['email'] = 'user with this email id already exist'

            if len(errors) > 0:
                raise FormValidationError(errors)
            
        return super().before_edit(request, data, obj)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        obj = await self.find_by_pk(request, pk)
           
        if obj.password != data['password']:
            data.update({'password': hash_password(data['password'])})
            
        return await super().edit(request, pk, data)
    
    
class BookView(ModelView):
    exclude_fields_from_edit = [
        book_model.Books.created_on, book_model.Books.last_updated]
    exclude_fields_from_create = [
        book_model.Books.created_on, book_model.Books.last_updated]


class BookTranscationView(ModelView):
    exclude_fields_from_edit = [
        book_model.BookTransaction.created_on, book_model.BookTransaction.last_updated]

    exclude_fields_from_create = [book_model.BookTransaction.created_on,
                                  book_model.BookTransaction.last_updated,
                                  book_model.BookTransaction.due_date,
                                  book_model.BookTransaction.borrow_date,
                                  ]
