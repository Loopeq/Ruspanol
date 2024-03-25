import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from magic_filter import F

from domain.basic.basic import cmd_start, cmd_sections, cmd_profile, cmd_change_page, SPagCallbackData, SPagState
from aiogram import Bot, Dispatcher

from domain.basic.quiz import cmd_start_quiz, FSMQuiz, cmd_add_answer
from domain.basic.words import cmd_words, cmd_words_pag, WordsPag
from domain.basic.words_voice import cmd_voice, cmd_delete_voice, cmd_return_to_sections, cmd_return_to_words
from domain.filters.filters import QuizCallbackData
from domain.utils.settings import settings

async def on_start(bot: Bot):
    await bot.send_message(text="Бот запущен.", chat_id=settings.admin_id)

async def on_stop(bot: Bot):
    await bot.send_message(text="Бот остановлен.", chat_id=settings.admin_id)

logging.basicConfig(level=logging.INFO)
default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
bot = Bot(token=settings.bot_token, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def start():
    dp.startup.register(on_start)
    dp.shutdown.register(on_stop)

    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(cmd_sections, Command(commands=['sections']))
    dp.message.register(cmd_profile, Command(commands=['profile']), StateFilter(default_state))
    dp.callback_query.register(cmd_words, lambda callback: callback.data.startswith("section"))
    dp.callback_query.register(cmd_voice, lambda callback: callback.data.startswith("word"))
    dp.callback_query.register(cmd_delete_voice, lambda callback: callback.data.startswith("delete_voice"))
    dp.callback_query.register(cmd_return_to_sections, lambda callback: callback.data.startswith("return_to_sections"),
                               )
    dp.callback_query.register(cmd_start_quiz, QuizCallbackData.filter())

    dp.callback_query.register(cmd_return_to_words, lambda callback: callback.data.startswith("return_to_words"))
    dp.callback_query.register(cmd_change_page, SPagCallbackData.filter())
    dp.message.register(cmd_add_answer, StateFilter(FSMQuiz.add_answer))
    dp.callback_query.register(cmd_words_pag, WordsPag.filter())

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())