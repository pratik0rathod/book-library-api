from sqlalchemy import select
from sqlalchemy.orm import Session
from apps.users import models,schema
from pydantic import EmailStr

def add_user(db:Session,UserObj:models.Users):
    db.add(UserObj)
    db.commit()
    return True

def get_user_by_username(db:Session,username:str):
    return db.query(models.Users).filter(models.Users.username ==username).first()  

def get_user_by_userid(db:Session,userid:int):
    return db.query(models.Users).filter(models.Users.id ==  userid).first()  

def check_email(db:Session,email:EmailStr):
    
    obj = db.query(models.Users).filter(models.Users.email ==  email).first()
    
    if obj is not None:
        return True
    
    return False

def check_username(db:Session,username:str):
  
    obj = db.query(models.Users).filter(models.Users.username ==  username).first()  
  
    if obj is not None:
        return True

    return False

def check_email_update(db:Session,email:EmailStr,userid:int):
    
    obj = db.query(models.Users).filter(models.Users.email ==  email,models.Users.id != userid).first()
    
    if obj is not None:
        return True
    
    return False

def check_username_update(db:Session,username:str,userid:int):
  
    obj = db.query(models.Users).filter(models.Users.username ==  username,models.Users.id != userid).first()  
    
    if obj is not None:
        return True
    
    return False

def get_all_reader(db:Session):
    obj = db.query(models.Users).filter(models.Users.user_type ==  models.UserEnum.READER).all()
    return obj

def get_a_reader(db:Session,reader_id:int):
    obj = db.query(models.Users).filter(models.Users.user_type ==  models.UserEnum.READER,models.Users.id == reader_id).first()
    return obj

def set_status(db:Session,reader_id:int,status:bool):
   
    obj = db.query(models.Users).filter(models.Users.user_type ==  models.UserEnum.READER,models.Users.id == reader_id).first()
   
    if obj is not None:
        obj.is_active = status
        db.add(obj)
        db.commit()
        return True
   
    return False

def search_reader(db:Session,filers:schema.FilterModelUser):
    query = select(models.Users)
    query = filers.filter(query)
    results = db.execute(query)
    return results.scalars().all()
