from aiogram import Bot
from aiogram.types import CallbackQuery

from data.database import get_user_section_by_id, get_us_words
from domain.user_section.callback_data import UserSectionsCD, EditUserSectionCD
from domain.user_section.keyboards import inline_edit_user_section, inline_user_section_words_kb
from resources.strings import Strings


async def edit_user_section(callback: CallbackQuery, callback_data: UserSectionsCD):
    user_section = get_user_section_by_id(str(callback_data.u_section_id))[0]
    await callback.message.edit_text(text=Strings.edit_user_section_info(user_section["section_title"]),
                                     inline_message_id=callback.inline_message_id,
                           reply_markup=inline_edit_user_section(str(user_section["id"])))
    await callback.answer()


async def finish_edit_user_section(callback: CallbackQuery, callback_data: EditUserSectionCD):
    us_id = callback_data.us_id
    words = get_us_words(us_id=us_id)
    user_section = get_user_section_by_id(us_id)[0]

    await callback.message.edit_text(text=user_section['section_title'],
                                         inline_message_id=callback.inline_message_id, reply_markup=
                                         inline_user_section_words_kb(us_id=str(us_id), words=words, page=0,
                                                                      ))
    await callback.answer()
