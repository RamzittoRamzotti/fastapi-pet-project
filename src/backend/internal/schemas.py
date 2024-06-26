import re
from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(2), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    email: Optional[EmailStr | None] = None
    password: str
    active: bool = True
    admin: bool = False

    @field_validator('password')
    @classmethod
    def password_strength(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        return value


class BookSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    title: str | None
    author: str | None
    description: str | None
    title_picture: str | None
    user_id: int | None = None
