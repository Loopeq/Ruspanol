from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from resources.strings import Strings
from speech_api.text_to_speech import get_voice_eden
from text_generation.dialogue_model import run_provider

M_LIMIT = 25

router = Router()


class FreeSpeechStates(StatesGroup):
    dialogue = State()


def is_correct_length(message: str):
    return len(message.split()) <= M_LIMIT


@router.message(StateFilter(FreeSpeechStates),  F.content_type.in_({'text', 'voice'}))
async def dialogue_process(message: Message, bot: Bot):
    if not is_correct_length(message.text):
        await message.answer(text=f"{Strings.message_length_info(limit=M_LIMIT)}")
        return

    message_load = await message.answer(text=Strings.wait_answer_info)
    response_answer = await run_provider(message=message.text, user_id=message.from_user.id)
    voice = await get_voice_eden(message=response_answer, user_id=message.from_user.id)
    voice_input = FSInputFile(voice)
    await message_load.edit_text(text=response_answer)
    await bot.send_voice(chat_id=message.from_user.id, voice=voice_input)


