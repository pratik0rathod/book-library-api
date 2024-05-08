from typing import Optional, Any

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic.types import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str

    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str

    SESSION_SECRET: SecretStr
    DATABASE_URI: Optional[PostgresDsn] = None

    LOGO_URL: str
    LOGIN_LOGO_URL: str

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        print("Creating DB_URI from .env file ...")
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            path=f"{values.data.get('POSTGRES_DB') or ''}",
        )


settings = Settings()
