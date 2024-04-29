from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries import insert_user, delete_history
from domain.free_speech import FreeSpeechStates
from resources.strings import Strings


cmd_router = Router()


class BotCommands(Enum):
    dialogue = "dialogue"


@cmd_router.message(Command(BotCommands.dialogue.value))
async def cmd_dialogue(message: Message, state: FSMContext):
    await message.answer("Начните беседу.")
    delete_history(user_id=message.from_user.id)
    await state.set_state(FreeSpeechStates.dialogue)


@cmd_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(Strings.entry_info)
    try:
        insert_user(message.from_user.id)
    except Exception as error:
        print(error)
        return
