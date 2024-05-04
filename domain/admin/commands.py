import enum

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from data.queries.user import select_users
from data.queries.user_history import select_history
from domain.filters import IsAdminFilter


class AdminCommands(enum.Enum):
    admin = "admin"


router = Router()


@router.message(Command(AdminCommands.admin.value), IsAdminFilter())
async def cmd_admin(message: Message):
    await message.answer("Admin")
    history = await select_history(tg_id=message.from_user.id, limit=5)
    print(history)

