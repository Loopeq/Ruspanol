import random

from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from data.queries.dictionary import select_user_dictionary
from domain.keyboards.dictionary_ikb import DictionaryActions, DictionaryCallbackData

router = Router()


class DictionaryState(StatesGroup):
    test_process = State()


@router.callback_query(DictionaryCallbackData.filter(F.action.in_({DictionaryActions.test})))
async def start_test(callback: CallbackQuery):
    user_dict = await select_user_dictionary(tg_id=str(callback.from_user.id))
    random.shuffle(user_dict)

    current_phrase = user_dict.pop() if len(user_dict) != 1 else user_dict[0]

    await callback.message.edit_text(text=f"Переведите с русском на испанский: \n"
                                          f"{current_phrase.ru}")

    await callback.answer()

