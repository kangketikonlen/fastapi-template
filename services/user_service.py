import uuid
import datetime

from utils.auth_util import AuthHandler
from utils.connection_util import database
from models.user_model import UsersOut, UsersDB, UserChangeProfilePicture

auth = AuthHandler()
collection = database.users


async def fetch_all_data():
    users = []
    cursor = collection.find({})
    async for document in cursor:
        users.append(UsersOut(**document))
    return users


async def post_data(data, random_pass):
    document = data.dict()
    hashed_password = auth.get_password_hash(random_pass)
    result = await collection.insert_one(
        UsersDB(
            **document,
            id=str(uuid.uuid4()),
            password=hashed_password,
            profile_image="/assets/images/profiles/default.png",
            created_at=datetime.datetime.today()
        ).dict()
    )
    return result


async def fetch_data_by_id(uid):
    document = await collection.find_one({"id": uid})
    if document:
        return UsersOut(**document)


async def fetch_data_by_username(username):
    document = await collection.find_one({"username": username})
    if document:
        return UsersOut(**document)


async def put_data(uid, new_data):
    old_data = await collection.find_one({"id": uid})
    response = await collection.update_one(
        {"id": uid},
        {
            "$set": UsersDB(
                **new_data.dict(),
                id=uid,
                password=old_data["password"],
                profile_image=old_data["profile_image"],
                created_at=old_data["created_at"],
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    return response


async def delete_data(uid):
    response = await collection.delete_one({"id": uid})
    return response


async def put_new_profile_picture(uid, filename):
    response = await collection.update_one(
        {"id": uid},
        {
            "$set": UserChangeProfilePicture(
                profile_image=f"assets/images/profiles/{filename}",
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    return response
