
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.dictionary.common import TestData, _check_word_equal, _get_current_phrase
from domain.keyboards.dictionary_ikb import test_ikb
from resources.strings import Strings
from domain.dictionary.user_dictionary import DictionaryState


router = Router()


@router.message(StateFilter(DictionaryState.test_process, F.data.in_({"text"})))
async def test_process(message: Message, state: FSMContext):
    data = await state.get_data()
    test_data: TestData = data["test_data"]

    is_correct = _check_word_equal(user_answer=message.text, correct_answer=test_data.prev_phrase.es)

    current_phrase = _get_current_phrase(phrases=test_data.user_dict)

    if is_correct:
        test_data.correct_count += 1
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
