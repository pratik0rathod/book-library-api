from apps.users import schema,models,crud,auth

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

def register_user(db:Session,user:schema.UserRegister):
    new_user  =  models.Users(username =user.username,email = user.email,password = auth.hash_password(user.password))
       
    try: 
        if crud.check_username(db,new_user.username):
            raise HTTPException(status_code=400,detail={"error":"Username is already taken"})
        
        if crud.check_email(db,new_user.email):
            raise HTTPException(status_code=400,detail={"error":"User with this email address is already registed"})
    
        if crud.add_user(db,new_user):
            return {"success":"User Added sucessfully"}

    except HTTPException as e:
        raise e
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})
    

def login_user(db:Session,user:schema.LoginUser):
    try:            
        user_obj = crud.get_user_by_username(db,user.username)
        
        if user_obj is not None:
            if auth.verify_password(user.password,user_obj.password):
           
                return auth.create_token(({'sub':user_obj.id}))
        
        raise HTTPException(status_code=400,detail={"error":"Username or password wrong"})
    
    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

    
def get_user(db:Session):    
    pass