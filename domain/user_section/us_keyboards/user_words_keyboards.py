import math
from typing import Optional

import aiogram
from aiogram import types

from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.basic.words_voice import VoiceCD
from domain.user_section.callback_data import UserSectionsCD, UserSectionQuizCD, EditUserSectionCD
from resources.strings import Strings


LIMIT = 5


def get_pagination_form(callback_data, page: int, data_ln: int,
                        builder: Optional[InlineKeyboardBuilder] = None):
    total_ln = math.ceil(data_ln / LIMIT)
    loc_builder = builder if builder else InlineKeyboardBuilder()
    pagination_data = (page + 1 if page < total_ln-1 else page, page - 1 if page > 0 else page)
    next_cb, prev_cb = callback_data.copy(), callback_data.copy()
    next_cb.page, prev_cb.page = pagination_data[0], pagination_data[1]
    loc_builder.row(types.InlineKeyboardButton(text="<=",
                                           callback_data=prev_cb.pack()),
                types.InlineKeyboardButton(text=f"{page + 1}/{total_ln}", callback_data="0"),
                types.InlineKeyboardButton(text="=>",
                                           callback_data=next_cb.pack()))
    return builder


def get_user_words_form(words: list, page: int):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    words = words[page*LIMIT:page*LIMIT + LIMIT]
    for word in words:
        builder.add(types.InlineKeyboardButton(text=word["espanol"], callback_data=VoiceCD(is_user_section=True,
                                                                                           word_id=str(
                                                                                               word["id"])).pack()))
        builder.add(types.InlineKeyboardButton(text=word["russian"], callback_data=VoiceCD(is_user_section=True,
                                                                                           word_id=str(                                                                                            word["id"])).pack()))
    builder.adjust(2)

    return builder

def get_user_words_edit_form(words: list, page: int):
    builder = InlineKeyboardBuilder()
    words = words[page * LIMIT:page * LIMIT + LIMIT]
    for word in words:
        builder.add(types.InlineKeyboardButton(text=word["espanol"], callback_data="0"))
        builder.add(types.InlineKeyboardButton(text=word["russian"], callback_data="0"))
        builder.add(types.InlineKeyboardButton(text=Strings.nope_quiz, callback_data=EditUserSectionCD(
            action="delete_word", word_id=str(word["id"]), us_id=str(word["us_id"]), page=page
        ).pack()))
    builder.adjust(3)

    return builder

def inline_user_section_words_kb(us_id: str, words: list, page: int):
    callback_data = UserSectionsCD(action="show_us_words", page=0, u_section_id=us_id)

    builder = get_user_words_form(words, page=page)
    builder = get_pagination_form(callback_data=callback_data, page=page, data_ln=len(words), builder=builder)

    builder.row(types.InlineKeyboardButton(text=Strings.us_start_practice, callback_data=
                UserSectionQuizCD(action="start_user_section_quiz", us_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.edit_us_info, callback_data=UserSectionsCD(action="start_edit",
                                                                                                             u_section_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.back_button,
                                           callback_data=UserSectionsCD(action="back_to_user_sections",
                                                                        u_section_id=us_id).pack()))

    return builder.as_markup(resize_keyboard=True)

def inline_user_section_words_edit_kb(words: list, page: int = 0):
    us_id = str(words[0]["us_id"])
    callback_data = EditUserSectionCD(action="show_delete_word", page=page, us_id=us_id)
    builder = get_user_words_edit_form(words, page=page)
    builder =  get_pagination_form(callback_data=callback_data, page=page, data_ln=len(words), builder=builder)
    builder.row(types.InlineKeyboardButton(text=Strings.back_button,
                                           callback_data=EditUserSectionCD(action="back_to_edit", us_id=us_id).pack()))
    return builder.as_markup(resize_keyboard=True)
