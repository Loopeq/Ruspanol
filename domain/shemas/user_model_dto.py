import datetime

from pydantic import BaseModel


class UserAddDto(BaseModel):
    tg_id: str


class UserDto(UserAddDto):
    id: int
    created_at: datetime.datetime


