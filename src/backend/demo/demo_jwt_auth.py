import jwt
from fastapi import APIRouter, Form, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.backend import utils as auth_utils
from src.backend.schemas import UserSchema

router = APIRouter(prefix='/jwt', tags=['JWT'])
http_bearer = HTTPBearer()


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


john = UserSchema(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@mail.ru',
)

sam = UserSchema(
    username='sam',
    password=auth_utils.hash_password('password'),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is not active",
        )
    return user


@router.post('/login', response_model=TokenInfo)
def auth_user_jwt_issue(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,

    }
    token = auth_utils.encode_jwt(jwt_payload, )
    return TokenInfo(
        access_token=token,
        token_type='Bearer',
    )


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> UserSchema:
    token = credentials.credentials
    payload = auth_utils.decode_jwt(token=token)
    return payload


def get_current_auth_user(payload: dict = Depends(get_current_token_payload)) -> UserSchema:
    username: str | None = payload.get('sub')
    if not (user := users_db.get(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not found",
        )
    return user


def get_current_active_auth_user(
        user: UserSchema = Depends(get_current_auth_user)
):
    if user.active:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user is not active",
        )


@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user)
):
    return {
        'username': user.username,
        'email': user.email,
    }
