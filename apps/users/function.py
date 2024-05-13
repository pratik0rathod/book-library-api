from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from apps.users import schema, models, auth, filters
from apps.users.crud import users_actions
from book_management.core.constant import UserEnum
from book_management.core.hash import hash_password, verify_password
from book_management.core.permission import role_permissions


def register_user(db: Session, user: schema.UserRegister):
    new_user = {
        'username': user.username,
        'email': user.email,
        'birth_date': user.birth_date,
        'password': hash_password(user.password)
    }

    errors: dict[str, str] = dict()

    if users_actions.filter_by(db, username=user.username, raise_exc=False):
        errors["username_error"] = "Username is already taken"

    if users_actions.filter_by(db, email=user.email, raise_exc=False):
        errors["useremail_error"] = "User with this email address is already registed"

    if len(errors) > 0:
        raise HTTPException(status_code=400, detail={"errors": errors})

    user_in = users_actions.create(db, obj_in=new_user)

    return user_in


def login_user(db: Session, user: schema.LoginUser):
    user_obj = users_actions.filter_by(
        db,
        username=user.username,
        raise_exc=False
    )

    if user_obj is not None:
        if verify_password(user.password, user_obj.password):
            if not user_obj.is_active or user_obj.soft_delete:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "account is disabled or deleted please"
                                 " contact libary staff or administrator"
                    }
                )

            return auth.create_token(({'sub': str(user_obj.id)}))

    raise HTTPException(
        status_code=400,
        detail={"error": "Username or password wrong"}
    )


def get_me(db: Session, user: models.Users):
    return jsonable_encoder(user)


def delete_me(db: Session, user: models.Users):
    user = users_actions.filter_by(
        db,
        raise_exc=False,
        username=user.username
    )

    for history in user.book_transaction:
        if history.return_date is None:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Book transaction still open please return books or contact staff"
                }
            )

    users_actions.update(
        db,
        db_obj=user,
        obj_in={
            'soft_delete': True,
        }
    )

    return {"message": "account deleted sucesfully"}


@role_permissions(roles=[UserEnum.LIBRARIAN])
def get_all_reader(db: Session, user: models.Users):
    users_obj = users_actions.get_multi(
        db,
        filters=False,
        sorting=False,
    )

    if users_obj is not None:
        return jsonable_encoder(users_obj)
    return {"message": "no user in database"}


@role_permissions(roles=[UserEnum.LIBRARIAN])
def get_a_reader(db: Session, user: models.Users, reader_id: int):
    users_obj = users_actions.get(db, reader_id)
    if users_obj is not None:
        return jsonable_encoder(users_obj)


@role_permissions(roles=[UserEnum.LIBRARIAN])
def set_status(db: Session, user: models.Users, reader_id: int, active: bool):
    users_obj = users_actions.get(db, reader_id)
    user_in = users_actions.update(
        db,
        db_obj=users_obj,
        obj_in={
            'is_active': active
        }
    )

    return user_in


@role_permissions(roles=[UserEnum.LIBRARIAN])
def search_reader(db: Session, user: models.Users, filers: filters.FilterModelUser):
    results = users_actions.get_multi(
        db,
        filters=True,
        filter_data=filers,
        sorting=False,
    )

    if len(results) == 0:
        return {"message": "No item found related to that term"}
    return jsonable_encoder(results)
