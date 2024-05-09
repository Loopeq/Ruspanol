from typing import List

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import aliased

from data.database import session_factory
from data.models.dictionary_model import DictionaryModel
from data.models.phrase_model import PhrasesModel
from domain.shemas.schemas_dto import DictionaryAddDto, PhrasesDto


async def select_user_dictionary(tg_id: str) -> List[PhrasesDto] | None:
    async with session_factory() as session:
        dm = aliased(DictionaryModel)
        pm = aliased(PhrasesModel)
        query = select(pm).join(dm, pm.id == dm.phrase_id).filter(dm.tg_id == tg_id)
        result = await session.execute(query)
        phrases_from_dict = result.scalars().all()
        phrases_from_dict_dto = [PhrasesDto.model_validate(row, from_attributes=True) for row in phrases_from_dict]
        return phrases_from_dict_dto


async def insert_phrase_into_dictionary(phrase: DictionaryAddDto):
    async with session_factory() as session:
        phrase = DictionaryModel(tg_id=phrase.tg_id, phrase_id=phrase.phrase_id)
        session.add(phrase)
        await session.commit()

