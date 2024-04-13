from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from data.queries import get_words, insert_user_progression
from domain.filters.filters import QuizCallbackData
from domain.keyboards.keyboards import inline_quiz_info
from domain.utils.common import replace_syg
from resources.strings import Strings
import random

class FSMQuiz(StatesGroup):
    add_answer = State()



async def cmd_start_quiz(callback: CallbackQuery, callback_data: QuizCallbackData, state: FSMContext):
    section_id = callback_data.section_id
    words = get_words(section_id)
    random.shuffle(words)
    await state.update_data(words=words, message_id = callback.message.message_id, current_step=1, false_count=0, true_count=0)
    await callback.message.edit_text(text=Strings.quiz_info + str(words[0]["russian"]),
                                     reply_markup=inline_quiz_info(section_id, total_count=len(words), false_count=0, true_count=0))
    await state.set_state(FSMQuiz.add_answer)
    await callback.answer()

async def cmd_add_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    words = data.get("words")
    message_id = data.get("message_id")
    section_id = words[0]["section_id"]
    current_step = data.get("current_step")
    true_count = data.get("true_count")
    false_count = data.get("false_count")

    if message.text.lower() == replace_syg(words[current_step-1]["espanol"]):
        await state.update_data(true_count=true_count+1)
        true_count += 1
    else:
        await state.update_data(false_count=false_count+1)
        false_count += 1

    r_markup = inline_quiz_info(section_id=section_id,
                                                              total_count=len(words), false_count=false_count, true_count=true_count,
                                                              current_answer=words[current_step-1]["espanol"], user_answer=message.text.lower()
                                                              )
    if current_step == len(words):

        await bot.edit_message_text(text=Strings.quiz_final, chat_id=message.from_user.id,
                                    message_id=message_id,
                                    reply_markup=r_markup)
        if true_count == len(words):
            insert_user_progression(user_id=str(message.from_user.id), section_id=str(section_id))
        await state.clear()
    else:
        await bot.edit_message_text(text=Strings.quiz_info + str(words[current_step]["russian"]),
                                    chat_id=message.from_user.id,
                                    message_id=message_id,
                                    reply_markup=r_markup)


        await state.set_state(FSMQuiz.add_answer)
        await state.update_data(current_step=current_step+1)
    await message.delete()





