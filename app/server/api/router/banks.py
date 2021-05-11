from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database

from ...models.banks import BankInUpdate, Bank
from ...models.users import UserInResponse

from ...crud.banks import create, get_all, get_by_id, update, delete
from ...crud.auth import get_current_active_user


router = APIRouter()


@router.get("/")
async def get_all_banks(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/{id}")
async def get_bank_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_id(db, id)
    return data


@router.post("/")
async def create_bank(bank: Bank, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, bank)
    return data


@router.put("/{id}")
async def update_bank(id: str, bank: BankInUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await update(db, id, bank)
    return data


@router.delete("/{id}")
async def delete_bank(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await delete(db, id)
    return data
