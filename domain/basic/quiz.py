from aiogram import Bot
from aiogram.types import CallbackQuery

from data.database import get_words
from domain.filters.filters import QuizCallbackData
from domain.keyboards.keyboards import inline_return_to_words


async def cmd_start_quiz(callback: CallbackQuery, callback_data: QuizCallbackData):
    section_id = callback_data.section_id
    words = get_words(section_id)
    await callback.message.edit_text(text="Переведите", reply_markup=inline_return_to_words(section_id))

