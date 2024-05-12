from pydantic_settings import BaseSettings
from pathlib import Path

DIR = Path(__file__).parent.name


class Settings(BaseSettings):

    db_url: str = f"sqlite+aiosqlite:///{DIR}/ruspanol.db"


settings = Settings()
