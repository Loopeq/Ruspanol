from enum import StrEnum
from aiogram.filters.callback_data import CallbackData


class AdminMenuCallbackData(CallbackData, prefix="admin_menu"):
    action: str


class BasicAdminActions(StrEnum):
    add_phrase = "add_phrase"
    cancel_add_phrase = "cancel_add_phrase"


class CheckActions(StrEnum):
    check_yes = "check_yes"
    check_no = "check_no"


