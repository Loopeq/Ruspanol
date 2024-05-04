import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from data.queries.user import create_table, select_users
from domain.commands import router as cmd_router, BotCommands
from domain.admin.commands import router as admin_router
from domain.free_speech import router as fs_router
from domain.translation_and_speak import router as tas_router
from domain.settings import settings


from resources.strings import Strings

logging.basicConfig(level=logging.INFO)
default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
bot = Bot(token=settings.bot_token, default=default)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def on_startup():
    await create_table()
    commands = [BotCommand(command=str(BotCommands.dialogue.value), description=Strings.cmd_dialogue_info),
                BotCommand(command=str(BotCommands.translate_and_speak.value), description=Strings.cmd_stt_info)]
    await bot.set_my_commands(commands=commands)


async def start():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    dp.include_routers(cmd_router, fs_router, tas_router)
    dp.include_router(admin_router)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
