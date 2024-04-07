from aiogram import Bot
from aiogram.types import CallbackQuery

from data.database import get_user_section_by_id
from domain.user_section.callback_data import UserSectionsCD
from domain.user_section.keyboards import inline_edit_user_section
from resources.strings import Strings


async def edit_user_section(callback: CallbackQuery, callback_data: UserSectionsCD, bot: Bot):
    user_section = get_user_section_by_id(str(callback_data.u_section_id))[0]
    await bot.send_message(chat_id=callback.from_user.id, text=Strings.edit_user_section_info(user_section["section_title"]),
                           reply_markup=inline_edit_user_section(user_section["id"]))
    await callback.answer()

async def finish_edit_user_section(callback: CallbackQuery, callback_data: UserSectionsCD):

    await callback.message.delete()


