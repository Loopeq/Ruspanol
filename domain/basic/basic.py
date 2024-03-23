from aiogram.types import Message
from resources.strings import Strings
from data.database import get_sections
from domain.keyboards.keyboards import inline_section_kb

async def cmd_start(message: Message):
    await message.answer(Strings.hello_words)

async def cmd_sections(message: Message):
   await message.answer(Strings.available_sections, reply_markup=inline_section_kb(get_sections()))

async def cmd_profile(message: Message):
    await message.answer("Профиль")

