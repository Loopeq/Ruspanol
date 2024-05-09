from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from resources.strings import Strings
from text_generation.text_gen_model import run_provider, generate_for_assistant

M_LIMIT = 128

router = Router()


class AssistantStates(StatesGroup):
    support_process = State()


def valid_message_length(message: str, limit: int):
    return len(message) <= limit


@router.message(StateFilter(AssistantStates), F.content_type.in_({'text'}))
async def assistant_response(message: Message, bot: Bot):

    if not valid_message_length(message.text, limit=M_LIMIT):
        await message.answer(text=Strings.message_length_info(limit=M_LIMIT))
        return

    message_load = await message.answer(text=Strings.wait_answer_info)
    response_answer = await generate_for_assistant(message=message.text, tg_id=message.from_user.id, bot=bot)

    if response_answer["status"] == 200:
        await message_load.edit_text(text=response_answer["message"])
    elif response_answer["status"] == 500:
        await message_load.edit_text(text="У нас что-то пошло нет. Попробуйте еще раз.")


