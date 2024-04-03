import asyncio

import aiogram
from aiogram import types, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from data.database import get_user_sections, insert_user_section, get_user_section_id, insert_words_to_user_section, \
    get_us_words, get_user_section_by_id, delete_user_section, get_user_id_by_us_id
from domain.basic.words_voice import VoiceCD
from domain.utils.common import parse_words
from resources.strings import Strings

class UserSectionsCD(CallbackData, prefix="user_section"):
    action: str
    u_section_id: int = None

class UserSectionsWordsCD(CallbackData, prefix="user_section_words"):
    action: str


class UserSectionState(StatesGroup):
    add_title = State()
    add_words = State()


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

def inline_user_section_words_kb(us_id: str, words: list):

    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()

    for word in words:
        builder.add(types.InlineKeyboardButton(text=word["espanol"], callback_data=VoiceCD(is_user_section=True, word_id=str(word["id"])).pack()))
        builder.add(types.InlineKeyboardButton(text=word["russian"], callback_data=VoiceCD(is_user_section=True, word_id=str(word["id"])).pack()))
    builder.adjust(2)
    builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data=UserSectionsCD(action="back_to_user_sections", u_section_id=us_id).pack()))
    builder.row(types.InlineKeyboardButton(text=Strings.remove_section,
                                           callback_data=UserSectionsCD(action="remove_user_section",
                                                                        u_section_id=us_id).pack()))

    return builder.as_markup(resize_keyboard=True)

async def cmd_back_to_user_sections(callback: CallbackQuery, callback_data: UserSectionsCD):
    user_id = get_user_id_by_us_id(us_id=str(callback_data.u_section_id))[0]["user_id"]
    await callback.message.edit_text(text=Strings.available_user_sections, inline_message_id=callback.inline_message_id,
                                     reply_markup=inline_user_sections_kb(user_id=user_id))


def inline_user_sections_cancel_kb():
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.cancel_button, callback_data="cancel_add_user_section"))
    return builder.as_markup(resize_keyboard=True)



async def cmd_my_sections(message: Message):
    await message.answer(Strings.available_user_sections, reply_markup=inline_user_sections_kb(message.from_user.id))

async def add_user_section_title(callback: CallbackQuery, bot: Bot, state: FSMContext):
    message = await bot.send_message(callback.from_user.id, Strings.add_us_title, reply_markup=inline_user_sections_cancel_kb())
    await state.set_state(UserSectionState.add_title)
    await state.update_data(current_message=message)
    await callback.answer()

async def add_user_section_words(message: Message, state: FSMContext, bot: Bot):
    title = message.text
    await state.update_data(title=title)
    await message.delete()
    await state.set_state(UserSectionState.add_words)
    data = await state.get_data()

    current_message_id = data["current_message"].message_id
    await bot.edit_message_text(text=Strings.add_us_word_info(section_title=title), chat_id=message.from_user.id, message_id=current_message_id,
                                reply_markup=inline_user_sections_cancel_kb())


async def add_user_section_finish(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(words=message.text)
    data = await state.get_data()
    current_message = data["current_message"]
    section_title = data["title"]
    await bot.edit_message_text(text=Strings.add_us_final_info(section_title), chat_id=message.from_user.id,
                                message_id=current_message.message_id)



    insert_user_section(str(message.from_user.id), section_title=section_title)
    us_id = get_user_section_id(user_id=str(message.from_user.id), section_title=section_title)[0]["id"]
    words = parse_words(words=data["words"], us_id=us_id)
    insert_words_to_user_section(words)

    await message.delete()
    await state.clear()

async def cancel_add_us(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if data:
        current_message = data["current_message"]
        await bot.delete_message(callback.from_user.id, current_message.message_id)
    else:
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await state.clear()
    await callback.answer()

async def get_user_section_words(callback: CallbackQuery, callback_data: UserSectionsCD):
    us_id = callback_data.u_section_id
    words = get_us_words(us_id=str(us_id))
    user_section = get_user_section_by_id(str(us_id))[0]
    await callback.message.edit_text(text=user_section['section_title'], inline_message_id=callback.inline_message_id, reply_markup=
                                     inline_user_section_words_kb(us_id=str(us_id), words=words))



async def remove_user_section(callback: CallbackQuery, callback_data: UserSectionsCD):
    us_id = callback_data.u_section_id
    delete_user_section(str(us_id))
    await callback.message.edit_text(text=Strings.available_sections, reply_markup=inline_user_sections_kb(callback.from_user.id))
    await callback.answer()



