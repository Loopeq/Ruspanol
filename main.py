import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from domain.commands import cmd_router, BotCommands
from domain.free_speech import fs_router
from domain.settings import settings


logging.basicConfig(level=logging.INFO)
default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
bot = Bot(token=settings.bot_token, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_startup():
    commands = [ BotCommand(command=BotCommands.dialogue.value, description='Свободный разговор с ИИ💬') ]
    await bot.set_my_commands(commands=commands)


async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp.include_routers(cmd_router, fs_router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
