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
