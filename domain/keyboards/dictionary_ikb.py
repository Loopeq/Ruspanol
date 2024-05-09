from enum import StrEnum
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class DictionaryCallbackData(CallbackData, prefix="dictionary"):
    action: str


class DictionaryActions(StrEnum):
    test = "test"


def dictionary_ikb():

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Начать тест🧾",
                                     callback_data=DictionaryCallbackData(action=DictionaryActions.test).pack()))
    return builder.as_markup()

