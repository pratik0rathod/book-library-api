from sqlalchemy import URL

from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic.types import SecretStr

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    DBDRIVER:str
    DBUSER:str
    DBPASSWORD:SecretStr
    DBHOST:str
    DB :str
    
    JWT_SECRET_KEY:SecretStr
    JWT_ALGORITHM : str
    
db_settings = DatabaseSettings()

def get_db_url():
    return URL.create(
        drivername=db_settings.DBDRIVER,
        username=db_settings.DBUSER,
        password=db_settings.DBPASSWORD,
        host=db_settings.DBHOST,
        database=db_settings.DB,
    )

def get_db_url_str():
    return f"{db_settings.DBDRIVER}://{db_settings.DBUSER}:{db_settings.DBPASSWORD.get_secret_value()}@{db_settings.DBHOST}/{db_settings.DB}"