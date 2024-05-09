from enum import Enum

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from data.queries.dictionary import select_user_dictionary
from data.queries.phrases import select_current_phrase
from data.queries.user import insert_user
from data.queries.user_history import delete_history
from domain.assistant import AssistantStates
from domain.keyboards.dictionary_ikb import dictionary_ikb
from domain.keyboards.phrases_ikb import phrases_ikb
from domain.phrases import PhrasesState
from domain.shemas.schemas_dto import UserAddDto
from resources.strings import Strings


router = Router()


class BotCommands(Enum):
    assistance = "assistance"
    phrases = "phrases"
    dictionary = "vocab"


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.welcome_cmd_start)
    await insert_user(user=UserAddDto(tg_id=message.from_user.id))


@router.message(Command(BotCommands.assistance.value))
async def cmd_dialogue(message: Message, state: FSMContext):
    await state.clear()
    await delete_history(tg_id=message.from_user.id)
    await message.answer(Strings.welcome_cmd_assistance)
    await state.set_state(AssistantStates.support_process)


@router.message(Command(BotCommands.phrases.value))
async def cmd_phrases(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(Strings.welcome_cmd_phrases)

    current_phrase = await select_current_phrase(tg_id=str(message.from_user.id))

    await message.answer(f"{current_phrase.es} - {current_phrase.ru}", reply_markup=phrases_ikb())

    await state.set_state(PhrasesState.phrase_process)
    await state.update_data(current_phrase_id=current_phrase.id)


@router.message(Command(BotCommands.dictionary.value))
async def cmd_dictionary(message: Message, state: FSMContext):
    await state.clear()
    phrases_from_dict = await select_user_dictionary(tg_id=str(message.from_user.id))

    if not phrases_from_dict:
        await message.answer(text=Strings.dictionary_error_message)
        return

    phrases_input = "\n".join([f"{phrase.es} - {phrase.ru}" for phrase in phrases_from_dict])
    await message.answer(phrases_input, reply_markup=dictionary_ikb())

