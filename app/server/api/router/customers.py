from fastapi import APIRouter, Depends

from ...db.mongodb import AsyncIOMotorClient, get_database

from ...models.customers import Customer, CustomerInUpdate, BillUpdate, PaymentUpdate
from ...models.users import UserInResponse

from ...crud.customers import create, get_all, get_by_id, update, delete, updateBills, updatePayments
from ...crud.auth import get_current_active_user


router = APIRouter()


@router.get("/")
async def get_all_customers(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/{id}")
async def get_customer_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_id(db, id)
    return data


@router.post("/")
async def create_customer(customer: Customer, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, customer)
    return data


@router.put("/updateBills/{customerId}")
async def update_customer_bills(customerId: str, billData: BillUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await updateBills(db, customerId, billData)
    return data


@router.put("/updatePayments/{customerId}")
async def update_customer_payments(customerId: str, paymentData: PaymentUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await updatePayments(db, customerId, paymentData)
    return data


@router.put("/{id}")
async def update_customer(id: str, customer: CustomerInUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await update(db, id, customer)
    return data


@router.delete("/{id}")
async def delete_customer(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await delete(db, id)
    return data
