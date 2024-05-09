from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, FSInputFile

from data.queries.dictionary import insert_phrase_into_dictionary
from data.queries.phrases import select_phrase_by_id
from domain.keyboards.phrases_ikb import PhrasesCallbackData, PhrasesActions, phrases_ikb, remove_voice_ikb
from domain.settings import settings
from domain.shemas.schemas_dto import DictionaryAddDto
from resources.strings import Strings
from speech_api.text_to_speech import get_audio_rss

router = Router()


class PhrasesState(StatesGroup):
    phrase_process = State()


async def _phrase_error_message_adm(bot: Bot, user_id: int):
    await bot.send_message(chat_id=settings.admin_id, text=f"Phrases is done for user: {user_id}")


async def _phrase_is_none(current_phrase: str | None, bot: Bot, user_id: int):
    if current_phrase is None:
        await _phrase_error_message_adm(bot=bot, user_id=user_id)
        return True
    return False


@router.callback_query(StateFilter(PhrasesState.phrase_process),
                       PhrasesCallbackData.filter(F.action.in_({PhrasesActions.add,
                                                                PhrasesActions.next,
                                                                PhrasesActions.voice})))
async def phrases_process(callback: CallbackQuery, callback_data: PhrasesCallbackData, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_phrase_id = data["current_phrase_id"]

    if callback_data.action == PhrasesActions.voice:
        current_phrase = await select_phrase_by_id(phrase_id=current_phrase_id)
        voice_path = await get_audio_rss(message=current_phrase.es, phrase_id=current_phrase.id)
        audio_input = FSInputFile(voice_path)
        await bot.send_voice(chat_id=callback.from_user.id, voice=audio_input,
                             caption=current_phrase.es, reply_markup=remove_voice_ikb())
        await callback.answer()
        return

    if callback_data.action == PhrasesActions.next:
        current_phrase = await select_phrase_by_id(phrase_id=current_phrase_id + 1)
        if await _phrase_is_none(current_phrase, bot=bot, user_id=callback.from_user.id):
            await callback.message.edit_text(text=Strings.phrase_error_message)
            await callback.answer()
            return

        await callback.message.edit_text(f"{current_phrase.es} - {current_phrase.ru}", reply_markup=phrases_ikb())
        await state.update_data(current_phrase_id=current_phrase_id + 1)
        await callback.answer()
        return

    if callback_data.action == PhrasesActions.add:
        current_phrase = await select_phrase_by_id(phrase_id=current_phrase_id)

        if await _phrase_is_none(current_phrase, bot=bot, user_id=callback.from_user.id):
            await callback.message.edit_text(text=Strings.phrase_error_message)
            await callback.answer()
            return
        await insert_phrase_into_dictionary(phrase=DictionaryAddDto(tg_id=str(callback.from_user.id),
                                                                    phrase_id=current_phrase.id))

        await callback.answer(text="Фраза добавлена в словарь✅", show_alert=False)
        return


@router.callback_query(StateFilter(PhrasesState.phrase_process),
                       PhrasesCallbackData.filter(F.action.in_({PhrasesActions.remove_voice})))
async def phrases_remove_voice(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

