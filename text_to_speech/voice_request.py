from pathlib import Path
from gtts import gTTS

ROOT_PATH = Path("text_to_speech/voices")

def get_voice(word: str, word_id: int, is_us: bool):
    pref = "us" if is_us else ""
    word_name = Path(f"{pref}{word_id}.mp3")
    apath = ROOT_PATH / word_name
    if not apath.exists():
        language = 'es'
        voice_obj = gTTS(text=word, tld="com", lang=language, slow=False)
        voice_obj.save(str(apath))
    return apath

