from apps.users import schema,models,crud,auth

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

def register_user(db:Session,user:schema.UserRegister):
    new_user  =  models.Users(username =user.username,email = user.email,birth_date = user.birth_date, password = auth.hash_password(user.password))
    errors:dict[str,str] = dict()
    
    try: 
        if crud.check_username(db,new_user.username):
            errors["username_error"] = "Username is already taken"
          
        if crud.check_email(db,new_user.email):
            errors["useremail_error"] = "User with this email address is already registed"
        
        if len(errors) > 0:
            raise HTTPException(status_code=400,detail={"errors":errors})
        
        if crud.add_user(db,new_user):
            return {"success":"User Added sucessfully"}

    except HTTPException as e:
        print(e)
        
        raise e
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})
    

def login_user(db:Session,user:schema.LoginUser):
    try:            
        user_obj = crud.get_user_by_username(db,user.username)
        
        if user_obj is not None:
            if auth.verify_password(user.password,user_obj.password):
           
                return auth.create_token(({'sub':str(user_obj.id)}))
        
        raise HTTPException(status_code=400,detail={"error":"Username or password wrong"})
    
    except HTTPException as e:
        raise e

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

    
def get_me(db:Session,userid:int):
    user_obj = crud.get_user_by_userid(db,userid)
    return jsonable_encoder(user_obj)
