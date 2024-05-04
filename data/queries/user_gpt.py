from data.database import session_factory
from data.models.user_model import UserHistGPTModel, Role


#
#
# def insert_history(user_id: int, message: str, is_user: bool = True):
#     cursor.execute("INSERT INTO UsersHist (user_id, message, is_user) VALUES(?, ?, ?)",
#                    (user_id, message, int(is_user)))
#     connection.commit()
#
#
# def get_history(user_id: int) -> tuple[dict, int]:
#     cursor.execute("SELECT * FROM UsersHist WHERE user_id = ?", (user_id,))
#     rows = get_rows(cursor)
#     cursor.execute("SELECT COUNT(*) as count FROM UsersHist WHERE user_id = ?", (user_id,))
#     count = get_rows(cursor)[0]["count"]
#     return rows, count
#
#
# def delete_history(user_id: int):
#     cursor.execute("DELETE FROM UsersHist WHERE user_id = ?", (user_id,))
#     connection.commit()

#
# async def insert_user(tg_id: int):
#     user = UserModel(tg_id=tg_id)
#     async with session_factory() as session:
#         existing_user = await session.scalars(select(UserModel).where(UserModel.tg_id == tg_id))
#         if existing_user.first():
#             return
#         session.add(user)
#         await session.commit()


async def insert_history(user_id: int, message: str, role: Role):
    history_obj = UserHistGPTModel(user_id=user_id, message=message, role=role)
    async with session_factory() as session:
        session.add(history_obj)
        await session.commit()


