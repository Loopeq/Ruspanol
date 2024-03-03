import re



def clip_id(word, flag):
    return int(re.sub(flag, "", word))


