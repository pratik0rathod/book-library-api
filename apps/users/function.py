from apps.users import schema,models,crud,auth

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


def reguler_user_exception(db,user_id):
    user = crud.get_user_by_userid(db,user_id)
    if user.user_type == models.UserEnum.READER:
        raise HTTPException(status_code=400,detail={"error":"You are not allowed to perform this action"})
    return True

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

def get_all_reader(db:Session,userid:int):
    try:
        reguler_user_exception(db,userid)

        users_obj =  crud.get_all_reader(db)
        if users_obj is not None:
            return jsonable_encoder(users_obj)
       
        raise HTTPException(status_code=400,detail={"error":"There are no readers"})
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

def get_a_reader(db:Session,user_id:int,reader_id):
    try:
        reguler_user_exception(db,user_id)

        users_obj =  crud.get_a_reader(db,reader_id)
     
        if users_obj is not None:
            return jsonable_encoder(users_obj)
       
        raise HTTPException(status_code=404,detail={"error":"User does not exist"})
    
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

def set_status(db,user_id,reader_id,active):
    try:
        reguler_user_exception(db,user_id)
       
        if crud.set_status(db,reader_id,active):
            return {"message":"user updated sucessfully"}
      
        raise HTTPException(status_code=404,detail={"error":"User does not exist"})
    
    except HTTPException as h:
        raise h
        
    except Exception as e: 
        print(e)
        raise HTTPException(status_code=500,detail={"error":"Internal server error"})

