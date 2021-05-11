from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.stocks import StockZeroResponse, Stock, StockInResponse
from ...models.users import UserInResponse
from ...crud.stocks import get_all_including_zero, get_by_company_id, get_all
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_all_stocks_including_zero(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all_including_zero(db)
    return data


@router.get("/bill")
async def get_all_stocks(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/{id}")
async def get_stock_by_company_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_company_id(db, id)
    return data
