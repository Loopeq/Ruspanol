import re
from aiogram.types import CallbackQuery

PLUG = "0"

def clip_id(word, flag):
    return int(re.sub(flag, "", word))

def parse_words(words: str, us_id: str):
    words = words.split(";")
    words = [word.split("-") for word in words]
    words_list = []
    for word_pair in words:
        esp = word_pair[0].strip()
        ru = word_pair[1].strip()
        words_list.append((esp, ru, us_id))
    return words_list

def replace_syg(word):
    result = word
    syg = {"á": "a", "ñ": "n", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    for i in syg.keys():
        result = result.replace(i, syg[i])
    return result


async def get_plug_callback(callback: CallbackQuery):
    await callback.answer()

def clip_level(level: str):
    level = level.split(",")
    level = list(map(lambda x: x.replace(" ", ""), level))

    if len(level) == 1:
        return level[0]
    return f"{level[0]} - {level[-1]}"