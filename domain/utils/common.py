import re

def clip_id(word, flag):
    return int(re.sub(flag, "", word))

def parse_words(words: str, us_id: str):
    words = words.split(";")
    words = [word.split("-") for word in words]
    words_list = []
    for word_pair in words:
        esp = word_pair[0].replace(" ", "")
        ru = word_pair[1].replace(" ", "")
        words_list.append((esp, ru, us_id))
    return words_list

def replace_syg(word):
    result = word
    syg = {"á": "a", "ñ": "n", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    for i in syg.keys():
        result = result.replace(i, syg[i])
    return result




