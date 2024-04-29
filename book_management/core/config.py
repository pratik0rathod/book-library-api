from sqlalchemy import URL

from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic.types import SecretStr



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    POSTGRES_DRIVER:str
    POSTGRES_USER:str
    POSTGRES_PASSWORD:SecretStr
    POSTGRES_HOST:str
    POSTGRES_DB :str
    
    JWT_SECRET_KEY:SecretStr
    JWT_ALGORITHM : str
    
    SESSION_SECRET:SecretStr
    
settings = Settings()

def get_db_url():
    return URL.create(
        drivername=settings.POSTGRES_DRIVER,
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
    )

def get_db_url_str():
    return f"{settings.POSTGRES_DRIVER}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"