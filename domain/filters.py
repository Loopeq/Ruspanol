from typing import Any, Union, Dict

from aiogram.filters import BaseFilter
from aiogram.types import Message

from domain.settings import settings


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == settings.admin_id
