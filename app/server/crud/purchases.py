from ..db.config import database_name, purchases_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.purchases import PurchaseMaster, PurchaseMasterInResponse
from .stocks import update
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    purchases = []
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
    rows = conn[database_name][purchases_collection_name].aggregate(
        pipeline)
    async for row in rows:
        purchases.append(PurchaseMasterInResponse(**row))
    return purchases


async def create(conn: AsyncIOMotorClient, purchases: PurchaseMaster):
    rows = await conn[database_name][purchases_collection_name].insert_one(purchases.dict())
    for purchaseData in purchases.purchaseDetails:
        stock = {}
        stock['companyId'] = purchases.companyId
        stock['productName'] = purchaseData.productName
        stock['productHSNCode'] = purchaseData.productHSNCode
        stock['productGST'] = purchaseData.productGST
        stock['unitPrice'] = purchaseData.unitPrice
        stock['sellingPrice'] = purchaseData.sellingPrice
        stock['availableQuantity'] = purchaseData.productQuantity
        stockData = await update(conn, stock)
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    purchases = []
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
                },
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
    rows = conn[database_name][purchases_collection_name].aggregate(
        pipeline)
    async for row in rows:
        purchases.append(PurchaseMasterInResponse(**row))
    return purchases


async def get_by_company_id(conn: AsyncIOMotorClient, id: str):
    purchases = []
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
                },
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
    rows = conn[database_name][purchases_collection_name].aggregate(
        pipeline)
    async for row in rows:
        purchases.append(PurchaseMasterInResponse(**row))
    return purchases
