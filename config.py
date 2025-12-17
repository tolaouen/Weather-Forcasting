import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    SECRET_KEY: str = Field(...)
    DATABASE_URL: str = Field(...)
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env.local"), 
        env_file_encoding="utf-8"
    )

settings = Settings()


class Config:
    SECRET_KEY = settings.SECRET_KEY
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = settings.DEBUG