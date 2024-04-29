import asyncio

from g4f import models
from g4f.client import Client

from text_generation.chat_hist import update_hist, get_hist

client = Client()


async def run_provider(message: str, user_id: str) -> str:

    update_hist(message=message, user_id=user_id, is_user=True)

    response = client.chat.completions.create(
        model=models.gpt_35_turbo,
        messages=get_hist(user_id),
        max_tokens=100
    )
    message = response.choices[0].message.content
    update_hist(message=message, user_id=user_id, is_user=False)
    return message


if __name__ == "__main__":
    asyncio.run(run_provider("Hola, como te llamas?"))

