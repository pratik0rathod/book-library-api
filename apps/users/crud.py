from pydantic import BaseModel

from apps.users.models import Users
from database.crud import CRUDBase


class CRUDUsers(CRUDBase[BaseModel, BaseModel, BaseModel]):
    ...


users_actions = CRUDUsers(Users)
