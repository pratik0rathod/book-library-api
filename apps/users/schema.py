from pydantic import BaseModel,EmailStr
from datetime import date


class User(BaseModel):
    username : str

class RetriveUser(User):
    birth_date: date
    email:EmailStr
  
class UserRegister(RetriveUser):
    password: str
    
class LoginUser(User):
    password:str
    
    
    