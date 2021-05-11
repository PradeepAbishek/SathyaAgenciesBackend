from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.payments import Payment, PaymentInResponse, PaymentCompany, PaymentInResponseCompany
from ...models.users import UserInResponse
from ...crud.payments import create, get_all, createCompany, get_all_company, get_by_company_id, get_by_customer_id
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/customer")
async def get_all_payments(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/customer/{id}")
async def get_payment_by_customer_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_customer_id(db, id)
    return data


@router.post("/customer")
async def create_payment(payment: Payment, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, payment)
    return data


@router.post("/company")
async def create_payment_company(payment: PaymentCompany, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await createCompany(db, payment)
    return data


@router.get("/company")
async def get_all_payments_company(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all_company(db)
    return data


@router.get("/company/{id}")
async def get_payment_by_company_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_company_id(db, id)
    return data
