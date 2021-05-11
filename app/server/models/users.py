from bson.objectid import ObjectId
from .dbmodel import IDModel
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    userName: str
    password: str
    isAdmin: Optional[bool] = False
    isActive: Optional[bool] = True


class UserInUpdate(BaseModel):
    userName: Optional[str]
    isAdmin: Optional[bool]
    isActive: Optional[bool]


class UserInResponse(IDModel):
    userName: str
    isAdmin: bool
    isActive: Optional[bool] = False


class LoginResponse(BaseModel):
    userName: str
    isAdmin: bool
    isActive: bool


class UserInDB(IDModel, User):
    pass
