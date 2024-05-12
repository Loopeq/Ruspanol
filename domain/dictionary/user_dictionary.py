import random
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message
from data.queries.dictionary import select_user_dictionary
from domain.dictionary.common import TestData, _get_current_phrase
from domain.keyboards.dictionary_ikb import DictionaryActions, DictionaryCallbackData, test_ikb
from resources.strings import Strings

router = Router()


class DictionaryState(StatesGroup):
    test_process = State()


@router.callback_query(DictionaryCallbackData.filter(F.action.in_({DictionaryActions.test})))
async def start_test(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    tmp_data: TestData = data.get("test_data")

    if tmp_data:
        message_id: Message = tmp_data.message_id
        if message_id:
            await bot.delete_message(message_id=message_id, chat_id=callback.from_user.id)

    await state.clear()

    user_dict = await select_user_dictionary(tg_id=str(callback.from_user.id))
    random.shuffle(user_dict)
    total_count = len(user_dict)
    current_phrase = _get_current_phrase(phrases=user_dict)

    test_data = TestData(user_dict=user_dict,
                         total_count=total_count,
                         prev_phrase=current_phrase,
                         correct_count=0,
                         incorrect_count=0)

    message = await callback.message.answer(text=Strings.test_info(
        current_task_phrase=current_phrase.ru),
        reply_markup=test_ikb(
            total_count=total_count))
    test_data.message_id = message.message_id

    await state.set_state(DictionaryState.test_process)
    await state.update_data(test_data=test_data)
    await callback.answer()


