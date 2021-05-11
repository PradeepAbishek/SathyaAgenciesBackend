from ..db.config import database_name, payments_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.payments import Payment, PaymentInResponse, PaymentCompany, PaymentInResponseCompany
from bson.objectid import ObjectId
import fiscalyear


fiscalyear.START_MONTH = 4


async def get_all(conn: AsyncIOMotorClient):
    payments = []
    pipeline = [
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
                'path': '$customerDetails'
            }
        }
    ]
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponse(**row))
    return payments


async def get_all_company(conn: AsyncIOMotorClient):
    payments = []
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
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponseCompany(**row))
    return payments


async def create(conn: AsyncIOMotorClient, payment: Payment):
    date = payment.paymentDate
    dates = date.split('-')
    financialYear = fiscalyear.FiscalDate(
        int(dates[0]), int(dates[1]), int(dates[2])).fiscal_year
    payment.financialYear = financialYear
    payment.paymentNumber = await get_payment_number_by_year(conn, financialYear)
    rows = await conn[database_name][payments_collection_name].insert_one(payment.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def createCompany(conn: AsyncIOMotorClient, payment: PaymentCompany):
    date = payment.paymentDate
    dates = date.split('-')
    financialYear = fiscalyear.FiscalDate(
        int(dates[0]), int(dates[1]), int(dates[2])).fiscal_year
    payment.financialYear = financialYear
    payment.paymentNumber = await get_payment_number_by_year(conn, financialYear)
    rows = await conn[database_name][payments_collection_name].insert_one(payment.dict())
    data = await get_by_id_companyDetails(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    payments = []
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
                'path': '$customerDetails'
            }
        }
    ]
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponse(**row))
    return payments


async def get_by_customer_id(conn: AsyncIOMotorClient, id: str):
    payments = []
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
                'path': '$customerDetails'
            }
        }
    ]
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponse(**row))
    return payments


async def get_by_id_companyDetails(conn: AsyncIOMotorClient, id: str):
    payments = []
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
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponseCompany(**row))
    return payments


async def get_by_company_id(conn: AsyncIOMotorClient, id: str):
    payments = []
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
                'path': '$companyDetails'
            }
        }
    ]
    rows = conn[database_name][payments_collection_name].aggregate(pipeline)
    async for row in rows:
        payments.append(PaymentInResponseCompany(**row))
    return payments


async def get_payment_number_by_year(conn: AsyncIOMotorClient, financialYear: int):
    count = await conn[database_name][payments_collection_name].count_documents(
        {"financialYear": financialYear})
    return count + 1
