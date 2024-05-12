from enum import StrEnum
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from domain.keyboards.constants import PLUG


class DictionaryCallbackData(CallbackData, prefix="dictionary"):
    action: str


class DictionaryActions(StrEnum):
    test = "test"


def dictionary_ikb():

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Начать тест🧾",
                                     callback_data=DictionaryCallbackData(action=DictionaryActions.test).pack()))
    return builder.as_markup()


def test_ikb(total_count: int, correct_count: int = 0, incorrect_count: int = 0):

    builder = InlineKeyboardBuilder()

    if (correct_count + incorrect_count) == 0:
        return None

    builder.add(InlineKeyboardButton(text=f"{correct_count}🟢", callback_data=PLUG),
                InlineKeyboardButton(text=f"{correct_count+incorrect_count}/{total_count}", callback_data=PLUG),
                InlineKeyboardButton(text=f"{incorrect_count}🔴", callback_data=PLUG))

    return builder.as_markup(resize_keyboard=True)
