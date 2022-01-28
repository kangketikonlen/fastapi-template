import datetime

from utils.connection_util import database
from utils.auth_util import AuthHandler
from models.auth_model import RegisterOut, AuthOut, NewPassOut

collection = database.users
auth = AuthHandler()


async def fetch_data_by_username(username, password=""):
    document = await collection.find_one({"username": username})
    if document and password != "":
        document["password"] = password
        return RegisterOut(**document)
    else:
        return None


async def fetch_new_data_by_username(username, password):
    document = await collection.find_one({"username": username})
    if document:
        document["password"] = password
        return RegisterOut(**document)


async def fetch_new_output_data_by_username(username, token):
    document = await collection.find_one({"username": username})
    if document:
        document["token"] = token
    return AuthOut(**document)


async def fetch_data_by_username_for_new_password(username, password):
    document = await collection.find_one({"username": username})
    if document:
        document["password"] = password
        return NewPassOut(**document)


async def put_last_login_user(username):
    response = await collection.update_one(
        {"username": username},
        {
            "$set": {"last_login": datetime.datetime.today()}
        }
    )
    return response


async def put_new_password(username, password):
    hashed_password = auth.get_password_hash(password)
    response = await collection.update_one(
        {"username": username},
        {
            "$set": NewPassOut(
                password=hashed_password,
                updated_at=datetime.datetime.today()
            ).dict()
        }
    )
    return response
