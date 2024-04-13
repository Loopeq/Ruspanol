from enum import Enum
from typing import Optional

from aiogram import types, Router, Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from magic_filter import F

from domain.utils.common import PLUG, clip_level
from resources.strings import Strings
from data.queries import get_sections

router = Router()


class SectionsCallbackActions(Enum):
    next = "next"
    prev = "prev"
    onClick = "onClick"


class SectionsCallback(CallbackData, prefix="sections_cd"):
    action: SectionsCallbackActions
    page: Optional[int] = 0
    length: Optional[int] = 0
    section_id: Optional[int] = 0


class SectionsState(StatesGroup):
    change_page = State()


def get_sections_ikb(sections: list[dict], page: int = 0):
    builder = InlineKeyboardBuilder()

    limit = 14
    length = len(sections) // limit

    sections = sections[limit * page:limit * page + limit]
    for section in sections:
        builder.add(InlineKeyboardButton(text=section["title"],
                                       callback_data=SectionsCallback(action=SectionsCallbackActions.onClick,
                                                                      sections_id=section["id"]).pack()),
                    InlineKeyboardButton(text=clip_level(section["level"]), callback_data=PLUG))

    builder.adjust(2)
    builder.row(
        InlineKeyboardButton(text='<=', callback_data=SectionsCallback(
            action=SectionsCallbackActions.prev, page=page, length=length).pack()),
        InlineKeyboardButton(text=f"{page + 1}/{length + 1}", callback_data=PLUG),
        InlineKeyboardButton(text='=>', callback_data=SectionsCallback(
            action=SectionsCallbackActions.next, page=page, length=length).pack()))

    return builder.as_markup(resize_keyboard=True)


@router.callback_query(SectionsCallback.filter(F.action.in_({SectionsCallbackActions.next,
                                                             SectionsCallbackActions.prev})))
async def sections_pagination(callback: CallbackQuery, callback_data: SectionsCallback, state: FSMContext):

    length = callback_data.length

    if callback_data.action == SectionsCallbackActions.next and callback_data.page != length:
        await callback.message.edit_text(Strings.sections_info,
                                         reply_markup=get_sections_ikb(get_sections(), page=callback_data.page + 1))
    elif callback_data.action == SectionsCallbackActions.prev and callback_data.page != 0:
        await callback.message.edit_text(Strings.sections_info,
                                         reply_markup=get_sections_ikb(get_sections(), page=callback_data.page - 1))
    await state.set_state(SectionsState.change_page)
    await callback.answer()

