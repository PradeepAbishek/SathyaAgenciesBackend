from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ...db.mongodb import AsyncIOMotorClient, get_database

from ...models.auth import TokenResponse, Token
from ...crud.auth import verify_user


router = APIRouter()


@router.post("/", response_model=TokenResponse)
async def login_for_access_token(db: AsyncIOMotorClient = Depends(get_database), formData: OAuth2PasswordRequestForm = Depends()):
    data = await verify_user(db, formData)
    return data
