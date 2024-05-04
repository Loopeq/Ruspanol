from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries.user import insert_user
from domain.free_speech import FreeSpeechStates
from domain.shemas.user_model_dto import UserAddDto
from domain.translation_and_speak import TranslationAndSpeakStates
from resources.strings import Strings


router = Router()


class BotCommands(Enum):
    dialogue = "dialogue"
    translate_and_speak = "translate_and_speak"


@router.message(Command(BotCommands.dialogue.value))
async def cmd_dialogue(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.start_conversation_info)
    #delete_history(user_id=message.from_user.id)
    await state.set_state(FreeSpeechStates.dialogue)


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
    await insert_user(user=UserAddDto(tg_id=str(message.from_user.id)))


