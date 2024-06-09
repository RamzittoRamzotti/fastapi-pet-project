from pathlib import Path

from pydantic import BaseModel
from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: str = BASE_DIR / "src" / "backend" / "jwt_private.pem"
    public_key_path: str = BASE_DIR / "src" / "backend" / "jwt_public.pem"


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
