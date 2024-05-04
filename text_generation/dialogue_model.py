import asyncio

from g4f import models
from g4f.client import Client

from data.models.user_model import Role
from data.queries.user_history import insert_history, select_history
from domain.settings import settings
from domain.shemas.schemas_dto import UserHistAddDto
from text_generation.chat_hist import LIMIT, get_history_wrapped

client = Client()


async def run_provider(message: str, tg_id: int) -> str:

    await insert_history(user_history=UserHistAddDto(tg_id=tg_id, message=message, role=Role.user))
    history = await select_history(tg_id=tg_id, limit=LIMIT)
    history_wrap = get_history_wrapped(history=history)

    response = client.chat.completions.create(
        model=models.gpt_35_turbo,
        messages=history_wrap,
        max_tokens=70
    )

    message = response.choices[0].message.content
    await insert_history(user_history=UserHistAddDto(tg_id=tg_id, message=message, role=Role.assistant))
    return message


if __name__ == "__main__":
    asyncio.run(run_provider("Hola, como te llamas?", tg_id=settings.admin_id))


