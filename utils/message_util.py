from pydantic import BaseModel
from typing import Optional


class MessageOut(BaseModel):
    data: Optional[dict] = []
    message: str


def output_message(data, message):
    return MessageOut(data=data, message=message)
