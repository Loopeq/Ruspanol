from aiogram.types import CallbackQuery


async def get_plug_callback(callback: CallbackQuery):
    await callback.answer()
