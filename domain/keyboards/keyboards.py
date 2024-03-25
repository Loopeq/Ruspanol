import aiogram.utils.keyboard
import aiogram
from aiogram import types

from resources.strings import Strings


def inline_quiz_info(section_id: int, total_count: int, true_count: int, false_count: int,
                     user_answer: str = None, current_answer: str = None):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=str(true_count) + Strings.yes_quiz, callback_data="0"))
    builder.add(types.InlineKeyboardButton(text=str(false_count) + Strings.nope_quiz, callback_data="0"))
    builder.add(types.InlineKeyboardButton(text=Strings.total_quiz + str(total_count), callback_data="0"))
    if user_answer and current_answer:
        builder.row(types.InlineKeyboardButton(text=f"Ваш ответ: {user_answer}", callback_data="0"), width=1)
        builder.row(types.InlineKeyboardButton(text=f"Правильный ответ: {current_answer}", callback_data="0"), width=1)
        builder.adjust(3,1,1)
    builder.row(types.InlineKeyboardButton(text=Strings.quit_button, callback_data=f"return_to_words{section_id}"), width=1)

    return builder.as_markup(resize_keyboard=True)

def inline_return_to_section_kb():
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)

def inline_delete_voice(word_id):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.delete_voice_button, callback_data=f"delete_voice{word_id}"), width=1)
    return builder.as_markup(resize_keyboard=True)