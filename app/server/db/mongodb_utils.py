from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db


MONGO_DETAILS = "mongodb://localhost:27017"


async def connect_to_mongo():
    print("Creating connection to Mongodb")
    db.client = AsyncIOMotorClient(MONGO_DETAILS)
    print("Connection Established")


async def close_mongo_connection():
    print("Closing connection")
    db.client.close()
    print("Connection closed")
