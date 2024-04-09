import aiogram
from aiogram import types
from data.database import get_user_sections
from domain.basic.words_voice import VoiceCD
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


def inline_user_section_words_kb(us_id: str, words: list, page: int = 0):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    limit = 5
    total_ln = len(words) // limit
    pagination_data = (page + 1 if page < total_ln else page, page - 1 if page > 0 else page)
    words = words[page*limit:page*limit + limit]

    for word in words:
        builder.add(types.InlineKeyboardButton(text=word["espanol"], callback_data=VoiceCD(is_user_section=True,
                                                                                           word_id=str(
                                                                                               word["id"])).pack()))
        builder.add(types.InlineKeyboardButton(text=word["russian"], callback_data=VoiceCD(is_user_section=True,
                                                                                           word_id=str(
                                                                                               word["id"])).pack()))
    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text="<=",
                                           callback_data=UserSectionsCD(action="show_us_words", page=pagination_data[1],
                                                                        u_section_id=us_id
                                                                        ).pack()),
                types.InlineKeyboardButton(text=f"{page + 1}/{total_ln + 1}", callback_data="0"),
                types.InlineKeyboardButton(text="=>",
                                           callback_data=UserSectionsCD(action="show_us_words", page=pagination_data[0],
                                                                        u_section_id=us_id
                                                                        ).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.us_start_practice, callback_data=
                UserSectionQuizCD(action="start_user_section_quiz", us_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.edit_us_info, callback_data=UserSectionsCD(action="edit_us",
                                                                                                             u_section_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.back_button,
                                           callback_data=UserSectionsCD(action="back_to_user_sections",
                                                                        u_section_id=us_id).pack()))

    return builder.as_markup(resize_keyboard=True)


def inline_user_section_quiz_kb(correct: int, incorrect: int, total: int, word: str,
                                correct_answer: str = "", user_answer: str = ""):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"{word}", callback_data="0"))
    builder.row(
        types.InlineKeyboardButton(text=f"{correct}{Strings.yes_quiz}", callback_data="0"),
        types.InlineKeyboardButton(text=f"{incorrect}{Strings.nope_quiz}", callback_data="0"),
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
    builder.row(types.InlineKeyboardButton(text=Strings.add_word_to_us, callback_data=UserSectionsCD(action="add_word_to_us").pack()))

    builder.row(types.InlineKeyboardButton(text=Strings.remove_section,
                                           callback_data=UserSectionsCD(action="remove_user_section",
                                                                        u_section_id=us_id).pack()))

    builder.row(types.InlineKeyboardButton(text=Strings.cancel_edit, callback_data=EditUserSectionCD(action="cancel_edit_us", us_id=us_id).pack()))
    return builder.as_markup(resize_keyboard=True)
