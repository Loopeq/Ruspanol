from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PhrasesCallbackData(CallbackData, prefix="phrases"):
    action: str


class PhrasesActions(StrEnum):
    add = "add"
    next = "next"
    voice = "voice"


def phrases_ikb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Добавить📖",
                             callback_data=PhrasesCallbackData(action=PhrasesActions.add).pack()),
        InlineKeyboardButton(text="Пропустить➡️",
                             callback_data=PhrasesCallbackData(action=PhrasesActions.next).pack()))
    builder.row(
        InlineKeyboardButton(text="Озвучить🎤",
                             callback_data=PhrasesCallbackData(action=PhrasesActions.voice).pack())
    )

    builder.adjust(2, 1)
    return builder.as_markup()
