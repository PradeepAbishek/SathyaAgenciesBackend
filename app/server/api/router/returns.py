from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.returns import ReturnMaster, ReturnMasterInResponse
from ...models.users import UserInResponse
from ...crud.returns import create, get_all, get_by_id, get_by_customer_id
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_all_returns(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.post("/")
async def create_return(returns: ReturnMaster, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, returns)
    return data


@router.get("/{customerId}")
async def get_all_returns_by_customer(customerId: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_customer_id(db, customerId)
    return data


@router.get("/payment/{id}")
async def get_returns_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_id(db, id)
    return data
