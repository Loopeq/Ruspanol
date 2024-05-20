from typing import List

from sqlalchemy import select, update, and_, func, asc
from sqlalchemy.orm import aliased

from data.database import session_factory
from data.models.dictionary_model import DictionaryModel
from data.models.phrase_model import PhrasesModel
from domain.dictionary.dictionary_ikb import TestFilterActions
from domain.shemas.schemas_dto import DictionaryAddDto, PhrasesDto


async def select_user_dictionary(tg_id: str, o_filter: TestFilterActions = None, limit: int = 10) \
        -> List[PhrasesDto] | None:
    async with session_factory() as session:
        dm = aliased(DictionaryModel)
        pm = aliased(PhrasesModel)
        query = select(pm).join(dm, pm.id == dm.phrase_id).filter(dm.tg_id == tg_id)

        match o_filter:
            case TestFilterActions.newest:
                query = query.order_by(asc(dm.created_at)).limit(limit)
            case TestFilterActions.unexplored:
                query = query.order_by(asc(dm.score)).limit(limit)
            case TestFilterActions.random:
                query = query.order_by(func.random()).limit(limit)

        result = await session.execute(query)
        phrases_from_dict = result.scalars().all()
        phrases_from_dict_dto = [PhrasesDto.model_validate(row, from_attributes=True) for row in phrases_from_dict]
        return phrases_from_dict_dto


async def insert_phrase_into_dictionary(phrase: DictionaryAddDto):
    async with session_factory() as session:
        phrase = DictionaryModel(tg_id=phrase.tg_id, phrase_id=phrase.phrase_id)
        session.add(phrase)
        await session.commit()


async def update_score(tg_id: str, phrase_id: int):
    async with session_factory() as session:
        query = update(DictionaryModel).filter(
            and_(DictionaryModel.tg_id == tg_id, DictionaryModel.phrase_id == phrase_id)) \
            .values(
            score=DictionaryModel.score + 1)
        await session.execute(query)
        await session.commit()


async def select_count_of_phrases(tg_id: str) -> int | None:
    async with session_factory() as session:
        query = select(func.count()).select_from(DictionaryModel).filter(DictionaryModel.tg_id == tg_id)
        count = await session.execute(query)
        count = count.scalar()
        return count


async def select_score_percent(tg_id: str) -> int:
    phrase_count = await select_count_of_phrases(tg_id=tg_id)
    async with session_factory() as session:
        query = select(func.sum(DictionaryModel.score)).select_from(DictionaryModel).filter(
            DictionaryModel.tg_id == tg_id)
        score_sum = await session.execute(query)
        score_sum = score_sum.scalar()
        return int(score_sum / (phrase_count * 10) * 100)

