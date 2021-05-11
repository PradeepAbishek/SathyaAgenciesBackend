from ..db.config import database_name, stocks_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.stocks import Stock, StockInResponse, StockZeroResponse
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    stocks = []
    rows = conn[database_name][stocks_collection_name].find(
        {'availableQuantity': {'$gt': 0}})
    async for row in rows:
        stocks.append(StockInResponse(**row))
    return stocks


async def get_all_including_zero(conn: AsyncIOMotorClient):
    stocks = []
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
                'path': '$companyDetails',
                'preserveNullAndEmptyArrays': True
            }
        }
    ]
    rows = conn[database_name][stocks_collection_name].aggregate(pipeline)
    async for row in rows:
        stocks.append(StockZeroResponse(**row))
    return stocks


async def get_by_company_id(conn: AsyncIOMotorClient, id: str):
    stocks = []
    pipeline = [
        {
            '$match': {
                'companyId': {
                    '$eq': id
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
                'path': '$companyDetails',
                'preserveNullAndEmptyArrays': True
            }
        }
    ]
    rows = conn[database_name][stocks_collection_name].aggregate(pipeline)
    async for row in rows:
        stocks.append(StockZeroResponse(**row))
    return stocks


async def update(conn: AsyncIOMotorClient, stock: Stock):
    row = await conn[database_name][stocks_collection_name].update_one(
        {
            "$and": [
                {"companyId": stock['companyId']},
                {"productName": stock['productName']},
                {"productGST": stock['productGST']},
                {"productHSNCode": stock['productHSNCode']},
                {"unitPrice": stock['unitPrice']}
            ]
        }, {'$inc': {"availableQuantity": stock['availableQuantity']}})
    if(row.modified_count > 0):
        data = await find_and_get_by_id(conn, stock)
    else:
        data = await create(conn, stock)
    return data


async def create(conn: AsyncIOMotorClient, stock: Stock):
    rows = await conn[database_name][stocks_collection_name].insert_one(stock)
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][stocks_collection_name].find_one({"_id": ObjectId(id)})
    return StockInResponse(**row)


async def find_and_get_by_id(conn: AsyncIOMotorClient, stock: Stock):
    row = await conn[database_name][stocks_collection_name].find_one(
        {
            "$and": [
                {"companyId": stock['companyId']},
                {"productName": stock['productName']},
                {"productGST": stock['productGST']},
                {"productHSNCode": stock['productHSNCode']},
                {"unitPrice": stock['unitPrice']}
            ]
        })
    data = await get_by_id(conn, row["_id"])
    return data


async def reduce_stock(conn: AsyncIOMotorClient, id: str, purchaseCount: str):
    row = await conn[database_name][stocks_collection_name].update_one({"_id": ObjectId(id)}, {'$inc': {"availableQuantity": -purchaseCount}})
    return row.modified_count


async def update_stock_by_id(conn: AsyncIOMotorClient, id: str, purchaseCount: str):
    row = await conn[database_name][stocks_collection_name].update_one({"_id": ObjectId(id)}, {'$inc': {"availableQuantity": purchaseCount}})
    return row.modified_count