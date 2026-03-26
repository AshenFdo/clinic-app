from math import e
from re import DEBUG

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    #App
    APP_NAME:str = "Clinic Management System"
    DEBUG: bool = True


    #Database
    DATABASE_URL:str

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str

    # JWT / Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()