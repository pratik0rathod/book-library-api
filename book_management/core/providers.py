from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette.responses import Response
from starlette_admin.auth import  AuthProvider
from starlette_admin.exceptions import LoginFailed
from fastapi.requests import Request
from apps.users import models, crud, auth
from database import base


class AdminUsernameAndPasswordProvider(AuthProvider):
    async def login(self, username: str, password: str, remember_me: bool, request: Request, response: Response) -> Response:

        with base.session_local() as db:
            user = crud.get_user_by_username(db, username)

            if user.user_type ==models.UserEnum.ADMIN:
                if user is not None:
                    if auth.verify_password(password, user.password):
                        request.session.update({"userid": user.id})
                        return response

            raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        with base.session_local() as db:
            user = crud.get_user_by_userid(
                db, request.session.get("userid", None)
                )

        if user is not None:
            request.state.user = user
            return True

        return False

    
    def get_admin_config(self, request: Request) -> AdminConfig | None:
        user = request.state.user 
        custom_app_title = "Hello, " +" user.username" + "!"  
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

