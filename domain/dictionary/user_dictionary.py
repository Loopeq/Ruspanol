from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from domain.keyboards.dictionary_ikb import DictionaryActions, DictionaryCallbackData, \
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


