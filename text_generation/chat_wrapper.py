from typing import List

from data.models.user_model import Role
from domain.shemas.schemas_dto import UserHistDto

LIMIT = 4

INITIAL_ASSISTANT = {"role": Role.system.value, "content": "Answer in Russian"
                                                 "Imagine that you are a Spanish teacher for russian student. "
                                                 "Answer the questions like a Spanish teacher. Try to answer "
                                                 "in a simple and understandable language for the student."
                                                 "Try to add a little theoretical background to the answers."}

INITIAL_PHRASE = {"role": Role.system.value, "content": ""}


def get_history_wrapped(history: List[UserHistDto]) -> List[dict]:
    history = history[::-1]
    history_wrapped = [{"role": hist.role.value, "content": hist.message} for hist in history]
    history_wrapped.insert(0, INITIAL_ASSISTANT)
    return history_wrapped



