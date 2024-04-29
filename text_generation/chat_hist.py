from enum import Enum

from data.queries import get_history, insert_history
from domain.settings import settings


LIMIT = 4


class Roles(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


INITIAL = {"role": Roles.system.value, "content": "Speak Spanish. Maintain a dialogue like a person in an anonymous chat, "
                                          "do not say that you are a bot or a robot. "
                                          "Keep the conversation going, but don't get hung up on one topic. "
                                          "Try to diversify your questions. "
                                         }


def get_role_message(role: Roles, message: str) -> dict:
    return {"role": role.value, "content": message}


def update_hist(message: str, user_id: str, is_user: bool = True):
    insert_history(user_id, message, is_user)


def get_hist(user_id: str):
    hist, count = get_history(user_id=user_id)
    messages = hist[-LIMIT:] if count >= LIMIT else hist
    messages_wrap = [{"role": Roles.user.value if message["is_user"] else Roles.assistant.value, "content": message["message"]} for message in messages]
    messages_wrap.insert(0, INITIAL)
    return messages_wrap




