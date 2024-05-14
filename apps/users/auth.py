from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio.session import AsyncSession
import book_management.core.config as config
from apps.users.crud import users_actions
from database.base import get_async_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl='user/login')

JWT_SECRET = config.settings.JWT_SECRET_KEY.get_secret_value()
JWT_ALGORITHM = config.settings.JWT_ALGORITHM


def create_token(data: dict, expire_time: timedelta | None = None):
    to_encode = data.copy()
    token = None

    if expire_time:
        expire = datetime.now(timezone.utc) + timedelta(expire_time)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {'access_token': token}


def decode_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])


async def get_user_obj(db: AsyncSession, user_id: int):
    return await users_actions.get(db, user_id)


async def get_user(token: Annotated[str, Depends(oauth_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        data = decode_token(token)
        async with await anext(get_async_db()) as db:
            user = await get_user_obj(db=db, user_id=int(data['sub']))

        return user

    except JWTError as e:
        raise credentials_exception

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'error': 'something went wrong from our side'
            }
        )
