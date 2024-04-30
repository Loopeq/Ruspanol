from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries import insert_user, delete_history
from domain.free_speech import FreeSpeechStates
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
    delete_history(user_id=message.from_user.id)
    await state.set_state(FreeSpeechStates.dialogue)


@router.message(Command(BotCommands.translate_and_speak.value))
async def cmd_translate_and_speak(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Как дела?")
    await state.set_state(TranslationAndSpeakStates.tas)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(Strings.entry_info)
    try:
        insert_user(message.from_user.id)
    except Exception as error:
        print(error)
        return
