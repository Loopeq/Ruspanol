import enum

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from domain.filters import IsAdminFilter


class AdminCommands(enum.Enum):
    admin = "admin"


router = Router()


@router.message(IsAdminFilter())
@router.message(Command(AdminCommands.admin.value))
async def cmd_admin(message: Message):
    await message.answer("Admin")

