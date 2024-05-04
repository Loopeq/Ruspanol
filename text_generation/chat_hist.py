from enum import Enum
from typing import List

from data.models.user_model import Role
from domain.shemas.schemas_dto import UserHistDto

LIMIT = 4

INITIAL = {"role": Role.system.value, "content": "Answer in Russian, but if you need to give an example or explain "
                                                 "something, you can switch to Spanish. Imagine that you are a Spanish "
                                                 "teacher. Answer the questions like a Spanish teacher. Try to answer "
                                                 "in a simple and understandable language for the student."}


def get_history_wrapped(history: List[UserHistDto]) -> List[dict]:
    history = history[::-1]
    history_wrapped = [{"role": hist.role.value, "content": hist.message} for hist in history]
    history_wrapped.insert(0, INITIAL)
    return history_wrapped

