from fastapi import APIRouter, Depends
from ...db.mongodb import AsyncIOMotorClient, get_database
from ...models.products import ProductInUpdate, Product
from ...models.users import UserInResponse
from ...crud.products import create, get_all, get_by_id, update, delete, get_by_company_id
from ...crud.auth import get_current_active_user

router = APIRouter()


@router.get("/")
async def get_all_products(db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_all(db)
    return data


@router.get("/{id}")
async def get_product_by_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_id(db, id)
    return data


@router.get("/company/{id}")
async def get_product_by_company_id(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await get_by_company_id(db, id)
    return data


@router.post("/")
async def create_product(product: Product, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await create(db, product)
    return data


@router.put("/{id}")
async def update_product(id: str, product: ProductInUpdate, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await update(db, id, product)
    return data


@router.delete("/{id}")
async def delete_product(id: str, db: AsyncIOMotorClient = Depends(get_database), current_user: UserInResponse = Depends(get_current_active_user)):
    data = await delete(db, id)
    return data
