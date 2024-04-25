from typing import Optional

from pydantic import BaseModel,EmailStr
from datetime import date
from apps.users import models
from fastapi_filter.contrib.sqlalchemy import Filter


class User(BaseModel):
    username : str

class RetriveUser(User):
    id:int
    birth_date: date
    email:EmailStr
  
class UserRegister(RetriveUser):
    password: str
    
class LoginUser(User):
    password:str
    
class FilterModelUser(Filter):
    username__like:Optional[str] = None
   
    class Constants(Filter.Constants):
        model = models.Users
        search_field_name = "search"
        search_model_fields = ['username']
