from enum import Enum
from typing import Type

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton

from domain.utils.common import PLUG


class PaginationActions(Enum):
    next = "next"
    prev = "prev"


class PaginationCallbackData(CallbackData, prefix="pag"):
    action: PaginationActions

class Pagination:


    def __init__(self, callback_data: Type[CallbackData],
                 limit: int, data: list = None):
        self.data = data
        self.limit = limit
        self.callback_data = callback_data
        self.length = len(self.data) if self.data else 0


    def get_buttons(self, page: int):
        if not self.data:
            raise ValueError("Data is empty. Try set_data() function first.")
        buttons = [ InlineKeyboardButton(text='<=', callback_data=self.callback_data(
            action=PaginationActions.prev, page=page, length=self.length).pack()),
        InlineKeyboardButton(text=f"{page + 1}/{self.length + 1}", callback_data=PLUG),
        InlineKeyboardButton(text='=>', callback_data=self.callback_data(
            action=PaginationActions.next, page=page, length=self.length).pack())]

        return buttons

    def set_data(self, data: list):
        if not data:
            raise TypeError("Data mustn't be None or empty")
        self.data = data
        self.length = len(self.data)

