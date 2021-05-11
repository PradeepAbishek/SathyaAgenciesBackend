from ..db.config import database_name, companies_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.companies import Company, CompanyInDB, CompanyInUpdate, CompanyInResponse, PurchaseUpdate, PaymentUpdate
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    companies = []
    pipeline = [
        {
            '$lookup': {
                'from': 'purchases',
                'localField': 'purchases',
                'foreignField': '_id',
                'as': 'purchases'
            }
        }, {
            '$lookup': {
                'from': 'payments',
                'localField': 'payments',
                'foreignField': '_id',
                'as': 'payments'
            }
        }
    ]
    rows = conn[database_name][companies_collection_name].aggregate(pipeline)
    async for row in rows:
        companies.append(CompanyInResponse(**row))
    return companies


async def create(conn: AsyncIOMotorClient, company: Company):
    rows = await conn[database_name][companies_collection_name].insert_one(company.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][companies_collection_name].find_one({"_id": ObjectId(id)})
    return CompanyInResponse(**row)


async def update(conn: AsyncIOMotorClient, id: str,  company: CompanyInUpdate):
    row = await conn[database_name][companies_collection_name].update_one({"_id": ObjectId(id)}, {'$set': company.dict()})
    data = await get_by_id(conn, id)
    return data


async def delete(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][companies_collection_name].delete_one({"_id": ObjectId(id)})
    return row.deleted_count


async def updatePurchases(conn: AsyncIOMotorClient, companyId: str, purchaseData: PurchaseUpdate):
    row = await conn[database_name][companies_collection_name].update_one({"_id": ObjectId(companyId)}, {'$inc': {'currentBalanceAmount': purchaseData.balancePurchaseAmount}, "$push": {'purchases': ObjectId(purchaseData.purchaseId)}})
    return row.modified_count


async def updatePayments(conn: AsyncIOMotorClient, companyId: str, paymentData: PaymentUpdate):
    row = await conn[database_name][companies_collection_name].update_one({"_id": ObjectId(companyId)}, {'$inc': {'currentBalanceAmount': -paymentData.paidAmount}, "$push": {'payments': ObjectId(paymentData.paymentId)}})
    return row.modified_count
