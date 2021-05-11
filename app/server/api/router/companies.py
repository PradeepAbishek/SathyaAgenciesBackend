from fastapi import APIRouter, Depends

from ...db.mongodb import AsyncIOMotorClient, get_database

from ...models.companies import Company, CompanyInUpdate, PurchaseUpdate, PaymentUpdate
from ...models.users import UserInResponse

from ...crud.companies import create, get_all, get_by_id, update, delete, updatePayments, updatePurchases
from ...crud.auth import get_current_active_user


router = APIRouter()


@router.get("/")
async def get_all_companies(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/{id}")
async def get_company_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_id(db, id)
    return data


@router.post("/")
async def create_company(company: Company, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, company)
    return data


@router.put("/updatePurchases/{companyId}")
async def update_company_purchases(companyId: str, purchaseData: PurchaseUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await updatePurchases(db, companyId, purchaseData)
    return data


@router.put("/updatePayments/{companyId}")
async def update_company_payments(companyId: str, paymentData: PaymentUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await updatePayments(db, companyId, paymentData)
    return data


@router.put("/{id}")
async def update_company(id: str, company: CompanyInUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await update(db, id, company)
    return data


@router.delete("/{id}")
async def delete_company(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await delete(db, id)
    return data
