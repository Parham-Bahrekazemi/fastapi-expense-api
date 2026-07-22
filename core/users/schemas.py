from pydantic import BaseModel, ConfigDict
from users.model import UserRole


class UserCreateSchema(BaseModel):
    name: str
    password: str


class UserLoginSchema(BaseModel):
    name: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    role: UserRole
    is_active: bool
