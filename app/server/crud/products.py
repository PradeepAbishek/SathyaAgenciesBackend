from ..db.config import database_name, products_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.products import Product, ProductInDB, ProductInUpdate, ProductInResponse
from bson.objectid import ObjectId


async def get_all(conn: AsyncIOMotorClient):
    products = []
    pipeline = [
        {
            '$match': {
                'isActive': {
                    '$eq': True
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
    rows = conn[database_name][products_collection_name].aggregate(pipeline)
    async for row in rows:
        products.append(ProductInResponse(**row))
    return products


async def create(conn: AsyncIOMotorClient, product: Product):
    rows = await conn[database_name][products_collection_name].insert_one(product.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    products = []
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
    rows = conn[database_name][products_collection_name].aggregate(pipeline)
    async for row in rows:
        products.append(ProductInResponse(**row))
    return products


async def get_by_company_id(conn: AsyncIOMotorClient, id: str):
    products = []
    pipeline = [
        {
            '$match': {
                'companyId': {
                    '$eq': (id)
                },
                'isActive': {
                    '$eq': True
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
    rows = conn[database_name][products_collection_name].aggregate(pipeline)
    async for row in rows:
        products.append(ProductInResponse(**row))
    return products


async def update(conn: AsyncIOMotorClient, id: str,  product: ProductInUpdate):
    row = await conn[database_name][products_collection_name].update_one({"_id": ObjectId(id)}, {'$set': product.dict()})
    data = await get_by_id(conn, id)
    return data


async def delete(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][products_collection_name].update_one({"_id": ObjectId(id)}, {'$set': {'isActive': False}})
    return row.modified_count
