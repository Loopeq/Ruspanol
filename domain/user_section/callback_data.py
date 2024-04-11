

from typing import Optional

from aiogram.filters.callback_data import CallbackData


class UserSectionQuizCD(CallbackData, prefix="user_section_quiz"):
    action: str
    us_id: str = ""

class UserSectionsCD(CallbackData, prefix="user_section"):
    action: str
    page: int = 0
    u_section_id: Optional[int] = None

class EditUserSectionCD(CallbackData, prefix="edit_us"):
    action: str
    us_id: Optional[str] = ""
    word_id: Optional[str] = ""
    page: Optional[int] = 0

class UserSectionsWordsCD(CallbackData, prefix="user_section_words"):
    action: str
