from apps.users import crud
from fastapi import HTTPException
from functools import wraps, update_wrapper
from fastapi import status
from book_management.core import constant

def role_permissions(roles: list | None | str):
    def decorator_auth(func):
        @wraps(func)
        def wrapper_auth(*args, **kwargs):
            print(args)
            print(kwargs.get('user_id'))
            
            # user = crud.get_user_by_userid(kwargs['user_id'])

            # if user.user_type not in roles:
            #     raise HTTPException(
            #         status_code=status.HTTP_403_FORBIDDEN,
            #         detail={"error": "You are not allowed to perform this action"}
            #     )
            return func(*args, **kwargs)
        return update_wrapper(wrapper_auth, func)
    return decorator_auth
