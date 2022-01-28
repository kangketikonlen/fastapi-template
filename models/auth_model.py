import datetime

from pydantic import BaseModel


class AuthIn(BaseModel):
    username: str
    password: str


class AuthOut(BaseModel):
    id: str
    fullname: str
    token: str
    last_login: datetime.datetime


class RegisterOut(BaseModel):
    id: str
    username: str
    password: str
    created_at: datetime.datetime


class NewPassOut(BaseModel):
    password: str
    updated_at: datetime.datetime
