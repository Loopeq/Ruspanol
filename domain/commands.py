from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries.user import insert_user
from data.queries.user_history import delete_history
from domain.assistant import AssistantStates
from domain.shemas.schemas_dto import UserAddDto
from resources.strings import Strings


router = Router()


class BotCommands(Enum):
    assistance = "assistance"
    translate_and_speak = "translate_and_speak"


@router.message(Command(BotCommands.assistance.value))
async def cmd_dialogue(message: Message, state: FSMContext):
    await state.clear()
    await delete_history(tg_id=message.from_user.id)
    await message.answer(Strings.assistance_info)
    await state.set_state(AssistantStates.support_process)


@router.message(Command(BotCommands.translate_and_speak.value))
async def cmd_translate_and_speak(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.start_stt_info)
    #phrases = get_phrases()
    #await message.answer(phrases[0]["es"])
    #await state.set_state(TranslationAndSpeakStates.tas)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(Strings.entry_info)
    await insert_user(user=UserAddDto(tg_id=message.from_user.id))



