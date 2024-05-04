from typing import List

from sqlalchemy import select, delete

from data.database import session_factory
from data.models.user_model import UserHistModel
from domain.shemas.schemas_dto import UserHistAddDto, UserHistDto


async def insert_history(user_history: UserHistAddDto) -> None:
    history_obj = UserHistModel(tg_id=user_history.tg_id, message=user_history.message, role=user_history.role)
    async with session_factory() as session:
        session.add(history_obj)
        await session.commit()


async def select_history(tg_id: int, limit: int) -> List[UserHistDto]:
    async with session_factory() as session:
        query = select(UserHistModel).filter(UserHistModel.tg_id == tg_id)\
            .order_by(UserHistModel.id.desc()).limit(limit)
        result = await session.execute(query)
        history = result.scalars().all()
        history_dto = [UserHistDto.model_validate(row, from_attributes=True) for row in history]
        return history_dto


async def delete_history(tg_id: int) -> None:
    async with session_factory() as session:
        query = delete(UserHistModel).filter(UserHistModel.tg_id == tg_id)
        await session.execute(query)
        await session.commit()
