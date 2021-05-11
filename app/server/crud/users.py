from ..db.config import database_name, users_collection_name
from ..db.mongodb import AsyncIOMotorClient
from ..models.users import User, UserInDB, UserInUpdate, UserInResponse
from bson.objectid import ObjectId
from .auth import get_password_hash


async def get_all(conn: AsyncIOMotorClient):
    users = []
    rows = conn[database_name][users_collection_name].find()
    async for row in rows:
        users.append(UserInResponse(**row))
    return users


async def create(conn: AsyncIOMotorClient, user: User):
    user.password = get_password_hash(user.password)
    rows = await conn[database_name][users_collection_name].insert_one(user.dict())
    data = await get_by_id(conn, rows.inserted_id)
    return data


async def get_by_id(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][users_collection_name].find_one({"_id": ObjectId(id)})
    return UserInResponse(**row)


async def update(conn: AsyncIOMotorClient, id: str,  user: UserInUpdate):
    updateObject = {}
    if(user.userName):
        updateObject['userName'] = user.userName
    updateObject['isAdmin'] = user.isAdmin
    updateObject['isActive'] = user.isActive
    row = await conn[database_name][users_collection_name].update_one({"_id": ObjectId(id)}, {'$set': updateObject})
    data = await get_by_id(conn, id)
    return data


async def delete(conn: AsyncIOMotorClient, id: str):
    row = await conn[database_name][users_collection_name].delete_one({"_id": ObjectId(id)})
    return row.deleted_count
