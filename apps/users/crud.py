from sqlalchemy.orm import Session
from apps.users.models import Users

from pydantic import EmailStr

def add_user(db:Session,UserObj:Users):
    db.add(UserObj)
    db.commit()
    return True


def get_user_by_username(db:Session,username:str):
    return db.query(Users).filter(Users.username ==  username).first()  

def get_user_by_userid(db:Session,userid:int):
    return db.query(Users).filter(Users.id ==  userid).first()  

def check_email(db:Session,email:EmailStr):
    
    obj = db.query(Users).filter(Users.email ==  email).first()
    
    if obj is not None:
        return True
    
    return False

def check_username(db:Session,username:str):
  
    obj = db.query(Users).filter(Users.username ==  username).first()  
  
    if obj is not None:
        return True
    
    return False

