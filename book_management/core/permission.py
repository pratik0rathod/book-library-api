from apps.users.models import Users
from fastapi import HTTPException
from functools import wraps, update_wrapper
from fastapi import status


def role_permissions(roles: list | None | str):
    def decorator_perms(func):
        @wraps(func)
        async def wrapper_perms(*args, **kwargs):
            user: Users = kwargs['user']
            if user.user_type not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "You are not allowed to perform this action"
                    }
                )
            return await func(*args, **kwargs)
        return update_wrapper(wrapper_perms, func)
    return decorator_perms
