from fastapi import HTTPException, Form
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError
from starlette import status
from typing import Annotated, Optional

from typing_extensions import Doc

from src.backend.jwt_utils import utils as auth_utils
from .crud import get_user_from_db_by_username, get_user_from_db_by_email
from .helpers import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.backend.schemas import UserSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/auth/")


class OAuth2PasswordRequestFormExtended(OAuth2PasswordRequestForm):
    def __init__(self,
                 *,
                 grant_type: Annotated[
                     str | None,
                     Form(pattern="password"),
                     Doc(
                         """
                         The OAuth2 spec says it is required and MUST be the fixed string
                         "password". Nevertheless, this dependency class is permissive and
                         allows not passing it. If you want to enforce it, use instead the
                         `OAuth2PasswordRequestFormStrict` dependency.
                         """
                     ),
                 ] = None,
                 username: Annotated[
                     str | None,
                     Form(),
                     Doc(
                         """
                         `username` string. The OAuth2 spec requires the exact field name
                         `username`.
                         """
                     ),
                 ] = None,
                 email: Annotated[
                     str | None,
                     Form(),
                     Doc(
                         """
                         `email` string. The OAuth2 spec requires the exact field name
                         `email".
                         """
                     ),
                 ] = None,
                 password: Annotated[
                     str,
                     Form(),
                     Doc(
                         """
                         `password` string. The OAuth2 spec requires the exact field name
                         `password".
                         """
                     ),
                 ],
                 scope: Annotated[
                     str,
                     Form(),
                     Doc(
                         """
                         A single string with actually several scopes separated by spaces. Each
                         scope is also a string.

                         For example, a single string with:

                         ```python
                         "items:read items:write users:read profile openid"
                         ````

                         would represent the scopes:

                         * `items:read`
                         * `items:write`
                         * `users:read`
                         * `profile`
                         * `openid`
                         """
                     ),
                 ] = "",
                 client_id: Annotated[
                     str | None,
                     Form(),
                     Doc(
                         """
                         If there's a `client_id`, it can be sent as part of the form fields.
                         But the OAuth2 specification recommends sending the `client_id` and
                         `client_secret` (if any) using HTTP Basic auth.
                         """
                     ),
                 ] = None,
                 client_secret: Annotated[
                     str | None,
                     Form(),
                     Doc(
                         """
                         If there's a `client_password` (and a `client_id`), they can be sent
                         as part of the form fields. But the OAuth2 specification recommends
                         sending the `client_id` and `client_secret` (if any) using HTTP Basic
                         auth.
                         """
                     ),
                 ] = None):
        self.email = email

        super(OAuth2PasswordRequestFormExtended, self).__init__(
            grant_type=grant_type,
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,

        )


# uvicorn src.backend.main:app --port 5005 --reload

def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )
    return payload


async def get_user_by_token_sub(payload: dict) -> UserSchema:
    username: str | None = payload.get('sub')
    if not (user := await get_user_from_db_by_username(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user is not found",
        )
    return user


class UserGetterFromToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(self, payload: dict = Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return await get_user_by_token_sub(payload)


get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type: str = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r}, expected: {token_type!r}"
    )


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


async def validate_auth_user(
        form_data: OAuth2PasswordRequestFormExtended = Depends(),

):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username/email or password",
    )

    if form_data.email is not None:
        if not (user := await get_user_from_db_by_email(form_data.email)):
            raise unauthed_exc
        if not auth_utils.validate_password(
                password=form_data.password,
                hashed_password=user.password
        ):
            raise unauthed_exc
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user is not active",
            )
    elif form_data.username is not None:
        if not (user := await get_user_from_db_by_username(form_data.username)):
            raise unauthed_exc
        if not auth_utils.validate_password(
                password=form_data.password,
                hashed_password=user.password
        ):
            raise unauthed_exc
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user is not active",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="you must enter either username or email",
        )
    return user
