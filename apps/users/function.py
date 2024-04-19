from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from apps.users import schema,models

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password,password):
    return verify_password(plain_password=plain_password,password=password)


def register_user(db:Session,user:schema.UserRegister):
    new_user  =  models.User(username =user.username,email = user.email,password = hash_password(user.password))
    return jsonable_encoder(new_user)

def login_user(db:Session):
    
    
    pass

def get_user(db:Session):
    
    
    pass



