import os

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file=os.getenv('ENV_FILE', '.env'))

    LOGGING_LEVEL: str = 'INFO'
    LOGGING_FORMAT: str = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'

    SECRET_KEY: str = 'jiduoduo'
    PERMANENT_SESSION_LIFETIME_MINUTES: int = 10

    SQLALCHEMY_DATABASE_URI: str = 'sqlite:///db.sqlite3'
    SQLALCHEMY_ECHO: bool = False

    CELERY_ALWAYS_EAGER: bool = False
    CELERY_BROKER_URL: str = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND: str = 'redis://redis:6379/0'


config = Config()
