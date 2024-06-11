from datetime import timedelta, datetime

import bcrypt
import jwt
from src.backend.config import settings


def encode_jwt(payload: dict, private_key: str = settings.auth_jwt.private_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm,
               expire_delta: timedelta | None = None,
               expire_minutes: int = settings.auth_jwt.access_expire_token_minutes):
    to_encode = payload.copy()
    if expire_delta:
        expire = datetime.now() + expire_delta
    else:
        expire = datetime.now() + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=datetime.now()
    )
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(token: str | bytes, public_key: str = settings.auth_jwt.public_key_path.read_text(),
               algorithm: str = settings.auth_jwt.algorithm):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password=hashed_password
    )
