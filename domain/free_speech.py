from aiogram import Router, Bot
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

fs_router = Router()


class FreeSpeechStates(StatesGroup):
    dialogue = State()


@fs_router.message(StateFilter(FreeSpeechStates))
async def dialogue_process(message: Message, bot: Bot):
    if message.voice:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id=file_id)
        file_name = f"speech_api/voices/audio.mp3"
        await bot.download_file(file.file_path, file_name)

    #
    # response = await run_provider(message=message.text, user_id=str(message.from_user.id))
    # voice_path = get_voice(word=response, user_id=message.from_user.id)
    # v_inp = FSInputFile(path=voice_path)
    # await bot.send_voice(chat_id=message.from_user.id, voice=v_inp)
    # await message.answer(text=f"<tg-spoiler>{response}</tg-spoiler>")

