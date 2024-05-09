from aiogram.types import BotCommand
from environs import Env
from dataclasses import dataclass


@dataclass
class Settings:
    bot_token: str
    admin_id: int
    api_key: str
    api_key_eden: str


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bot_token=env.str("TOKEN"),
        admin_id=env.int("ADMIN_ID"),
        api_key=env.str("API_KEY"),
        api_key_eden=env.str("API_KEY_EDEN")
    )


settings = get_settings("secrets")
