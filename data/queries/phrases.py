from typing import List

from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy import update
from sqlalchemy.orm.exc import NoResultFound
from data.database import session_factory
from data.models.phrase_model import PhrasesModel, UserPhrasesProgressModel
from domain.shemas.schemas_dto import PhrasesDto, PhrasesAddDto, UserPhrasesProgressDto, UserPhrasesProgressAddDto


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


async def select_current_phrase(tg_id: str) -> PhrasesDto | None:
    async with session_factory() as session:
        pm = aliased(PhrasesModel)
        up = aliased(UserPhrasesProgressModel)
        query = select(pm).join(up, up.phrase_id == pm.id).filter(up.tg_id == tg_id)
        progress = await session.execute(query)
        try:
            progress = progress.scalars().one()
            progress_dto = PhrasesDto.model_validate(progress, from_attributes=True)
            return progress_dto
        except NoResultFound as er:
            return None


async def select_phrase_by_id(phrase_id: str) -> PhrasesDto:
    async with session_factory() as session:
        query = select(PhrasesModel).where(PhrasesModel.id == phrase_id)
        phrase = await session.execute(query)
        try:
            phrase = phrase.scalars().one()
            phrase_dto = PhrasesDto.model_validate(phrase, from_attributes=True)
            return phrase_dto
        except NoResultFound:
            return None


async def update_current_phrase(phrase_progress: UserPhrasesProgressAddDto) -> None:
    async with session_factory() as session:
        phrase_progress = UserPhrasesProgressModel(tg_id=phrase_progress.tg_id, phrase_id=phrase_progress.phrase_id)
        query = (update(UserPhrasesProgressModel)
                 .where(UserPhrasesProgressModel.tg_id == phrase_progress.tg_id)
                 .values(phrase_id=phrase_progress.phrase_id))
        await session.execute(query)
        await session.commit()
