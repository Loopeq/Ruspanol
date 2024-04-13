from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from data.queries import get_user_section_by_id, get_us_words, insert_words_to_user_section, delete_word_by_id
from domain.user_section.callback_data import UserSectionsCD, EditUserSectionCD
from domain.user_section.fsm_states import UserSectionEdit
from domain.user_section.us_keyboards.keyboards import inline_edit_user_section, inline_back_to_edit
from domain.user_section.us_keyboards.user_words_keyboards import inline_user_section_words_kb, \
    inline_user_section_words_edit_kb
from domain.utils.common import parse_words
from resources.strings import Strings
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

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


async def edit_add_words_info(callback: CallbackQuery, callback_data: EditUserSectionCD, state: FSMContext):
    us_id = callback_data.us_id
    user_section = get_user_section_by_id(us_id)[0]

    await callback.message.edit_text(text=Strings.add_us_word_info(section_title=user_section["section_title"]),
                                     inline_message_id=callback.inline_message_id, reply_markup=inline_back_to_edit(us_id)
                    )
    await state.set_state(UserSectionEdit.edit_add_words)
    await state.update_data(us_id=us_id)
    await callback.answer()

async def edit_add_words(message: Message, state: FSMContext):
    data = await state.get_data()
    words = parse_words(message.text, data["us_id"])
    insert_words_to_user_section(words)
    await message.delete()

async def cmd_back_to_edit(callback: CallbackQuery, callback_data: EditUserSectionCD, state: FSMContext):
    await state.clear()
    us_id = callback_data.us_id
    user_section = get_user_section_by_id(us_id)[0]
    await callback.message.edit_text(text=Strings.edit_user_section_info(user_section["section_title"]),
                                     inline_message_id=callback.inline_message_id,
                                     reply_markup=inline_edit_user_section(str(user_section["id"])))
    await callback.answer()

async def show_words_to_delete(callback: CallbackQuery, callback_data: EditUserSectionCD):
    us_id = callback_data.us_id
    user_section = get_user_section_by_id(us_id)
    page = callback_data.page
    words = get_us_words(us_id)
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text=Strings.delete_word_us_info(
            user_section[0]["section_title"]
        ), inline_message_id=callback.inline_message_id, reply_markup=
        inline_user_section_words_edit_kb(words, page=page))
    await callback.answer()

async def delete_words(callback: CallbackQuery, callback_data: EditUserSectionCD):
    word_id, us_id, page = callback_data.word_id, callback_data.us_id, callback_data.page
    delete_word_by_id(word_id=word_id, us_id=us_id)
    user_section = get_user_section_by_id(us_id)
    words = get_us_words(us_id)
    await callback.message.edit_text(
        text=Strings.delete_word_us_info(
            user_section[0]["section_title"]
        ), inline_message_id=callback.inline_message_id, reply_markup=
        inline_user_section_words_edit_kb(words, page=page))
    await callback.answer()
