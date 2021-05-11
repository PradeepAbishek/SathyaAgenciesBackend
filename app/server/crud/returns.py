from ..db.config import database_name, returns_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.returns import ReturnMaster, ReturnMasterInResponse, ReturnMasterInResponseWithPayment
from .stocks import update_stock_by_id
from bson.objectid import ObjectId
from datetime import datetime
import fiscalyear

fiscalyear.START_MONTH = 4


async def get_all(conn: AsyncIOMotorClient):
    returns = []
    pipeline = [
        {
            '$addFields': {
                'customerObjectId': {
                    '$toObjectId': '$customerId'
                },
                'returnId': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$lookup': {
                'from': 'customers',
                'localField': 'customerObjectId',
                'foreignField': '_id',
                'as': 'customerDetails'
            }
        }, {
            '$unwind': {
                'path': '$customerDetails',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                'from': 'payments',
                'localField': 'returnId',
                'foreignField': 'returnId',
                'as': 'paymentDetails'
            }
        }, {
            '$unwind': {
                'path': '$paymentDetails',
                'preserveNullAndEmptyArrays': True
            }
        }
    ]
    rows = conn[database_name][returns_collection_name].aggregate(
        pipeline)
    async for row in rows:
        returns.append(ReturnMasterInResponseWithPayment(**row))
    return returns


async def create(conn: AsyncIOMotorClient, returns: ReturnMaster):
    date = returns.returnDate
    dates = date.split('-')
    financialYear = fiscalyear.FiscalDate(
        int(dates[0]), int(dates[1]), int(dates[2])).fiscal_year
    returns.financialYear = financialYear
    returns.returnNumber = await get_return_number_by_year(conn, financialYear)
    rows = await conn[database_name][returns_collection_name].insert_one(returns.dict())
    for returnData in returns.returnDetails:
        stockData = await update_stock_by_id(conn, returnData.stockId, returnData.productQuantity)
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    returns = []
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
                'customerObjectId': {
                    '$toObjectId': '$customerId'
                },
            }
        }, {
            '$lookup': {
                'from': 'customers',
                'localField': 'customerObjectId',
                'foreignField': '_id',
                'as': 'customerDetails'
            }
        }, {
            '$unwind': {
                'path': '$customerDetails',
                'preserveNullAndEmptyArrays': True
            }
        }
    ]
    rows = conn[database_name][returns_collection_name].aggregate(
        pipeline)
    async for row in rows:
        returns.append(ReturnMasterInResponse(**row))
    return returns


async def get_by_customer_id(conn: AsyncIOMotorClient, id: str):
    returns = []
    pipeline = [
        {
            '$match': {
                'customerId': {
                    '$eq': id
                }
            }
        },
        {
            '$addFields': {
                'customerObjectId': {
                    '$toObjectId': '$customerId'
                },
            }
        }, {
            '$lookup': {
                'from': 'customers',
                'localField': 'customerObjectId',
                'foreignField': '_id',
                'as': 'customerDetails'
            }
        }, {
            '$unwind': {
                'path': '$customerDetails',
                'preserveNullAndEmptyArrays': True
            }
        }
    ]
    rows = conn[database_name][returns_collection_name].aggregate(
        pipeline)
    async for row in rows:
        returns.append(ReturnMasterInResponse(**row))
    return returns


async def get_return_number_by_year(conn: AsyncIOMotorClient, financialYear: int):
    count = await conn[database_name][returns_collection_name].count_documents(
        {"financialYear": financialYear})
    return count + 1
