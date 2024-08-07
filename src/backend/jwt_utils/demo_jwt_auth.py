import os
import sys

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer)
from starlette import status

from internal.models import User
from jwt_utils.crud import get_user_from_db_by_username, get_user_from_db_by_email, insert_new_user
from jwt_utils.utils import hash_password
from jwt_utils.validation import get_current_token_payload, \
    get_current_auth_user_for_refresh, get_current_active_auth_user, validate_auth_user
from jwt_utils.helpers import (
    create_access_token,
    create_refresh_token)
from internal.schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
router = APIRouter(prefix='/api/login', tags=['JWT'], dependencies=[Depends(http_bearer)])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@router.post('/auth/', response_model=TokenInfo)
def auth_user_jwt_issue(
        user: UserSchema = Depends(validate_auth_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get('/users/me/')
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        'username': user.username,
        'email': user.email,
        'admin': user.admin,
        'logged_in': iat
    }


@router.get("/users/id/")
async def get_user_id(user: UserSchema = Depends(get_current_active_auth_user)):
    user_db = await get_user_from_db_by_username(user.username)
    return {'user_id': user_db.id, 'email': user.email}


@router.post('/refresh/', response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )


@router.post('/register/')
async def register_new_user(user: UserSchema):
    username = user.username
    email = user.email
    if await get_user_from_db_by_username(username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Username already registered',
        )
    elif email is not None and await get_user_from_db_by_email(email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Email already registered',
        )
    else:
        new_user = User(username=username, email=email, password=hash_password(user.password))
        await insert_new_user(new_user)
        return HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail='User created successfully',
        )
