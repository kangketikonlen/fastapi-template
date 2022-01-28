import os
import aiofiles

from werkzeug.utils import secure_filename
from fastapi import APIRouter, HTTPException, exceptions, File, UploadFile
from fastapi_pagination import Page, add_pagination, paginate

from utils.message_util import MessageOut, output_message
from models.user_model import UsersIn, UsersOut
from utils.generator_util import password_generator
from services.user_service import (
    fetch_all_data, fetch_data_by_username, post_data, fetch_data_by_id, put_data,
    delete_data, put_new_profile_picture
)

router = APIRouter()

BASE_PATH = os.path.abspath(os.path.dirname("."))
PROFILE_UPLOAD_PATH = os.path.join(BASE_PATH, "assets/images/profiles/")


@router.get("/", response_model=Page[UsersOut])
async def show_all_users():
    documents = await fetch_all_data()
    return paginate(documents)


@router.post("/", status_code=201, response_model=MessageOut)
async def create_user(data: UsersIn):
    random_pass = password_generator()
    search_data = await fetch_data_by_username(data.username)
    if search_data:
        raise HTTPException(status_code=400, detail=f"This {data.username} data exists!")
    try:
        await post_data(data, random_pass)
        output_data = await fetch_data_by_username(data.username)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when creating data, {e}")
    return output_message(output_data, f"Data created successfully. The password is {random_pass}!")


@router.get("/{user_id}", response_model=UsersOut)
async def get_single_user(user_id: str):
    document = await fetch_data_by_id(user_id)
    if document:
        return document
    raise HTTPException(status_code=404, detail="Data not found!")


@router.put("/{user_id}", response_model=MessageOut)
async def update_user(user_id: str, data: UsersIn):
    is_exists = await fetch_data_by_id(user_id)
    if is_exists is None:
        raise HTTPException(status_code=404, detail="Data not found!")
    is_duplicate = await fetch_data_by_username(data.username)
    if is_duplicate and is_exists.username != data.username:
        raise HTTPException(status_code=400, detail=f"This {data.username} data exists!")
    try:
        await put_data(user_id, data)
        output_data = await fetch_data_by_username(data.username)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when creating data, {e}")
    return output_message(output_data, "Data updated successfully!")


@router.delete("/{user_id}", response_model=MessageOut)
async def delete_user(user_id: str):
    is_exists = await fetch_data_by_id(user_id)
    if is_exists is None:
        raise HTTPException(status_code=404, detail="Data not found!")
    try:
        await delete_data(user_id)
        output_data = await fetch_data_by_id(user_id)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when deleting data, {e}")
    return output_message(output_data, "Data deleted successfully!")


@router.put("/upload-profile/{user_id}", response_model=MessageOut)
async def upload_profile_user(user_id: str, file: UploadFile = File(...)):
    is_exists = await fetch_data_by_id(user_id)
    if is_exists is None:
        raise HTTPException(status_code=404, detail="Data not found!")
    try:
        ext = file.filename.rsplit(".", 1)[1]
        filename = secure_filename(user_id + "." + ext).lower()
        folder = os.path.join(PROFILE_UPLOAD_PATH, filename)
        async with aiofiles.open(folder, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        await put_new_profile_picture(user_id, filename)
        output_data = await fetch_data_by_id(user_id)
    except exceptions as e:
        raise HTTPException(status_code=400, detail=f"Server error when updating profile picture, {e}")
    return output_message(output_data, "Profile picture updated successfully!")


add_pagination(router)
