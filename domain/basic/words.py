import aiogram
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from data.database import get_section, get_words
from domain.filters.filters import QuizCallbackData
from domain.keyboards.keyboards import inline_return_to_section_kb
from domain.utils.common import clip_id
from resources.strings import Strings


class WordsPag(CallbackData, prefix="w_pag"):
    action: str
    page: int
    total_count: int

class FSMPagWords(StatesGroup):
    select_page = State()


def inline_words_kb(words, page: int, is_us: bool = False):

    padding = 10
    current_page = padding * page
    total_count = len(words) // padding
    builder = aiogram.utils.keyboard.InlineKeyboardBuilder()
    for word in words[current_page:current_page+padding]:
        builder.add(types.InlineKeyboardButton(text=f"{word['espanol']}", callback_data=f'word{word["id"]}'))
        builder.add(types.InlineKeyboardButton(text=f"{word['russian']}", callback_data=f'word{word["id"]}'))
    builder.adjust(2)
    builder.row(
        types.InlineKeyboardButton(text='<=', callback_data=WordsPag(
            action="prev", page=page, total_count=total_count
        ).pack()),
        types.InlineKeyboardButton(text=f"{page + 1}/{total_count+1}", callback_data="0"),
        types.InlineKeyboardButton(text='=>', callback_data=WordsPag(
            action="next", page=page, total_count=total_count
        ).pack())
    )
    if not is_us:
        builder.row(types.InlineKeyboardButton(text=Strings.start_quiz,
                                           callback_data=QuizCallbackData(stage=0, section_id=words[0]["section_id"]).pack()), width=1)
        builder.row(types.InlineKeyboardButton(text=Strings.back_button, callback_data="return_to_sections"), width=1)
    return builder.as_markup(resize_keyboard=True)


async def cmd_words(callback: CallbackQuery, state: FSMContext):

    section_id = clip_id(callback.data, "section")
    section = get_section(section_id)[0]
    words = get_words(section_id)

    if not words:
        await callback.message.edit_text(text=Strings.oops_message,
                                         reply_markup=inline_return_to_section_kb())
    else:
        await callback.message.edit_text(text=section['title'] + Strings.voice_info,
                                         reply_markup=inline_words_kb(words=words, page=0))
        await state.update_data(words=words, section_title=section["title"])
        await state.set_state(FSMPagWords.select_page)

    await callback.answer()


async def cmd_words_pag(callback: CallbackQuery, callback_data, state: FSMContext):
    if callback_data.page == callback_data.total_count or callback_data.page == 0:
        await callback.answer()
        await state.set_state(FSMPagWords.select_page)
    data = await state.get_data()
    if callback_data.action == "next" and callback_data.page != callback_data.total_count:
        await state.update_data(page=callback_data.page + 1)
        await callback.message.edit_text(text=data['section_title'] + Strings.voice_info,
                                         reply_markup=inline_words_kb(words=data["words"], page=callback_data.page + 1))
    elif callback_data.action == "prev" and callback_data.page != 0:
        await state.update_data(page=callback_data.page - 1)
        await callback.message.edit_text(text=data['section_title'] + Strings.voice_info,
                                         reply_markup=inline_words_kb(words=data["words"], page=callback_data.page -1))
    await state.set_state(FSMPagWords.select_page)
    await callback.answer()