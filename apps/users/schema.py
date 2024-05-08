from datetime import date

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str


class RetriveUser(User):
    birth_date: date
    email: EmailStr


class UserRegister(RetriveUser):
    password: str


class LoginUser(User):
    password: str
