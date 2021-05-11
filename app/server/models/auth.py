from pydantic import BaseModel
from .users import LoginResponse
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TokenResponse(LoginResponse, Token):
    pass
