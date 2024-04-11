from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from data.database import get_us_words
from domain.user_section.callback_data import UserSectionQuizCD
from domain.user_section.fsm_states import UserSectionQuizState
from domain.user_section.us_keyboards.keyboards import inline_user_section_quiz_kb, inline_user_sections_kb
from domain.utils.common import replace_syg

from resources.strings import Strings
import random


async def cmd_start_user_section_quiz(callback: CallbackQuery, callback_data: UserSectionQuizCD, state: FSMContext):
    us_id = callback_data.us_id
    words = get_us_words(us_id=us_id)
    word = random.choice(words)
    await callback.message.edit_text(text=Strings.user_quiz_info, inline_message_id=callback.inline_message_id,
                                     reply_markup=inline_user_section_quiz_kb(
                                         correct=0, incorrect=0, total=0, word=word["russian"],
                                         ))
    await state.set_state(UserSectionQuizState.add_answer)
    await state.update_data(answer=word["espanol"], words=words, message_id=callback.message.message_id,
                            total=0, correct=0, incorrect=0)
    await callback.answer()


async def cmd_add_answer_us(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    mod_user_answer = replace_syg(message.text)
    mod_correct_answer = replace_syg(data["answer"])
    message_id = data["message_id"]
    total, correct, incorrect = data["total"], data["correct"], data["incorrect"]
    is_correct = mod_correct_answer == mod_user_answer
    if is_correct:
        correct +=1
    else:
        incorrect+=1

    total+=1
    next_word = random.choice(data["words"])
    await state.update_data(total=total, correct=correct, incorrect=incorrect, answer=next_word["espanol"])

    await bot.edit_message_text(text=Strings.user_quiz_info, chat_id=message.from_user.id, message_id=message_id,
                                reply_markup=inline_user_section_quiz_kb(
                                    correct=correct, incorrect=incorrect, total=total, word=next_word["russian"],
                                    correct_answer=data["answer"], user_answer=message.text, is_correct=is_correct
                                ))
    await message.delete()


async def cancel_user_section_quiz(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(Strings.available_user_sections, reply_markup=inline_user_sections_kb(callback.from_user.id))
    await state.clear()
    await callback.answer()


