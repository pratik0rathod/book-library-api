from typing import Any, Coroutine, Dict

from fastapi.requests import Request
from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from starlette_admin.exceptions import FormValidationError

from apps.users import models as user_model
from apps.users.crud import users_actions
from book_management.core.hash import hash_password
from database import base


class UserView(ModelView):
    exclude_fields_from_list = [
        user_model.Users.password
    ]

    exclude_fields_from_edit = [
        user_model.Users.created_on,
        user_model.Users.last_updated,
        user_model.Users.added_by_admin,
    ]

    exclude_fields_from_create = [
        user_model.Users.created_on,
        user_model.Users.last_updated,
        user_model.Users.added_by_admin,
        user_model.Users.soft_delete,
        user_model.Users.is_active,
        user_model.Users.added_books,
        user_model.Users.book_transaction
    ]

    exclude_fields_from_detail = [
        user_model.Users.password
    ]

    # override the default query
    def get_list_query(self):
        return super().get_list_query().where(
            user_model.Users.user_type != user_model.UserEnum.ADMIN
        )

    def get_count_query(self):
        return super().get_count_query().where(
            user_model.Users.user_type != user_model.UserEnum.ADMIN
        )

    async def before_create(
            self, request: Request, data: Dict[str, Any],
            obj: user_model.Users
    ) -> Coroutine[Any, Any, None]:
        errors: Dict[str, str] = dict()

        with base.session_local() as db:
            if users_actions.filter_by(db, username=data['username'], raise_exc=False):
                errors['username'] = 'user with this username is already exist'

            if users_actions.filter_by(db, email=data['email'], raise_exc=False):
                errors['email'] = 'user with this email id already exist'

            if len(errors) > 0:
                raise FormValidationError(errors)

        data.update({'password': hash_password(data['password'])})

        obj.password = data['password']

        obj.added_by_admin = True
        return await super().before_create(request, data, obj)

    async def before_edit(
            self, request: Request,
            data: Dict[str, Any],
            obj: user_model.Users
    ) -> Coroutine[Any, Any, None]:
        errors: Dict[str, str] = dict()

        with base.session_local() as db:

            if users_actions.filter_by(db, username=data['username'], raise_exc=False):
                errors['username'] = 'user with this username is already exist'

            if users_actions.filter_by(db, email=data['email'], raise_exc=False):
                errors['email'] = 'user with this email id already exist'

            if len(errors) > 0:
                raise FormValidationError(errors)

        return await super().before_edit(request, data, obj)

    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        obj = await self.find_by_pk(request, pk)

        if obj.password != data['password']:
            data.update({'password': hash_password(data['password'])})

        return await super().edit(request, pk, data)
