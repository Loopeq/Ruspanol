from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from resources.strings import Strings
from speech_api.text_to_speech import get_voice_eden
from text_generation.dialogue_model import run_provider

M_LIMIT = 25

router = Router()


class AssistantStates(StatesGroup):
    support_process = State()


@router.message(StateFilter(AssistantStates), F.content_type.in_({'text'}))
async def assistant_process(message: Message):
    message_load = await message.answer(text=Strings.wait_answer_info)
    response_answer = await run_provider(message=message.text, tg_id=message.from_user.id)
    await message_load.edit_text(text=response_answer)



