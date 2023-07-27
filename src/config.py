from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    DATABASE_URL: str
    SITE_DOMAIN: str = "myapp.com"


settings = Settings()
