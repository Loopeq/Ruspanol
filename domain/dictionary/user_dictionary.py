from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from data.queries.dictionary import select_user_dictionary
from domain.dictionary.dictionary_ikb import DictionaryActions, DictionaryCallbackData, \
    dictionary_test_filter_ikb
from resources.strings import Strings

router = Router()


class DictionaryState(StatesGroup):
    test_process = State()


@router.callback_query(DictionaryCallbackData.filter(F.action.in_({DictionaryActions.test})))
async def show_test_filters(callback: CallbackQuery):
    await callback.message.answer(text=Strings.welcome_cmd_test_filter,
                                  reply_markup=dictionary_test_filter_ikb())
    await callback.answer()


@router.callback_query(DictionaryCallbackData.filter(F.action.in_({DictionaryActions.phrases})))
async def show_phrases(callback: CallbackQuery):
    phrases = await select_user_dictionary(tg_id=str(callback.from_user.id))
    phrase_wrapped = "\n".join([f"{index + 1}. {phrase.es} - {phrase.ru}" for index, phrase in enumerate(phrases)])
    await callback.message.answer(text=phrase_wrapped)
    await callback.answer()
