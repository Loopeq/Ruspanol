from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from resources.strings import Strings
from text_generation.dialogue_model import run_provider

M_LIMIT = 128

router = Router()


class AssistantStates(StatesGroup):
    support_process = State()


def valid_message_length(message: str, limit: int):
    return len(message) <= limit


@router.message(StateFilter(AssistantStates), F.content_type.in_({'text'}))
async def assistant_process(message: Message):
    if not valid_message_length(message.text, limit=M_LIMIT):
        await message.answer(text=Strings.message_length_info(limit=M_LIMIT))
        return
    message_load = await message.answer(text=Strings.wait_answer_info)
    response_answer = await run_provider(message=message.text, tg_id=message.from_user.id)
    await message_load.edit_text(text=response_answer)



