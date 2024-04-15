import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from domain.commands import cmd_router
from domain.pagination import Pagination
from domain.sections import sections_router, SectionsCallback, SectionsCallbackActions
from domain.utils.settings import settings

logging.basicConfig(level=logging.INFO)
default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
bot = Bot(token=settings.bot_token, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def start():

    # dp.callback_query.register(get_plug_callback, lambda callback: callback.data.startswith("0"))
    #
    # dp.callback_query.register(cmd_words, lambda callback: callback.data.startswith("section"))
    # dp.callback_query.register(cmd_voice, VoiceCD.filter())
    # dp.callback_query.register(cmd_delete_voice, lambda callback: callback.data.startswith("delete_voice"))
    # dp.callback_query.register(cmd_return_to_sections, lambda callback: callback.data.startswith("return_to_sections"),
    #                            )
    # dp.callback_query.register(cmd_start_quiz, QuizCallbackData.filter())
    # dp.callback_query.register(cmd_return_to_words, lambda callback: callback.data.startswith("return_to_words"))

    # dp.message.register(cmd_add_answer, StateFilter(FSMQuiz.add_answer))
    # dp.callback_query.register(cmd_words_pag, WordsPag.filter())
    # dp.callback_query.register(add_user_section_title, lambda callback: callback.data.startswith("add_user_section"))
    # dp.message.register(add_user_section_words, StateFilter(UserSectionState.add_title))
    # dp.callback_query.register(cancel_add_us, lambda callback: callback.data.startswith("cancel_add_user_section"))
    # dp.message.register(add_user_section_finish, StateFilter(UserSectionState.add_words))
    # dp.callback_query.register(get_user_section_words, UserSectionsCD.filter(F.action == "show_us_words"))
    # dp.callback_query.register(remove_user_section, UserSectionsCD.filter(F.action == "remove_user_section"))
    # dp.callback_query.register(edit_user_section, UserSectionsCD.filter(F.action == "start_edit"))
    # dp.callback_query.register(cmd_back_to_user_sections, UserSectionsCD.filter(F.action == "back_to_user_sections"))
    # dp.callback_query.register(cmd_start_user_section_quiz,
    #                            UserSectionQuizCD.filter(F.action == "start_user_section_quiz"))
    # dp.callback_query.register(cancel_user_section_quiz,
    #                            lambda callback: callback.data.startswith("finish_user_section_quiz"))
    # dp.message.register(cmd_add_answer_us, StateFilter(UserSectionQuizState.add_answer))
    # dp.callback_query.register(finish_edit_user_section, EditUserSectionCD.filter(F.action == "cancel_edit_us"))
    # dp.callback_query.register(edit_add_words_info, EditUserSectionCD.filter(F.action == "add_words"))
    # dp.callback_query.register(cmd_back_to_edit, EditUserSectionCD.filter(F.action == "back_to_edit"))
    # dp.message.register(edit_add_words, StateFilter(UserSectionEdit.edit_add_words))
    # dp.callback_query.register(show_words_to_delete, EditUserSectionCD.filter(F.action == "show_delete_word"))
    # dp.callback_query.register(delete_words, EditUserSectionCD.filter(F.action == "delete_word"))
    dp.include_routers(cmd_router, sections_router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
