from fastapi import APIRouter, Depends

from ...db.mongodb import AsyncIOMotorClient, get_database

from ...models.users import User, UserInUpdate, UserInDB, UserInResponse

from ...crud.users import create, get_all, get_by_id, update, delete
from ...crud.auth import get_current_admin_user


router = APIRouter()


@router.get("/")
async def get_all_users(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_admin_user)):
    data = await get_all(db)
    return data


@router.get("/{id}", response_model=UserInResponse)
async def get_user_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_admin_user)):
    data = await get_by_id(db, id)
    return data


@router.post("/", response_model=UserInResponse)
async def create_user(user: User, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_admin_user)):
    data = await create(db, user)
    return data


@router.put("/{id}", response_model=UserInResponse)
async def update_user(id: str, user: UserInUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_admin_user)):
    data = await update(db, id, user)
    return data


@router.delete("/{id}")
async def delete_user(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_admin_user)):
    data = await delete(db, id)
    return data
