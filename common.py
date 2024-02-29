import re



def clip_id(word, flag):
    return int(re.sub(flag, "", word))

def create_word_box(words, line_length: int = 50):
    word_box = ""
    for obj in words:
        space = line_length - len(obj["espanol"])

        line = "{}{}{}".format(obj["espanol"], " " * space, obj["russian"])
        word_box += (line + "\n")
    return word_box

