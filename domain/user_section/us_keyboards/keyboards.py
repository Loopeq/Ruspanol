from typing import Optional

import aiogram
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery

from data.queries import get_user_sections
from domain.fixme.words_voice import VoiceCD
from domain.user_section.callback_data import UserSectionQuizCD, UserSectionsCD, EditUserSectionCD
from resources.strings import Strings


def inline_user_sections_kb(user_id):
    user_sections = get_user_sections(str(user_id))
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    add_button = types.InlineKeyboardButton(text=Strings.add_user_section, callback_data="add_user_sections")
    if user_sections:
        for section in user_sections:
            builder.row(types.InlineKeyboardButton(text=section["section_title"],
                                                   callback_data=UserSectionsCD(action="show_us_words",
                                                                                u_section_id=section["id"]).pack()))
    builder.row(add_button)
    return builder.as_markup(resize_keyboard=True)



def inline_user_section_quiz_kb(correct: int, incorrect: int, total: int, word: str, is_correct: bool = None,
                                correct_answer: str = "", user_answer: str = ""):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{word}", callback_data="0"))

    correct_icon = Strings.yes_quiz if is_correct else ''
    incorrect_icon = Strings.nope_quiz if not is_correct and is_correct is not None else ''

    builder.row(
        types.InlineKeyboardButton(text=f"{correct}{correct_icon}", callback_data="0"),
        types.InlineKeyboardButton(text=f"{incorrect}{incorrect_icon}", callback_data="0"),
        types.InlineKeyboardButton(text=f"{total}", callback_data="0"),
    )
    if correct_answer and user_answer:
        builder.row(types.InlineKeyboardButton(text=f"Ваш ответ: {user_answer}", callback_data="0"))
        builder.row(types.InlineKeyboardButton(text=f"Правильный ответ: {correct_answer}", callback_data="0"))
    builder.row(types.InlineKeyboardButton(text=Strings.cancel_user_quiz,
                                           callback_data="finish_user_section_quiz"))

    return builder.as_markup(resize_keyboard=True)


def inline_edit_user_section(us_id: str):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.add_word_to_us,
                                           callback_data=EditUserSectionCD(action="add_words", us_id=us_id).pack()),
    types.InlineKeyboardButton(text=Strings.delete_word_info, callback_data=EditUserSectionCD(action="delete_word", us_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.remove_section,
                                           callback_data=UserSectionsCD(action="remove_user_section",
                                                                        u_section_id=us_id).pack()))

    builder.row(types.InlineKeyboardButton(text=Strings.cancel_edit, callback_data=EditUserSectionCD(action="cancel_edit_us", us_id=us_id).pack()))
    return builder.as_markup(resize_keyboard=True)

def inline_back_to_edit(us_id: str):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text=Strings.back_button,
                                           callback_data=EditUserSectionCD(action="back_to_edit", us_id=us_id).pack()))
    return builder.as_markup(resize_keyboard=True)

