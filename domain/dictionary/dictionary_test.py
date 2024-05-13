from aiogram import F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from data.queries.dictionary import update_score, select_user_dictionary
from domain.dictionary.common import TestData, _check_word_equal, _get_current_phrase
from domain.keyboards.dictionary_ikb import test_ikb, DictionaryCallbackData, TestFilterActions
from resources.strings import Strings
from domain.dictionary.user_dictionary import DictionaryState

router = Router()


@router.callback_query(
    DictionaryCallbackData.filter(F.action.in_({TestFilterActions.newest, TestFilterActions.unexplored,
                                                TestFilterActions.random})))
async def start_test(callback: CallbackQuery, state: FSMContext, callback_data: DictionaryCallbackData, bot: Bot):
    # data = await state.get_data()
    # tmp_data: TestData = data.get("test_data")
    #
    # if tmp_data:
    #     message_id: Message = tmp_data.message_id
    #     if message_id:
    #         await bot.delete_message(message_id=message_id, chat_id=callback.from_user.id)
    #
    # await state.clear()
    match callback_data.action:
        case TestFilterActions.newest:
            user_dict = await select_user_dictionary(tg_id=str(callback.from_user.id),
                                                     o_filter=TestFilterActions.newest)
        case TestFilterActions.random:
            user_dict = await select_user_dictionary(tg_id=str(callback.from_user.id),
                                                     o_filter=TestFilterActions.random)
        case TestFilterActions.unexplored:
            user_dict = await select_user_dictionary(tg_id=str(callback.from_user.id),
                                                     o_filter=TestFilterActions.unexplored)
        case _:
            user_dict = []

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


@router.message(StateFilter(DictionaryState.test_process, F.data.in_({"text"})))
async def test_process(message: Message, state: FSMContext):
    data = await state.get_data()
    test_data: TestData = data["test_data"]

    is_correct = _check_word_equal(user_answer=message.text, correct_answer=test_data.prev_phrase.es)

    current_phrase = _get_current_phrase(phrases=test_data.user_dict)

    if is_correct:
        test_data.correct_count += 1
        await update_score(tg_id=str(message.from_user.id), phrase_id=test_data.prev_phrase.id)
    else:
        test_data.incorrect_count += 1

    await message.answer(text=Strings.test_info(user_phrase=message.text,
                                                correct_phrase=test_data.prev_phrase.es,
                                                prev_task_phrase=test_data.prev_phrase.ru,
                                                current_task_phrase=current_phrase.ru
                                                if current_phrase is not None else None,
                                                is_correct=is_correct),
                         reply_markup=test_ikb(total_count=test_data.total_count,
                                               correct_count=test_data.correct_count,
                                               incorrect_count=test_data.incorrect_count))

    if current_phrase is None:
        await state.clear()

    else:
        test_data.prev_phrase = current_phrase
        await state.update_data(test_data=test_data)
