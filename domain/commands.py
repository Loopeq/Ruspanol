from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries.phrases import get_phrases
from data.queries.user import insert_user
from data.queries.user_history import delete_history
from domain.assistant import AssistantStates
from domain.phrases import PhrasesState
from domain.shemas.schemas_dto import UserAddDto
from resources.strings import Strings


router = Router()


class BotCommands(Enum):
    assistance = "assistance"
    phrases = "phrases"


@router.message(Command(BotCommands.assistance.value))
async def cmd_dialogue(message: Message, state: FSMContext):
    await state.clear()
    await delete_history(tg_id=message.from_user.id)
    await message.answer(Strings.assistance_info)
    await state.set_state(AssistantStates.support_process)


@router.message(Command(BotCommands.phrases.value))
async def cmd_phrases(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.start_stt_info)
    phrases = await get_phrases()
    await message.answer(text=f"{phrases[0].es}\n{phrases[0].ru}")
    await state.set_state(PhrasesState.process)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.entry_info)
    await insert_user(user=UserAddDto(tg_id=message.from_user.id))



