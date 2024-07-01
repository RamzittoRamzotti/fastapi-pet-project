import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(base_dir, '.env'))

BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseModel):
    DB_HOST: str = os.getenv('POSTGRES_HOST')
    DB_PORT: int = os.getenv('POSTGRES_PORT')
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DB_NAME: str = os.getenv('POSTGRES_DB')

    @property
    def DB_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class CelerySettings(BaseModel):
    config_celery: dict = {
        'CELERY_ENABLE_UTC': True,
        'CELERY_SEND_TASK_SENT_EVENT': True,
        'CELERY_RESULT_BACKEND': 'redis://redis:6379/0',
        'CELERY_TASK_SERIALIZER': 'pickle',
        'CELERY_RESULT_SERIALIZER': 'pickle',
        'CELERY_ACCEPT_CONTENT': ['pickle', 'json'],

    }
    mail: str = os.getenv('mail')
    password: str = os.getenv('password')


class AuthJWT(BaseModel):
    private_key_path: str = BASE_DIR / "backend" / "certs" / "jwt_private.pem"
    public_key_path: str = BASE_DIR / "backend" / "certs" / "jwt_public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 1
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    db: DBSettings = DBSettings()
    celery: CelerySettings = CelerySettings()


settings = Settings()
