from apps.users import crud
from fastapi import HTTPException
from functools import wraps, update_wrapper
from fastapi import status


def role_permissions(roles: list | None | str):
    def decorator_perms(func):
        @wraps(func)
        def wrapper_perms(*args, **kwargs):
            user = crud.get_user_by_userid(args[0], args[1])

            if user.user_type not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"error": "You are not allowed to perform this action"}
                )
            return func(*args, **kwargs)
        return update_wrapper(wrapper_perms, func)
    return decorator_perms
