from typing import List

from sqlalchemy import select, insert

from data.database import session_factory
from data.models.phrase_model import PhrasesModel
from domain.shemas.schemas_dto import PhrasesDto, PhrasesAddDto


async def get_phrases() -> List[PhrasesDto]:
    async with session_factory() as session:
        query = select(PhrasesModel)
        result = await session.execute(query)
        phrases = result.scalars().all()
        phrases_dto = [PhrasesDto.model_validate(row, from_attributes=True) for row in phrases]
        return phrases_dto


async def insert_phrase(phrase: PhrasesAddDto) -> None:
    async with session_factory() as session:
        phrase = PhrasesModel(ru=phrase.ru, es=phrase.es)
        session.add(phrase)
        await session.commit()

