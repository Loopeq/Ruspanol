import asyncio
from typing import Any

from aiogram import Bot
from g4f import models
from g4f.client import Client

from data.models.user_model import Role
from data.queries.user_history import insert_history, select_history
from domain.settings import settings
from domain.shemas.schemas_dto import UserHistAddDto
from text_generation.chat_wrapper import LIMIT, get_history_wrapped

client = Client()


async def run_provider(message_request: dict, bot: Bot):
    try:
        response = client.chat.completions.create(
            model=models.gpt_35_turbo,
            messages=message_request,
            max_tokens=70
        )
        message = response.choices[0].message.content
        return {"status": 200, "message": message}

    except Exception as er:
        await bot.send_message(chat_id=settings.admin_id, text=f"GPT provider error: {er}")
        return {"status": 500}


async def generate_for_assistant(message: str, tg_id: int, bot: Bot) -> dict[int, str]:
    tg_id = str(tg_id)
    await insert_history(user_history=UserHistAddDto(tg_id=tg_id, message=message, role=Role.user))
    history = await select_history(tg_id=tg_id, limit=LIMIT)
    message_request = get_history_wrapped(history=history)
    response = await run_provider(message_request=message_request, bot=bot)
    if response["status"] == 200:
        await insert_history(user_history=UserHistAddDto(tg_id=tg_id, message=response["message"], role=Role.assistant))
    return response





