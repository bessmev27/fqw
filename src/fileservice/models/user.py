
from typing import Optional
from .base import BasePydanticModel
from pydantic import EmailStr


class User(BasePydanticModel):
    id: int
    name: str
    login: str
    email: Optional[str]


class UserCreate(BasePydanticModel):
    name: str
    login: str
    email: Optional[str]
    password: str


class Token(BasePydanticModel):
    access_token: str
    token_type: str = "bearer"
