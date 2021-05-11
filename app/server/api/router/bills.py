from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.bills import BillMaster, BillMasterInResponse, Filter
from ...models.users import UserInResponse
from ...crud.bills import create, get_all, get_by_id, filter_by_date, get_by_customer_id
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_all_bills(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.post("/")
async def create_bill(bills: BillMaster, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, bills)
    return data


@router.post("/filter")
async def filter_bills(dates: Filter, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await filter_by_date(db, dates)
    return data


@router.get("/{customerId}")
async def get_all_bills_by_customer(customerId: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_customer_id(db, customerId)
    return data
