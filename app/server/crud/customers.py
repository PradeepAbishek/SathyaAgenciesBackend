from ..db.config import database_name, customers_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.customers import Customer, CustomerInUpdate, CustomerInResponse, BillUpdate, PaymentUpdate
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    customers = []
    pipeline = [
        {
            '$match': {
                'isActive': {
                    '$eq': True
                }
            }
        }, {
            '$lookup': {
                'from': 'bills',
                'localField': 'bills',
                'foreignField': '_id',
                'as': 'bills'
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
    rows = conn[database_name][customers_collection_name].aggregate(pipeline)
    async for row in rows:
        customers.append(CustomerInResponse(**row))
    return customers


async def create(conn: AsyncIOMotorClient, customer: Customer):
    rows = await conn[database_name][customers_collection_name].insert_one(customer.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    customers = []
    pipeline = [
        {
            '$match': {
                'isActive': {
                    '$eq': True
                },
                '_id': {
                    '$eq': ObjectId(id)
                }
            }
        }, {
            '$lookup': {
                'from': 'bills',
                'localField': 'bills',
                'foreignField': '_id',
                'as': 'bills'
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
    rows = conn[database_name][customers_collection_name].aggregate(pipeline)
    async for row in rows:
        customers.append(CustomerInResponse(**row))
    return customers


async def update(conn: AsyncIOMotorClient, id: str,  customer: CustomerInUpdate):
    row = await conn[database_name][customers_collection_name].update_one({"_id": ObjectId(id)}, {'$set': customer.dict()})
    data = await get_by_id(conn, id)
    return data


async def delete(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][customers_collection_name].update_one({"_id": ObjectId(id)}, {'$set': {'isActive': False}})
    return row.modified_count


async def updateBills(conn: AsyncIOMotorClient, customerId: str, billData: BillUpdate):
    row = await conn[database_name][customers_collection_name].update_one({"_id": ObjectId(customerId)}, {'$inc': {'currentBalanceAmount': billData.balanceBillAmount}, "$push": {'bills': ObjectId(billData.billId)}})
    return row.modified_count


async def updatePayments(conn: AsyncIOMotorClient, customerId: str, paymentData: PaymentUpdate):
    row = await conn[database_name][customers_collection_name].update_one({"_id": ObjectId(customerId)}, {'$inc': {'currentBalanceAmount': -paymentData.paidAmount}, "$push": {'payments': ObjectId(paymentData.paymentId)}})
    return row.modified_count
