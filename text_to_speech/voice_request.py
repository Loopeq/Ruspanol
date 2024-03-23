from pathlib import Path
from gtts import gTTS

ROOT_PATH = Path("text_to_speech/voices")

def get_voice(word: str, word_id: int):
    apath = ROOT_PATH / Path(f"{word_id}.mp3")
    if not apath.exists():
        language = 'es'
        voice_obj = gTTS(text=word, tld="com", lang=language, slow=False)
        voice_obj.save(str(apath))
    return apath

