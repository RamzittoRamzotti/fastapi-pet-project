from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel
from fastapi.security import (
    HTTPBearer)

from src.backend.jwt_utils.validation import get_current_token_payload, \
    get_current_auth_user_for_refresh, get_current_active_auth_user, validate_auth_user
from src.backend.jwt_utils.helpers import (create_access_token,
                                           create_refresh_token)
from src.backend.schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix='/login', tags=['JWT'], dependencies=[Depends(http_bearer)])


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


@router.post('/auth', response_model=TokenInfo)
def auth_user_jwt_issue(
        user: UserSchema = Depends(validate_auth_user)
):
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get('/users/me')
def auth_user_check_self_info(
        payload: dict = Depends(get_current_token_payload),
        user: UserSchema = Depends(get_current_active_auth_user),

):
    iat = payload.get("iat")
    return {
        'username': user.username,
        'email': user.email,
        'logged_in': iat
    }


@router.post('/refresh', response_model=TokenInfo, response_model_exclude_none=True)
def auth_refresh_jwt(user: UserSchema = Depends(get_current_auth_user_for_refresh)):
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )
