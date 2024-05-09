import datetime

from pydantic import BaseModel

from data.models.user_model import Role


class UserAddDto(BaseModel):
    tg_id: int


class UserDto(UserAddDto):
    id: int
    created_at: datetime.datetime


class UserHistAddDto(BaseModel):
    tg_id: str
    message: str
    role: Role


class UserHistDto(UserHistAddDto):
    id: int


class PhrasesAddDto(BaseModel):
    ru: str
    es: str


class PhrasesDto(PhrasesAddDto):
    id: int


class UserPhrasesProgressAddDto(BaseModel):
    tg_id: str
    phrase_id: int


class UserPhrasesProgressDto(UserPhrasesProgressAddDto):
    id: int


class DictionaryAddDto(BaseModel):
    tg_id: str
    phrase_id: int


class DictionaryDto(DictionaryAddDto):
    id: int
    score: int
