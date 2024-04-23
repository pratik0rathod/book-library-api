from typing import Any, Coroutine, Dict

from apps.users.auth import hash_password
from apps.users import models, crud

from database import base
from fastapi.requests import Request

from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

class UserView(ModelView):
    exclude_fields_from_list = [models.Users.password]
    exclude_fields_from_edit = [models.Users.created_on,models.Users.last_updated]
    exclude_fields_from_create = [models.Users.created_on,models.Users.last_updated]
    exclude_fields_from_detail = [models.Users.password]
   
    async def before_create(self, request: Request, data: Dict[str, Any], obj: models.Users) -> Coroutine[Any, Any, None]:
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
        
        return super().before_create(request, data, obj)

    async def before_edit(self, request: Request, data: Dict[str, Any], obj: models.Users) -> Coroutine[Any, Any, None]:
        errors: Dict[str, str] = dict()

        with base.session_local() as db:

            if crud.check_username_update(db, data['username'], obj.id):
                errors['username'] = 'user with this use,rname is already exist'

            if crud.check_email_update(db, data['email'], obj.id):
                errors['email'] = 'user with this email id already exist'

            if len(errors) > 0:
                raise FormValidationError(errors)

        data.update({'password': hash_password(data['password'])})
        obj.password = data['password']

        return super().before_edit(request, data, obj)

class BookView(ModelView):
    exclude_fields_from_edit = [models.Books.created_on,models.Books.last_updated]
    exclude_fields_from_create = [models.Books.user,models.Books.created_on,models.Books.last_updated]
    
    