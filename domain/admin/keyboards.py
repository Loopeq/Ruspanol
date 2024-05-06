from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from domain.admin.callback_models import CheckActions, AdminMenuCallbackData, BasicAdminActions


def admin_menu_ikb():
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="Add phrase",
                                     callback_data=AdminMenuCallbackData(action=BasicAdminActions.add_phrase).pack()))
    return builder.as_markup()


def admin_check_ikb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Yes",
                             callback_data=AdminMenuCallbackData(action=CheckActions.check_yes).pack()),
        InlineKeyboardButton(text="No",
                             callback_data=AdminMenuCallbackData(action=CheckActions.check_no).pack()))
    builder.row(
        InlineKeyboardButton(text="Cancel",
                             callback_data=AdminMenuCallbackData(action=BasicAdminActions.cancel_add_phrase).pack())
    )
    builder.adjust(2, 1)
    return builder.as_markup()
