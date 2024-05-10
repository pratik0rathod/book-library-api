from apps.users.models import Users
from database.crud import CRUDBase
from pydantic import BaseModel

class CRUDUsers(CRUDBase[BaseModel, BaseModel, BaseModel]):
    ...
    
users_actions = CRUDUsers(Users)
