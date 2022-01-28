import datetime

from typing import Optional
from pydantic import BaseModel


class UsersIn(BaseModel):
    fullname: str
    username: str


class UsersOut(BaseModel):
    id: str
    fullname: str
    username: str
    profile_image: str
    last_login: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


class UsersDB(BaseModel):
    id: str
    fullname: str
    username: str
    password: str
    profile_image: str
    last_login: Optional[datetime.datetime]
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime]


class UserChangeProfilePicture(BaseModel):
    profile_image: str
    updated_at: Optional[datetime.datetime]
