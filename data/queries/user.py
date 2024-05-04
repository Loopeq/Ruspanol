from typing import List

from sqlalchemy import select

from data.models.user_model import UserModel
from data.database import engine, session_factory, Base
from domain.shemas.schemas_dto import UserAddDto, UserDto


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def insert_user(user: UserAddDto):
    async with session_factory() as session:
        existing_user = await session.scalars(select(UserModel).where(UserModel.tg_id == user.tg_id))
        if existing_user.first():
            return
        user = UserModel(tg_id=user.tg_id)
        session.add(user)
        await session.commit()


async def select_users() -> List[UserDto]:
    async with session_factory() as session:
        query = select(UserModel)
        result = await session.execute(query)
        users = result.scalars().all()
        users_dto = [UserDto.model_validate(row, from_attributes=True) for row in users]
        return users_dto
