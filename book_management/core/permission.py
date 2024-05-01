from apps.users import crud, constant
from fastapi import HTTPException


def reguler_user_permission(func):
    def wrapper(*args, **kwargs):
        user = crud.get_user_by_userid(args[0], args[1])

        if user.user_type == constant.UserEnum.READER:
            raise HTTPException(status_code=401, detail={
                                "error": "You are not allowed to perform this action"})

        result = func(*args, **kwargs)
        return result
    return wrapper
