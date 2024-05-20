from enum import StrEnum
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from domain.keyboards.constants import PLUG


class DictionaryCallbackData(CallbackData, prefix="dictionary"):
    action: str


class DictionaryActions(StrEnum):
    test = "test"
    phrases = "phrases"


class TestFilterActions(StrEnum):
    unexplored = "unexplored"
    newest = "newest"
    random = "random"


def dictionary_ikb():

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Начать тест🧾",
                                     callback_data=DictionaryCallbackData(action=DictionaryActions.test).pack()),
                InlineKeyboardButton(text="Посмотреть свои фразы✍️",
                                     callback_data=DictionaryCallbackData(action=DictionaryActions.phrases).pack()))
    return builder.as_markup()


def dictionary_test_filter_ikb():

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Самые малоизученные☁️",
                                     callback_data=DictionaryCallbackData(action=TestFilterActions.unexplored).pack()))
    builder.row(InlineKeyboardButton(text="Недавно добавленные🕞",
                                     callback_data=DictionaryCallbackData(action=TestFilterActions.newest).pack()))
    builder.row(InlineKeyboardButton(text="Случайные🎲",
                                     callback_data=DictionaryCallbackData(action=TestFilterActions.random).pack()))

    return builder.as_markup(resize_keyboard=True)


def test_ikb(total_count: int, correct_count: int = 0, incorrect_count: int = 0):

    builder = InlineKeyboardBuilder()

    if (correct_count + incorrect_count) == 0:
        return None

    builder.add(InlineKeyboardButton(text=f"{correct_count}🟢", callback_data=PLUG),
                InlineKeyboardButton(text=f"{correct_count+incorrect_count}/{total_count}", callback_data=PLUG),
                InlineKeyboardButton(text=f"{incorrect_count}🔴", callback_data=PLUG))

    return builder.as_markup(resize_keyboard=True)
