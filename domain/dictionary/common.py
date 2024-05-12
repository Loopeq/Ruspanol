from dataclasses import dataclass
from typing import Optional

from domain.shemas.schemas_dto import PhrasesDto


@dataclass
class TestData:
    user_dict: list[PhrasesDto]
    total_count: int
    correct_count: int
    incorrect_count: int
    prev_phrase: PhrasesDto
    message_id: Optional[int] = None


def _get_current_phrase(phrases: list[PhrasesDto]) -> PhrasesDto | None:
    if not phrases:
        return None
    return phrases.pop()


def _check_word_equal(user_answer: str, correct_answer: str) -> bool:
    symbols = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ñ": "n",
        "ú": "u"
    }
    user_answer = "".join(filter(str.isalnum, user_answer)).lower()
    correct_answer = "".join(filter(str.isalnum, correct_answer)).lower()

    for symbol in symbols:
        user_answer = user_answer.replace(symbol, symbols[symbol])
        correct_answer = correct_answer.replace(symbol, symbols[symbol])
    return user_answer == correct_answer
