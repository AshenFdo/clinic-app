from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Settings for the application, loaded from environment variables  in .env file.
    """
    #App
    APP_NAME:str = "Clinic Management System"
    DEBUG: bool = True
    #Database
    DATABASE_URL:str
    SYNC_DATABASE_URL:str
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # JWT / Auth
    SUPABASE_JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "ES256"
    BYPASS_EMAIL_CONFIRMATION_ON_FAILURE: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Cache settings instance to avoid reloading from environment on every access
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()