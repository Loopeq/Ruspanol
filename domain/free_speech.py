from aiogram import Router, Bot
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from text_generation.dialogue_model import run_provider

fs_router = Router()


class FreeSpeechStates(StatesGroup):
    dialogue = State()


@fs_router.message(StateFilter(FreeSpeechStates))
async def dialogue_process(message: Message, bot: Bot):
    response = await run_provider(message=message.text, user_id=str(message.from_user.id))
    await message.answer(text=response)

