from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from data.queries.phrases import select_current_phrase, update_current_phrase, select_phrase_by_id
from domain.keyboards.phrases_ikb import PhrasesCallbackData, PhrasesActions, phrases_ikb
from domain.settings import settings
from domain.shemas.schemas_dto import UserPhrasesProgressAddDto
from resources.strings import Strings
from speech_api.speech_to_text import get_text_from_voice

router = Router()


class PhrasesState(StatesGroup):
    phrase_process = State()

async def _phrase_error_message_adm(bot: Bot, user_id: int):
    await bot.send_message(chat_id=settings.admin_id, text=f"Phrases is done for user: {user_id}")


@router.callback_query(StateFilter(PhrasesState.phrase_process),
                       PhrasesCallbackData.filter(F.action.in_({PhrasesActions.add,
                                                                PhrasesActions.next,
                                                                PhrasesActions.voice})))
async def phrases_process(callback: CallbackQuery, callback_data: PhrasesCallbackData, state: FSMContext, bot: Bot):

    data = await state.get_data()
    current_phrase_id = data["current_phrase_id"]
    current_phrase = await select_phrase_by_id(phrase_id=current_phrase_id + 1)

    if current_phrase is None:
        await _phrase_error_message_adm(bot=bot, user_id=callback.from_user.id)
        await callback.message.edit_text(text=Strings.phrase_error_message)
        return

    if callback_data.action == PhrasesActions.voice:
        return

    if callback_data.action == PhrasesActions.add:
         pass

    await callback.message.edit_text(f"{current_phrase.es} - {current_phrase.ru}", reply_markup=phrases_ikb())
    await state.update_data(current_phrase_id=current_phrase_id + 1)
    await update_current_phrase(UserPhrasesProgressAddDto(tg_id=str(callback.from_user.id),
                                                          phrase_id=current_phrase_id + 1))

    await callback.answer()
