from ..db.config import database_name, banks_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.banks import Bank, BankInDB, BankInUpdate, BankInResponse
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    banks = []
    pipeline = [
        {
            '$addFields': {
                'companyObjectId': {
                    '$toObjectId': '$companyId'
                }
            }
        }, {
            '$lookup': {
                'from': 'companies',
                'localField': 'companyObjectId',
                'foreignField': '_id',
                'as': 'companyDetails'
            }
        }, {
            '$unwind': {
                'path': '$companyDetails'
            }
        }
    ]
    rows = conn[database_name][banks_collection_name].aggregate(pipeline)
    async for row in rows:
        banks.append(BankInResponse(**row))
    return banks


async def create(conn: AsyncIOMotorClient, bank: Bank):
    rows = await conn[database_name][banks_collection_name].insert_one(bank.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    banks = []
    pipeline = [
        {
            '$match': {
                '_id': {
                    '$eq': ObjectId(id)
                }
            }
        },
        {
            '$addFields': {
                'companyObjectId': {
                    '$toObjectId': '$companyId'
                }
            }
        }, {
            '$lookup': {
                'from': 'companies',
                'localField': 'companyObjectId',
                'foreignField': '_id',
                'as': 'companyDetails'
            }
        }, {
            '$unwind': {
                'path': '$companyDetails'
            }
        }
    ]
    rows = conn[database_name][banks_collection_name].aggregate(pipeline)
    async for row in rows:
        banks.append(BankInResponse(**row))
    return banks


async def update(conn: AsyncIOMotorClient, id: str,  bank: BankInUpdate):
    row = await conn[database_name][banks_collection_name].update_one({"_id": ObjectId(id)}, {'$set': bank.dict()})
    data = await get_by_id(conn, id)
    return data


async def delete(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][banks_collection_name].delete_one({"_id": ObjectId(id)})
    return row.deleted_count
