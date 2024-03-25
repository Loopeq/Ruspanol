
import aiogram
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from resources.strings import Strings
from data.database import get_sections, insert_user, get_user_progression


async def cmd_start(message: Message):
    await message.answer(Strings.hello_words)
    try:
        insert_user(str(message.from_user.id))
    except Exception as error:
        print(error)


class SPagCallbackData(CallbackData, prefix="sec_pag"):
    action: str
    page: int
    total_count: int


class SPagState(StatesGroup):
    change_page = State()


def inline_section_kb(data: list[dict], page: int, user_id: int):
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()

    user_progress = get_user_progression(user_id=str(user_id))
    sections = [obj["section_id"] for obj in user_progress]

    padding = 10
    sec_count = padding * page
    total_count = len(data) // padding

    buttons = []
    data = data[sec_count:sec_count + padding]
    for ind in range(len(data)):
        is_complete = ""
        obj = data[ind]
        if obj["id"] in sections:
            is_complete = Strings.yes_quiz
        buttons.append(types.InlineKeyboardButton(text=obj["title"]+is_complete, callback_data=f"section{str(obj['id'])}" ))


    for button in buttons:
        builder.add(button)
    builder.adjust(2)
    builder.row(
                types.InlineKeyboardButton(text='<=', callback_data=SPagCallbackData(
                action="prev", page=page, total_count=total_count
                ).pack()),
                types.InlineKeyboardButton(text=f"{page+1}/{total_count+1}", callback_data="0"),
                types.InlineKeyboardButton(text='=>', callback_data=SPagCallbackData(
                    action="next", page=page, total_count = total_count
                ).pack())
        )

    return builder.as_markup(resize_keyboard=True)

async def cmd_sections(message: Message, state: FSMContext):
    await message.answer(Strings.available_sections, reply_markup=inline_section_kb(get_sections(), page=0, user_id=message.from_user.id))
    await state.set_state(SPagState.change_page)

async def cmd_change_page(callback: CallbackQuery, callback_data: SPagCallbackData, state: FSMContext):
    if callback_data.page == callback_data.total_count or callback_data.page == 0:
        await callback.answer()
        await state.set_state(SPagState.change_page)

    if callback_data.action == "next" and callback_data.page != callback_data.total_count:
        await state.update_data(page=callback_data.page + 1)
        await callback.message.edit_text(Strings.available_sections,
                                         reply_markup=inline_section_kb(get_sections(), page=callback_data.page + 1, user_id=callback.from_user.id))
    elif callback_data.action == "prev" and callback_data.page != 0:
        await state.update_data(page=callback_data.page - 1)
        await callback.message.edit_text(Strings.available_sections,
                                         reply_markup=inline_section_kb(get_sections(), page=callback_data.page - 1, user_id=callback.from_user.id))
    await state.set_state(SPagState.change_page)
    await callback.answer()




async def cmd_profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Профиль")

