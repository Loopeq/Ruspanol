import asyncio
from typing import Any

from aiogram import Bot
from g4f import models
from g4f.client import Client

from domain.settings import settings
from domain.shemas.schemas_dto import UserHistAddDto

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


async def generate_for_assistant(message: str, bot: Bot) -> dict[int, str]:
    response = await run_provider(message_request={"role": "user", "content": message}, bot=bot)
    return response





