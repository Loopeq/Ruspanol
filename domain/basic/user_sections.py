import asyncio

import aiogram
from aiogram import types, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from data.database import get_user_sections, insert_user_section, get_user_section_id, insert_words_to_user_section, \
    get_us_words
from domain.basic.words import inline_words_kb
from domain.utils.common import parse_words
from resources.strings import Strings

class UserSectionsCD(CallbackData, prefix="user_section"):
    action: str
    u_section_id: int = None

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


def inline_user_sections_cancel_kn():
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=Strings.cancel_button, callback_data="cancel_add_user_section"))
    return builder.as_markup(resize_keyboard=True)



async def cmd_my_sections(message: Message):
    await message.answer(Strings.available_user_sections, reply_markup=inline_user_sections_kb(message.from_user.id))

async def add_user_section_title(callback: CallbackQuery, bot: Bot, state: FSMContext):
    message = await bot.send_message(callback.from_user.id, Strings.add_us_title, reply_markup=inline_user_sections_cancel_kn())
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
                                reply_markup=inline_user_sections_cancel_kn())


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
    await callback.message.edit_text(text="Доступные слова", inline_message_id=callback.inline_message_id, reply_markup=
                                     inline_words_kb(words=words, page=0, is_us=True))







