from fastapi import APIRouter, HTTPException, exceptions

from models.auth_model import AuthIn
from models.user_model import UsersIn
from utils.message_util import MessageOut, output_message
from utils.auth_util import AuthHandler
from utils.generator_util import password_generator
from services.user_service import post_data
from services.auth_service import (
    fetch_data_by_username, fetch_new_data_by_username,
    fetch_new_output_data_by_username, fetch_data_by_username_for_new_password,
    put_last_login_user, put_new_password
)

router = APIRouter()
auth = AuthHandler()


@router.post("/", response_model=MessageOut)
async def auth_user(data: AuthIn):
    search_data = await fetch_data_by_username(data.username)
    if search_data is None:
        raise HTTPException(status_code=400, detail=f"Data with username: {data.username} is not exists!")
    is_valid = auth.verify_password(data.password, search_data.password)
    if is_valid is not True:
        raise HTTPException(status_code=401, detail="Username or password is not correct!")
    try:
        token = auth.encode_token(search_data.id)
        await put_last_login_user(data.username)
        output_data = await fetch_new_output_data_by_username(data.username, token)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when trying to login, {e}")
    return output_message(output_data, "Logged in successfully!")


@router.post("/register", status_code=201, response_model=MessageOut)
async def register_user(data: UsersIn):
    random_pass = password_generator()
    search_data = await fetch_data_by_username(data.username)
    if search_data:
        raise HTTPException(status_code=400, detail=f"User with username: {data.username} data already exists!")
    try:
        await post_data(data, random_pass)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when creating data, {e}")
    output_user = await fetch_new_data_by_username(data.username, random_pass)
    return output_message(output_user, "Data created successfully!")


@router.put("/reset-password", response_model=MessageOut)
async def reset_password_user(username: str):
    random_pass = password_generator()
    is_exists = await fetch_data_by_username(username)
    if is_exists is None:
        raise HTTPException(status_code=404, detail="Data not found!")
    try:
        await put_new_password(username, random_pass)
        output_data = await fetch_data_by_username_for_new_password(username, random_pass)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when updating new password data, {e}")
    return output_message(output_data, f"A new password updated successfully!")
