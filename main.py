import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from magic_filter import F

from domain.basic.basic import cmd_start, cmd_sections, cmd_profile
from aiogram import Bot, Dispatcher

from domain.basic.quiz import cmd_start_quiz
from domain.basic.words_voice import cmd_voice, cmd_delete_voice, cmd_words, cmd_return_to_sections, cmd_return_to_words
from domain.filters.filters import QuizCallbackData
from domain.utils.settings import settings

async def on_start(bot: Bot):
    await bot.send_message(text="Бот запущен.", chat_id=settings.admin_id)

async def on_stop(bot: Bot):
    await bot.send_message(text="Бот остановлен.", chat_id=settings.admin_id)



async def start():
    logging.basicConfig(level=logging.INFO)
    default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
    bot = Bot(token=settings.bot_token, default=default)

    dp = Dispatcher()
    dp.startup.register(on_start)
    dp.shutdown.register(on_stop)

    dp.message.register(cmd_start, Command(commands=['start']))
    dp.message.register(cmd_sections, Command(commands=['sections']))
    dp.message.register(cmd_profile, Command(commands=['profile']))
    dp.callback_query.register(cmd_words, lambda callback: callback.data.startswith("section"))
    dp.callback_query.register(cmd_voice, lambda callback: callback.data.startswith("word"))
    dp.callback_query.register(cmd_delete_voice, lambda callback: callback.data.startswith("delete_voice"))
    dp.callback_query.register(cmd_return_to_sections, lambda callback: callback.data.startswith("return_to_sections"))
    dp.callback_query.register(cmd_start_quiz, QuizCallbackData.filter())
    dp.callback_query.register(cmd_return_to_words, lambda callback: callback.data.startswith("return_to_words"))


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())