from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from speech_api.speech_to_text import get_text_from_voice

router = Router()


class TranslationAndSpeakStates(StatesGroup):
    tas = State()


@router.message(StateFilter(TranslationAndSpeakStates), F.content_type.in_({'text', 'voice'}))
async def translation_and_speak_process(message: Message, bot: Bot):
    content_type = message.content_type

    if content_type == "voice":
        audio_file_id = message.voice.file_id
        audio_file = await bot.get_file(file_id=audio_file_id)
        audio_file_path = audio_file.file_path
        current_path = f"speech_api/voices/tas{message.from_user.id}.mp3"
        await bot.download_file(file_path=audio_file_path,
                                destination=current_path)
        text = await get_text_from_voice(voice_path=current_path)

        await message.answer(text)
    elif content_type == "text":
        pass





