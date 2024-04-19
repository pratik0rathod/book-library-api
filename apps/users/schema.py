from pydantic import BaseModel,EmailStr


class User(BaseModel):
    username : str

class RetriveUser(User):
    email:EmailStr

class UserRegister(RetriveUser):
    password: str
    
    
    