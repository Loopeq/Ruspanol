from environs import Env
from dataclasses import dataclass

@dataclass
class Settings:
    bot_token: str
    admin_id: int
    rss_token: str

def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bot_token=env.str("TOKEN"),
        admin_id=env.int("ADMIN_ID"),
        rss_token=env.str("RSS_TOKEN")
    )


settings = get_settings("adminfo")