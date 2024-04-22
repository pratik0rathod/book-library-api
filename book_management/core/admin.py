from typing import Any, Coroutine, Dict, Type

# from starlette_admin.contrib.sqla.converters import BaseSQLAModelConverter
from apps.users.auth import hash_password
from apps.users import models, function, schema, crud

from database import base
from fastapi.requests import Request
from fastapi import HTTPException

from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.views import CustomView
from starlette_admin.exceptions import FormValidationError

# from starlette.authentication import


class UserView(ModelView):

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

            if crud.check_username_update(db, data['username'],obj.id):
                errors['username'] = 'user with this use,rname is already exist'

            if crud.check_email_update(db, data['email'],obj.id):
                errors['email'] = 'user with this email id already exist'
                
            if len(errors) > 0:
                raise FormValidationError(errors)

        data.update({'password': hash_password(data['password'])})
        obj.password = data['password']

        return super().before_edit(request, data, obj)


admin = Admin(
    engine=base.engine,
    title='Admin',
    logo_url="https://preview.tabler.io/static/logo-white.svg",
    login_logo_url="`https://preview.tabler.io/static/logo.svg",
    index_view=CustomView(label="Home", icon="fa fa-home",),

)

admin.add_view(UserView(
    model=models.Users,
    label="Users",
    icon="fa fa-users",
    pydantic_model=schema.UserRegister
))
