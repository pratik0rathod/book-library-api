
import book_management.core.config as config

from typing import Annotated

from fastapi import HTTPException,Depends,status

from fastapi.security import OAuth2PasswordBearer

from datetime import timedelta,datetime,timezone

from jose import JWTError,jwt

oauth_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

JWT_SECRET = config.settings.JWT_SECRET_KEY.get_secret_value() 
JWT_ALGORITHM = config.settings.JWT_ALGORITHM 

def create_token(data:dict,expire_time:timedelta | None = None):

    to_encode = data.copy()
    token = None    
    
    if expire_time:
        expire = datetime.now(timezone.utc) + timedelta(expire_time)
    
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        
    to_encode.update({"exp":expire})
    
    token = jwt.encode(to_encode,JWT_SECRET,algorithm=JWT_ALGORITHM)

    return {'access_token':token}
    
def decode_token(token):
    return jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])


def get_user(token:Annotated[str,Depends(oauth_scheme)]):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:    

        data = decode_token(token)
        return data['sub']
    
    except JWTError as e:
        print(e)
        raise credentials_exception
