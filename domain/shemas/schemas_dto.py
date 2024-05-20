import datetime

from pydantic import BaseModel


class UserAddDto(BaseModel):
    tg_id: int


class UserDto(UserAddDto):
    id: int
    created_at: datetime.datetime


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
