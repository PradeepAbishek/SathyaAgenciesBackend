from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.purchases import PurchaseMaster, PurchaseMasterInResponse
from ...models.users import UserInResponse
from ...crud.purchases import create, get_all, get_by_id, get_by_company_id
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_all_purchases(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.post("/")
async def create_purchase(purchases: PurchaseMaster, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, purchases)
    return data


@router.get("/{companyId}")
async def get_all_purchases_by_company(companyId: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_company_id(db, companyId)
    return data