from fastapi.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser
from starlette_admin.auth import AuthProvider
from starlette_admin.exceptions import LoginFailed

from apps.users import models
from book_management.core.hash import verify_password
from database import base
from database.base import get_async_db
from book_management.core.constant import UserEnum
from apps.users.crud import users_actions


class AdminUsernameAndPasswordProvider(AuthProvider):
    async def login(
            self, username: str,
            password: str, remember_me: bool,
            request: Request, response: Response) -> Response:

        async with await anext(get_async_db()) as db:
            user: models.Users = await users_actions.filter_by(
                db, username=username,
                raise_exc=False
            )
            if user is not None:
                if user.user_type == UserEnum.ADMIN and user.is_active:
                    if verify_password(password, user.password):
                        request.session.update({"userid": user.id})
                        return response

            raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        
        async with await anext(get_async_db()) as db:
            user = await users_actions.get(
                db,
                request.session.get("userid", None),
                raise_exc=False
            )

            if user is not None:
                request.state.user = user
                return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig | None:
        user = request.state.user
        custom_app_title = "Hello, " + " user.username" + "!"
        return AdminConfig(
            app_title=custom_app_title,
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Retrieve current user
        photo_url = "https://avatar.iran.liara.run/public/40"
        return AdminUser(username=user.username, photo_url=photo_url)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
