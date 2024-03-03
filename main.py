import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram.utils.markdown import text

from database import get_subsections, get_sections, get_words, get_subsection
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from keyboards import inline_section_kb, inline_subsection_kb, inline_return_to_section_kb, \
    inline_return_to_subsection_kb, inline_words_kb
from common import clip_id
from strings import Strings

logging.basicConfig(level=logging.INFO)
default = DefaultBotProperties(allow_sending_without_reply=True, parse_mode="HTML")
bot = Bot(token="7026242085:AAE1GU-GY4oBdy6gL0qL6t2p6o8jV47L6vo", default=default)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(Strings.hello_words)

@dp.message(Command("sections"))
async def cmd_sections(message: types.Message):
    await message.answer(Strings.available_sections, reply_markup=inline_section_kb(get_sections()))

@dp.callback_query(F.data == "return_to_sections")
async def cmd_back_to_sections(callback: types.CallbackQuery):
    await callback.answer()
    message_text = text(f"<b>{Strings.available_sections}</b>")
    await callback.message.edit_text(message_text, reply_markup=inline_section_kb(get_sections()))


@dp.callback_query(lambda text: text.data.startswith("section"))
async def cmd_subsections(callback: types.CallbackQuery):
    await callback.answer()
    section_id = clip_id(callback.data, "section")
    subsection = get_subsections(section_id)
    if not subsection:
        await callback.message.edit_text(text=Strings.oops_message, reply_markup=inline_return_to_section_kb())
    else:
        section_id = subsection[0]["section_id"]
        section_title = get_sections()[section_id-1]["title"]
        await callback.message.edit_text(text=section_title, reply_markup=inline_subsection_kb(subsection))
    await callback.answer()


@dp.callback_query(lambda text: text.data.startswith("subsection"))
async def cmd_subsections(callback: types.CallbackQuery):
    subsection_id = clip_id(callback.data, "subsection")
    subsection = get_subsection(subsection_id)[0]
    words = get_words(subsection_id)
    if not words:
        await callback.message.edit_text(text=Strings.oops_message,
                                         reply_markup=inline_return_to_subsection_kb(subsection["section_id"]))
    else:
        await callback.message.edit_text(text=subsection['title'], reply_markup=inline_words_kb(section_id=subsection["section_id"], words=words))

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())