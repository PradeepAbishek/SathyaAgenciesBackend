from ..db.config import database_name, bills_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.bills import BillMaster, BillMasterInResponse, Filter
from .stocks import reduce_stock
from bson.objectid import ObjectId
from datetime import datetime
import fiscalyear

fiscalyear.START_MONTH = 4


async def get_all(conn: AsyncIOMotorClient):
    bills = []
    pipeline = [
        {
            '$addFields': {
                'customerObjectId': {
                    '$toObjectId': '$customerId'
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
        }
    ]
    rows = conn[database_name][bills_collection_name].aggregate(
        pipeline)
    async for row in rows:
        bills.append(BillMasterInResponse(**row))
    return bills


async def create(conn: AsyncIOMotorClient, bills: BillMaster):
    date = bills.billDate
    dates = date.split('-')
    financialYear = fiscalyear.FiscalDate(
        int(dates[0]), int(dates[1]), int(dates[2])).fiscal_year
    bills.financialYear = financialYear
    bills.billNumber = await get_bill_number_by_year(conn, financialYear)
    rows = await conn[database_name][bills_collection_name].insert_one(bills.dict())
    for billData in bills.billDetails:
        stockData = await reduce_stock(conn, billData.stockId, billData.productQuantity)
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    bills = []
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
    rows = conn[database_name][bills_collection_name].aggregate(
        pipeline)
    async for row in rows:
        bills.append(BillMasterInResponse(**row))
    return bills


async def get_by_customer_id(conn: AsyncIOMotorClient, id: str):
    bills = []
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
    rows = conn[database_name][bills_collection_name].aggregate(
        pipeline)
    async for row in rows:
        bills.append(BillMasterInResponse(**row))
    return bills


async def filter_by_date(conn: AsyncIOMotorClient, dates: Filter):
    bills = []
    pipeline = [
        {
            '$addFields': {
                'convertedBillDate': {
                    '$toDate': '$billDate'
                },
            }
        }, {
            '$match': {
                'convertedBillDate': {
                    '$gte': datetime.strptime(dates.startDate, "%Y-%m-%d"),
                    '$lte': datetime.strptime(dates.endDate, "%Y-%m-%d")
                }
            }
        }, {
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
    rows = conn[database_name][bills_collection_name].aggregate(pipeline)
    async for row in rows:
        bills.append(BillMasterInResponse(**row))
    return bills


async def get_bill_number_by_year(conn: AsyncIOMotorClient, financialYear: int):
    count = await conn[database_name][bills_collection_name].count_documents(
        {"financialYear": financialYear})
    return count + 1
